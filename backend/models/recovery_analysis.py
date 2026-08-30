import json
from datetime import datetime, timezone
from extensions import db


class RecoveryAnalysis(db.Model):
    __tablename__ = 'recovery_analyses'

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    recommended_action = db.Column(db.String(30), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    risk_level = db.Column(db.String(10), nullable=False)
    recovery_probability = db.Column(db.Float, nullable=False)
    suggested_follow_up_date = db.Column(db.Date, nullable=True)
    payment_plan_allowed = db.Column(db.Boolean, default=False)
    suggested_message = db.Column(db.Text, nullable=True)
    evidence_json = db.Column(db.Text, nullable=True)
    model_name = db.Column(db.String(50), default='mock')
    confidence = db.Column(db.Float, default=0.0)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    creator = db.relationship('User', foreign_keys=[created_by])

    def to_dict(self):
        evidence = []
        if self.evidence_json:
            try:
                evidence = json.loads(self.evidence_json)
            except (json.JSONDecodeError, TypeError):
                evidence = []
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'recommended_action': self.recommended_action,
            'reason': self.reason,
            'risk_level': self.risk_level,
            'recovery_probability': self.recovery_probability,
            'suggested_follow_up_date': (
                self.suggested_follow_up_date.isoformat()
                if self.suggested_follow_up_date else None
            ),
            'payment_plan_allowed': self.payment_plan_allowed,
            'suggested_message': self.suggested_message,
            'evidence': evidence,
            'model_name': self.model_name,
            'confidence': self.confidence,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
