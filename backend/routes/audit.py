"""Audit log routes."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.audit_log import AuditLog

audit_bp = Blueprint('audit', __name__, url_prefix='/api/audit-logs')


@audit_bp.route('', methods=['GET'])
@jwt_required()
def list_audit_logs():
    """List audit logs with filters."""
    query = AuditLog.query

    # Filter by action type
    action = request.args.get('action')
    if action:
        query = query.filter(AuditLog.action == action)

    # Filter by date range
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if date_from:
        from datetime import datetime
        try:
            query = query.filter(AuditLog.created_at >= datetime.fromisoformat(date_from))
        except ValueError:
            pass
    if date_to:
        from datetime import datetime
        try:
            query = query.filter(AuditLog.created_at <= datetime.fromisoformat(date_to))
        except ValueError:
            pass

    # Filter by entity type
    entity_type = request.args.get('entity_type')
    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    per_page = min(per_page, 200)

    paginated = query.order_by(AuditLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'logs': [e.to_dict() for e in paginated.items],
        'total': paginated.total,
        'page': paginated.page,
        'pages': paginated.pages,
    }), 200
