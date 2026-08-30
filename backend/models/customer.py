from datetime import datetime, timezone
from extensions import db


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    customer_segment = db.Column(db.String(50), nullable=False, default='smb')
    lifetime_value = db.Column(db.Float, default=0.0)
    payment_reliability_score = db.Column(db.Float, default=0.5)
    total_paid = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    invoices = db.relationship('Invoice', backref='customer', lazy='dynamic')
    support_tickets = db.relationship('SupportTicket', backref='customer', lazy='dynamic')

    def to_dict(self, include_stats=False):
        data = {
            'id': self.id,
            'name': self.name,
            'company': self.company,
            'email': self.email,
            'phone': self.phone,
            'customer_segment': self.customer_segment,
            'lifetime_value': self.lifetime_value,
            'payment_reliability_score': self.payment_reliability_score,
            'total_paid': self.total_paid,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if include_stats:
            overdue = self.invoices.filter(
                Invoice.status.in_(['overdue', 'reminder_sent'])
            ).count() if self.invoices else 0
            outstanding = db.session.query(
                db.func.coalesce(db.func.sum(Invoice.amount), 0)
            ).filter(
                Invoice.customer_id == self.id,
                Invoice.status.in_(['sent', 'overdue', 'reminder_sent'])
            ).scalar()
            data['overdue_count'] = overdue
            data['outstanding_amount'] = float(outstanding or 0)
            # Risk based on payment reliability
            if self.payment_reliability_score >= 0.8:
                data['risk'] = 'low'
            elif self.payment_reliability_score >= 0.5:
                data['risk'] = 'medium'
            else:
                data['risk'] = 'high'
        return data


# Import here to avoid circular imports at module level
from models.invoice import Invoice
