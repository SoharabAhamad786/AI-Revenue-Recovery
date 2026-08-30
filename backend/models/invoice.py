from datetime import datetime, date, timezone
from extensions import db


class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    issue_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    paid_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='sent')
    dispute_status = db.Column(db.String(20), default='none')
    payment_method = db.Column(db.String(30), default='bank_transfer')
    days_overdue = db.Column(db.Integer, default=0)
    recovery_probability = db.Column(db.Float, default=0.5)
    risk_level = db.Column(db.String(10), default='medium')
    recommended_action = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    payment_events = db.relationship('PaymentEvent', backref='invoice', lazy='dynamic')
    recovery_analyses = db.relationship('RecoveryAnalysis', backref='invoice', lazy='dynamic')
    recovery_actions = db.relationship('RecoveryAction', backref='invoice', lazy='dynamic')
    notes = db.relationship('Note', backref='invoice', lazy='dynamic')
    support_tickets = db.relationship('SupportTicket', backref='invoice', lazy='dynamic')

    def compute_days_overdue(self):
        """Calculate days overdue from due_date."""
        if self.status == 'paid' or not self.due_date:
            return 0
        today = date.today()
        if today > self.due_date:
            return (today - self.due_date).days
        return 0

    def to_dict(self, include_customer=False, include_events=False, include_analyses=False):
        data = {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'customer_id': self.customer_id,
            'amount': self.amount,
            'currency': self.currency,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'paid_date': self.paid_date.isoformat() if self.paid_date else None,
            'status': self.status,
            'dispute_status': self.dispute_status,
            'payment_method': self.payment_method,
            'days_overdue': self.compute_days_overdue(),
            'recovery_probability': self.recovery_probability,
            'risk_level': self.risk_level,
            'recommended_action': self.recommended_action,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_customer and self.customer:
            data['customer'] = self.customer.to_dict()
        if include_events:
            data['payment_events'] = [e.to_dict() for e in self.payment_events.all()]
        if include_analyses:
            analyses = self.recovery_analyses.order_by(
                RecoveryAnalysis.created_at.desc()
            ).all()
            data['analyses'] = [a.to_dict() for a in analyses]
        return data


from models.recovery_analysis import RecoveryAnalysis
