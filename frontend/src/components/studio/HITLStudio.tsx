import React, { useState } from 'react';
import { UserCheck, RefreshCw, CheckCircle2, AlertOctagon, Activity, Database } from 'lucide-react';

export const HITLStudio: React.FC = () => {
  const [retrainingStatus, setRetrainingStatus] = useState<string | null>(null);

  const triggerRetraining = () => {
    setRetrainingStatus('RUNNING');
    setTimeout(() => {
      setRetrainingStatus('COMPLETED');
    }, 2000);
  };

  return (
    <div className="w-full h-full bg-[#030712] p-6 overflow-y-auto space-y-6 font-sans select-none">
      {/* Studio Header */}
      <div className="flex items-center justify-between border-b border-cyber-border pb-4">
        <div>
          <div className="flex items-center gap-2">
            <UserCheck className="w-6 h-6 text-cyber-cyan animate-pulse" />
            <h2 className="font-display font-extrabold text-xl text-slate-100 uppercase tracking-wider">
              MODEL GOVERNANCE & ACTIVE LEARNING RETRAINING STUDIO
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Human-in-the-Loop domain expert feedback logger, model drift metrics, and active learning gradient update pipeline.
          </p>
        </div>

        <button
          onClick={triggerRetraining}
          disabled={retrainingStatus === 'RUNNING'}
          className="px-4 py-2 rounded-xl bg-cyber-cyan text-black font-bold text-xs hover:bg-cyan-300 transition flex items-center gap-2 shadow-cyan-glow disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${retrainingStatus === 'RUNNING' ? 'animate-spin' : ''}`} />
          <span>{retrainingStatus === 'RUNNING' ? 'RETRAINING MODEL...' : 'TRIGGER ACTIVE LEARNING RETRAIN'}</span>
        </button>
      </div>

      {retrainingStatus === 'COMPLETED' && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/40 text-emerald-400 text-xs font-mono flex items-center gap-3 animate-pulse">
          <CheckCircle2 className="w-5 h-5" />
          <div>
            <div className="font-bold">ACTIVE LEARNING GRADIENT UPDATE SUCCESSFUL!</div>
            <div>Model weights updated with 12 new domain expert annotations. Precision improved by +1.4%.</div>
          </div>
        </div>
      )}

      {/* Grid: Model Confusion Matrix + Feedback Log Stream */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Confusion Matrix Card */}
        <div className="p-6 rounded-2xl bg-[#0B132B]/90 border border-cyber-border space-y-4 backdrop-blur-xl shadow-2xl">
          <span className="font-display font-bold text-sm text-slate-100 uppercase">
            MODEL CONFUSION MATRIX (VERIFIED BENCHMARK)
          </span>

          <div className="grid grid-cols-2 gap-3 text-xs font-mono text-center">
            <div className="p-4 bg-[#030712] border border-emerald-500/40 rounded-xl">
              <div className="text-slate-400 text-[10px]">TRUE POSITIVE (TP)</div>
              <div className="text-2xl font-bold text-emerald-400 mt-1">94.2%</div>
            </div>

            <div className="p-4 bg-[#030712] border border-cyan-500/40 rounded-xl">
              <div className="text-slate-400 text-[10px]">TRUE NEGATIVE (TN)</div>
              <div className="text-2xl font-bold text-cyber-cyan mt-1">97.8%</div>
            </div>

            <div className="p-4 bg-[#030712] border border-rose-500/40 rounded-xl">
              <div className="text-slate-400 text-[10px]">FALSE POSITIVE (FP)</div>
              <div className="text-2xl font-bold text-rose-400 mt-1">3.4%</div>
            </div>

            <div className="p-4 bg-[#030712] border border-amber-500/40 rounded-xl">
              <div className="text-slate-400 text-[10px]">FALSE NEGATIVE (FN)</div>
              <div className="text-2xl font-bold text-amber-400 mt-1">2.2%</div>
            </div>
          </div>
        </div>

        {/* Feedback Logs Table */}
        <div className="p-6 rounded-2xl bg-[#0B132B]/90 border border-cyber-border space-y-4 backdrop-blur-xl shadow-2xl">
          <span className="font-display font-bold text-sm text-slate-100 uppercase">
            ACTIVE ANNOTATION FEEDBACK STREAM (3 LOGS)
          </span>

          <div className="space-y-3 font-mono text-xs">
            {[
              { id: 'HITL-0012', type: 'FALSE_POSITIVE', note: 'Agricultural crop harvest misclassified as building.', time: '10 mins ago' },
              { id: 'HITL-0011', type: 'BOUNDARY_CORRECTION', note: 'Jebel Ali waterfront polygon boundary shifted +12m.', time: '1 hour ago' },
              { id: 'HITL-0010', type: 'FALSE_NEGATIVE', note: 'Shadowed high-rise missed by optical model.', time: '3 hours ago' }
            ].map(log => (
              <div key={log.id} className="p-3.5 rounded-xl bg-[#030712] border border-slate-800 space-y-1">
                <div className="flex justify-between">
                  <span className="font-bold text-cyber-cyan">{log.id}</span>
                  <span className="text-amber-400 text-[10px]">{log.type}</span>
                </div>
                <div className="text-slate-300 text-[11px]">{log.note}</div>
                <div className="text-slate-500 text-[10px] text-right">{log.time}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
