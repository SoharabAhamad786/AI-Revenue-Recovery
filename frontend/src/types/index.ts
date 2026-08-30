export interface User {
  id: number;
  name: string;
  email: string;
  role: 'finance_manager' | 'finance_analyst';
  created_at: string;
}

export interface Customer {
  id: number;
  name: string;
  company: string;
  email: string | null;
  phone: string;
  customer_segment: string;
  lifetime_value: number;
  payment_reliability_score: number;
  total_paid: number;
  created_at: string;
  overdue_count?: number;
  outstanding_amount?: number;
  risk?: string;
  invoices?: Invoice[];
}

export interface Invoice {
  id: number;
  invoice_number: string;
  customer_id: number;
  amount: number;
  currency: string;
  issue_date: string;
  due_date: string;
  paid_date: string | null;
  status: string;
  dispute_status: string;
  payment_method: string;
  days_overdue: number;
  recovery_probability: number;
  risk_level: string;
  recommended_action: string | null;
  created_at: string;
  updated_at: string;
  customer?: Customer;
  payment_events?: PaymentEvent[];
  analyses?: RecoveryAnalysis[];
  notes?: Note[];
  recovery_actions?: RecoveryAction[];
  support_tickets?: SupportTicket[];
  can_send_reminder?: boolean;
  send_reminder_blocked_reason?: string | null;
  requires_manager_approval?: boolean;
  is_high_value?: boolean;
  has_duplicate_warning?: boolean;
  duplicate_ids?: string[];
  payment_link?: string;
}

export interface PaymentEvent {
  id: number;
  invoice_id: number;
  event_type: string;
  amount: number;
  event_date: string;
  failure_reason: string | null;
  reference_id: string;
  created_at: string;
}

export interface RecoveryAnalysis {
  id: number;
  invoice_id: number;
  recommended_action: string;
  reason: string;
  risk_level: string;
  recovery_probability: number;
  suggested_follow_up_date: string;
  payment_plan_allowed: boolean;
  suggested_message: string;
  evidence: EvidenceItem[];
  model_name: string;
  confidence: number;
  created_by: number;
  created_at: string;
}

export interface EvidenceItem {
  source: string;
  detail: string;
}

export interface RecoveryAction {
  id: number;
  invoice_id: number;
  action_type: string;
  action_status: string;
  message: string;
  approved_by: number | null;
  sent_at: string | null;
  idempotency_key: string;
  created_at: string;
}

export interface SupportTicket {
  id: number;
  customer_id: number;
  invoice_id: number | null;
  subject: string;
  description: string;
  status: string;
  priority: string;
  created_at: string;
}

export interface Note {
  id: number;
  invoice_id: number;
  user_id: number;
  user_name: string;
  content: string;
  created_at: string;
}

export interface AuditLog {
  id: number;
  user_id: number;
  user_name: string;
  action: string;
  entity_type: string;
  entity_id: string;
  result: string;
  details: Record<string, unknown>;
  created_at: string;
}

export interface DashboardSummary {
  total_outstanding: number;
  overdue_amount: number;
  recoverable_amount: number;
  open_disputes: number;
  failed_payments: number;
  recovery_rate: number;
  attention_required: number;
}

export interface TrendData {
  monthly_trends: {
    month: string;
    recovered: number;
    outstanding: number;
    at_risk: number;
  }[];
  status_distribution: {
    status: string;
    count: number;
  }[];
}

export interface AnalyticsOverview {
  recovery_rate: number;
  amount_recovered: number;
  amount_at_risk: number;
  average_days_to_payment: number;
}
