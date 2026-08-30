import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { invoiceApi } from '../services/api';
import { useAuth } from '../hooks/useAuth';
import { use3D } from '../3d/ThreeDContext';
import { Card3D } from '../3d/Card3D';
import { AIOrb3D } from '../3d/AIOrb3D';
import { Invoice, RecoveryAnalysis } from '../types';
import toast, { Toaster } from 'react-hot-toast';
import {
  ArrowLeft, Brain, Send, AlertTriangle, CheckCircle, XCircle,
  MessageSquare, DollarSign, ShieldAlert, Clock, FileText,
  Sparkles, User, ChevronDown, ChevronUp, Loader2, Ban,
  Flag, StickyNote, RefreshCw, AlertCircle, ExternalLink, ShieldCheck, CheckCircle2
} from 'lucide-react';

const InvoiceDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { user, isManager } = useAuth();
  const { isPitchMode } = use3D();
  const navigate = useNavigate();
  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [analysis, setAnalysis] = useState<RecoveryAnalysis | null>(null);
  const [message, setMessage] = useState('');
  const [noteText, setNoteText] = useState('');
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [sending, setSending] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [showEscalateModal, setShowEscalateModal] = useState(false);
  const [escalateReason, setEscalateReason] = useState('');
  const [error, setError] = useState('');

  const loadInvoice = async () => {
    if (!id) return;
    setLoading(true);
    setError('');
    try {
      const res = await invoiceApi.get(parseInt(id));
      setInvoice(res.data);
      // Load latest analysis if exists
      if (res.data.analyses && res.data.analyses.length > 0) {
        const latest = res.data.analyses[0];
        setAnalysis(latest);
        if (latest.suggested_message) setMessage(latest.suggested_message);
      }
    } catch {
      setError('Failed to load invoice details');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadInvoice(); }, [id]);

  const handleAnalyze = async () => {
    if (!invoice) return;
    setAnalyzing(true);
    try {
      const res = await invoiceApi.analyze(invoice.id);
      setAnalysis(res.data.analysis);
      if (res.data.analysis.suggested_message) {
        setMessage(res.data.analysis.suggested_message);
      }
      toast.success('AI recovery analysis generated with evidence citations.');
      loadInvoice();
    } catch (err: any) {
      toast.error(err.response?.data?.error || 'Analysis failed');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleSendReminder = async () => {
    if (!invoice || !message.trim()) return;
    setSending(true);
    try {
      const key = `send-${invoice.id}-${Date.now()}`;
      await invoiceApi.sendReminder(invoice.id, message, key);
      toast.success('Financial recovery reminder dispatched (Mock Channel).');
      setShowConfirmModal(false);
      loadInvoice();
    } catch (err: any) {
      toast.error(err.response?.data?.error || 'Failed to send reminder');
    } finally {
      setSending(false);
    }
  };

  const handleEscalate = async () => {
    if (!invoice) return;
    try {
      await invoiceApi.escalate(invoice.id, escalateReason || 'Escalated for senior human review');
      toast.success('Invoice escalated to senior collections team.');
      setShowEscalateModal(false);
      loadInvoice();
    } catch (err: any) {
      toast.error(err.response?.data?.error || 'Escalation failed');
    }
  };

  const handleMarkPaid = async () => {
    if (!invoice) return;
    if (!confirm('Mark this invoice as fully recovered and paid?')) return;
    try {
      await invoiceApi.markPaid(invoice.id);
      toast.success('Invoice marked as recovered and paid.');
      loadInvoice();
    } catch (err: any) {
      toast.error(err.response?.data?.error || 'Failed to mark as paid');
    }
  };

  const handleAddNote = async () => {
    if (!invoice || !noteText.trim()) return;
    try {
      await invoiceApi.addNote(invoice.id, noteText.trim());
      setNoteText('');
      toast.success('Audit note logged.');
      loadInvoice();
    } catch (err: any) {
      toast.error(err.response?.data?.error || 'Failed to add note');
    }
  };

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  if (error || !invoice) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-rose-400 mx-auto mb-3" />
          <p className="text-slate-300">{error || 'Invoice not found'}</p>
          <button onClick={() => navigate(-1)} className="mt-3 text-indigo-400 font-medium text-sm">Go Back</button>
        </div>
      </div>
    );
  }

  const canSend = invoice.can_send_reminder && (isManager || !invoice.requires_manager_approval);
  const isDisputed = invoice.dispute_status === 'open';
  const isPaid = invoice.status === 'paid';

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      <Toaster position="top-right" />

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate(-1)}
            className="p-2.5 bg-slate-900/90 hover:bg-slate-800 border border-slate-700 text-slate-300 hover:text-white rounded-xl transition-colors cursor-pointer"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl lg:text-3xl font-extrabold text-white font-mono tracking-tight">
                {invoice.invoice_number}
              </h1>
              {invoice.has_duplicate_warning && (
                <span className="flex items-center gap-1 px-2.5 py-0.5 bg-amber-950/80 text-amber-300 border border-amber-800/60 rounded-full text-xs font-semibold">
                  <AlertTriangle className="w-3.5 h-3.5" /> Possible Duplicate
                </span>
              )}
            </div>
            <p className="text-sm text-indigo-300/90 font-medium">{invoice.customer?.company}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400 font-mono">Operator: <strong className="text-white">{user?.name}</strong> ({user?.role})</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Invoice Details, AI Core, Message */}
        <div className="lg:col-span-2 space-y-6">
          {/* Invoice Summary */}
          <div className="bg-slate-900/85 backdrop-blur-xl rounded-2xl border border-slate-800/80 p-6 shadow-xl">
            <h3 className="font-bold text-white mb-5 flex items-center gap-2 text-sm uppercase tracking-wider font-mono">
              <FileText className="w-4 h-4 text-cyan-400" /> Invoice Overview
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-5">
              <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/70">
                <p className="text-[11px] font-mono text-slate-400 uppercase mb-1">Total Amount</p>
                <p className="text-xl font-extrabold text-white">${invoice.amount.toLocaleString()}</p>
              </div>
              <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/70">
                <p className="text-[11px] font-mono text-slate-400 uppercase mb-1">Status</p>
                <span className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-bold capitalize ${
                  isPaid ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
                  invoice.status === 'overdue' ? 'bg-rose-950 text-rose-300 border border-rose-800' :
                  invoice.status === 'reminder_sent' ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                  'bg-slate-800 text-slate-300'
                }`}>{invoice.status.replace('_', ' ')}</span>
              </div>
              <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/70">
                <p className="text-[11px] font-mono text-slate-400 uppercase mb-1">Due Date</p>
                <p className="font-mono text-sm text-slate-200">{invoice.due_date}</p>
              </div>
              <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/70">
                <p className="text-[11px] font-mono text-slate-400 uppercase mb-1">Days Overdue</p>
                <p className={`font-mono text-sm font-bold ${invoice.days_overdue > 30 ? 'text-rose-400' : invoice.days_overdue > 0 ? 'text-amber-400' : 'text-slate-400'}`}>
                  {invoice.days_overdue > 0 ? `${invoice.days_overdue} days` : 'Current'}
                </p>
              </div>
              <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/70">
                <p className="text-[11px] font-mono text-slate-400 uppercase mb-1">Risk Level</p>
                <span className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-bold capitalize ${
                  invoice.risk_level === 'high' ? 'bg-rose-950 text-rose-300 border border-rose-800' :
                  invoice.risk_level === 'medium' ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                  'bg-emerald-950 text-emerald-300 border border-emerald-800'
                }`}>{invoice.risk_level}</span>
              </div>
              <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/70">
                <p className="text-[11px] font-mono text-slate-400 uppercase mb-1">Dispute Status</p>
                <span className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-bold capitalize ${
                  isDisputed ? 'bg-rose-950 text-rose-300 border border-rose-700 animate-pulse' : 'bg-slate-800 text-slate-300'
                }`}>{invoice.dispute_status}</span>
              </div>
            </div>
          </div>

          {/* Customer Profile */}
          {invoice.customer && (
            <div className="bg-slate-900/85 backdrop-blur-xl rounded-2xl border border-slate-800/80 p-6 shadow-xl">
              <h3 className="font-bold text-white mb-4 flex items-center gap-2 text-sm uppercase tracking-wider font-mono">
                <User className="w-4 h-4 text-purple-400" /> Customer Financial Profile
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-xs">
                <div><p className="text-slate-400 mb-0.5">Contact Name</p><p className="font-semibold text-white">{invoice.customer.name}</p></div>
                <div><p className="text-slate-400 mb-0.5">Company</p><p className="font-semibold text-white">{invoice.customer.company}</p></div>
                <div><p className="text-slate-400 mb-0.5">Email</p><p className="text-indigo-300 font-mono">{invoice.customer.email || 'No email'}</p></div>
                <div><p className="text-slate-400 mb-0.5">Customer Segment</p><p className="capitalize font-semibold text-white">{invoice.customer.customer_segment.replace('_', ' ')}</p></div>
                <div><p className="text-slate-400 mb-0.5">Lifetime Value</p><p className="font-bold text-emerald-400">${invoice.customer.lifetime_value.toLocaleString()}</p></div>
                <div><p className="text-slate-400 mb-0.5">Reliability Score</p><p className="font-bold text-cyan-400 font-mono">{(invoice.customer.payment_reliability_score * 100).toFixed(0)}%</p></div>
              </div>
            </div>
          )}

          {/* AI Analysis with 3D Holographic Neural Core */}
          <div className="bg-slate-900/90 border border-indigo-500/30 rounded-2xl p-6 relative overflow-hidden shadow-2xl">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-white flex items-center gap-2 text-sm">
                <Sparkles className="w-4 h-4 text-cyan-400 animate-pulse" /> AI Neural Recovery Copilot
              </h3>
              <span className="text-[10px] font-mono text-cyan-300 bg-cyan-950/80 border border-cyan-800/60 px-2.5 py-1 rounded-full">
                {analyzing ? 'Synthesizing Neural Matrix...' : 'AI Active Engine'}
              </span>
            </div>

            {/* 3D Holographic AI Neural Orb */}
            <div className="flex flex-col sm:flex-row items-center gap-4 bg-slate-950/80 p-5 rounded-2xl border border-indigo-900/50 mb-5">
              <AIOrb3D isAnalyzing={analyzing} size={110} />
              <div className="text-center sm:text-left flex-1">
                <h4 className="text-sm font-bold text-white flex items-center justify-center sm:justify-start gap-1.5">
                  <span>Holographic Recovery Strategy</span>
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
                </h4>
                <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                  {analyzing
                    ? 'Processing invoice parameters, customer payment reliability, and dispute safeguards...'
                    : analysis
                    ? 'Strategy synthesized with deterministic business validation rules.'
                    : 'Click "Analyze with AI" to compute recovery probability, tone strategy, and evidence citations.'}
                </p>
              </div>
            </div>

            {analysis ? (
              <div className="space-y-4">
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="bg-indigo-950/70 border border-indigo-800/60 rounded-xl p-3.5">
                    <p className="text-[10px] text-indigo-400 uppercase font-mono font-semibold mb-1">Recommended</p>
                    <p className="text-sm font-bold text-indigo-200 capitalize">{analysis.recommended_action.replace(/_/g, ' ')}</p>
                  </div>
                  <div className="bg-slate-950/70 border border-slate-800/60 rounded-xl p-3.5">
                    <p className="text-[10px] text-slate-400 uppercase font-mono font-semibold mb-1">Risk Level</p>
                    <p className={`text-sm font-bold capitalize ${analysis.risk_level === 'high' ? 'text-rose-400' : analysis.risk_level === 'medium' ? 'text-amber-400' : 'text-emerald-400'}`}>{analysis.risk_level}</p>
                  </div>
                  <div className="bg-slate-950/70 border border-slate-800/60 rounded-xl p-3.5">
                    <p className="text-[10px] text-slate-400 uppercase font-mono font-semibold mb-1">Recovery Prob.</p>
                    <p className="text-sm font-bold text-cyan-300 font-mono">{(analysis.recovery_probability * 100).toFixed(0)}%</p>
                  </div>
                  <div className="bg-slate-950/70 border border-slate-800/60 rounded-xl p-3.5">
                    <p className="text-[10px] text-slate-400 uppercase font-mono font-semibold mb-1">Confidence</p>
                    <p className="text-sm font-bold text-white font-mono">{(analysis.confidence * 100).toFixed(0)}%</p>
                  </div>
                </div>

                <div className="bg-indigo-950/50 border border-indigo-800/50 rounded-xl p-4">
                  <p className="text-xs text-slate-200 leading-relaxed">{analysis.reason}</p>
                </div>

                {analysis.payment_plan_allowed && (
                  <div className="flex items-center gap-2 text-xs text-emerald-300 bg-emerald-950/50 border border-emerald-800/50 rounded-xl px-3.5 py-2.5">
                    <CheckCircle className="w-4 h-4 text-emerald-400" /> Installment / Payment plan option permitted for this profile
                  </div>
                )}

                <div>
                  <p className="text-xs text-slate-400 mb-2 font-semibold uppercase tracking-wider font-mono">Evidence Citations</p>
                  <div className="space-y-2">
                    {analysis.evidence?.map((ev, i) => (
                      <div key={i} className="flex items-start gap-2 text-xs bg-slate-950/80 p-2.5 rounded-xl border border-slate-800/60">
                        <span className="px-2 py-0.5 bg-indigo-950 text-indigo-300 border border-indigo-800/60 rounded text-[10px] font-mono shrink-0 mt-0.5">{ev.source}</span>
                        <span className="text-slate-300">{ev.detail}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <p className="text-[10px] text-slate-500 font-mono">Engine: {analysis.model_name} • Optimal Follow-up Date: {analysis.suggested_follow_up_date}</p>
              </div>
            ) : (
              <div className="text-center py-6">
                <Brain className="w-10 h-10 text-cyan-400/60 mx-auto mb-2 animate-pulse" />
                <p className="text-slate-400 text-xs">Ready to evaluate customer behavioral telemetry and compute recovery strategy.</p>
              </div>
            )}
          </div>

          {/* Customer Message Card (Clearly Labeled) */}
          <div className="bg-slate-900/85 backdrop-blur-xl rounded-2xl border border-slate-800/80 p-6 shadow-xl">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-bold text-white flex items-center gap-2 text-sm">
                <MessageSquare className="w-4 h-4 text-cyan-400" /> Suggested Customer Message
              </h3>
              {message && (
                <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/60 border border-cyan-800/50 px-2.5 py-0.5 rounded-full flex items-center gap-1">
                  <Sparkles className="w-3 h-3" /> AI-Generated Draft
                </span>
              )}
            </div>
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows={8}
              className="w-full px-4 py-3 bg-slate-950/90 border border-slate-700/80 text-white rounded-xl text-xs focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none resize-y leading-relaxed font-sans"
              placeholder="Suggested recovery message will appear here after AI analysis..."
            />
          </div>

          {/* Notes & Audit History */}
          <div className="bg-slate-900/85 backdrop-blur-xl rounded-2xl border border-slate-800/80 p-6 shadow-xl">
            <h3 className="font-bold text-white mb-3 flex items-center gap-2 text-sm">
              <StickyNote className="w-4 h-4 text-indigo-400" /> Operator Audit Notes
            </h3>
            <div className="flex gap-2 mb-4">
              <input
                type="text"
                value={noteText}
                onChange={(e) => setNoteText(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') handleAddNote(); }}
                placeholder="Log internal note or payment agreement..."
                className="flex-1 px-4 py-2.5 bg-slate-950/90 border border-slate-700/80 text-white rounded-xl text-xs focus:ring-2 focus:ring-indigo-500 outline-none font-sans"
              />
              <button
                onClick={handleAddNote}
                disabled={!noteText.trim()}
                className="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold disabled:opacity-50 transition-colors cursor-pointer"
              >
                Add Note
              </button>
            </div>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {invoice.notes?.map(n => (
                <div key={n.id} className="bg-slate-950/70 border border-slate-800/70 rounded-xl px-3.5 py-2.5">
                  <div className="flex items-center justify-between">
                    <p className="text-xs font-bold text-indigo-300">{n.user_name}</p>
                    <p className="text-[10px] text-slate-400 font-mono">{new Date(n.created_at).toLocaleString()}</p>
                  </div>
                  <p className="text-xs text-slate-300 mt-1">{n.content}</p>
                </div>
              ))}
              {(!invoice.notes || invoice.notes.length === 0) && (
                <p className="text-slate-500 text-xs text-center py-3 font-mono">No operator notes recorded yet</p>
              )}
            </div>
          </div>
        </div>

        {/* Right Column - Actions & Safety Guardrails */}
        <div className="space-y-6">
          {/* Action Center */}
          <div className="bg-slate-900/90 backdrop-blur-xl rounded-2xl border border-slate-800/80 p-6 space-y-4 shadow-2xl">
            <h3 className="font-bold text-white text-sm uppercase tracking-wider font-mono flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-indigo-400" /> Action & Safety Center
            </h3>

            {/* 1. Prominent AI Analysis Button */}
            <button
              onClick={handleAnalyze}
              disabled={analyzing || isPaid}
              className="w-full flex items-center justify-center gap-2 px-4 py-3.5 bg-gradient-to-r from-indigo-600 via-purple-600 to-cyan-500 hover:from-indigo-500 hover:to-cyan-400 text-white rounded-xl text-xs font-bold shadow-lg shadow-indigo-600/30 transition-all transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 cursor-pointer"
            >
              {analyzing ? <Loader2 className="w-4 h-4 animate-spin" /> : <Brain className="w-4 h-4 animate-pulse" />}
              <span>{analyzing ? 'Analyzing Parameters...' : 'Analyze with AI'}</span>
            </button>

            {/* Disputed Guardrail Notice */}
            {isDisputed && (
              <div className="p-3.5 bg-rose-950/80 border border-rose-800/80 rounded-xl text-rose-300 text-xs leading-relaxed flex items-start gap-2.5">
                <Ban className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                <div>
                  <strong className="text-rose-200 block mb-0.5">Dispute Guardrail Active:</strong>
                  Sending reminders is disabled for disputed invoices — Escalate to Human review required.
                </div>
              </div>
            )}

            {/* 2. Prominent Approve & Send Button */}
            <button
              onClick={() => setShowConfirmModal(true)}
              disabled={!canSend || !message.trim() || !analysis || isPaid || isDisputed}
              title={isDisputed ? "Sending reminders is disabled for disputed invoices" : "Approve and send reminder"}
              className="w-full flex items-center justify-center gap-2 px-4 py-3.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-emerald-600/30 transition-all transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
            >
              <Send className="w-4 h-4" />
              <span>Approve & Send Reminder</span>
            </button>

            {/* 3. Escalate to Human */}
            <button
              onClick={() => setShowEscalateModal(true)}
              disabled={isPaid}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-amber-600/80 hover:bg-amber-600 text-white rounded-xl text-xs font-semibold border border-amber-500/40 transition-colors disabled:opacity-50 cursor-pointer"
            >
              <Flag className="w-4 h-4" />
              <span>Escalate to Human</span>
            </button>

            {/* 4. Mark Paid */}
            <button
              onClick={handleMarkPaid}
              disabled={isPaid}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-slate-800/90 hover:bg-slate-800 text-slate-200 hover:text-white rounded-xl text-xs font-semibold border border-slate-700 transition-colors disabled:opacity-50 cursor-pointer"
            >
              <DollarSign className="w-4 h-4 text-emerald-400" />
              <span>Mark as Paid</span>
            </button>

            {invoice.requires_manager_approval && !isManager && (
              <div className="p-3 bg-amber-950/60 border border-amber-800/60 rounded-xl text-amber-300 text-xs flex items-center gap-2">
                <ShieldAlert className="w-4 h-4 text-amber-400 shrink-0" />
                <span>High value: Requires Finance Manager sign-off</span>
              </div>
            )}
          </div>

          {/* Support Tickets */}
          {invoice.support_tickets && invoice.support_tickets.length > 0 && (
            <div className="bg-slate-900/85 backdrop-blur-xl rounded-2xl border border-rose-900/50 p-6 shadow-xl">
              <h3 className="font-bold text-rose-300 mb-3 flex items-center gap-2 text-xs uppercase tracking-wider font-mono">
                <AlertTriangle className="w-4 h-4 text-rose-400" /> Linked Support Tickets
              </h3>
              {invoice.support_tickets.map(t => (
                <div key={t.id} className="bg-rose-950/60 border border-rose-800/50 rounded-xl p-3.5 text-xs text-slate-300">
                  <p className="font-bold text-white">{t.subject}</p>
                  <p className="text-slate-400 text-xs mt-1">{t.description}</p>
                  <div className="flex items-center gap-2 mt-2 font-mono">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-900/80 text-rose-200 border border-rose-700/60">{t.priority} priority</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-300">{t.status}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Activity Timeline */}
          <div className="bg-slate-900/85 backdrop-blur-xl rounded-2xl border border-slate-800/80 p-6 shadow-xl">
            <h3 className="font-bold text-white mb-4 flex items-center gap-2 text-xs uppercase tracking-wider font-mono">
              <Clock className="w-4 h-4 text-indigo-400" /> Recovery Action History
            </h3>
            <div className="space-y-3 max-h-72 overflow-y-auto">
              {invoice.recovery_actions?.map((a: any) => (
                <div key={a.id} className="flex items-start gap-2.5 text-xs border-l-2 border-indigo-500/40 pl-3 py-1">
                  <div>
                    <p className="font-semibold text-slate-200 capitalize">{a.action_type.replace(/_/g, ' ')} ({a.action_status})</p>
                    <p className="text-[10px] text-slate-400 mt-0.5 line-clamp-1">{a.message}</p>
                    <p className="text-[10px] text-slate-500 font-mono mt-0.5">{new Date(a.created_at).toLocaleString()}</p>
                  </div>
                </div>
              ))}
              {(!invoice.recovery_actions || invoice.recovery_actions.length === 0) && (
                <p className="text-slate-500 text-xs text-center py-3 font-mono">No recovery dispatches recorded yet</p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Confirmation Modal */}
      {showConfirmModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-md w-full p-6 shadow-2xl text-slate-200">
            <h3 className="text-lg font-bold text-white mb-2">Approve and Send Recovery Notice</h3>
            <p className="text-xs text-slate-400 mb-4">
              You are about to dispatch a tailored reminder to <strong className="text-white">{invoice.customer?.name}</strong>.
            </p>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs text-slate-300 max-h-40 overflow-y-auto mb-5 font-mono">
              {message}
            </div>
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowConfirmModal(false)}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-semibold"
              >
                Cancel
              </button>
              <button
                onClick={handleSendReminder}
                disabled={sending}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold flex items-center gap-1.5"
              >
                {sending ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Send className="w-3.5 h-3.5" />}
                <span>Confirm & Dispatch</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Escalation Modal */}
      {showEscalateModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-md w-full p-6 shadow-2xl text-slate-200">
            <h3 className="text-lg font-bold text-white mb-2">Escalate Invoice to Senior Review</h3>
            <textarea
              value={escalateReason}
              onChange={(e) => setEscalateReason(e.target.value)}
              placeholder="Provide context for escalation (e.g. open billing discrepancy, VIP account negotiation)..."
              rows={3}
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white outline-none mb-4"
            />
            <div className="flex gap-3 justify-end">
              <button onClick={() => setShowEscalateModal(false)} className="px-4 py-2 bg-slate-800 text-white rounded-xl text-xs">
                Cancel
              </button>
              <button onClick={handleEscalate} className="px-4 py-2 bg-amber-600 text-white rounded-xl text-xs font-bold">
                Confirm Escalation
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default InvoiceDetailPage;
