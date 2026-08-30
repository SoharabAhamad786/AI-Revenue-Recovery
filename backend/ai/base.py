"""AI Service base class and factory."""
import json
import os
from datetime import date


VALID_ACTIONS = {'send_reminder', 'offer_payment_plan', 'escalate_to_human', 'mark_for_review', 'no_action'}
VALID_RISK_LEVELS = {'low', 'medium', 'high'}
VALID_SOURCES = {'invoice', 'customer', 'payment_event', 'support_ticket', 'policy'}


def validate_analysis_result(result: dict) -> dict:
    """Validate AI output against the expected schema without pydantic."""
    errors = []

    action = result.get('recommended_action')
    if action not in VALID_ACTIONS:
        errors.append(f"Invalid recommended_action: {action}")

    risk = result.get('risk_level')
    if risk not in VALID_RISK_LEVELS:
        errors.append(f"Invalid risk_level: {risk}")

    prob = result.get('recovery_probability')
    if not isinstance(prob, (int, float)) or prob < 0 or prob > 1:
        errors.append(f"Invalid recovery_probability: {prob}")

    confidence = result.get('confidence')
    if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
        errors.append(f"Invalid confidence: {confidence}")

    follow_up = result.get('suggested_follow_up_date')
    if follow_up:
        try:
            date.fromisoformat(follow_up)
        except (ValueError, TypeError):
            errors.append(f"Invalid date format: {follow_up}")

    if not isinstance(result.get('reason', ''), str):
        errors.append("reason must be a string")

    if not isinstance(result.get('payment_plan_allowed', False), bool):
        errors.append("payment_plan_allowed must be a boolean")

    evidence = result.get('evidence', [])
    if not isinstance(evidence, list):
        errors.append("evidence must be a list")

    if errors:
        raise ValueError(f"AI output validation failed: {'; '.join(errors)}")

    return result


SYSTEM_PROMPT = """You are RecoverAI, an accounts-receivable decision-support assistant.
Analyze only the verified structured data provided to you.
Never invent amounts, dates, discounts, payment terms, customer details, or payment links.
If an invoice has an open dispute, recommend escalation to a human.
You may recommend actions, but you cannot send messages, modify invoices, issue refunds, or make payments.
Return only valid JSON matching the required schema.
Explain your recommendation using the provided evidence.

Required JSON schema:
{
  "recommended_action": "send_reminder | offer_payment_plan | escalate_to_human | mark_for_review | no_action",
  "reason": "string explaining the recommendation",
  "risk_level": "low | medium | high",
  "recovery_probability": 0.0 to 1.0,
  "suggested_follow_up_date": "YYYY-MM-DD",
  "payment_plan_allowed": true or false,
  "suggested_message": "the email/message to send to the customer",
  "evidence": [{"source": "invoice|customer|payment_event|support_ticket|policy", "detail": "string"}],
  "confidence": 0.0 to 1.0
}"""


class AIService:
    """Factory for AI providers."""

    @staticmethod
    def get_provider(provider_name=None):
        if provider_name is None:
            provider_name = os.getenv('AI_PROVIDER', 'mock')

        if provider_name == 'openai':
            try:
                from .openai_provider import OpenAIProvider
                return OpenAIProvider()
            except ImportError:
                from .mock_provider import MockAIProvider
                return MockAIProvider()
        elif provider_name == 'gemini':
            try:
                from .gemini_provider import GeminiProvider
                return GeminiProvider()
            except ImportError:
                from .mock_provider import MockAIProvider
                return MockAIProvider()
        else:
            from .mock_provider import MockAIProvider
            return MockAIProvider()

    @staticmethod
    def validate_result(result_dict: dict) -> dict:
        """Validate AI output against the schema."""
        return validate_analysis_result(result_dict)

    @staticmethod
    def build_context(invoice, customer, payment_events, support_tickets):
        """Build structured context for AI analysis."""
        context = {
            'invoice': {
                'invoice_number': invoice.invoice_number,
                'amount': invoice.amount,
                'currency': invoice.currency,
                'issue_date': invoice.issue_date.isoformat() if invoice.issue_date else None,
                'due_date': invoice.due_date.isoformat() if invoice.due_date else None,
                'status': invoice.status,
                'dispute_status': invoice.dispute_status,
                'payment_method': invoice.payment_method,
                'days_overdue': invoice.compute_days_overdue(),
            },
            'customer': {
                'name': customer.name,
                'company': customer.company,
                'email': customer.email,
                'segment': customer.customer_segment,
                'lifetime_value': customer.lifetime_value,
                'payment_reliability_score': customer.payment_reliability_score,
                'total_paid': customer.total_paid,
            },
            'payment_events': [
                {
                    'event_type': pe.event_type,
                    'amount': pe.amount,
                    'event_date': pe.event_date.isoformat() if pe.event_date else None,
                    'failure_reason': pe.failure_reason,
                }
                for pe in payment_events
            ],
            'support_tickets': [
                {
                    'subject': t.subject,
                    'status': t.status,
                    'priority': t.priority,
                    'description': t.description,
                }
                for t in support_tickets
            ],
        }
        return context
