import React from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { use3D } from '../3d/ThreeDContext';
import { ThreeDBackground } from '../3d/ThreeDBackground';
import { ThreeDToggle } from '../3d/ThreeDToggle';
import { PitchGuideHelper } from '../components/PitchGuideHelper';
import {
  LayoutDashboard, Users, BarChart3, Shield,
  Settings, LogOut, ListChecks, Zap, Sparkles, Video, UserCheck
} from 'lucide-react';

const standardNavItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/recovery-queue', icon: ListChecks, label: 'Recovery Queue' },
  { to: '/customers', icon: Users, label: 'Customers' },
  { to: '/analytics', icon: BarChart3, label: 'Analytics' },
  { to: '/audit-log', icon: Shield, label: 'Audit Log' },
  { to: '/settings', icon: Settings, label: 'Settings' },
];

const pitchNavItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/recovery-queue', icon: ListChecks, label: 'Recovery Queue' },
  { to: '/analytics', icon: BarChart3, label: 'Analytics' },
  { to: '/audit-log', icon: Shield, label: 'Audit Log' },
  { to: '/settings', icon: Settings, label: 'Settings' },
];

const AppLayout: React.FC = () => {
  const { user, logout } = useAuth();
  const { is3DMode, isPitchMode, togglePitchMode } = use3D();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = isPitchMode ? pitchNavItems : standardNavItems;

  return (
    <div className={`relative flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans ${
      isPitchMode ? 'text-[15px]' : ''
    }`}>
      {/* 3D Interactive Three.js Particle & Geometry Background */}
      <ThreeDBackground />

      {/* Sidebar with 3D Cyber Depth */}
      <aside className={`w-64 flex flex-col shrink-0 z-20 transition-all duration-300 ${
        is3DMode 
          ? 'bg-slate-900/85 backdrop-blur-xl border-r border-indigo-500/20 shadow-2xl shadow-indigo-950/50' 
          : 'bg-slate-900 border-r border-slate-800'
      }`}>
        <div className="p-5 border-b border-slate-800/80">
          <div className="flex items-center gap-2.5">
            <div className={`w-10 h-10 rounded-xl flex items-center justify-center transition-all ${
              is3DMode 
                ? 'bg-gradient-to-tr from-indigo-600 via-purple-600 to-cyan-400 shadow-lg shadow-indigo-500/40' 
                : 'bg-indigo-600'
            }`}>
              <Zap className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-100 to-indigo-200 bg-clip-text text-transparent">
                RecoverAI
              </h1>
              <p className="text-[10px] text-indigo-400/90 font-mono tracking-wider uppercase flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                By Soharab Ahamad
              </p>
            </div>
          </div>
          <p className="text-[10px] text-slate-400 mt-2 font-medium leading-tight">
            Intelligent Invoice & Payment Recovery Assistant
          </p>
        </div>

        <nav className="flex-1 py-4 px-3 space-y-1.5 overflow-y-auto">
          {navItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `group flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? is3DMode
                      ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-600/30 border border-indigo-400/30 translate-x-1'
                      : 'bg-indigo-600 text-white'
                    : 'text-slate-400 hover:bg-slate-800/60 hover:text-white hover:translate-x-0.5'
                }`
              }
            >
              <Icon className="w-4 h-4 transition-transform group-hover:scale-110" />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-800/80 bg-slate-900/40">
          <div className="flex items-center gap-3 mb-3 bg-slate-800/50 p-2.5 rounded-xl border border-slate-700/50">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center text-xs font-bold text-white shadow-md">
              {user?.name?.charAt(0) || 'U'}
            </div>
            <div className="min-w-0">
              <p className="text-xs font-semibold text-white truncate">{user?.name}</p>
              <p className="text-[10px] text-indigo-400 capitalize font-mono">{user?.role?.replace('_', ' ')}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 px-3 py-2 text-xs font-medium text-slate-400 hover:text-white hover:bg-rose-500/20 hover:border-rose-500/30 border border-transparent rounded-lg transition-all cursor-pointer"
          >
            <LogOut className="w-3.5 h-3.5" />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden z-10">
        {/* Pitch Mode Presentation Banner */}
        {isPitchMode && (
          <div className="bg-gradient-to-r from-indigo-900 via-purple-900 to-cyan-900 px-6 py-2 border-b border-cyan-500/30 flex items-center justify-between text-xs font-mono text-cyan-200">
            <div className="flex items-center gap-2">
              <Video className="w-4 h-4 text-cyan-400 animate-pulse" />
              <span className="font-bold tracking-wide">🎬 Pitch Video Recording Mode</span>
              <span className="text-slate-400">•</span>
              <span>Demo Scenarios & High-Contrast Visuals Active</span>
            </div>
            <span className="bg-cyan-950/80 border border-cyan-700/60 px-2.5 py-0.5 rounded-full text-[11px] font-semibold text-cyan-300">
              Built by Soharab Ahamad
            </span>
          </div>
        )}

        {/* Futuristic Top Bar with 3D and Pitch Mode Toggles */}
        <header className="h-16 px-6 flex items-center justify-between border-b border-slate-800/80 bg-slate-900/50 backdrop-blur-md shrink-0">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 text-xs text-slate-400 font-mono">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              <span>System: <strong className="text-slate-200">Online</strong></span>
            </div>
            <span className="text-slate-700">|</span>
            <div className="hidden md:flex items-center gap-1.5 text-xs text-indigo-300 font-mono bg-indigo-950/60 px-2.5 py-1 rounded-full border border-indigo-800/40">
              <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
              RecoverAI — Built by Soharab Ahamad
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Pitch Mode Toggle */}
            <button
              onClick={togglePitchMode}
              title={isPitchMode ? "Exit Pitch Video Mode" : "Activate Pitch Video Recording Mode"}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-all cursor-pointer ${
                isPitchMode
                  ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-lg shadow-orange-500/30 border border-white/30 scale-105'
                  : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700'
              }`}
            >
              <Video className="w-3.5 h-3.5" />
              <span>{isPitchMode ? 'Pitch Mode Active' : 'Pitch Mode'}</span>
            </button>

            {/* 3D Mode Toggle Button */}
            <ThreeDToggle />
          </div>
        </header>

        {/* Dynamic Page Views */}
        <main className="flex-1 overflow-auto bg-slate-950/40 text-slate-900">
          <Outlet />
        </main>
      </div>

      {/* Internal Presenter Pitch Guide Drawer */}
      <PitchGuideHelper />
    </div>
  );
};

export default AppLayout;
