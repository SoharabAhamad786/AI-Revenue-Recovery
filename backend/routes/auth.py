"""Authentication routes."""
from flask import Blueprint, request, jsonify
# pyrefly: ignore [missing-import]
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, get_jwt
)
from models.user import User
from extensions import db
from services.audit_service import AuditService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Create JWT with user info
    additional_claims = {'role': user.role, 'name': user.name}
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims=additional_claims
    )

    # Audit log
    AuditService.log(
        user_id=user.id,
        action='user_login',
        entity_type='user',
        entity_id=user.id,
        details={'method': 'password', 'email': email}
    )

    return jsonify({
        'token': access_token,
        'user': user.to_dict(),
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """Get current authenticated user."""
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': user.to_dict()}), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout (client should discard token)."""
    user_id = int(get_jwt_identity())
    AuditService.log(
        user_id=user_id,
        action='user_logout',
        entity_type='user',
        entity_id=user_id,
    )
    return jsonify({'message': 'Logged out successfully'}), 200
