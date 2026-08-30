"""Business rules engine for RecoverAI."""
from datetime import date, datetime, timedelta, timezone
from models.invoice import Invoice
from models.recovery_action import RecoveryAction
from extensions import db


class BusinessRules:
    """Deterministic business rules that override AI recommendations."""

    def __init__(self, settings=None):
        self.high_value_threshold = 10000
        self.reminder_cooldown_hours = 48
        self.max_auto_reminder_amount = 5000
        self.escalation_threshold_days = 60
        if settings:
            self.high_value_threshold = float(settings.get('high_value_threshold', 10000))
            self.reminder_cooldown_hours = int(settings.get('reminder_cooldown_hours', 48))
            self.max_auto_reminder_amount = float(settings.get('max_auto_reminder_amount', 5000))
            self.escalation_threshold_days = int(settings.get('escalation_threshold_days', 60))

    def is_overdue(self, invoice):
        """Check if invoice is overdue."""
        if invoice.status == 'paid':
            return False
        if invoice.due_date and invoice.due_date < date.today():
            return True
        return False

    def has_open_dispute(self, invoice):
        """Check if invoice has an open dispute."""
        return invoice.dispute_status == 'open'

    def is_paid(self, invoice):
        """Check if invoice is already paid."""
        return invoice.status == 'paid'

    def is_high_value(self, invoice):
        """Check if invoice is above high-value threshold."""
        return invoice.amount >= self.high_value_threshold

    def requires_manager_approval(self, invoice):
        """Check if action requires Finance Manager approval."""
        return self.is_high_value(invoice)

    def can_send_reminder(self, invoice):
        """Check if a reminder can be sent for this invoice."""
        if self.is_paid(invoice):
            return False, "Invoice is already paid"
        if self.has_open_dispute(invoice):
            return False, "Invoice has an open dispute - must escalate to human"
        # Check cooldown
        cooldown_cutoff = datetime.now(timezone.utc) - timedelta(hours=self.reminder_cooldown_hours)
        recent_reminder = RecoveryAction.query.filter(
            RecoveryAction.invoice_id == invoice.id,
            RecoveryAction.action_type == 'reminder',
            RecoveryAction.action_status.in_(['SENT', 'APPROVED']),
            RecoveryAction.created_at >= cooldown_cutoff
        ).first()
        if recent_reminder:
            return False, f"A reminder was already sent within the last {self.reminder_cooldown_hours} hours"
        return True, "OK"

    def has_customer_email(self, customer):
        """Check if customer has a valid email address."""
        return customer.email is not None and len(customer.email.strip()) > 0

    def check_duplicate_invoice(self, invoice):
        """Check if there are duplicate-looking invoices."""
        duplicates = Invoice.query.filter(
            Invoice.customer_id == invoice.customer_id,
            Invoice.amount == invoice.amount,
            Invoice.id != invoice.id,
            Invoice.status != 'cancelled'
        ).all()
        return duplicates

    def apply_safety_overrides(self, invoice, customer, ai_result):
        """Apply safety rules to override AI recommendations."""
        overrides = []

        # Rule: Disputed invoices must be escalated
        if self.has_open_dispute(invoice):
            ai_result['recommended_action'] = 'escalate_to_human'
            ai_result['risk_level'] = 'high'
            ai_result['payment_plan_allowed'] = False
            overrides.append({
                'rule': 'dispute_override',
                'detail': 'Invoice has an open dispute - forced escalation to human'
            })

        # Rule: Paid invoices - no action
        if self.is_paid(invoice):
            ai_result['recommended_action'] = 'no_action'
            ai_result['risk_level'] = 'low'
            overrides.append({
                'rule': 'paid_override',
                'detail': 'Invoice is already paid - no action required'
            })

        # Rule: No customer email - mark for review
        if not self.has_customer_email(customer):
            if ai_result['recommended_action'] == 'send_reminder':
                ai_result['recommended_action'] = 'mark_for_review'
                overrides.append({
                    'rule': 'no_email_override',
                    'detail': 'Customer has no email on file - marked for manual review'
                })

        # Rule: Very overdue invoices - consider escalation
        days_overdue = invoice.compute_days_overdue()
        if days_overdue > self.escalation_threshold_days and ai_result['recommended_action'] == 'send_reminder':
            ai_result['recommended_action'] = 'offer_payment_plan'
            ai_result['risk_level'] = 'high'
            overrides.append({
                'rule': 'age_escalation',
                'detail': f'Invoice is {days_overdue} days overdue - payment plan recommended'
            })

        # Add override evidence
        if overrides:
            if 'evidence' not in ai_result:
                ai_result['evidence'] = []
            for o in overrides:
                ai_result['evidence'].append({
                    'source': 'policy',
                    'detail': f"[Safety Override] {o['detail']}"
                })

        return ai_result, overrides
