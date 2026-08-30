"""Invoice routes - CRUD, AI analysis, and recovery actions."""
import json
import uuid
from datetime import datetime, date, timedelta, timezone
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db
from models.invoice import Invoice
from models.customer import Customer
from models.payment_event import PaymentEvent
from models.support_ticket import SupportTicket
from models.recovery_analysis import RecoveryAnalysis
from models.recovery_action import RecoveryAction
from models.note import Note
from ai.base import AIService
from rules import BusinessRules
from services.audit_service import AuditService
from services.mock_email_service import MockEmailService
from services.mock_payment_service import MockPaymentService
from models.setting import Setting

invoices_bp = Blueprint('invoices', __name__, url_prefix='/api/invoices')


def _get_settings():
    """Load settings into a dict."""
    settings = Setting.query.all()
    return {s.key: s.value for s in settings}


@invoices_bp.route('', methods=['GET'])
@jwt_required()
def list_invoices():
    """List invoices with filtering and sorting."""
    query = Invoice.query

    # Filters
    status = request.args.get('status')
    if status and status != 'all':
        if status == 'high_value':
            threshold = float(_get_settings().get('high_value_threshold', 10000))
            query = query.filter(Invoice.amount >= threshold, Invoice.status != 'paid')
        elif status == 'failed_payment':
            from sqlalchemy import exists
            query = query.filter(
                Invoice.id.in_(
                    db.session.query(PaymentEvent.invoice_id).filter(
                        PaymentEvent.event_type == 'failure'
                    )
                )
            )
        elif status == 'disputed':
            query = query.filter(Invoice.dispute_status == 'open')
        else:
            query = query.filter(Invoice.status == status)

    # Search
    search = request.args.get('search', '').strip()
    if search:
        query = query.join(Customer).filter(
            db.or_(
                Invoice.invoice_number.ilike(f'%{search}%'),
                Customer.name.ilike(f'%{search}%'),
                Customer.company.ilike(f'%{search}%'),
            )
        )

    # Sorting
    sort = request.args.get('sort', 'priority')
    if sort == 'amount':
        query = query.order_by(Invoice.amount.desc())
    elif sort == 'days_overdue':
        query = query.order_by(Invoice.due_date.asc())
    elif sort == 'recovery_probability':
        query = query.order_by(Invoice.recovery_probability.asc())
    else:  # priority - high risk first, then amount
        query = query.order_by(
            db.case(
                (Invoice.risk_level == 'high', 0),
                (Invoice.risk_level == 'medium', 1),
                else_=2
            ),
            Invoice.amount.desc()
        )

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    invoices = []
    for inv in paginated.items:
        inv_dict = inv.to_dict(include_customer=True)
        # Check for duplicates
        duplicates = BusinessRules().check_duplicate_invoice(inv)
        if duplicates:
            inv_dict['has_duplicate_warning'] = True
            inv_dict['duplicate_ids'] = [d.invoice_number for d in duplicates]
        else:
            inv_dict['has_duplicate_warning'] = False
        invoices.append(inv_dict)

    return jsonify({
        'invoices': invoices,
        'total': paginated.total,
        'page': paginated.page,
        'pages': paginated.pages,
        'per_page': per_page,
    }), 200


@invoices_bp.route('/<int:invoice_id>', methods=['GET'])
@jwt_required()
def get_invoice(invoice_id):
    """Get invoice details with all related data."""
    invoice = db.session.get(Invoice, invoice_id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404

    inv_dict = invoice.to_dict(include_customer=True, include_events=True, include_analyses=True)

    # Add notes
    notes = Note.query.filter_by(invoice_id=invoice_id).order_by(Note.created_at.desc()).all()
    inv_dict['notes'] = [n.to_dict() for n in notes]

    # Add recovery actions
    actions = RecoveryAction.query.filter_by(invoice_id=invoice_id).order_by(
        RecoveryAction.created_at.desc()
    ).all()
    inv_dict['recovery_actions'] = [a.to_dict() for a in actions]

    # Add support tickets
    tickets = SupportTicket.query.filter_by(invoice_id=invoice_id).all()
    inv_dict['support_tickets'] = [t.to_dict() for t in tickets]

    # Check for duplicates
    duplicates = BusinessRules().check_duplicate_invoice(invoice)
    inv_dict['has_duplicate_warning'] = len(duplicates) > 0
    inv_dict['duplicate_ids'] = [d.invoice_number for d in duplicates]

    # Business rules checks
    rules = BusinessRules(_get_settings())
    can_send, reason = rules.can_send_reminder(invoice)
    inv_dict['can_send_reminder'] = can_send
    inv_dict['send_reminder_blocked_reason'] = reason if not can_send else None
    inv_dict['requires_manager_approval'] = rules.requires_manager_approval(invoice)
    inv_dict['is_high_value'] = rules.is_high_value(invoice)

    # Payment link
    inv_dict['payment_link'] = MockPaymentService.generate_payment_link(invoice.invoice_number)

    return jsonify(inv_dict), 200


@invoices_bp.route('/<int:invoice_id>/analyze', methods=['POST'])
@jwt_required()
def analyze_invoice(invoice_id):
    """Run AI analysis on an invoice."""
    user_id = int(get_jwt_identity())

    invoice = db.session.get(Invoice, invoice_id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404

    customer = db.session.get(Customer, invoice.customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    # Load related data
    payment_events = PaymentEvent.query.filter_by(invoice_id=invoice_id).all()
    support_tickets = SupportTicket.query.filter(
        SupportTicket.invoice_id == invoice_id,
        SupportTicket.status == 'open'
    ).all()

    # Build context
    context = AIService.build_context(invoice, customer, payment_events, support_tickets)

    # Get AI provider
    settings = _get_settings()
    provider = AIService.get_provider(settings.get('ai_provider', 'mock'))

    # Call AI
    try:
        ai_result = provider.analyze(context)
        model_name = provider.MODEL_NAME
    except Exception as e:
        # Fallback to mock if real AI fails
        from ai.mock_provider import MockAIProvider
        fallback = MockAIProvider()
        ai_result = fallback.analyze(context)
        model_name = f"{fallback.MODEL_NAME}-fallback"
        ai_result['evidence'].append({
            'source': 'policy',
            'detail': f'[Fallback] Real AI provider unavailable: {str(e)[:100]}. Using deterministic analysis.'
        })

    # Validate AI output
    try:
        validated = AIService.validate_result(ai_result)
        ai_result = validated.model_dump()
    except Exception as e:
        # If validation fails, use mock provider
        from ai.mock_provider import MockAIProvider
        fallback = MockAIProvider()
        ai_result = fallback.analyze(context)
        model_name = f"mock-validation-fallback"
        ai_result['evidence'].append({
            'source': 'policy',
            'detail': f'[Fallback] AI output failed validation. Using deterministic analysis.'
        })

    # Apply business rule overrides
    rules = BusinessRules(settings)
    ai_result, overrides = rules.apply_safety_overrides(invoice, customer, ai_result)

    # Save analysis
    analysis = RecoveryAnalysis(
        invoice_id=invoice_id,
        recommended_action=ai_result['recommended_action'],
        reason=ai_result['reason'],
        risk_level=ai_result['risk_level'],
        recovery_probability=ai_result['recovery_probability'],
        suggested_follow_up_date=date.fromisoformat(ai_result['suggested_follow_up_date']),
        payment_plan_allowed=ai_result['payment_plan_allowed'],
        suggested_message=ai_result['suggested_message'],
        evidence_json=json.dumps(ai_result['evidence']),
        model_name=model_name,
        confidence=ai_result['confidence'],
        created_by=user_id,
    )
    db.session.add(analysis)

    # Update invoice with latest analysis
    invoice.recovery_probability = ai_result['recovery_probability']
    invoice.risk_level = ai_result['risk_level']
    invoice.recommended_action = ai_result['recommended_action']
    invoice.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    # Audit log
    AuditService.log(
        user_id=user_id,
        action='ai_analysis_completed',
        entity_type='invoice',
        entity_id=invoice.invoice_number,
        details={
            'model': model_name,
            'recommended_action': ai_result['recommended_action'],
            'risk_level': ai_result['risk_level'],
            'overrides_applied': len(overrides),
        }
    )

    return jsonify({
        'analysis': analysis.to_dict(),
        'overrides': overrides,
    }), 200


@invoices_bp.route('/<int:invoice_id>/actions/draft-reminder', methods=['POST'])
@jwt_required()
def draft_reminder(invoice_id):
    """Draft a reminder for an invoice."""
    user_id = int(get_jwt_identity())

    invoice = db.session.get(Invoice, invoice_id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404

    rules = BusinessRules(_get_settings())
    can_send, reason = rules.can_send_reminder(invoice)
    if not can_send:
        return jsonify({'error': reason}), 400

    data = request.get_json() or {}
    message = data.get('message', '')

    if not message:
        # Generate a default message
        customer = db.session.get(Customer, invoice.customer_id)
        from ai.mock_provider import MockAIProvider
        provider = MockAIProvider()
        customer_name = customer.name if customer else 'Valued Customer'
        customer_company = customer.company if customer else 'Company'
        message = provider._generate_reminder_message(
            customer_name, customer_company, invoice.invoice_number,
            invoice.amount, invoice.due_date.isoformat() if invoice.due_date else 'N/A',
            invoice.compute_days_overdue()
        )

    action = RecoveryAction(
        invoice_id=invoice_id,
        action_type='reminder',
        action_status='DRAFTED',
        message=message,
        idempotency_key=str(uuid.uuid4()),
    )
    db.session.add(action)
    db.session.commit()

    AuditService.log(
        user_id=user_id,
        action='reminder_drafted',
        entity_type='invoice',
        entity_id=invoice.invoice_number,
        details={'action_id': action.id},
    )

    return jsonify({'action': action.to_dict()}), 201


@invoices_bp.route('/<int:invoice_id>/actions/send-reminder', methods=['POST'])
@jwt_required()
def send_reminder(invoice_id):
    """Approve and send a reminder (mock)."""
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    user_role = claims.get('role', 'finance_analyst')

    invoice = db.session.get(Invoice, invoice_id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404

    customer = db.session.get(Customer, invoice.customer_id)

    data = request.get_json() or {}
    message = data.get('message', '')
    idempotency_key = data.get('idempotency_key', str(uuid.uuid4()))

    # Check idempotency first - before any validation
    existing = RecoveryAction.query.filter_by(idempotency_key=idempotency_key).first()
    if existing:
        return jsonify({'action': existing.to_dict(), 'message': 'Action already processed'}), 200

    rules = BusinessRules(_get_settings())

    # Check permissions
    if rules.requires_manager_approval(invoice) and user_role != 'finance_manager':
        return jsonify({
            'error': 'This high-value invoice requires Finance Manager approval'
        }), 403

    can_send, reason = rules.can_send_reminder(invoice)
    if not can_send:
        return jsonify({'error': reason}), 400

    if not message:
        return jsonify({'error': 'Message content is required'}), 400

    # Create and approve the action
    action = RecoveryAction(
        invoice_id=invoice_id,
        action_type='reminder',
        action_status='SENT',
        message=message,
        approved_by=user_id,
        sent_at=datetime.now(timezone.utc),
        idempotency_key=idempotency_key,
    )
    db.session.add(action)

    # Mock send email
    email_result = MockEmailService.send(
        to_email=customer.email if customer else None,
        subject=f'Payment Reminder: Invoice {invoice.invoice_number}',
        body=message,
        invoice_number=invoice.invoice_number,
    )

    # Update invoice status
    invoice.status = 'reminder_sent'
    invoice.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    AuditService.log(
        user_id=user_id,
        action='reminder_sent',
        entity_type='invoice',
        entity_id=invoice.invoice_number,
        result='success',
        details={
            'amount': invoice.amount,
            'customer': customer.name if customer else 'Unknown',
            'email_result': email_result,
        }
    )

    return jsonify({
        'action': action.to_dict(),
        'email_result': email_result,
        'message': 'Reminder sent successfully (mock)',
    }), 200


@invoices_bp.route('/<int:invoice_id>/actions/escalate', methods=['POST'])
@jwt_required()
def escalate_invoice(invoice_id):
    """Escalate an invoice to human review."""
    user_id = int(get_jwt_identity())

    invoice = db.session.get(Invoice, invoice_id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404

    data = request.get_json() or {}
    reason = data.get('reason', 'Escalated for manual review')

    action = RecoveryAction(
        invoice_id=invoice_id,
        action_type='escalation',
        action_status='ESCALATED',
        message=reason,
        approved_by=user_id,
        sent_at=datetime.now(timezone.utc),
        idempotency_key=str(uuid.uuid4()),
    )
    db.session.add(action)

    invoice.recommended_action = 'escalate_to_human'
    invoice.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    customer = db.session.get(Customer, invoice.customer_id)
    AuditService.log(
        user_id=user_id,
        action='invoice_escalated',
        entity_type='invoice',
        entity_id=invoice.invoice_number,
        details={
            'reason': reason,
            'customer': customer.name if customer else 'Unknown',
        }
    )

    return jsonify({
        'action': action.to_dict(),
        'message': 'Invoice escalated for human review',
    }), 200


@invoices_bp.route('/<int:invoice_id>/mark-paid', methods=['POST'])
@jwt_required()
def mark_paid(invoice_id):
    """Mark an invoice as paid."""
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    user_role = claims.get('role', 'finance_analyst')

    invoice = db.session.get(Invoice, invoice_id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404

    if invoice.status == 'paid':
        return jsonify({'error': 'Invoice is already marked as paid'}), 400

    # High-value requires manager
    rules = BusinessRules(_get_settings())
    if rules.requires_manager_approval(invoice) and user_role != 'finance_manager':
        return jsonify({
            'error': 'Marking this high-value invoice as paid requires Finance Manager approval'
        }), 403

    invoice.status = 'paid'
    invoice.paid_date = date.today()
    invoice.recovery_probability = 1.0
    invoice.risk_level = 'low'
    invoice.recommended_action = None
    invoice.updated_at = datetime.now(timezone.utc)

    # Add payment event
    pe = PaymentEvent(
        invoice_id=invoice_id,
        event_type='payment',
        amount=invoice.amount,
        event_date=datetime.now(timezone.utc),
        reference_id=f'MANUAL-{invoice.invoice_number}',
    )
    db.session.add(pe)
    db.session.commit()

    customer = db.session.get(Customer, invoice.customer_id)
    AuditService.log(
        user_id=user_id,
        action='invoice_marked_paid',
        entity_type='invoice',
        entity_id=invoice.invoice_number,
        details={
            'amount': invoice.amount,
            'customer': customer.name if customer else 'Unknown',
        }
    )

    return jsonify({
        'invoice': invoice.to_dict(),
        'message': 'Invoice marked as paid',
    }), 200


@invoices_bp.route('/<int:invoice_id>/notes', methods=['POST'])
@jwt_required()
def add_note(invoice_id):
    """Add a note to an invoice."""
    user_id = int(get_jwt_identity())

    invoice = db.session.get(Invoice, invoice_id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404

    data = request.get_json()
    if not data or not data.get('content', '').strip():
        return jsonify({'error': 'Note content is required'}), 400

    note = Note(
        invoice_id=invoice_id,
        user_id=user_id,
        content=data['content'].strip(),
    )
    db.session.add(note)
    db.session.commit()

    AuditService.log(
        user_id=user_id,
        action='note_added',
        entity_type='invoice',
        entity_id=invoice.invoice_number,
        details={'note_id': note.id},
    )

    return jsonify({'note': note.to_dict()}), 201
