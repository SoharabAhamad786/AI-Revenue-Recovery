from datetime import datetime, timezone
from extensions import db


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', foreign_keys=[user_id])

    def to_dict(self):
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else 'Unknown',
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
