from datetime import datetime, timezone
from extensions import db


class PaymentEvent(db.Model):
    __tablename__ = 'payment_events'

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    event_type = db.Column(db.String(20), nullable=False)  # payment, failure, refund, chargeback
    amount = db.Column(db.Float, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    failure_reason = db.Column(db.String(200), nullable=True)
    reference_id = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'event_type': self.event_type,
            'amount': self.amount,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'failure_reason': self.failure_reason,
            'reference_id': self.reference_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
