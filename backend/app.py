"""RecoverAI - Intelligent Invoice and Payment Recovery Assistant."""
import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from config import config_map
from extensions import db, jwt, cors


def create_app(config_name=None):
    """Application factory."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_map.get(config_name, config_map['development']))

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": [app.config.get('FRONTEND_URL', 'http://localhost:5173')],
            "supports_credentials": True,
        }
    })

    # Register blueprints
    from routes import (
        auth_bp, dashboard_bp, invoices_bp, customers_bp,
        analytics_bp, audit_bp, settings_bp
    )
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(settings_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({'error': 'Unprocessable entity'}), 422

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401

    @jwt.invalid_token_loader
    def invalid_token(error):
        return jsonify({'error': 'Invalid token'}), 401

    @jwt.unauthorized_loader
    def missing_token(error):
        return jsonify({'error': 'Authorization token is required'}), 401

    # Health check
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy', 'service': 'RecoverAI API'}), 200

    # Create tables and seed
    with app.app_context():
        db.create_all()
        # Seed if empty
        from models.user import User
        if User.query.count() == 0:
            from seed import seed_database
            seed_database()
            print("[OK] Database seeded successfully")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
