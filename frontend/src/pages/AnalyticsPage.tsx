import React, { useEffect, useState } from 'react';
import { analyticsApi } from '../services/api';
import { AnalyticsOverview } from '../types';
import { TrendingUp, DollarSign, AlertTriangle, Clock, RefreshCw, AlertCircle } from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell, Legend
} from 'recharts';

const SEGMENT_COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];
const AGE_COLORS = ['#10b981', '#6366f1', '#f59e0b', '#ef4444', '#991b1b'];

const AnalyticsPage: React.FC = () => {
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null);
  const [segments, setSegments] = useState<any[]>([]);
  const [ageBuckets, setAgeBuckets] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const [o, s, a] = await Promise.all([
        analyticsApi.overview(),
        analyticsApi.bySegment(),
        analyticsApi.byAge(),
      ]);
      setOverview(o.data);
      setSegments(s.data.segments);
      setAgeBuckets(a.data.age_buckets);
    } catch {
      setError('Failed to load analytics data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  if (loading) {
    return (
      <div className="p-8 space-y-6">
        <div className="h-8 bg-gray-200 rounded w-48 animate-pulse" />
        <div className="grid grid-cols-4 gap-4">
          {[1,2,3,4].map(i => <div key={i} className="h-28 bg-white rounded-xl animate-pulse" />)}
        </div>
        <div className="grid grid-cols-2 gap-6">
          {[1,2].map(i => <div key={i} className="h-72 bg-white rounded-xl animate-pulse" />)}
        </div>
      </div>
    );
  }

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

  const kpis = [
    { label: 'Recovery Rate', value: `${overview?.recovery_rate || 0}%`, icon: TrendingUp, color: 'text-emerald-600', bg: 'bg-emerald-50' },
    { label: 'Amount Recovered', value: `$${(overview?.amount_recovered || 0).toLocaleString()}`, icon: DollarSign, color: 'text-indigo-600', bg: 'bg-indigo-50' },
    { label: 'Amount at Risk', value: `$${(overview?.amount_at_risk || 0).toLocaleString()}`, icon: AlertTriangle, color: 'text-red-600', bg: 'bg-red-50' },
    { label: 'Avg Days to Payment', value: `${overview?.average_days_to_payment || 0}d`, icon: Clock, color: 'text-amber-600', bg: 'bg-amber-50' },
  ];

  return (
    <div className="p-6 lg:p-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
        <p className="text-sm text-gray-500 mt-0.5">Recovery performance insights</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map(({ label, value, icon: Icon, color, bg }) => (
          <div key={label} className="bg-white rounded-xl border border-gray-100 p-5 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">{label}</span>
              <div className={`w-9 h-9 ${bg} rounded-lg flex items-center justify-center`}>
                <Icon className={`w-4.5 h-4.5 ${color}`} />
              </div>
            </div>
            <p className="text-2xl font-bold text-gray-900">{value}</p>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recovery by Segment */}
        <div className="bg-white rounded-xl border border-gray-100 p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Recovery by Customer Segment</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={segments}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="segment" tick={{ fontSize: 11 }} stroke="#94a3b8" />
              <YAxis tick={{ fontSize: 11 }} stroke="#94a3b8" tickFormatter={(v) => `$${(v/1000).toFixed(0)}k`} />
              <Tooltip formatter={(value: any) => [`$${Number(value || 0).toLocaleString()}`, '']} />
              <Bar dataKey="recovered_amount" fill="#10b981" name="Recovered" radius={[4, 4, 0, 0]} />
              <Bar dataKey="total_amount" fill="#e0e7ff" name="Total" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-3 space-y-2">
            {segments.map((s, i) => (
              <div key={s.segment} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full" style={{ backgroundColor: SEGMENT_COLORS[i % SEGMENT_COLORS.length] }} />
                  <span className="capitalize text-gray-700">{s.segment.replace('_', ' ')}</span>
                </div>
                <span className="font-semibold text-gray-900">{s.recovery_rate}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Recovery by Age */}
        <div className="bg-white rounded-xl border border-gray-100 p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Outstanding by Invoice Age</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={ageBuckets} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis type="number" tick={{ fontSize: 11 }} stroke="#94a3b8" tickFormatter={(v) => `$${(v/1000).toFixed(0)}k`} />
              <YAxis type="category" dataKey="age_bucket" tick={{ fontSize: 11 }} stroke="#94a3b8" width={80} />
              <Tooltip formatter={(value: any) => [`$${Number(value || 0).toLocaleString()}`, 'Amount']} />
              <Bar dataKey="total_amount" radius={[0, 4, 4, 0]}>
                {ageBuckets.map((_, i) => (
                  <Cell key={i} fill={AGE_COLORS[i % AGE_COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-3 space-y-2">
            {ageBuckets.map((b, i) => (
              <div key={b.age_bucket} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full" style={{ backgroundColor: AGE_COLORS[i % AGE_COLORS.length] }} />
                  <span className="text-gray-700">{b.age_bucket}</span>
                </div>
                <div className="text-right">
                  <span className="font-semibold text-gray-900">{b.count} invoices</span>
                  <span className="text-gray-400 ml-2">${b.total_amount.toLocaleString()}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Top Opportunities */}
      <div className="bg-white rounded-xl border border-gray-100 p-5">
        <h3 className="font-semibold text-gray-900 mb-4">Top Recovery Opportunities</h3>
        <p className="text-sm text-gray-500">
          Focus recovery efforts on the <strong className="text-gray-900">enterprise</strong> and <strong className="text-gray-900">mid-market</strong> segments
          which represent the highest outstanding amounts. Invoices in the 31–60 day overdue bracket typically have
          the best response to payment reminders.
        </p>
      </div>
    </div>
  );
};

export default AnalyticsPage;
