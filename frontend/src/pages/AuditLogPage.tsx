import React, { useEffect, useState } from 'react';
import { auditApi } from '../services/api';
import { AuditLog } from '../types';
import { Shield, RefreshCw, AlertCircle, ChevronLeft, ChevronRight, Filter } from 'lucide-react';

const ACTION_LABELS: Record<string, string> = {
  user_login: 'User Login',
  user_logout: 'User Logout',
  ai_analysis_completed: 'AI Analysis Completed',
  reminder_drafted: 'Reminder Drafted',
  reminder_sent: 'Reminder Sent',
  reminder_approved: 'Reminder Approved',
  invoice_escalated: 'Invoice Escalated',
  invoice_marked_paid: 'Invoice Marked Paid',
  note_added: 'Note Added',
  settings_updated: 'Settings Updated',
};

const RESULT_STYLES: Record<string, string> = {
  success: 'bg-emerald-100 text-emerald-700',
  failure: 'bg-red-100 text-red-700',
  blocked: 'bg-amber-100 text-amber-700',
};

const AuditLogPage: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [total, setTotal] = useState(0);
  const [pages, setPages] = useState(1);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [actionFilter, setActionFilter] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const params: Record<string, string | number> = { page, per_page: 25 };
      if (actionFilter) params.action = actionFilter;
      const res = await auditApi.list(params);
      setLogs(res.data.logs);
      setTotal(res.data.total);
      setPages(res.data.pages);
    } catch {
      setError('Failed to load audit logs');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [page, actionFilter]);

  if (error) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[50vh]">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-3" />
          <p className="text-gray-600">{error}</p>
          <button onClick={load} className="mt-3 text-indigo-600 font-medium text-sm flex items-center gap-1 mx-auto"><RefreshCw className="w-4 h-4" /> Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 lg:p-8 space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Shield className="w-6 h-6 text-indigo-500" /> Audit Log
          </h1>
          <p className="text-sm text-gray-500 mt-0.5">{total} entries · Read-only</p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-3 items-center">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-gray-400" />
          <select
            value={actionFilter}
            onChange={(e) => { setActionFilter(e.target.value); setPage(1); }}
            className="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
          >
            <option value="">All Actions</option>
            {Object.entries(ACTION_LABELS).map(([k, v]) => (
              <option key={k} value={k}>{v}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl border border-gray-100 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-100">
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Timestamp</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">User</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Action</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Entity</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Entity ID</th>
                <th className="text-center px-4 py-3 font-semibold text-gray-600">Result</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Details</th>
              </tr>
            </thead>
            <tbody>
              {loading ? Array.from({ length: 8 }).map((_, i) => (
                <tr key={i} className="border-b border-gray-50">
                  {Array.from({ length: 7 }).map((_, j) => (
                    <td key={j} className="px-4 py-3"><div className="h-4 bg-gray-100 rounded animate-pulse" /></td>
                  ))}
                </tr>
              )) : logs.length === 0 ? (
                <tr>
                  <td colSpan={7} className="text-center py-12 text-gray-400">No audit log entries found</td>
                </tr>
              ) : logs.map(log => (
                <tr key={log.id} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                  <td className="px-4 py-3 text-xs text-gray-500 whitespace-nowrap">
                    {new Date(log.created_at).toLocaleString()}
                  </td>
                  <td className="px-4 py-3 font-medium text-gray-900">{log.user_name}</td>
                  <td className="px-4 py-3">
                    <span className="text-gray-700">{ACTION_LABELS[log.action] || log.action}</span>
                  </td>
                  <td className="px-4 py-3 text-gray-600 capitalize">{log.entity_type}</td>
                  <td className="px-4 py-3 font-mono text-xs text-gray-500">{log.entity_id || '—'}</td>
                  <td className="px-4 py-3 text-center">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${RESULT_STYLES[log.result] || 'bg-gray-100 text-gray-600'}`}>
                      {log.result}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-xs text-gray-500 max-w-[200px] truncate">
                    {log.details && Object.keys(log.details).length > 0
                      ? JSON.stringify(log.details).substring(0, 80) + '...'
                      : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {pages > 1 && (
          <div className="flex items-center justify-between px-4 py-3 border-t border-gray-100">
            <p className="text-xs text-gray-500">Page {page} of {pages} ({total} entries)</p>
            <div className="flex gap-1">
              <button onClick={() => setPage(Math.max(1, page - 1))} disabled={page <= 1} className="p-1.5 rounded hover:bg-gray-100 disabled:opacity-40">
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button onClick={() => setPage(Math.min(pages, page + 1))} disabled={page >= pages} className="p-1.5 rounded hover:bg-gray-100 disabled:opacity-40">
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuditLogPage;
