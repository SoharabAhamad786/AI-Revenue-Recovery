"""Tests for RecoverAI backend."""
import json
import sys
import os
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from extensions import db
from models import User, Invoice, Customer


@pytest.fixture
def app():
    """Create test application."""
    app = create_app('testing')
    # create_app already seeds the database when User.query.count() == 0
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()


@pytest.fixture
def manager_token(client):
    """Get manager JWT token."""
    res = client.post('/api/auth/login', json={
        'email': 'manager@recoverai.demo',
        'password': 'manager123',
    })
    return res.get_json()['token']


@pytest.fixture
def analyst_token(client):
    """Get analyst JWT token."""
    res = client.post('/api/auth/login', json={
        'email': 'analyst@recoverai.demo',
        'password': 'analyst123',
    })
    return res.get_json()['token']


def auth_header(token):
    return {'Authorization': f'Bearer {token}'}


# ── Auth Tests ──

class TestAuth:
    def test_login_success(self, client):
        res = client.post('/api/auth/login', json={
            'email': 'manager@recoverai.demo',
            'password': 'manager123',
        })
        assert res.status_code == 200
        data = res.get_json()
        assert 'token' in data
        assert data['user']['role'] == 'finance_manager'

    def test_login_wrong_password(self, client):
        res = client.post('/api/auth/login', json={
            'email': 'manager@recoverai.demo',
            'password': 'wrong',
        })
        assert res.status_code == 401

    def test_login_missing_fields(self, client):
        res = client.post('/api/auth/login', json={'email': ''})
        assert res.status_code == 400

    def test_protected_route_no_token(self, client):
        res = client.get('/api/auth/me')
        assert res.status_code == 401

    def test_me_with_token(self, client, manager_token):
        res = client.get('/api/auth/me', headers=auth_header(manager_token))
        assert res.status_code == 200
        assert res.get_json()['user']['email'] == 'manager@recoverai.demo'

    def test_logout(self, client, manager_token):
        res = client.post('/api/auth/logout', headers=auth_header(manager_token))
        assert res.status_code == 200


# ── Dashboard Tests ──

class TestDashboard:
    def test_summary(self, client, manager_token):
        res = client.get('/api/dashboard/summary', headers=auth_header(manager_token))
        assert res.status_code == 200
        data = res.get_json()
        assert 'total_outstanding' in data
        assert 'recovery_rate' in data
        assert data['total_outstanding'] > 0

    def test_trends(self, client, manager_token):
        res = client.get('/api/dashboard/trends', headers=auth_header(manager_token))
        assert res.status_code == 200
        data = res.get_json()
        assert 'monthly_trends' in data
        assert 'status_distribution' in data

    def test_recent_activity(self, client, manager_token):
        res = client.get('/api/dashboard/recent-activity', headers=auth_header(manager_token))
        assert res.status_code == 200


# ── Invoice Tests ──

class TestInvoices:
    def test_list_invoices(self, client, manager_token):
        res = client.get('/api/invoices', headers=auth_header(manager_token))
        assert res.status_code == 200
        data = res.get_json()
        assert 'invoices' in data
        assert data['total'] > 0

    def test_filter_overdue(self, client, manager_token):
        res = client.get('/api/invoices?status=overdue', headers=auth_header(manager_token))
        assert res.status_code == 200
        invoices = res.get_json()['invoices']
        for inv in invoices:
            assert inv['status'] in ['overdue']

    def test_filter_paid(self, client, manager_token):
        res = client.get('/api/invoices?status=paid', headers=auth_header(manager_token))
        assert res.status_code == 200
        invoices = res.get_json()['invoices']
        for inv in invoices:
            assert inv['status'] == 'paid'

    def test_get_invoice_detail(self, client, manager_token):
        # Get first invoice
        res = client.get('/api/invoices', headers=auth_header(manager_token))
        inv_id = res.get_json()['invoices'][0]['id']
        res = client.get(f'/api/invoices/{inv_id}', headers=auth_header(manager_token))
        assert res.status_code == 200
        data = res.get_json()
        assert 'customer' in data
        assert 'can_send_reminder' in data

    def test_invoice_not_found(self, client, manager_token):
        res = client.get('/api/invoices/99999', headers=auth_header(manager_token))
        assert res.status_code == 404


# ── AI Analysis Tests ──

class TestAIAnalysis:
    def test_analyze_overdue_invoice(self, client, manager_token, app):
        with app.app_context():
            # Find an overdue invoice
            inv = Invoice.query.filter_by(status='overdue', dispute_status='none').first()
            assert inv is not None
            res = client.post(f'/api/invoices/{inv.id}/analyze', headers=auth_header(manager_token))
            assert res.status_code == 200
            analysis = res.get_json()['analysis']
            assert analysis['recommended_action'] in ['send_reminder', 'offer_payment_plan', 'mark_for_review', 'escalate_to_human']
            assert 0 <= analysis['recovery_probability'] <= 1
            assert analysis['risk_level'] in ['low', 'medium', 'high']

    def test_analyze_disputed_invoice(self, client, manager_token, app):
        with app.app_context():
            inv = Invoice.query.filter_by(dispute_status='open').first()
            assert inv is not None
            res = client.post(f'/api/invoices/{inv.id}/analyze', headers=auth_header(manager_token))
            assert res.status_code == 200
            analysis = res.get_json()['analysis']
            assert analysis['recommended_action'] == 'escalate_to_human'
            assert analysis['risk_level'] == 'high'
            assert analysis['payment_plan_allowed'] == False

    def test_analyze_paid_invoice(self, client, manager_token, app):
        with app.app_context():
            inv = Invoice.query.filter_by(status='paid').first()
            assert inv is not None
            res = client.post(f'/api/invoices/{inv.id}/analyze', headers=auth_header(manager_token))
            assert res.status_code == 200
            analysis = res.get_json()['analysis']
            assert analysis['recommended_action'] == 'no_action'


# ── Business Rules Tests ──

class TestBusinessRules:
    def test_cannot_send_reminder_to_paid(self, client, manager_token, app):
        with app.app_context():
            inv = Invoice.query.filter_by(status='paid').first()
            res = client.post(f'/api/invoices/{inv.id}/actions/send-reminder',
                              headers=auth_header(manager_token),
                              json={'message': 'test', 'idempotency_key': 'test-key-1'})
            assert res.status_code == 400

    def test_cannot_send_reminder_to_disputed(self, client, manager_token, app):
        with app.app_context():
            inv = Invoice.query.filter_by(dispute_status='open').first()
            res = client.post(f'/api/invoices/{inv.id}/actions/send-reminder',
                              headers=auth_header(manager_token),
                              json={'message': 'test', 'idempotency_key': 'test-key-2'})
            assert res.status_code == 400

    def test_high_value_requires_manager(self, client, analyst_token, app):
        with app.app_context():
            inv = Invoice.query.filter(Invoice.amount >= 10000, Invoice.status != 'paid').first()
            if inv:
                res = client.post(f'/api/invoices/{inv.id}/actions/send-reminder',
                                  headers=auth_header(analyst_token),
                                  json={'message': 'test', 'idempotency_key': 'test-key-3'})
                assert res.status_code == 403

    def test_manager_can_send_high_value(self, client, manager_token, app):
        with app.app_context():
            inv = Invoice.query.filter(
                Invoice.amount >= 10000,
                Invoice.status == 'overdue',
                Invoice.dispute_status == 'none'
            ).first()
            if inv:
                # First analyze
                client.post(f'/api/invoices/{inv.id}/analyze', headers=auth_header(manager_token))
                res = client.post(f'/api/invoices/{inv.id}/actions/send-reminder',
                                  headers=auth_header(manager_token),
                                  json={'message': 'Test reminder message', 'idempotency_key': 'test-key-4'})
                assert res.status_code == 200

    def test_idempotency_key_prevents_duplicate(self, client, manager_token, app):
        with app.app_context():
            inv = Invoice.query.filter(
                Invoice.amount < 10000,
                Invoice.status == 'overdue',
                Invoice.dispute_status == 'none'
            ).first()
            if inv:
                key = 'idempotency-test-key-unique'
                # First send
                res1 = client.post(f'/api/invoices/{inv.id}/actions/send-reminder',
                                   headers=auth_header(manager_token),
                                   json={'message': 'Test reminder', 'idempotency_key': key})
                assert res1.status_code == 200
                # Second send with same key should return the existing action
                res2 = client.post(f'/api/invoices/{inv.id}/actions/send-reminder',
                                   headers=auth_header(manager_token),
                                   json={'message': 'Test reminder', 'idempotency_key': key})
                assert res2.status_code == 200
                assert 'already processed' in res2.get_json().get('message', '').lower()


# ── Audit Log Tests ──

class TestAuditLog:
    def test_audit_log_created_on_login(self, client):
        client.post('/api/auth/login', json={
            'email': 'manager@recoverai.demo',
            'password': 'manager123',
        })
        # Login to get token, then check audit logs
        res = client.post('/api/auth/login', json={
            'email': 'manager@recoverai.demo',
            'password': 'manager123',
        })
        token = res.get_json()['token']
        res = client.get('/api/audit-logs?action=user_login', headers=auth_header(token))
        assert res.status_code == 200
        logs = res.get_json()['logs']
        assert len(logs) > 0

    def test_audit_log_on_analysis(self, client, manager_token, app):
        with app.app_context():
            inv = Invoice.query.filter_by(status='overdue').first()
            client.post(f'/api/invoices/{inv.id}/analyze', headers=auth_header(manager_token))
            res = client.get('/api/audit-logs?action=ai_analysis_completed', headers=auth_header(manager_token))
            assert res.status_code == 200
            assert len(res.get_json()['logs']) > 0


# ── Customer Tests ──

class TestCustomers:
    def test_list_customers(self, client, manager_token):
        res = client.get('/api/customers', headers=auth_header(manager_token))
        assert res.status_code == 200
        data = res.get_json()
        assert len(data['customers']) > 0

    def test_get_customer(self, client, manager_token, app):
        with app.app_context():
            cust = Customer.query.first()
            res = client.get(f'/api/customers/{cust.id}', headers=auth_header(manager_token))
            assert res.status_code == 200
            assert 'invoices' in res.get_json()


# ── Role Permission Tests ──

class TestPermissions:
    def test_analyst_cannot_update_settings(self, client, analyst_token):
        res = client.put('/api/settings',
                         headers=auth_header(analyst_token),
                         json={'high_value_threshold': '20000'})
        assert res.status_code == 403

    def test_manager_can_update_settings(self, client, manager_token):
        res = client.put('/api/settings',
                         headers=auth_header(manager_token),
                         json={'high_value_threshold': '20000'})
        assert res.status_code == 200


# ── Note Tests ──

class TestNotes:
    def test_add_note(self, client, manager_token, app):
        with app.app_context():
            inv = Invoice.query.first()
            res = client.post(f'/api/invoices/{inv.id}/notes',
                              headers=auth_header(manager_token),
                              json={'content': 'Test note'})
            assert res.status_code == 201
            assert res.get_json()['note']['content'] == 'Test note'

    def test_add_empty_note_fails(self, client, manager_token, app):
        with app.app_context():
            inv = Invoice.query.first()
            res = client.post(f'/api/invoices/{inv.id}/notes',
                              headers=auth_header(manager_token),
                              json={'content': ''})
            assert res.status_code == 400


# ── Escalation Tests ──

class TestEscalation:
    def test_escalate_invoice(self, client, manager_token, app):
        with app.app_context():
            inv = Invoice.query.filter_by(status='overdue').first()
            res = client.post(f'/api/invoices/{inv.id}/actions/escalate',
                              headers=auth_header(manager_token),
                              json={'reason': 'Needs human review'})
            assert res.status_code == 200

    def test_mark_paid(self, client, manager_token, app):
        with app.app_context():
            inv = Invoice.query.filter_by(status='overdue').first()
            res = client.post(f'/api/invoices/{inv.id}/mark-paid',
                              headers=auth_header(manager_token))
            assert res.status_code == 200
            assert res.get_json()['invoice']['status'] == 'paid'
