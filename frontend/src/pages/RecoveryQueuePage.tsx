import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { invoiceApi } from '../services/api';
import { Invoice } from '../types';
import { use3D } from '../3d/ThreeDContext';
import {
  Search, Filter, AlertTriangle, ArrowUpDown, RefreshCw,
  AlertCircle, ChevronLeft, ChevronRight, Sparkles, Star, ShieldAlert, CheckCircle2
} from 'lucide-react';

const FILTERS = [
  { key: 'all', label: 'All Invoices' },
  { key: 'overdue', label: 'Overdue' },
  { key: 'failed_payment', label: 'Failed Payment' },
  { key: 'disputed', label: 'Disputed' },
  { key: 'high_value', label: 'High Value' },
  { key: 'reminder_sent', label: 'Reminder Sent' },
  { key: 'paid', label: 'Paid' },
];

const SORT_OPTIONS = [
  { key: 'priority', label: 'Sort: Priority' },
  { key: 'amount', label: 'Sort: Amount' },
  { key: 'days_overdue', label: 'Sort: Days Overdue' },
  { key: 'recovery_probability', label: 'Sort: Recovery Prob.' },
];

const riskBadge = (risk: string) => {
  const cls = risk === 'high' ? 'bg-rose-950/80 text-rose-300 border border-rose-800/60' :
              risk === 'medium' ? 'bg-amber-950/80 text-amber-300 border border-amber-800/60' :
              'bg-emerald-950/80 text-emerald-300 border border-emerald-800/60';
  return <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-semibold capitalize ${cls}`}>{risk}</span>;
};

const statusBadge = (status: string) => {
  const cls = status === 'paid' ? 'bg-emerald-950/80 text-emerald-300 border border-emerald-800/60' :
              status === 'overdue' ? 'bg-rose-950/80 text-rose-300 border border-rose-800/60' :
              status === 'reminder_sent' ? 'bg-amber-950/80 text-amber-300 border border-amber-800/60' :
              'bg-slate-800 text-slate-300 border border-slate-700';
  return <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-semibold capitalize ${cls}`}>{status.replace('_', ' ')}</span>;
};

const RecoveryQueuePage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [total, setTotal] = useState(0);
  const [pages, setPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isDemoScenario, setIsDemoScenario] = useState(false);
  const { isPitchMode } = use3D();
  const navigate = useNavigate();

  const currentFilter = searchParams.get('status') || 'all';
  const currentSort = searchParams.get('sort') || 'priority';
  const currentSearch = searchParams.get('search') || '';
  const currentPage = parseInt(searchParams.get('page') || '1');

  const loadInvoices = async () => {
    setLoading(true);
    setError('');
    try {
      const params: Record<string, string | number> = {
        status: currentFilter,
        sort: currentSort,
        page: currentPage,
        per_page: 15,
      };
      if (currentSearch) params.search = currentSearch;
      const res = await invoiceApi.list(params);
      setInvoices(res.data.invoices);
      setTotal(res.data.total);
      setPages(res.data.pages);
    } catch {
      setError('Failed to load invoices');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadInvoices(); }, [currentFilter, currentSort, currentSearch, currentPage]);

  const updateParam = (key: string, value: string) => {
    const newParams = new URLSearchParams(searchParams);
    newParams.set(key, value);
    if (key !== 'page') newParams.set('page', '1');
    setSearchParams(newParams);
  };

  // Demo invoice special IDs:
  // INV-2024-024 (Jennifer Lee - Overdue $4,850, high recovery prob, clean profile -> Recommended for Demo)
  // INV-2024-004 (Acme Corp - $14,500, Disputed -> Demo Escalation)
  // INV-2024-012 (Global Logistics - $38,000, Overdue -> Demo High Value Gate)
  const isRecommendedDemo = (invNum: string) => invNum === 'INV-2024-024';
  const isDisputedDemo = (invNum: string) => invNum === 'INV-2024-004';
  const isHighValueDemo = (invNum: string) => invNum === 'INV-2024-012';

  const displayedInvoices = isDemoScenario
    ? invoices.filter(i => isRecommendedDemo(i.invoice_number) || isDisputedDemo(i.invoice_number) || isHighValueDemo(i.invoice_number))
    : invoices;

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl lg:text-3xl font-extrabold text-white tracking-tight">
              Recovery Queue
            </h1>
            <span className="text-xs font-mono px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
              {total} Invoices
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Prioritized ledger queue for AI revenue recovery and human sign-off
          </p>
        </div>

        {/* 5-Minute Demo Scenario Filter Toggle */}
        <button
          onClick={() => setIsDemoScenario(prev => !prev)}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold transition-all shadow-lg cursor-pointer ${
            isDemoScenario
              ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-amber-500/30 border border-white/30 scale-105'
              : 'bg-slate-900/90 hover:bg-slate-800 text-amber-300 border border-amber-500/30'
          }`}
        >
          <Star className={`w-4 h-4 ${isDemoScenario ? 'text-white fill-white' : 'text-amber-400'}`} />
          <span>{isDemoScenario ? 'Showing Demo Invoices (3)' : '⭐ 5-Min Demo Scenarios'}</span>
        </button>
      </div>

      {/* Search, Filter, and Sort Controls */}
      <div className="flex flex-wrap gap-3 items-center justify-between bg-slate-900/70 backdrop-blur-md p-4 rounded-2xl border border-slate-800/80">
        <div className="relative flex-1 min-w-[240px] max-w-md">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search customer, company, or invoice ID..."
            defaultValue={currentSearch}
            onKeyDown={(e) => { if (e.key === 'Enter') updateParam('search', (e.target as HTMLInputElement).value); }}
            className="w-full pl-10 pr-4 py-2.5 bg-slate-950/80 border border-slate-700/70 rounded-xl text-xs text-white placeholder-slate-500 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none font-sans"
          />
        </div>

        <div className="flex items-center gap-3">
          <select
            value={currentSort}
            onChange={(e) => updateParam('sort', e.target.value)}
            className="px-3.5 py-2.5 bg-slate-950/80 border border-slate-700/70 text-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-indigo-500 outline-none cursor-pointer"
          >
            {SORT_OPTIONS.map(s => <option key={s.key} value={s.key}>{s.label}</option>)}
          </select>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 flex-wrap pb-1">
        {FILTERS.map(f => (
          <button
            key={f.key}
            onClick={() => {
              setIsDemoScenario(false);
              updateParam('status', f.key);
            }}
            className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
              currentFilter === f.key && !isDemoScenario
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md shadow-indigo-600/30 border border-indigo-400/30'
                : 'bg-slate-900/60 hover:bg-slate-800 text-slate-400 hover:text-white border border-slate-800/80'
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      {/* Error state */}
      {error && (
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <AlertCircle className="w-10 h-10 text-rose-400 mx-auto mb-2" />
            <p className="text-slate-300 text-sm">{error}</p>
            <button onClick={loadInvoices} className="mt-3 text-indigo-400 hover:text-indigo-300 text-sm font-medium flex items-center gap-1 mx-auto">
              <RefreshCw className="w-3.5 h-3.5" /> Retry
            </button>
          </div>
        </div>
      )}

      {/* Data Table */}
      {!error && (
        <div className="bg-slate-900/85 backdrop-blur-xl rounded-2xl border border-slate-800/80 overflow-hidden shadow-2xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead>
                <tr className="bg-slate-950/80 border-b border-slate-800 text-slate-400 font-mono text-[11px] uppercase tracking-wider">
                  <th className="px-4 py-3.5 font-bold">Invoice</th>
                  <th className="px-4 py-3.5 font-bold">Customer & Company</th>
                  <th className="px-4 py-3.5 text-right font-bold">Amount</th>
                  <th className="px-4 py-3.5 font-bold">Due Date</th>
                  <th className="px-4 py-3.5 text-right font-bold">Days Overdue</th>
                  <th className="px-4 py-3.5 text-center font-bold">Status</th>
                  <th className="px-4 py-3.5 text-center font-bold">Risk Level</th>
                  <th className="px-4 py-3.5 text-right font-bold">Recovery Prob.</th>
                  <th className="px-4 py-3.5 font-bold">AI Recommended Action</th>
                  <th className="px-4 py-3.5 text-center font-bold">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {loading ? (
                  Array.from({ length: 6 }).map((_, i) => (
                    <tr key={i} className="animate-pulse">
                      {Array.from({ length: 10 }).map((_, j) => (
                        <td key={j} className="px-4 py-3.5"><div className="h-4 bg-slate-800/60 rounded" /></td>
                      ))}
                    </tr>
                  ))
                ) : displayedInvoices.length === 0 ? (
                  <tr>
                    <td colSpan={10} className="text-center py-16 text-slate-500 font-mono">
                      No invoices match the selected filter criteria
                    </td>
                  </tr>
                ) : displayedInvoices.map(inv => {
                  const isRec = isRecommendedDemo(inv.invoice_number);
                  const isDisp = isDisputedDemo(inv.invoice_number);
                  const isHighVal = isHighValueDemo(inv.invoice_number);

                  return (
                    <tr
                      key={inv.id}
                      onClick={() => navigate(`/invoices/${inv.id}`)}
                      className={`hover:bg-slate-800/50 cursor-pointer transition-colors group ${
                        isRec
                          ? 'bg-indigo-950/40 border-l-4 border-l-amber-400'
                          : isDisp
                          ? 'bg-rose-950/25 border-l-4 border-l-rose-500'
                          : isHighVal
                          ? 'bg-purple-950/25 border-l-4 border-l-purple-500'
                          : ''
                      }`}
                    >
                      <td className="px-4 py-3.5 font-mono text-white font-semibold">
                        <div className="flex items-center gap-1.5">
                          <span>{inv.invoice_number}</span>
                          {isRec && (
                            <span className="bg-amber-400/20 text-amber-300 border border-amber-400/40 text-[9px] px-1.5 py-0.5 rounded font-bold flex items-center gap-0.5">
                              <Star className="w-2.5 h-2.5 fill-amber-300 text-amber-300" /> Demo
                            </span>
                          )}
                          {isDisp && (
                            <span className="bg-rose-400/20 text-rose-300 border border-rose-400/40 text-[9px] px-1.5 py-0.5 rounded font-bold">
                              Disputed
                            </span>
                          )}
                          {isHighVal && (
                            <span className="bg-purple-400/20 text-purple-300 border border-purple-400/40 text-[9px] px-1.5 py-0.5 rounded font-bold">
                              High Value
                            </span>
                          )}
                          {inv.has_duplicate_warning && (
                            <span className="text-amber-400" title="Possible duplicate">
                              <AlertTriangle className="w-3.5 h-3.5 inline" />
                            </span>
                          )}
                        </div>
                      </td>

                      <td className="px-4 py-3.5">
                        <p className="font-semibold text-white group-hover:text-indigo-300 transition-colors">
                          {inv.customer?.name}
                        </p>
                        <p className="text-[11px] text-slate-400">{inv.customer?.company}</p>
                      </td>

                      <td className="px-4 py-3.5 text-right font-black text-white">
                        ${inv.amount.toLocaleString()}
                      </td>

                      <td className="px-4 py-3.5 font-mono text-slate-400">{inv.due_date}</td>

                      <td className="px-4 py-3.5 text-right font-mono">
                        {inv.days_overdue > 0 ? (
                          <span className={`font-bold ${inv.days_overdue > 30 ? 'text-rose-400' : 'text-amber-400'}`}>
                            {inv.days_overdue}d
                          </span>
                        ) : (
                          <span className="text-slate-500">—</span>
                        )}
                      </td>

                      <td className="px-4 py-3.5 text-center">{statusBadge(inv.status)}</td>

                      <td className="px-4 py-3.5 text-center">{riskBadge(inv.risk_level)}</td>

                      <td className="px-4 py-3.5 text-right font-bold text-white font-mono">
                        {(inv.recovery_probability * 100).toFixed(0)}%
                      </td>

                      <td className="px-4 py-3.5 capitalize text-slate-300 max-w-[130px] truncate">
                        {inv.recommended_action?.replace(/_/g, ' ') || 'Pending AI'}
                      </td>

                      <td className="px-4 py-3.5 text-center">
                        <button className="px-3 py-1 bg-indigo-600/30 hover:bg-indigo-600 text-indigo-300 hover:text-white rounded-lg text-xs font-semibold transition-all border border-indigo-500/40 cursor-pointer">
                          View
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {!isDemoScenario && pages > 1 && (
            <div className="flex items-center justify-between px-6 py-4 bg-slate-950/60 border-t border-slate-800 text-xs text-slate-400">
              <span>Page {currentPage} of {pages} ({total} Total Records)</span>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => updateParam('page', String(Math.max(1, currentPage - 1)))}
                  disabled={currentPage <= 1}
                  className="p-1.5 bg-slate-800 hover:bg-slate-700 disabled:opacity-30 rounded-lg text-white transition-colors cursor-pointer"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <button
                  onClick={() => updateParam('page', String(Math.min(pages, currentPage + 1)))}
                  disabled={currentPage >= pages}
                  className="p-1.5 bg-slate-800 hover:bg-slate-700 disabled:opacity-30 rounded-lg text-white transition-colors cursor-pointer"
                >
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RecoveryQueuePage;
