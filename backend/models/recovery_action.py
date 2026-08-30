from datetime import datetime, timezone
from extensions import db


class RecoveryAction(db.Model):
    __tablename__ = 'recovery_actions'

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    action_type = db.Column(db.String(30), nullable=False)
    action_status = db.Column(db.String(20), nullable=False, default='DRAFTED')
    message = db.Column(db.Text, nullable=True)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)
    idempotency_key = db.Column(db.String(64), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    approver = db.relationship('User', foreign_keys=[approved_by])

    def to_dict(self):
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'action_type': self.action_type,
            'action_status': self.action_status,
            'message': self.message,
            'approved_by': self.approved_by,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'idempotency_key': self.idempotency_key,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
