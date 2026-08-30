"""Routes package for RecoverAI."""
from .auth import auth_bp
from .dashboard import dashboard_bp
from .invoices import invoices_bp
from .customers import customers_bp
from .analytics import analytics_bp
from .audit import audit_bp
from .settings import settings_bp

__all__ = [
    'auth_bp', 'dashboard_bp', 'invoices_bp', 'customers_bp',
    'analytics_bp', 'audit_bp', 'settings_bp',
]
