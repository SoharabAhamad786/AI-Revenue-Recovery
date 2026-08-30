"""Settings routes."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from extensions import db
from models.setting import Setting
from services.audit_service import AuditService
from flask_jwt_extended import get_jwt_identity

settings_bp = Blueprint('settings', __name__, url_prefix='/api/settings')


@settings_bp.route('', methods=['GET'])
@jwt_required()
def get_settings():
    """Get all settings."""
    settings = Setting.query.all()
    return jsonify({
        'settings': {s.key: s.value for s in settings},
    }), 200


@settings_bp.route('', methods=['PUT'])
@jwt_required()
def update_settings():
    """Update settings (Finance Manager only)."""
    claims = get_jwt()
    if claims.get('role') != 'finance_manager':
        return jsonify({'error': 'Only Finance Manager can update settings'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    updated = []
    for key, value in data.items():
        setting = Setting.query.filter_by(key=key).first()
        if setting:
            setting.value = str(value)
            updated.append(key)
        else:
            new_setting = Setting(key=key, value=str(value))
            db.session.add(new_setting)
            updated.append(key)

    db.session.commit()

    user_id = int(get_jwt_identity())
    AuditService.log(
        user_id=user_id,
        action='settings_updated',
        entity_type='settings',
        details={'updated_keys': updated},
    )

    settings = Setting.query.all()
    return jsonify({
        'settings': {s.key: s.value for s in settings},
        'message': f'Updated {len(updated)} setting(s)',
    }), 200
