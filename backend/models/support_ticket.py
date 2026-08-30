from datetime import datetime, timezone
from extensions import db


class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=True)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='open')
    priority = db.Column(db.String(10), default='medium')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'invoice_id': self.invoice_id,
            'subject': self.subject,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
