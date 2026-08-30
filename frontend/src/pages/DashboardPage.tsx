import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { dashboardApi } from '../services/api';
import { DashboardSummary, TrendData, AuditLog } from '../types';
import { Card3D } from '../3d/Card3D';
import { RevenueGalaxy3D } from '../3d/RevenueGalaxy3D';
import { use3D } from '../3d/ThreeDContext';
import {
  DollarSign, AlertTriangle, TrendingUp, Clock,
  AlertCircle, CheckCircle, ListChecks, RefreshCw, Sparkles, ArrowRight
} from 'lucide-react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';

const STATUS_COLORS: Record<string, string> = {
  paid: '#10b981',
  overdue: '#ef4444',
  reminder_sent: '#f59e0b',
  sent: '#6366f1',
  draft: '#94a3b8',
  cancelled: '#64748b',
};

const ACTION_LABELS: Record<string, string> = {
  user_login: 'User Login',
  user_logout: 'User Logout',
  ai_analysis_completed: 'AI Analysis',
  reminder_drafted: 'Reminder Drafted',
  reminder_sent: 'Reminder Sent',
  reminder_approved: 'Reminder Approved',
  invoice_escalated: 'Invoice Escalated',
  invoice_marked_paid: 'Marked Paid',
  note_added: 'Note Added',
  settings_updated: 'Settings Updated',
};

const DashboardPage: React.FC = () => {
  const { is3DMode } = use3D();
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [trends, setTrends] = useState<TrendData | null>(null);
  const [activity, setActivity] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadData = async () => {
    setLoading(true);
    setError('');
    try {
      const [s, t, a] = await Promise.all([
        dashboardApi.summary(),
        dashboardApi.trends(),
        dashboardApi.recentActivity(),
      ]);
      setSummary(s.data);
      setTrends(t.data);
      setActivity(a.data.activities);
    } catch {
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadData(); }, []);

  if (loading) {
    return (
      <div className="p-8 space-y-6">
        <div className="h-8 bg-slate-800/60 rounded-xl w-48 animate-pulse" />
        <div className="grid grid-cols-3 gap-4">
          {[1,2,3,4,5,6].map(i => (
            <div key={i} className="h-28 bg-slate-800/40 rounded-2xl animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[50vh]">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-rose-500 mx-auto mb-3" />
          <p className="text-slate-300">{error}</p>
          <button onClick={loadData} className="mt-3 text-indigo-400 hover:text-indigo-300 font-medium text-sm flex items-center gap-1 mx-auto">
            <RefreshCw className="w-4 h-4" /> Retry
          </button>
        </div>
      </div>
    );
  }

  const kpis = [
    { label: 'Total Outstanding', value: `$${(summary?.total_outstanding || 0).toLocaleString()}`, icon: DollarSign, color: 'text-indigo-400', bg: 'bg-indigo-950/60 border border-indigo-800/40', glow: 'rgba(99, 102, 241, 0.35)' },
    { label: 'Overdue Amount', value: `$${(summary?.overdue_amount || 0).toLocaleString()}`, icon: AlertTriangle, color: 'text-rose-400', bg: 'bg-rose-950/60 border border-rose-800/40', glow: 'rgba(244, 63, 94, 0.35)' },
    { label: 'Recoverable', value: `$${(summary?.recoverable_amount || 0).toLocaleString()}`, icon: TrendingUp, color: 'text-emerald-400', bg: 'bg-emerald-950/60 border border-emerald-800/40', glow: 'rgba(16, 185, 129, 0.35)' },
    { label: 'Open Disputes', value: summary?.open_disputes || 0, icon: AlertCircle, color: 'text-amber-400', bg: 'bg-amber-950/60 border border-amber-800/40', glow: 'rgba(245, 158, 11, 0.35)' },
    { label: 'Failed Payments', value: summary?.failed_payments || 0, icon: Clock, color: 'text-cyan-400', bg: 'bg-cyan-950/60 border border-cyan-800/40', glow: 'rgba(6, 182, 212, 0.35)' },
    { label: 'Recovery Rate', value: `${summary?.recovery_rate || 0}%`, icon: CheckCircle, color: 'text-purple-400', bg: 'bg-purple-950/60 border border-purple-800/40', glow: 'rgba(168, 85, 247, 0.35)' },
  ];

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl lg:text-3xl font-extrabold text-white tracking-tight">
              Recovery Dashboard
            </h1>
            {is3DMode && (
              <span className="text-[11px] font-mono px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-400/30 flex items-center gap-1 shadow-sm">
                <Sparkles className="w-3 h-3 text-cyan-400 animate-spin" style={{ animationDuration: '4s' }} />
                3D Hologram Mode
              </span>
            )}
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Real-time accounts receivable analytics and AI recovery orchestration
          </p>
        </div>
        <Link
          to="/recovery-queue"
          className="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-xl text-sm font-semibold shadow-lg shadow-indigo-500/25 transition-all transform hover:scale-[1.02] active:scale-[0.98] shrink-0"
        >
          <ListChecks className="w-4 h-4" /> Open Recovery Queue
        </Link>
      </div>

      {/* 3D Financial Galaxy Visualizer (When 3D Mode is Active) */}
      {is3DMode && (
        <RevenueGalaxy3D stats={summary || undefined} />
      )}

      {/* KPI Cards (Enhanced with 3D Tilt and Specular Reflection) */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
        {kpis.map(({ label, value, icon: Icon, color, bg, glow }) => (
          <Card3D key={label} intensity={18} glowColor={glow} className="bg-slate-900/80 border-slate-800/80 p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider">{label}</span>
              <div className={`w-8 h-8 ${bg} rounded-xl flex items-center justify-center shadow-inner`}>
                <Icon className={`w-4 h-4 ${color}`} />
              </div>
            </div>
            <p className="text-xl font-black text-white tracking-tight">{value}</p>
          </Card3D>
        ))}
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Trend Chart */}
        <Card3D intensity={8} className="lg:col-span-2 bg-slate-900/80 border-slate-800/80 p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-bold text-white text-base">Monthly Cash Recovery Velocity</h3>
            <span className="text-xs text-slate-400 font-mono">Last 6 Months</span>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={trends?.monthly_trends || []}>
              <defs>
                <linearGradient id="recoveredGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="outstandingGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="riskGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#94a3b8' }} stroke="#475569" />
              <YAxis tick={{ fontSize: 12, fill: '#94a3b8' }} stroke="#475569" tickFormatter={(v) => `$${(v/1000).toFixed(0)}k`} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff' }}
                formatter={(value: any) => [`$${Number(value).toLocaleString()}`, '']}
              />
              <Area type="monotone" dataKey="recovered" stroke="#10b981" strokeWidth={2.5} fillOpacity={1} fill="url(#recoveredGrad)" name="Recovered" />
              <Area type="monotone" dataKey="outstanding" stroke="#6366f1" strokeWidth={2} fillOpacity={1} fill="url(#outstandingGrad)" name="Outstanding" />
              <Area type="monotone" dataKey="at_risk" stroke="#ef4444" strokeWidth={1.5} fillOpacity={1} fill="url(#riskGrad)" name="At Risk" />
            </AreaChart>
          </ResponsiveContainer>
        </Card3D>

        {/* Status Distribution */}
        <Card3D intensity={8} className="bg-slate-900/80 border-slate-800/80 p-5 flex flex-col justify-between">
          <div>
            <h3 className="font-bold text-white text-base mb-2">Portfolio Health</h3>
            <p className="text-xs text-slate-400 mb-4">Invoice state breakdown</p>
          </div>
          <ResponsiveContainer width="100%" height={170}>
            <PieChart>
              <Pie
                data={trends?.status_distribution || []}
                cx="50%"
                cy="50%"
                innerRadius={48}
                outerRadius={75}
                paddingAngle={4}
                dataKey="count"
                nameKey="status"
              >
                {(trends?.status_distribution || []).map((entry) => (
                  <Cell key={entry.status} fill={STATUS_COLORS[entry.status] || '#94a3b8'} stroke="#0f172a" strokeWidth={2} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '10px', color: '#fff' }} />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex flex-wrap gap-2.5 mt-3 justify-center">
            {(trends?.status_distribution || []).map(({ status, count }) => (
              <div key={status} className="flex items-center gap-1.5 text-[11px] bg-slate-800/60 px-2 py-1 rounded-md border border-slate-700/50">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: STATUS_COLORS[status] || '#94a3b8' }} />
                <span className="text-slate-300 capitalize">{status.replace('_', ' ')}:</span>
                <span className="font-bold text-white">{count}</span>
              </div>
            ))}
          </div>
        </Card3D>
      </div>

      {/* Attention Required + Live Audit Stream */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Attention Required */}
        <Card3D intensity={10} className="bg-slate-900/80 border-slate-800/80 p-5">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-amber-400" />
              <h3 className="font-bold text-white">Accounts Requiring Attention</h3>
            </div>
            <span className="px-3 py-1 bg-amber-500/20 text-amber-300 border border-amber-500/30 rounded-full text-xs font-bold font-mono">
              {summary?.attention_required || 0} Critical
            </span>
          </div>
          <p className="text-xs text-slate-400 mb-4">
            Invoices categorized as high-risk or open disputes requiring human manager approval.
          </p>
          <Link
            to="/recovery-queue?status=overdue"
            className="inline-flex items-center gap-2 text-indigo-400 hover:text-indigo-300 text-sm font-semibold group"
          >
            <span>Review Overdue Queue</span>
            <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
          </Link>
        </Card3D>

        {/* Live Audit Log Stream */}
        <Card3D intensity={10} className="bg-slate-900/80 border-slate-800/80 p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-bold text-white">Live AI & Human Activity Stream</h3>
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
          </div>
          <div className="space-y-3 max-h-56 overflow-y-auto pr-1">
            {activity.map((a) => (
              <div key={a.id} className="flex items-start gap-3 text-xs bg-slate-800/40 p-2.5 rounded-xl border border-slate-700/40">
                <div className="w-2 h-2 rounded-full bg-indigo-400 mt-1.5 shrink-0 shadow-sm" />
                <div className="min-w-0 flex-1">
                  <p className="text-slate-200">
                    <span className="font-bold text-white">{a.user_name}</span>{' '}
                    <span className="text-indigo-300">{ACTION_LABELS[a.action] || a.action}</span>
                    {a.entity_id && <span className="text-slate-400 font-mono ml-1">[{a.entity_id}]</span>}
                  </p>
                  <p className="text-[10px] text-slate-500 font-mono mt-0.5">
                    {new Date(a.created_at).toLocaleString()}
                  </p>
                </div>
              </div>
            ))}
            {activity.length === 0 && (
              <p className="text-slate-500 text-xs text-center py-4">No recent activity</p>
            )}
          </div>
        </Card3D>
      </div>
    </div>
  );
};

export default DashboardPage;
