"""Analytics routes."""
from flask import Blueprint, jsonify
# pyrefly: ignore [missing-import]
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from extensions import db
from models.invoice import Invoice
from models.customer import Customer
from datetime import date

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@analytics_bp.route('/overview', methods=['GET'])
@jwt_required()
def overview():
    """Get analytics overview."""
    today = date.today()

    # Recovery rate
    total_paid = db.session.query(func.count(Invoice.id)).filter(
        Invoice.status == 'paid'
    ).scalar()
    total_actionable = db.session.query(func.count(Invoice.id)).filter(
        Invoice.status.in_(['paid', 'overdue', 'reminder_sent'])
    ).scalar()
    recovery_rate = (total_paid / total_actionable * 100) if total_actionable > 0 else 0

    # Amount recovered
    amount_recovered = db.session.query(
        func.coalesce(func.sum(Invoice.amount), 0)
    ).filter(Invoice.status == 'paid').scalar()

    # Amount at risk
    amount_at_risk = db.session.query(
        func.coalesce(func.sum(Invoice.amount), 0)
    ).filter(
        Invoice.status.in_(['overdue', 'reminder_sent']),
        Invoice.risk_level.in_(['medium', 'high'])
    ).scalar()

    # Average days to payment (for paid invoices)
    paid_invoices = Invoice.query.filter(
        Invoice.status == 'paid',
        Invoice.paid_date.isnot(None),
    ).all()

    if paid_invoices:
        total_days = sum(
            (inv.paid_date - inv.due_date).days
            for inv in paid_invoices
            if inv.paid_date and inv.due_date
        )
        avg_days = total_days / len(paid_invoices) if paid_invoices else 0
    else:
        avg_days = 0

    return jsonify({
        'recovery_rate': round(recovery_rate, 1),
        'amount_recovered': float(amount_recovered),
        'amount_at_risk': float(amount_at_risk),
        'average_days_to_payment': round(avg_days, 1),
    }), 200


@analytics_bp.route('/recovery-by-segment', methods=['GET'])
@jwt_required()
def recovery_by_segment():
    """Get recovery performance by customer segment."""
    segments = db.session.query(
        Customer.customer_segment,
        func.count(Invoice.id).label('total_invoices'),
        func.sum(db.case(
            (Invoice.status == 'paid', 1),
            else_=0
        )).label('paid_count'),
        func.coalesce(func.sum(Invoice.amount), 0).label('total_amount'),
        func.coalesce(func.sum(db.case(
            (Invoice.status == 'paid', Invoice.amount),
            else_=0
        )), 0).label('recovered_amount'),
    ).join(Invoice, Customer.id == Invoice.customer_id).group_by(
        Customer.customer_segment
    ).all()

    data = []
    for seg in segments:
        total = seg.total_invoices or 1
        rate = (seg.paid_count / total * 100) if total > 0 else 0
        data.append({
            'segment': seg.customer_segment,
            'total_invoices': seg.total_invoices,
            'paid_count': seg.paid_count,
            'total_amount': float(seg.total_amount),
            'recovered_amount': float(seg.recovered_amount),
            'recovery_rate': round(rate, 1),
        })

    return jsonify({'segments': data}), 200


@analytics_bp.route('/recovery-by-age', methods=['GET'])
@jwt_required()
def recovery_by_age():
    """Get recovery performance by invoice age bucket."""
    today = date.today()

    buckets = [
        {'label': '0-15 days', 'min': 0, 'max': 15},
        {'label': '16-30 days', 'min': 16, 'max': 30},
        {'label': '31-60 days', 'min': 31, 'max': 60},
        {'label': '61-90 days', 'min': 61, 'max': 90},
        {'label': '90+ days', 'min': 91, 'max': 9999},
    ]

    data = []
    for bucket in buckets:
        overdue_invoices = Invoice.query.filter(
            Invoice.status.in_(['overdue', 'reminder_sent']),
            Invoice.due_date.isnot(None)
        ).all()

        count = 0
        total_amount = 0
        for inv in overdue_invoices:
            days = (today - inv.due_date).days
            if bucket['min'] <= days <= bucket['max']:
                count += 1
                total_amount += inv.amount

        data.append({
            'age_bucket': bucket['label'],
            'count': count,
            'total_amount': round(total_amount, 2),
        })

    return jsonify({'age_buckets': data}), 200
