"""Mock AI provider - deterministic rules-based engine."""
from datetime import date, timedelta


class MockAIProvider:
    """Deterministic AI provider that works without any API key."""

    MODEL_NAME = 'recoverai-mock-v1'

    def analyze(self, context: dict) -> dict:
        """Produce a deterministic analysis based on invoice and customer data."""
        invoice = context['invoice']
        customer = context['customer']
        payment_events = context.get('payment_events', [])
        support_tickets = context.get('support_tickets', [])

        days_overdue = invoice.get('days_overdue', 0)
        amount = invoice.get('amount', 0)
        reliability = customer.get('payment_reliability_score', 0.5)
        dispute_status = invoice.get('dispute_status', 'none')
        status = invoice.get('status', 'sent')
        customer_name = customer.get('name', 'Customer')
        company = customer.get('company', 'Company')
        inv_number = invoice.get('invoice_number', 'INV-UNKNOWN')
        due_date = invoice.get('due_date', date.today().isoformat())
        has_email = customer.get('email') is not None and customer.get('email', '').strip() != ''

        evidence = []
        follow_up_date = (date.today() + timedelta(days=7)).isoformat()

        # ── Determine action ──

        # Paid invoices
        if status == 'paid':
            return {
                'recommended_action': 'no_action',
                'reason': 'This invoice has already been paid. No further action is required.',
                'risk_level': 'low',
                'recovery_probability': 1.0,
                'suggested_follow_up_date': follow_up_date,
                'payment_plan_allowed': False,
                'suggested_message': '',
                'evidence': [{'source': 'invoice', 'detail': f'Invoice {inv_number} is marked as paid.'}],
                'confidence': 0.99,
            }

        # Open disputes
        has_open_dispute = dispute_status == 'open'
        open_tickets = [t for t in support_tickets if t.get('status') == 'open']

        if has_open_dispute or open_tickets:
            ticket_details = ''
            if open_tickets:
                ticket_details = f" Related ticket: \"{open_tickets[0].get('subject', 'N/A')}\" (Priority: {open_tickets[0].get('priority', 'medium')})"
            return {
                'recommended_action': 'escalate_to_human',
                'reason': f'This invoice has an active dispute that must be resolved before any collection activity.{ticket_details}',
                'risk_level': 'high',
                'recovery_probability': 0.30,
                'suggested_follow_up_date': (date.today() + timedelta(days=3)).isoformat(),
                'payment_plan_allowed': False,
                'suggested_message': '',
                'evidence': [
                    {'source': 'invoice', 'detail': f'Invoice {inv_number} has dispute status: {dispute_status}'},
                    {'source': 'support_ticket', 'detail': f'Active support tickets found: {len(open_tickets)}'},
                    {'source': 'policy', 'detail': 'Company policy requires human review for disputed invoices'},
                ],
                'confidence': 0.95,
            }

        # No email - manual review
        if not has_email:
            return {
                'recommended_action': 'mark_for_review',
                'reason': f'Customer {customer_name} ({company}) has no email address on file. Manual outreach is required.',
                'risk_level': 'medium',
                'recovery_probability': 0.50,
                'suggested_follow_up_date': (date.today() + timedelta(days=3)).isoformat(),
                'payment_plan_allowed': False,
                'suggested_message': '',
                'evidence': [
                    {'source': 'customer', 'detail': 'No customer email address on file'},
                    {'source': 'policy', 'detail': 'Cannot send automated reminder without valid email'},
                ],
                'confidence': 0.90,
            }

        # Check failed payments
        failed_payments = [pe for pe in payment_events if pe.get('event_type') == 'failure']

        # Very overdue or low reliability → payment plan
        if days_overdue > 45 and reliability < 0.5:
            evidence = [
                {'source': 'invoice', 'detail': f'Invoice {inv_number} is {days_overdue} days overdue'},
                {'source': 'customer', 'detail': f'Payment reliability score: {reliability:.0%} (below threshold)'},
                {'source': 'customer', 'detail': f'Customer segment: {customer.get("segment", "unknown")}'},
            ]
            if failed_payments:
                evidence.append({
                    'source': 'payment_event',
                    'detail': f'Recent payment failure: {failed_payments[0].get("failure_reason", "Unknown reason")}'
                })
            return {
                'recommended_action': 'offer_payment_plan',
                'reason': f'Invoice {inv_number} is significantly overdue ({days_overdue} days) and the customer has a low payment reliability score ({reliability:.0%}). A structured payment plan may increase the likelihood of recovery.',
                'risk_level': 'high',
                'recovery_probability': max(0.20, reliability * 0.6),
                'suggested_follow_up_date': (date.today() + timedelta(days=5)).isoformat(),
                'payment_plan_allowed': True,
                'suggested_message': self._generate_payment_plan_message(
                    customer_name, company, inv_number, amount, due_date
                ),
                'evidence': evidence,
                'confidence': 0.82,
            }

        # Moderately overdue with failed payments
        if failed_payments and days_overdue > 0:
            reason = failed_payments[0].get('failure_reason', 'Unknown reason')
            evidence = [
                {'source': 'invoice', 'detail': f'Invoice {inv_number} is {days_overdue} days overdue'},
                {'source': 'payment_event', 'detail': f'Payment failure detected: {reason}'},
                {'source': 'customer', 'detail': f'Payment reliability score: {reliability:.0%}'},
            ]
            prob = max(0.30, min(0.70, reliability * 0.8))
            return {
                'recommended_action': 'send_reminder',
                'reason': f'A payment attempt for invoice {inv_number} failed ({reason}). Sending a reminder with updated payment instructions is recommended.',
                'risk_level': 'medium' if reliability > 0.5 else 'high',
                'recovery_probability': prob,
                'suggested_follow_up_date': (date.today() + timedelta(days=5)).isoformat(),
                'payment_plan_allowed': days_overdue > 30,
                'suggested_message': self._generate_payment_failure_message(
                    customer_name, company, inv_number, amount, due_date, reason
                ),
                'evidence': evidence,
                'confidence': 0.85,
            }

        # Standard overdue → send reminder
        if days_overdue > 0:
            if reliability >= 0.8:
                risk = 'low'
                prob = max(0.70, min(0.95, reliability))
                confidence = 0.90
            elif reliability >= 0.5:
                risk = 'medium'
                prob = max(0.50, min(0.80, reliability * 0.9))
                confidence = 0.85
            else:
                risk = 'high'
                prob = max(0.25, reliability * 0.7)
                confidence = 0.78

            evidence = [
                {'source': 'invoice', 'detail': f'Invoice {inv_number} is {days_overdue} days past due date ({due_date})'},
                {'source': 'customer', 'detail': f'Customer {customer_name} ({company}) — Segment: {customer.get("segment", "unknown")}'},
                {'source': 'customer', 'detail': f'Lifetime value: ${customer.get("lifetime_value", 0):,.2f} | Payment reliability: {reliability:.0%}'},
                {'source': 'customer', 'detail': f'Total previously paid: ${customer.get("total_paid", 0):,.2f}'},
            ]

            return {
                'recommended_action': 'send_reminder',
                'reason': f'Invoice {inv_number} for ${amount:,.2f} is {days_overdue} days overdue. Based on the customer\'s payment history (reliability: {reliability:.0%}) and lifetime value (${customer.get("lifetime_value", 0):,.2f}), a professional payment reminder is recommended.',
                'risk_level': risk,
                'recovery_probability': prob,
                'suggested_follow_up_date': follow_up_date,
                'payment_plan_allowed': days_overdue > 30 or amount > 10000,
                'suggested_message': self._generate_reminder_message(
                    customer_name, company, inv_number, amount, due_date, days_overdue
                ),
                'evidence': evidence,
                'confidence': confidence,
            }

        # Not overdue
        return {
            'recommended_action': 'no_action',
            'reason': f'Invoice {inv_number} is not yet overdue. No action is required at this time.',
            'risk_level': 'low',
            'recovery_probability': 0.95,
            'suggested_follow_up_date': follow_up_date,
            'payment_plan_allowed': False,
            'suggested_message': '',
            'evidence': [
                {'source': 'invoice', 'detail': f'Invoice {inv_number} due date ({due_date}) has not passed.'}
            ],
            'confidence': 0.95,
        }

    def _generate_reminder_message(self, name, company, inv_num, amount, due_date, days_overdue):
        return (
            f"Dear {name},\n\n"
            f"I hope this message finds you well. I'm writing regarding invoice {inv_num} "
            f"for ${amount:,.2f}, which was due on {due_date} and is now {days_overdue} days past due.\n\n"
            f"We understand that oversights can happen, and we'd like to help resolve this promptly. "
            f"Could you please arrange payment at your earliest convenience?\n\n"
            f"Payment can be made via:\n"
            f"• Online: https://demo.recoverai.local/pay/{inv_num}\n"
            f"• Bank transfer to our account on file\n\n"
            f"If you have any questions about this invoice or need to discuss payment arrangements, "
            f"please don't hesitate to contact our accounts receivable team at ar@recoverai.demo or "
            f"call us at +1-555-0100.\n\n"
            f"Thank you for your continued partnership.\n\n"
            f"Best regards,\n"
            f"Accounts Receivable Team\n"
            f"RecoverAI Demo Corp"
        )

    def _generate_payment_failure_message(self, name, company, inv_num, amount, due_date, failure_reason):
        return (
            f"Dear {name},\n\n"
            f"We're writing to let you know that a recent payment attempt for invoice {inv_num} "
            f"(${amount:,.2f}, due {due_date}) was unsuccessful.\n\n"
            f"Reason: {failure_reason}\n\n"
            f"To ensure uninterrupted service, please update your payment method or arrange "
            f"an alternative payment:\n\n"
            f"• Update payment method: https://demo.recoverai.local/pay/{inv_num}\n"
            f"• Contact us to arrange payment: ar@recoverai.demo\n\n"
            f"If you believe this is an error or need assistance, our team is here to help.\n\n"
            f"Best regards,\n"
            f"Accounts Receivable Team\n"
            f"RecoverAI Demo Corp"
        )

    def _generate_payment_plan_message(self, name, company, inv_num, amount, due_date):
        return (
            f"Dear {name},\n\n"
            f"We're reaching out regarding the outstanding balance on invoice {inv_num} "
            f"(${amount:,.2f}, originally due {due_date}).\n\n"
            f"We understand that managing cash flow can be challenging, and we'd like to work "
            f"with you to find a solution. We can offer a structured payment plan to help you "
            f"clear this balance over time.\n\n"
            f"To discuss payment plan options, please:\n"
            f"• Reply to this message\n"
            f"• Contact our team at ar@recoverai.demo\n"
            f"• Call us at +1-555-0100\n\n"
            f"We value our relationship with {company} and want to find an arrangement "
            f"that works for both of us.\n\n"
            f"Best regards,\n"
            f"Accounts Receivable Team\n"
            f"RecoverAI Demo Corp"
        )
