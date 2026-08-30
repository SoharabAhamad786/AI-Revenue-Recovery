import React, { useEffect, useState } from 'react';
import { customerApi } from '../services/api';
import { Customer } from '../types';
import { Search, Users, AlertCircle, RefreshCw, Building2, Mail, Phone } from 'lucide-react';

const CustomersPage: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState<Customer | null>(null);

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const params: Record<string, string> = {};
      if (search) params.search = search;
      const res = await customerApi.list(params);
      setCustomers(res.data.customers);
    } catch {
      setError('Failed to load customers');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [search]);

  const loadDetail = async (id: number) => {
    try {
      const res = await customerApi.get(id);
      setSelected(res.data);
    } catch {
      setSelected(null);
    }
  };

  const riskColor = (risk: string) =>
    risk === 'high' ? 'text-red-600 bg-red-50' : risk === 'medium' ? 'text-amber-600 bg-amber-50' : 'text-emerald-600 bg-emerald-50';

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
    <div className="p-6 lg:p-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Customers</h1>
          <p className="text-sm text-gray-500 mt-0.5">{customers.length} customers</p>
        </div>
      </div>

      <div className="relative max-w-sm mb-5">
        <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          placeholder="Search customers..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
        />
      </div>

      <div className="flex gap-6">
        {/* Customer List */}
        <div className="flex-1">
          <div className="bg-white rounded-xl border border-gray-100 overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-100">
                  <th className="text-left px-4 py-3 font-semibold text-gray-600">Customer</th>
                  <th className="text-left px-4 py-3 font-semibold text-gray-600">Segment</th>
                  <th className="text-right px-4 py-3 font-semibold text-gray-600">Lifetime Value</th>
                  <th className="text-right px-4 py-3 font-semibold text-gray-600">Outstanding</th>
                  <th className="text-center px-4 py-3 font-semibold text-gray-600">Reliability</th>
                  <th className="text-center px-4 py-3 font-semibold text-gray-600">Risk</th>
                  <th className="text-right px-4 py-3 font-semibold text-gray-600">Overdue</th>
                </tr>
              </thead>
              <tbody>
                {loading ? Array.from({ length: 5 }).map((_, i) => (
                  <tr key={i} className="border-b border-gray-50">
                    {Array.from({ length: 7 }).map((_, j) => (
                      <td key={j} className="px-4 py-3"><div className="h-4 bg-gray-100 rounded animate-pulse" /></td>
                    ))}
                  </tr>
                )) : customers.map(c => (
                  <tr
                    key={c.id}
                    className={`border-b border-gray-50 hover:bg-gray-50 cursor-pointer transition-colors ${selected?.id === c.id ? 'bg-indigo-50' : ''}`}
                    onClick={() => loadDetail(c.id)}
                  >
                    <td className="px-4 py-3">
                      <p className="font-medium text-gray-900">{c.name}</p>
                      <p className="text-xs text-gray-400">{c.company}</p>
                    </td>
                    <td className="px-4 py-3 capitalize text-gray-600">{c.customer_segment.replace('_', ' ')}</td>
                    <td className="px-4 py-3 text-right font-medium">${c.lifetime_value.toLocaleString()}</td>
                    <td className="px-4 py-3 text-right font-medium">${(c.outstanding_amount || 0).toLocaleString()}</td>
                    <td className="px-4 py-3 text-center font-medium">{(c.payment_reliability_score * 100).toFixed(0)}%</td>
                    <td className="px-4 py-3 text-center">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${riskColor(c.risk || 'low')}`}>
                        {c.risk || 'low'}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-right">{c.overdue_count || 0}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Customer Detail Drawer */}
        {selected && (
          <div className="w-80 shrink-0">
            <div className="bg-white rounded-xl border border-gray-100 p-5 sticky top-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold">
                  {selected.name.charAt(0)}
                </div>
                <div>
                  <p className="font-semibold text-gray-900">{selected.name}</p>
                  <p className="text-xs text-gray-500">{selected.company}</p>
                </div>
              </div>
              <div className="space-y-3 text-sm">
                <div className="flex items-center gap-2 text-gray-600">
                  <Mail className="w-4 h-4 text-gray-400" />
                  {selected.email || <span className="text-red-500">No email</span>}
                </div>
                <div className="flex items-center gap-2 text-gray-600">
                  <Phone className="w-4 h-4 text-gray-400" />
                  {selected.phone || 'N/A'}
                </div>
                <div className="flex items-center gap-2 text-gray-600">
                  <Building2 className="w-4 h-4 text-gray-400" />
                  <span className="capitalize">{selected.customer_segment.replace('_', ' ')}</span>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3 mt-4 pt-4 border-t border-gray-100">
                <div>
                  <p className="text-[10px] text-gray-500 uppercase">Lifetime Value</p>
                  <p className="font-semibold">${selected.lifetime_value.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-[10px] text-gray-500 uppercase">Total Paid</p>
                  <p className="font-semibold">${selected.total_paid.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-[10px] text-gray-500 uppercase">Reliability</p>
                  <p className="font-semibold">{(selected.payment_reliability_score * 100).toFixed(0)}%</p>
                </div>
                <div>
                  <p className="text-[10px] text-gray-500 uppercase">Overdue</p>
                  <p className="font-semibold">{selected.overdue_count || 0}</p>
                </div>
              </div>
              {selected.invoices && selected.invoices.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-100">
                  <p className="text-xs font-semibold text-gray-700 mb-2">Recent Invoices</p>
                  <div className="space-y-1.5 max-h-40 overflow-y-auto">
                    {selected.invoices.map(inv => (
                      <div key={inv.id} className="flex items-center justify-between text-xs bg-gray-50 rounded px-2 py-1.5">
                        <span className="font-mono">{inv.invoice_number}</span>
                        <span className={`font-semibold ${inv.status === 'paid' ? 'text-emerald-600' : inv.status === 'overdue' ? 'text-red-600' : 'text-gray-600'}`}>
                          ${inv.amount.toLocaleString()}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CustomersPage;
