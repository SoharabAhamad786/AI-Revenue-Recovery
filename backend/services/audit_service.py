"""Audit logging service."""
import json
from datetime import datetime, timezone
from extensions import db
from models.audit_log import AuditLog


class AuditService:
    """Append-only audit log service."""

    @staticmethod
    def log(user_id, action, entity_type=None, entity_id=None, result='success', details=None):
        """Create an audit log entry."""
        details_json = None
        if details:
            # Redact sensitive fields
            safe_details = {k: v for k, v in details.items() if k not in ('password', 'api_key', 'token')}
            details_json = json.dumps(safe_details, default=str)

        entry = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=str(entity_id) if entity_id else None,
            result=result,
            details_json=details_json,
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(entry)
        db.session.commit()
        return entry
