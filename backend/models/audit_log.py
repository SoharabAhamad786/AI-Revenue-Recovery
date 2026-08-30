import json
from datetime import datetime, timezone
from extensions import db


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(50), nullable=False)
    entity_type = db.Column(db.String(30), nullable=True)
    entity_id = db.Column(db.String(30), nullable=True)
    result = db.Column(db.String(20), default='success')
    details_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', foreign_keys=[user_id])

    def to_dict(self):
        details = {}
        if self.details_json:
            try:
                details = json.loads(self.details_json)
            except (json.JSONDecodeError, TypeError):
                details = {}
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else 'System',
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'result': self.result,
            'details': details,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
