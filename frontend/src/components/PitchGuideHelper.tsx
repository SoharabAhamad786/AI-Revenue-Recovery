import React, { useState } from 'react';
import { Video, ChevronDown, ChevronUp, Clock, CheckCircle2, Sparkles, ExternalLink, HelpCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

export const PitchGuideHelper: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeStep, setActiveStep] = useState(0);

  const steps = [
    {
      time: '0:00 – 0:40',
      title: 'The Revenue Recovery Problem',
      route: '/',
      cue: 'Manual accounts receivable follow-up is slow, error-prone, and burns customer goodwill. Companies lose millions in overdue invoices.',
      actions: ['Show Dashboard KPI cards ($315K Outstanding, $281K Overdue)', 'Point out 6 Accounts Requiring Attention'],
    },
    {
      time: '0:40 – 1:30',
      title: 'RecoverAI Product Overview',
      route: '/',
      cue: 'RecoverAI is built by Soharab Ahamad as an intelligent AR recovery assistant that combines AI autonomous analysis with strict human-in-the-loop controls.',
      actions: ['Highlight 3D Revenue Recovery Galaxy', 'Show Recovery Velocity Trends and Portfolio Health'],
    },
    {
      time: '1:30 – 2:40',
      title: 'Live Demo: AI Strategy & Evidence',
      route: '/recovery-queue',
      cue: 'Let\'s open the Recovery Queue. We select our recommended demo invoice (INV-2024-024 for Jennifer Lee) and run AI Analysis.',
      actions: ['Click "Demo Scenario" filter in Recovery Queue', 'Open INV-2024-024', 'Click "Analyze with AI" — notice 3D Neural Orb', 'Explain 85% Recovery Probability and Evidence citations'],
    },
    {
      time: '2:40 – 3:35',
      title: 'Approval & Guardrails (Dispute Block)',
      route: '/invoices/24',
      cue: 'The finance manager reviews and can edit the tailored reminder message before approving. Reminders on disputed invoices are strictly blocked.',
      actions: ['Click "Approve & Send" on INV-2024-024 (Mock Email sent)', 'Open Disputed Invoice INV-2024-004 to show blocked send button & forced escalation'],
    },
    {
      time: '3:35 – 4:25',
      title: 'Technical Architecture & Audit Trail',
      route: '/audit-log',
      cue: 'Full-stack architecture: React + TypeScript frontend, Flask REST API, business rules safety engine, and immutable audit trail.',
      actions: ['Open Audit Log to verify every login, AI inference, and send event is logged', 'Show Settings recovery policies'],
    },
    {
      time: '4:25 – 5:00',
      title: 'Business Impact & Closing',
      route: '/analytics',
      cue: 'RecoverAI cuts days-to-payment, boosts recovery rates to 24%+, and keeps finance teams in complete control. Built by Soharab Ahamad.',
      actions: ['Show Recovery by Segment and Age Bucket analytics', 'Conclude 5-minute pitch presentation'],
    },
  ];

  return (
    <div className="fixed bottom-4 right-4 z-50 select-none">
      {!isOpen ? (
        <button
          onClick={() => setIsOpen(true)}
          className="flex items-center gap-2.5 px-4 py-2.5 bg-gradient-to-r from-indigo-600 via-purple-600 to-cyan-500 hover:from-indigo-500 hover:to-cyan-400 text-white rounded-2xl shadow-2xl shadow-indigo-500/40 border border-white/20 text-xs font-bold transition-all transform hover:scale-105 cursor-pointer"
        >
          <Video className="w-4 h-4 animate-pulse text-cyan-200" />
          <span>Pitch Guide (Internal)</span>
          <span className="bg-white/20 text-[10px] px-1.5 py-0.5 rounded-full font-mono">5-Min Video</span>
        </button>
      ) : (
        <div className="w-[420px] max-h-[580px] bg-slate-900/95 backdrop-blur-2xl border border-indigo-500/30 rounded-3xl shadow-2xl overflow-hidden flex flex-col text-slate-200">
          {/* Header */}
          <div className="p-4 border-b border-slate-800 bg-slate-950/80 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
                <Video className="w-4 h-4" />
              </div>
              <div>
                <h3 className="font-bold text-xs text-white">Pitch Guide (Internal Presenter)</h3>
                <p className="text-[10px] text-indigo-400 font-mono">RecoverAI • Built by Soharab Ahamad</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors cursor-pointer"
            >
              <ChevronDown className="w-4 h-4" />
            </button>
          </div>

          {/* Body */}
          <div className="p-4 overflow-y-auto space-y-3 flex-1 text-xs">
            <div className="flex items-center justify-between bg-indigo-950/50 p-2.5 rounded-xl border border-indigo-800/40">
              <span className="text-[11px] text-indigo-300 font-medium">5-Minute Pitch Outline</span>
              <span className="text-[10px] font-mono text-cyan-300 bg-cyan-950 px-2 py-0.5 rounded-full border border-cyan-800/50">
                Step {activeStep + 1} of {steps.length}
              </span>
            </div>

            <div className="space-y-2.5">
              {steps.map((s, idx) => (
                <div
                  key={idx}
                  onClick={() => setActiveStep(idx)}
                  className={`p-3 rounded-2xl border transition-all cursor-pointer ${
                    activeStep === idx
                      ? 'bg-slate-800/90 border-indigo-500/60 shadow-md'
                      : 'bg-slate-950/50 border-slate-800/60 hover:bg-slate-900/60'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="font-bold text-white flex items-center gap-1.5">
                      <span className={`w-2 h-2 rounded-full ${activeStep === idx ? 'bg-cyan-400 animate-ping' : 'bg-slate-600'}`} />
                      {s.title}
                    </span>
                    <span className="font-mono text-[10px] text-indigo-400 bg-indigo-950/80 px-2 py-0.5 rounded-md border border-indigo-900/60">
                      {s.time}
                    </span>
                  </div>

                  {activeStep === idx && (
                    <div className="space-y-2 pt-2 border-t border-slate-700/50 mt-2">
                      <div className="bg-slate-950/80 p-2.5 rounded-xl border border-indigo-900/30 text-[11px] text-slate-300 leading-relaxed">
                        <strong className="text-cyan-300 block mb-0.5">Presenter Cue:</strong>
                        "{s.cue}"
                      </div>
                      <div>
                        <strong className="text-[11px] text-slate-400 block mb-1">On-Screen Actions:</strong>
                        <ul className="space-y-1">
                          {s.actions.map((act, aIdx) => (
                            <li key={aIdx} className="flex items-start gap-1.5 text-[11px] text-slate-300">
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                              <span>{act}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div className="pt-1 flex justify-end">
                        <Link
                          to={s.route}
                          className="inline-flex items-center gap-1 text-[11px] text-indigo-400 hover:text-indigo-300 font-semibold"
                        >
                          Navigate to Screen <ExternalLink className="w-3 h-3" />
                        </Link>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Footer Navigation */}
          <div className="p-3 border-t border-slate-800 bg-slate-950/80 flex items-center justify-between">
            <button
              disabled={activeStep === 0}
              onClick={() => setActiveStep(prev => Math.max(0, prev - 1))}
              className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-white rounded-lg text-xs font-medium cursor-pointer"
            >
              Previous
            </button>
            <span className="text-[10px] text-slate-400 font-mono">Owner: Soharab Ahamad</span>
            <button
              disabled={activeStep === steps.length - 1}
              onClick={() => setActiveStep(prev => Math.min(steps.length - 1, prev + 1))}
              className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white rounded-lg text-xs font-semibold cursor-pointer"
            >
              Next Step
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
