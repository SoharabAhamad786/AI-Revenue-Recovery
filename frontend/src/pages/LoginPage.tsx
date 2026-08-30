import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { ThreeDBackground } from '../3d/ThreeDBackground';
import { Card3D } from '../3d/Card3D';
import toast, { Toaster } from 'react-hot-toast';
import { Zap, AlertCircle, Sparkles, ArrowRight, ShieldCheck, Loader2 } from 'lucide-react';

const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const executeLogin = async (loginEmail: string, loginPass: string) => {
    setError('');
    if (!loginEmail || !loginPass) {
      setError('Email and password are required');
      return;
    }
    setLoading(true);
    try {
      await login(loginEmail, loginPass);
      toast.success('Authentication successful! Welcome to RecoverAI.');
      navigate('/');
    } catch (err: any) {
      const errMsg = err.response?.data?.error || 'Login failed. Please verify your credentials or ensure backend is running.';
      setError(errMsg);
      toast.error(errMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    executeLogin(email, password);
  };

  const handle1ClickDemo = (role: 'manager' | 'analyst') => {
    const demoEmail = role === 'manager' ? 'manager@recoverai.demo' : 'analyst@recoverai.demo';
    const demoPass = role === 'manager' ? 'manager123' : 'analyst123';
    setEmail(demoEmail);
    setPassword(demoPass);
    executeLogin(demoEmail, demoPass);
  };

  return (
    <div className="relative min-h-screen bg-slate-950 flex items-center justify-center p-4 overflow-hidden">
      <Toaster position="top-right" />
      {/* 3D Particle Background */}
      <ThreeDBackground />

      <div className="w-full max-w-md z-10">
        {/* 3D Cyber Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-tr from-indigo-600 via-purple-600 to-cyan-400 rounded-2xl mb-4 shadow-2xl shadow-indigo-500/50 border border-white/20 transform hover:rotate-6 transition-transform">
            <Zap className="w-9 h-9 text-white animate-pulse" />
          </div>
          <h1 className="text-3xl lg:text-4xl font-extrabold text-white tracking-tight flex items-center justify-center gap-2">
            <span>RecoverAI</span>
            <Sparkles className="w-5 h-5 text-cyan-400" />
          </h1>
          <p className="text-indigo-300/80 font-mono text-xs mt-1 uppercase tracking-widest">
            3D Intelligent Revenue Recovery Platform
          </p>
        </div>

        {/* 3D Glassmorphic Login Card */}
        <Card3D intensity={12} className="bg-slate-900/90 backdrop-blur-2xl border-slate-800/90 shadow-2xl p-8 rounded-3xl">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-white tracking-tight">Access Terminal</h2>
            <span className="text-[11px] font-mono text-cyan-400 bg-cyan-950/60 border border-cyan-800/50 px-2.5 py-1 rounded-full flex items-center gap-1">
              <ShieldCheck className="w-3 h-3" /> Secure Auth
            </span>
          </div>

          {error && (
            <div className="mb-5 flex items-center gap-2 bg-rose-950/60 border border-rose-800/60 text-rose-300 px-4 py-3 rounded-xl text-xs font-medium">
              <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5 font-mono uppercase tracking-wide">
                Email Address
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950/80 border border-slate-700/70 text-white rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all text-sm"
                placeholder="manager@recoverai.demo"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5 font-mono uppercase tracking-wide">
                Password
              </label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950/80 border border-slate-700/70 text-white rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all text-sm"
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-indigo-600 via-purple-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 text-white font-semibold py-3 rounded-xl shadow-lg shadow-indigo-600/30 transition-all transform hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50 text-sm flex items-center justify-center gap-2 mt-2 cursor-pointer"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Authenticating...</span>
                </>
              ) : (
                <>
                  <span>Enter System</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* 1-Click Instant Demo Login */}
          <div className="mt-6 pt-5 border-t border-slate-800/80">
            <p className="text-xs text-slate-400 mb-3 text-center font-mono">⚡ 1-Click Instant Demo Sign In</p>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                disabled={loading}
                onClick={() => handle1ClickDemo('manager')}
                className="px-3.5 py-3 bg-slate-950/90 hover:bg-indigo-950/60 rounded-xl text-left transition-all border border-indigo-500/30 hover:border-indigo-500/80 group cursor-pointer disabled:opacity-50"
              >
                <div className="flex items-center justify-between">
                  <p className="text-xs font-bold text-white group-hover:text-indigo-300">Finance Manager</p>
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 group-hover:animate-ping" />
                </div>
                <p className="text-[10px] text-indigo-400/90 font-mono mt-0.5">Full Approval Access</p>
              </button>
              <button
                type="button"
                disabled={loading}
                onClick={() => handle1ClickDemo('analyst')}
                className="px-3.5 py-3 bg-slate-950/90 hover:bg-purple-950/60 rounded-xl text-left transition-all border border-purple-500/30 hover:border-purple-500/80 group cursor-pointer disabled:opacity-50"
              >
                <div className="flex items-center justify-between">
                  <p className="text-xs font-bold text-white group-hover:text-purple-300">Finance Analyst</p>
                  <span className="w-1.5 h-1.5 rounded-full bg-purple-400 group-hover:animate-ping" />
                </div>
                <p className="text-[10px] text-purple-400/90 font-mono mt-0.5">Draft & Review Mode</p>
              </button>
            </div>
          </div>
        </Card3D>

        <p className="text-center text-xs text-slate-500 mt-6 font-mono">
          Synthetic Financial Data Sandbox • Track 3 AI Revenue Recovery
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
