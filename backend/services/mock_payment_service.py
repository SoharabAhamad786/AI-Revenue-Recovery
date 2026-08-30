"""Mock payment service - generates demo payment links."""


class MockPaymentService:
    """Mock payment service that generates demo payment links."""

    BASE_URL = 'https://demo.recoverai.local/pay'

    @classmethod
    def generate_payment_link(cls, invoice_number):
        """Generate a mock payment link."""
        return f"{cls.BASE_URL}/{invoice_number}"

    @classmethod
    def process_payment(cls, invoice_number, amount):
        """Simulate processing a payment (always succeeds in demo)."""
        return {
            'success': True,
            'transaction_id': f'mock-txn-{invoice_number}',
            'amount': amount,
            'provider': 'mock',
        }
