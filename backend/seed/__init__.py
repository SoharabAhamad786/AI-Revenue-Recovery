"""Seed data for RecoverAI demo environment."""
import json
from datetime import datetime, date, timedelta, timezone
from extensions import db
from models import (
    User, Customer, Invoice, PaymentEvent, SupportTicket,
    AuditLog, Setting
)


def seed_database():
    """Populate database with synthetic demo data."""
    print("[SEED] Seeding database...")

    # ── Users ──
    manager = User(name='Sarah Chen', email='manager@recoverai.demo', role='finance_manager')
    manager.set_password('manager123')
    analyst = User(name='James Rodriguez', email='analyst@recoverai.demo', role='finance_analyst')
    analyst.set_password('analyst123')
    db.session.add_all([manager, analyst])
    db.session.flush()

    # ── Customers (12+) ──
    customers_data = [
        {'name': 'Michael Thompson', 'company': 'Apex Industries', 'email': 'michael@apexind.com',
         'phone': '+1-555-0101', 'segment': 'enterprise', 'ltv': 285000, 'reliability': 0.92, 'paid': 245000},
        {'name': 'Emily Zhang', 'company': 'NovaTech Solutions', 'email': 'emily.z@novatech.io',
         'phone': '+1-555-0102', 'segment': 'enterprise', 'ltv': 420000, 'reliability': 0.88, 'paid': 380000},
        {'name': 'Robert Martinez', 'company': 'Coastal Dynamics LLC', 'email': 'rmartinez@coastaldyn.com',
         'phone': '+1-555-0103', 'segment': 'mid_market', 'ltv': 95000, 'reliability': 0.45, 'paid': 62000},
        {'name': 'Jessica Patel', 'company': 'BrightPath Analytics', 'email': 'jpatel@brightpath.co',
         'phone': '+1-555-0104', 'segment': 'mid_market', 'ltv': 128000, 'reliability': 0.78, 'paid': 105000},
        {'name': 'David Kim', 'company': 'Summit Retail Group', 'email': 'dkim@summitretail.com',
         'phone': '+1-555-0105', 'segment': 'enterprise', 'ltv': 510000, 'reliability': 0.95, 'paid': 490000},
        {'name': 'Amanda Foster', 'company': 'Velocity Startups Inc', 'email': 'amanda@velocitystartups.io',
         'phone': '+1-555-0106', 'segment': 'startup', 'ltv': 18000, 'reliability': 0.35, 'paid': 8500},
        {'name': 'Christopher Brown', 'company': 'Heritage Manufacturing', 'email': 'cbrown@heritagemfg.com',
         'phone': '+1-555-0107', 'segment': 'mid_market', 'ltv': 175000, 'reliability': 0.82, 'paid': 152000},
        {'name': 'Lisa Wong', 'company': 'Pacific Health Systems', 'email': 'lwong@pacifichealth.org',
         'phone': '+1-555-0108', 'segment': 'enterprise', 'ltv': 360000, 'reliability': 0.90, 'paid': 330000},
        {'name': 'Daniel Harris', 'company': 'QuickServe Logistics', 'email': None,
         'phone': '+1-555-0109', 'segment': 'smb', 'ltv': 42000, 'reliability': 0.55, 'paid': 28000},
        {'name': 'Rachel Green', 'company': 'Evergreen Consulting', 'email': 'rgreen@evergreenconsult.com',
         'phone': '+1-555-0110', 'segment': 'smb', 'ltv': 67000, 'reliability': 0.72, 'paid': 54000},
        {'name': 'Mark Anderson', 'company': 'TechForge Labs', 'email': 'manderson@techforge.dev',
         'phone': '+1-555-0111', 'segment': 'startup', 'ltv': 25000, 'reliability': 0.60, 'paid': 15000},
        {'name': 'Sarah Mitchell', 'company': 'Urban Design Co', 'email': 'smitchell@urbandesign.co',
         'phone': '+1-555-0112', 'segment': 'smb', 'ltv': 55000, 'reliability': 0.85, 'paid': 48000},
        {'name': 'Thomas Clark', 'company': 'Pinnacle Financial Services', 'email': 'tclark@pinnaclefs.com',
         'phone': '+1-555-0113', 'segment': 'enterprise', 'ltv': 620000, 'reliability': 0.96, 'paid': 600000},
        {'name': 'Jennifer Lee', 'company': 'CloudSync Media', 'email': 'jlee@cloudsync.media',
         'phone': '+1-555-0114', 'segment': 'mid_market', 'ltv': 140000, 'reliability': 0.68, 'paid': 98000},
    ]

    customers = []
    for c in customers_data:
        cust = Customer(
            name=c['name'], company=c['company'], email=c['email'],
            phone=c['phone'], customer_segment=c['segment'],
            lifetime_value=c['ltv'], payment_reliability_score=c['reliability'],
            total_paid=c['paid']
        )
        customers.append(cust)
    db.session.add_all(customers)
    db.session.flush()

    today = date.today()

    # ── Invoices (25+) ──
    invoices_data = [
        # 1. Normal overdue - low risk, high recovery (Apex Industries)
        {'num': 'INV-2024-001', 'cust': 0, 'amount': 4500, 'issue': today - timedelta(days=45),
         'due': today - timedelta(days=15), 'status': 'overdue', 'dispute': 'none',
         'method': 'bank_transfer', 'prob': 0.85, 'risk': 'low', 'action': 'send_reminder'},
        # 2. Normal overdue - medium risk (NovaTech)
        {'num': 'INV-2024-002', 'cust': 1, 'amount': 12500, 'issue': today - timedelta(days=60),
         'due': today - timedelta(days=30), 'status': 'overdue', 'dispute': 'none',
         'method': 'bank_transfer', 'prob': 0.72, 'risk': 'medium', 'action': 'send_reminder'},
        # 3. Failed recurring payment (Coastal Dynamics)
        {'num': 'INV-2024-003', 'cust': 2, 'amount': 3200, 'issue': today - timedelta(days=35),
         'due': today - timedelta(days=5), 'status': 'overdue', 'dispute': 'none',
         'method': 'credit_card', 'prob': 0.55, 'risk': 'medium', 'action': 'send_reminder'},
        # 4. Open disputed invoice (BrightPath)
        {'num': 'INV-2024-004', 'cust': 3, 'amount': 8750, 'issue': today - timedelta(days=50),
         'due': today - timedelta(days=20), 'status': 'overdue', 'dispute': 'open',
         'method': 'bank_transfer', 'prob': 0.30, 'risk': 'high', 'action': 'escalate_to_human'},
        # 5. High-value late payment (Summit Retail - enterprise)
        {'num': 'INV-2024-005', 'cust': 4, 'amount': 47500, 'issue': today - timedelta(days=55),
         'due': today - timedelta(days=25), 'status': 'overdue', 'dispute': 'none',
         'method': 'wire_transfer', 'prob': 0.80, 'risk': 'medium', 'action': 'send_reminder'},
        # 6. Payment plan eligible (Velocity Startups - low reliability)
        {'num': 'INV-2024-006', 'cust': 5, 'amount': 6800, 'issue': today - timedelta(days=70),
         'due': today - timedelta(days=40), 'status': 'overdue', 'dispute': 'none',
         'method': 'credit_card', 'prob': 0.40, 'risk': 'high', 'action': 'offer_payment_plan'},
        # 7. Already paid (Heritage Manufacturing)
        {'num': 'INV-2024-007', 'cust': 6, 'amount': 15200, 'issue': today - timedelta(days=40),
         'due': today - timedelta(days=10), 'status': 'paid', 'dispute': 'none',
         'method': 'bank_transfer', 'prob': 1.0, 'risk': 'low', 'action': None,
         'paid_date': today - timedelta(days=8)},
        # 8. No customer email (QuickServe - manual review)
        {'num': 'INV-2024-008', 'cust': 8, 'amount': 2100, 'issue': today - timedelta(days=42),
         'due': today - timedelta(days=12), 'status': 'overdue', 'dispute': 'none',
         'method': 'check', 'prob': 0.50, 'risk': 'medium', 'action': 'mark_for_review'},
        # 9. Overdue - Evergreen Consulting
        {'num': 'INV-2024-009', 'cust': 9, 'amount': 5600, 'issue': today - timedelta(days=38),
         'due': today - timedelta(days=8), 'status': 'overdue', 'dispute': 'none',
         'method': 'bank_transfer', 'prob': 0.75, 'risk': 'low', 'action': 'send_reminder'},
        # 10. Reminder already sent (TechForge Labs)
        {'num': 'INV-2024-010', 'cust': 10, 'amount': 3400, 'issue': today - timedelta(days=50),
         'due': today - timedelta(days=20), 'status': 'reminder_sent', 'dispute': 'none',
         'method': 'credit_card', 'prob': 0.60, 'risk': 'medium', 'action': 'send_reminder'},
        # 11. Paid on time (Urban Design)
        {'num': 'INV-2024-011', 'cust': 11, 'amount': 7800, 'issue': today - timedelta(days=30),
         'due': today - timedelta(days=2), 'status': 'paid', 'dispute': 'none',
         'method': 'bank_transfer', 'prob': 1.0, 'risk': 'low', 'action': None,
         'paid_date': today - timedelta(days=5)},
        # 12. High-value, high reliability (Pinnacle)
        {'num': 'INV-2024-012', 'cust': 12, 'amount': 85000, 'issue': today - timedelta(days=35),
         'due': today - timedelta(days=5), 'status': 'overdue', 'dispute': 'none',
         'method': 'wire_transfer', 'prob': 0.90, 'risk': 'low', 'action': 'send_reminder'},
        # 13. Overdue with dispute resolved (CloudSync)
        {'num': 'INV-2024-013', 'cust': 13, 'amount': 9200, 'issue': today - timedelta(days=48),
         'due': today - timedelta(days=18), 'status': 'overdue', 'dispute': 'resolved',
         'method': 'bank_transfer', 'prob': 0.65, 'risk': 'medium', 'action': 'send_reminder'},
        # 14. Pacific Health - on time
        {'num': 'INV-2024-014', 'cust': 7, 'amount': 22000, 'issue': today - timedelta(days=25),
         'due': today + timedelta(days=5), 'status': 'sent', 'dispute': 'none',
         'method': 'wire_transfer', 'prob': 0.95, 'risk': 'low', 'action': None},
        # 15. Duplicate-looking invoice 1 (Apex Industries)
        {'num': 'INV-2024-015', 'cust': 0, 'amount': 4500, 'issue': today - timedelta(days=44),
         'due': today - timedelta(days=14), 'status': 'overdue', 'dispute': 'none',
         'method': 'bank_transfer', 'prob': 0.82, 'risk': 'low', 'action': 'send_reminder'},
        # 16. Paid (NovaTech)
        {'num': 'INV-2024-016', 'cust': 1, 'amount': 18000, 'issue': today - timedelta(days=60),
         'due': today - timedelta(days=30), 'status': 'paid', 'dispute': 'none',
         'method': 'wire_transfer', 'prob': 1.0, 'risk': 'low', 'action': None,
         'paid_date': today - timedelta(days=28)},
        # 17. Very overdue - Coastal Dynamics (high risk)
        {'num': 'INV-2024-017', 'cust': 2, 'amount': 7600, 'issue': today - timedelta(days=95),
         'due': today - timedelta(days=65), 'status': 'overdue', 'dispute': 'none',
         'method': 'credit_card', 'prob': 0.25, 'risk': 'high', 'action': 'offer_payment_plan'},
        # 18. BrightPath - paid
        {'num': 'INV-2024-018', 'cust': 3, 'amount': 4300, 'issue': today - timedelta(days=55),
         'due': today - timedelta(days=25), 'status': 'paid', 'dispute': 'none',
         'method': 'bank_transfer', 'prob': 1.0, 'risk': 'low', 'action': None,
         'paid_date': today - timedelta(days=22)},
        # 19. Summit Retail - another overdue
        {'num': 'INV-2024-019', 'cust': 4, 'amount': 32000, 'issue': today - timedelta(days=40),
         'due': today - timedelta(days=10), 'status': 'overdue', 'dispute': 'none',
         'method': 'wire_transfer', 'prob': 0.88, 'risk': 'low', 'action': 'send_reminder'},
        # 20. Velocity - another with failed payment
        {'num': 'INV-2024-020', 'cust': 5, 'amount': 2400, 'issue': today - timedelta(days=45),
         'due': today - timedelta(days=15), 'status': 'overdue', 'dispute': 'none',
         'method': 'credit_card', 'prob': 0.35, 'risk': 'high', 'action': 'offer_payment_plan'},
        # 21. Heritage - current
        {'num': 'INV-2024-021', 'cust': 6, 'amount': 11500, 'issue': today - timedelta(days=20),
         'due': today + timedelta(days=10), 'status': 'sent', 'dispute': 'none',
         'method': 'bank_transfer', 'prob': 0.90, 'risk': 'low', 'action': None},
        # 22. QuickServe - small overdue
        {'num': 'INV-2024-022', 'cust': 8, 'amount': 1800, 'issue': today - timedelta(days=30),
         'due': today - timedelta(days=3), 'status': 'overdue', 'dispute': 'none',
         'method': 'check', 'prob': 0.60, 'risk': 'medium', 'action': 'mark_for_review'},
        # 23. Evergreen - paid
        {'num': 'INV-2024-023', 'cust': 9, 'amount': 3200, 'issue': today - timedelta(days=50),
         'due': today - timedelta(days=20), 'status': 'paid', 'dispute': 'none',
         'method': 'bank_transfer', 'prob': 1.0, 'risk': 'low', 'action': None,
         'paid_date': today - timedelta(days=15)},
        # 24. CloudSync - disputed
        {'num': 'INV-2024-024', 'cust': 13, 'amount': 15800, 'issue': today - timedelta(days=42),
         'due': today - timedelta(days=12), 'status': 'overdue', 'dispute': 'open',
         'method': 'bank_transfer', 'prob': 0.20, 'risk': 'high', 'action': 'escalate_to_human'},
        # 25. Pinnacle - large paid
        {'num': 'INV-2024-025', 'cust': 12, 'amount': 120000, 'issue': today - timedelta(days=45),
         'due': today - timedelta(days=15), 'status': 'paid', 'dispute': 'none',
         'method': 'wire_transfer', 'prob': 1.0, 'risk': 'low', 'action': None,
         'paid_date': today - timedelta(days=12)},
        # 26. TechForge - small
        {'num': 'INV-2024-026', 'cust': 10, 'amount': 1200, 'issue': today - timedelta(days=28),
         'due': today - timedelta(days=1), 'status': 'overdue', 'dispute': 'none',
         'method': 'credit_card', 'prob': 0.65, 'risk': 'low', 'action': 'send_reminder'},
        # 27. Pacific Health - overdue
        {'num': 'INV-2024-027', 'cust': 7, 'amount': 28000, 'issue': today - timedelta(days=52),
         'due': today - timedelta(days=22), 'status': 'overdue', 'dispute': 'none',
         'method': 'wire_transfer', 'prob': 0.82, 'risk': 'medium', 'action': 'send_reminder'},
    ]

    invoices = []
    for inv in invoices_data:
        invoice = Invoice(
            invoice_number=inv['num'],
            customer_id=customers[inv['cust']].id,
            amount=inv['amount'],
            currency='USD',
            issue_date=inv['issue'],
            due_date=inv['due'],
            paid_date=inv.get('paid_date'),
            status=inv['status'],
            dispute_status=inv['dispute'],
            payment_method=inv['method'],
            recovery_probability=inv['prob'],
            risk_level=inv['risk'],
            recommended_action=inv['action'],
        )
        invoices.append(invoice)
    db.session.add_all(invoices)
    db.session.flush()

    # ── Payment Events ──
    payment_events = [
        # Failed payment for Coastal Dynamics INV-003
        PaymentEvent(
            invoice_id=invoices[2].id, event_type='failure', amount=3200,
            event_date=datetime.now(timezone.utc) - timedelta(days=3),
            failure_reason='Insufficient funds - card declined',
            reference_id='PE-FAIL-001'
        ),
        # Failed payment for Velocity Startups INV-020
        PaymentEvent(
            invoice_id=invoices[19].id, event_type='failure', amount=2400,
            event_date=datetime.now(timezone.utc) - timedelta(days=10),
            failure_reason='Card expired',
            reference_id='PE-FAIL-002'
        ),
        # Successful payment for Heritage INV-007
        PaymentEvent(
            invoice_id=invoices[6].id, event_type='payment', amount=15200,
            event_date=datetime.now(timezone.utc) - timedelta(days=8),
            reference_id='PE-PAY-001'
        ),
        # Successful payment for Pinnacle INV-025
        PaymentEvent(
            invoice_id=invoices[24].id, event_type='payment', amount=120000,
            event_date=datetime.now(timezone.utc) - timedelta(days=12),
            reference_id='PE-PAY-002'
        ),
        # Partial payment attempt for Coastal Dynamics INV-017
        PaymentEvent(
            invoice_id=invoices[16].id, event_type='failure', amount=7600,
            event_date=datetime.now(timezone.utc) - timedelta(days=30),
            failure_reason='Payment gateway timeout',
            reference_id='PE-FAIL-003'
        ),
        # Successful payment for NovaTech INV-016
        PaymentEvent(
            invoice_id=invoices[15].id, event_type='payment', amount=18000,
            event_date=datetime.now(timezone.utc) - timedelta(days=28),
            reference_id='PE-PAY-003'
        ),
    ]
    db.session.add_all(payment_events)

    # ── Support Tickets ──
    tickets = [
        # Open dispute for BrightPath INV-004
        SupportTicket(
            customer_id=customers[3].id, invoice_id=invoices[3].id,
            subject='Billing dispute - incorrect service charges',
            description='Customer reports they were charged for services not rendered in Q3. '
                        'Requesting itemized breakdown and adjustment.',
            status='open', priority='high'
        ),
        # Open dispute for CloudSync INV-024
        SupportTicket(
            customer_id=customers[13].id, invoice_id=invoices[23].id,
            subject='Invoice amount discrepancy',
            description='Customer claims the agreed-upon rate was different from what was invoiced. '
                        'Requesting contract review.',
            status='open', priority='high'
        ),
        # Resolved ticket for Coastal Dynamics
        SupportTicket(
            customer_id=customers[2].id, invoice_id=invoices[2].id,
            subject='Payment method update request',
            description='Customer wants to update their payment method on file.',
            status='resolved', priority='medium'
        ),
    ]
    db.session.add_all(tickets)

    # ── Audit Logs (recent activity) ──
    now = datetime.now(timezone.utc)
    audit_entries = [
        AuditLog(
            user_id=manager.id, action='user_login', entity_type='user',
            entity_id=str(manager.id), result='success',
            details_json=json.dumps({'method': 'password'}),
            created_at=now - timedelta(hours=2)
        ),
        AuditLog(
            user_id=analyst.id, action='user_login', entity_type='user',
            entity_id=str(analyst.id), result='success',
            details_json=json.dumps({'method': 'password'}),
            created_at=now - timedelta(hours=1, minutes=45)
        ),
        AuditLog(
            user_id=analyst.id, action='ai_analysis_completed', entity_type='invoice',
            entity_id='INV-2024-001', result='success',
            details_json=json.dumps({'model': 'mock', 'recommended_action': 'send_reminder'}),
            created_at=now - timedelta(hours=1, minutes=30)
        ),
        AuditLog(
            user_id=manager.id, action='reminder_approved', entity_type='invoice',
            entity_id='INV-2024-009', result='success',
            details_json=json.dumps({'amount': 5600, 'customer': 'Evergreen Consulting'}),
            created_at=now - timedelta(hours=1)
        ),
        AuditLog(
            user_id=manager.id, action='invoice_escalated', entity_type='invoice',
            entity_id='INV-2024-004', result='success',
            details_json=json.dumps({'reason': 'Open dispute', 'customer': 'BrightPath Analytics'}),
            created_at=now - timedelta(minutes=45)
        ),
    ]
    db.session.add_all(audit_entries)

    # ── Settings ──
    default_settings = [
        Setting(key='company_name', value='RecoverAI Demo Corp'),
        Setting(key='high_value_threshold', value='10000'),
        Setting(key='reminder_cooldown_hours', value='48'),
        Setting(key='max_auto_reminder_amount', value='5000'),
        Setting(key='payment_plan_min_amount', value='2000'),
        Setting(key='payment_plan_max_installments', value='6'),
        Setting(key='ai_provider', value='mock'),
        Setting(key='ai_temperature', value='0.3'),
        Setting(key='default_follow_up_days', value='7'),
        Setting(key='escalation_threshold_days', value='60'),
    ]
    db.session.add_all(default_settings)

    db.session.commit()
    print(f"[OK] Seeded: {len(customers)} customers, {len(invoices)} invoices, "
          f"{len(payment_events)} payment events, {len(tickets)} support tickets")


# Need to import Invoice for the seed script
from models.invoice import Invoice
