"""Customer routes."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.customer import Customer
from models.invoice import Invoice
from sqlalchemy import func

customers_bp = Blueprint('customers', __name__, url_prefix='/api/customers')


@customers_bp.route('', methods=['GET'])
@jwt_required()
def list_customers():
    """List all customers with stats."""
    query = Customer.query

    search = request.args.get('search', '').strip()
    if search:
        query = query.filter(
            db.or_(
                Customer.name.ilike(f'%{search}%'),
                Customer.company.ilike(f'%{search}%'),
            )
        )

    segment = request.args.get('segment')
    if segment:
        query = query.filter(Customer.customer_segment == segment)

    customers = query.order_by(Customer.lifetime_value.desc()).all()

    return jsonify({
        'customers': [c.to_dict(include_stats=True) for c in customers],
    }), 200


@customers_bp.route('/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    """Get customer details with invoices."""
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    cust_dict = customer.to_dict(include_stats=True)

    # Include invoices
    invoices = Invoice.query.filter_by(customer_id=customer_id).order_by(
        Invoice.due_date.desc()
    ).all()
    cust_dict['invoices'] = [i.to_dict() for i in invoices]

    return jsonify(cust_dict), 200
