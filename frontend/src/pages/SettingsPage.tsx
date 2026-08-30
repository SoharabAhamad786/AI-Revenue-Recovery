import React, { useEffect, useState } from 'react';
import { settingsApi } from '../services/api';
import { useAuth } from '../hooks/useAuth';
import { use3D } from '../3d/ThreeDContext';
import toast, { Toaster } from 'react-hot-toast';
import {
  Settings, Save, AlertCircle, RefreshCw, Info,
  Sparkles, Video, UserCheck, Code, ShieldCheck, Database
} from 'lucide-react';

const SettingsPage: React.FC = () => {
  const { isManager } = useAuth();
  const { isPitchMode, togglePitchMode, is3DMode, toggle3DMode } = use3D();
  const [settings, setSettings] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await settingsApi.get();
      setSettings(res.data.settings);
    } catch {
      setError('Failed to load settings');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      await settingsApi.update(settings);
      toast.success('System recovery policies updated successfully');
    } catch (err: any) {
      toast.error(err.response?.data?.error || 'Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  const update = (key: string, value: string) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  if (loading) {
    return (
      <div className="p-8 space-y-6 max-w-4xl mx-auto">
        <div className="h-8 bg-slate-800 rounded w-48 animate-pulse" />
        {[1,2,3].map(i => <div key={i} className="h-40 bg-slate-900 rounded-2xl animate-pulse" />)}
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[50vh]">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-rose-400 mx-auto mb-3" />
          <p className="text-slate-300">{error}</p>
          <button onClick={load} className="mt-3 text-indigo-400 font-medium text-sm flex items-center gap-1 mx-auto"><RefreshCw className="w-4 h-4" /> Retry</button>
        </div>
      </div>
    );
  }

  const Field = ({ label, settingKey, type = 'text', helpText }: { label: string; settingKey: string; type?: string; helpText?: string }) => (
    <div>
      <label className="block text-xs font-mono text-slate-300 uppercase tracking-wider mb-1.5">{label}</label>
      <input
        type={type}
        value={settings[settingKey] || ''}
        onChange={(e) => update(settingKey, e.target.value)}
        disabled={!isManager}
        className="w-full px-3.5 py-2.5 bg-slate-950/80 border border-slate-700/80 rounded-xl text-xs text-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none disabled:opacity-50 disabled:bg-slate-900 font-sans"
      />
      {helpText && <p className="text-[11px] text-slate-400 mt-1">{helpText}</p>}
    </div>
  );

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-4xl mx-auto">
      <Toaster position="top-right" />

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl lg:text-3xl font-extrabold text-white tracking-tight flex items-center gap-2.5">
            <Settings className="w-7 h-7 text-cyan-400" /> System Settings & Policy
          </h1>
          <p className="text-sm text-slate-400 mt-0.5">Configure autonomous recovery thresholds, AI behavior, and presentation modes</p>
        </div>
        {isManager && (
          <button
            onClick={handleSave}
            disabled={saving}
            className="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-indigo-600/30 transition-all cursor-pointer"
          >
            <Save className="w-4 h-4" />
            {saving ? 'Saving...' : 'Save Policy Changes'}
          </button>
        )}
      </div>

      {/* About RecoverAI / Project Metadata Card */}
      <div className="bg-gradient-to-br from-slate-900 via-slate-900 to-indigo-950/60 border border-indigo-500/30 rounded-3xl p-6 shadow-2xl">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-cyan-400 flex items-center justify-center text-white shadow-lg">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">RecoverAI</h2>
              <p className="text-xs text-indigo-300 font-mono">Intelligent Invoice and Payment Recovery Assistant</p>
            </div>
          </div>
          <span className="text-[11px] font-mono text-cyan-300 bg-cyan-950/80 border border-cyan-800/60 px-3 py-1 rounded-full">
            Track 3 Internship Project
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-3 border-t border-slate-800/80 text-xs">
          <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/60">
            <p className="text-slate-400 text-[11px] uppercase font-mono">Project Owner</p>
            <p className="font-bold text-white text-sm mt-0.5">Soharab Ahamad</p>
          </div>
          <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/60">
            <p className="text-slate-400 text-[11px] uppercase font-mono">Architecture</p>
            <p className="font-bold text-cyan-300 text-sm mt-0.5">React + Flask + Three.js 3D</p>
          </div>
          <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/60">
            <p className="text-slate-400 text-[11px] uppercase font-mono">Safety Paradigm</p>
            <p className="font-bold text-emerald-400 text-sm mt-0.5">Human-in-the-Loop Guardrails</p>
          </div>
        </div>
      </div>

      {/* Presentation & Pitch Mode Controls */}
      <div className="bg-slate-900/85 backdrop-blur-xl rounded-2xl border border-slate-800/80 p-6 shadow-xl space-y-4">
        <h3 className="font-bold text-white text-sm uppercase tracking-wider font-mono flex items-center gap-2">
          <Video className="w-4 h-4 text-amber-400" /> Presentation & Video Recording Modes
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="bg-slate-950/70 p-4 rounded-xl border border-slate-800/70 flex items-center justify-between">
            <div>
              <p className="text-xs font-bold text-white">5-Minute Pitch Mode</p>
              <p className="text-[11px] text-slate-400 mt-0.5">Streamlined navigation & high-contrast video banner</p>
            </div>
            <button
              onClick={togglePitchMode}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                isPitchMode
                  ? 'bg-amber-500 text-white shadow-md shadow-amber-500/30'
                  : 'bg-slate-800 hover:bg-slate-700 text-slate-300'
              }`}
            >
              {isPitchMode ? 'Active' : 'Enable'}
            </button>
          </div>

          <div className="bg-slate-950/70 p-4 rounded-xl border border-slate-800/70 flex items-center justify-between">
            <div>
              <p className="text-xs font-bold text-white">3D Holographic UI Mode</p>
              <p className="text-[11px] text-slate-400 mt-0.5">Interactive particle constellation & neural orbs</p>
            </div>
            <button
              onClick={toggle3DMode}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                is3DMode
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'bg-slate-800 hover:bg-slate-700 text-slate-300'
              }`}
            >
              {is3DMode ? 'Active' : 'Enable'}
            </button>
          </div>
        </div>
      </div>

      {/* Recovery Policy */}
      <div className="bg-slate-900/85 backdrop-blur-xl rounded-2xl border border-slate-800/80 p-6 shadow-xl">
        <h3 className="font-bold text-white text-sm uppercase tracking-wider font-mono mb-4 flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-indigo-400" /> Recovery & Approval Policy
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Field label="High Value Threshold ($)" settingKey="high_value_threshold" type="number" helpText="Invoices above this amount mandate Finance Manager approval" />
          <Field label="Reminder Cooldown (hours)" settingKey="reminder_cooldown_hours" type="number" helpText="Minimum time required between repeated reminders" />
          <Field label="Max Auto Reminder Amount ($)" settingKey="max_auto_reminder_amount" type="number" helpText="Ceiling amount eligible for automated reminders" />
          <Field label="Escalation Threshold (days)" settingKey="escalation_threshold_days" type="number" helpText="Days overdue before mandatory human escalation" />
        </div>
      </div>

      {/* Payment Plan Rules */}
      <div className="bg-slate-900/85 backdrop-blur-xl rounded-2xl border border-slate-800/80 p-6 shadow-xl">
        <h3 className="font-bold text-white text-sm uppercase tracking-wider font-mono mb-4">Payment Plan Guardrails</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Field label="Minimum Amount for Plans ($)" settingKey="payment_plan_min_amount" type="number" />
          <Field label="Max Allowed Installments" settingKey="payment_plan_max_installments" type="number" />
        </div>
      </div>

      {/* AI Configuration */}
      <div className="bg-slate-900/85 backdrop-blur-xl rounded-2xl border border-slate-800/80 p-6 shadow-xl">
        <h3 className="font-bold text-white text-sm uppercase tracking-wider font-mono mb-4 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-cyan-400" /> AI Neural Engine Configuration
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-mono text-slate-300 uppercase tracking-wider mb-1.5">AI Provider</label>
            <select
              value={settings.ai_provider || 'mock'}
              onChange={(e) => update('ai_provider', e.target.value)}
              disabled={!isManager}
              className="w-full px-3.5 py-2.5 bg-slate-950/80 border border-slate-700/80 rounded-xl text-xs text-white focus:ring-2 focus:ring-indigo-500 outline-none disabled:opacity-50 font-sans cursor-pointer"
            >
              <option value="mock">Deterministic Neural Engine (Offline Demo)</option>
              <option value="openai">OpenAI GPT-4o</option>
              <option value="gemini">Google Gemini 1.5 Pro</option>
            </select>
          </div>
          <Field label="AI Temperature" settingKey="ai_temperature" type="number" helpText="0.0 = deterministic finance rules, 1.0 = creative" />
          <Field label="Default Follow-up Days" settingKey="default_follow_up_days" type="number" />
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
