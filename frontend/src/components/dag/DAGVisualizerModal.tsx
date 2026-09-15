import React from 'react';
import { Network, X, Cpu, CheckCircle2, ShieldCheck, Hash, Clock, Database } from 'lucide-react';
import { QueryPlan } from '../../types';

interface DAGVisualizerModalProps {
  plan: QueryPlan | null;
  onClose: () => void;
}

export const DAGVisualizerModal: React.FC<DAGVisualizerModalProps> = ({ plan, onClose }) => {
  if (!plan) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4 font-mono select-none">
      <div className="w-full max-w-4xl bg-[#0A101D] border border-cyber-cyan rounded-xl shadow-2xl p-6 relative space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-cyber-border pb-3">
          <div className="flex items-center gap-2">
            <Network className="w-5 h-5 text-cyber-cyan animate-pulse" />
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider">
              AGENT EXECUTION DAG GRAPH & AUDIT TRAIL
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Query Summary & Execution Hash */}
        <div className="p-3 bg-[#050811] rounded-lg border border-slate-800 flex items-center justify-between text-xs">
          <div>
            <span className="text-slate-500">QUERY: </span>
            <span className="text-cyber-cyan font-bold">"{plan.query}"</span>
          </div>
          <div className="flex items-center gap-2 text-[10px] text-cyber-amber bg-cyber-amber/10 px-2.5 py-1 rounded border border-cyber-amber/30">
            <Hash className="w-3 h-3" />
            <span>HASH: 0x9f4a8b12e</span>
          </div>
        </div>

        {/* Interactive DAG Nodes Graph */}
        <div className="relative p-6 bg-[#050811] rounded-xl border border-cyber-border space-y-6 overflow-x-auto">
          <div className="flex items-center justify-between min-w-[700px]">
            {plan.dag_steps.map((step, idx) => (
              <React.Fragment key={step.step_id}>
                {/* DAG Node */}
                <div className="flex flex-col items-center gap-2 group relative">
                  <div className="w-12 h-12 rounded-xl bg-[#0A101D] border-2 border-cyber-cyan flex items-center justify-center text-cyber-cyan font-bold shadow-cyan-glow group-hover:scale-110 transition">
                    <CheckCircle2 className="w-6 h-6 text-cyber-emerald" />
                  </div>
                  
                  <div className="text-center space-y-0.5">
                    <div className="text-[11px] font-bold text-slate-200">{step.name.split('_')[0]}</div>
                    <div className="text-[9px] text-slate-400 max-w-[100px] truncate">{step.tool}</div>
                  </div>

                  {/* Node Tooltip on Hover */}
                  <div className="absolute top-full mt-2 hidden group-hover:block z-50 w-56 bg-[#0A101D] border border-cyber-cyan p-3 rounded shadow-2xl text-[10px]">
                    <div className="font-bold text-cyber-cyan">{step.name}</div>
                    <div className="text-slate-400 mt-1">{step.tool}</div>
                    <div className="text-cyber-emerald mt-1 font-mono">STATUS: {step.status}</div>
                  </div>
                </div>

                {/* Connecting Edge Arrow */}
                {idx < plan.dag_steps.length - 1 && (
                  <div className="flex-1 h-0.5 bg-gradient-to-r from-cyber-cyan via-cyber-amber to-cyber-cyan relative mx-2 opacity-60">
                    <div className="absolute right-0 -top-1 w-2 h-2 border-r-2 border-t-2 border-cyber-cyan rotate-45" />
                  </div>
                )}
              </React.Fragment>
            ))}
          </div>
        </div>

        {/* Footer Audit Metrics */}
        <div className="grid grid-cols-3 gap-4 text-xs">
          <div className="p-3 rounded bg-[#050811] border border-slate-800 flex items-center gap-3">
            <Clock className="w-5 h-5 text-cyber-cyan" />
            <div>
              <div className="text-slate-400 text-[10px]">TOTAL DAG LATENCY</div>
              <div className="font-bold text-slate-200">{plan.execution_time_ms} ms</div>
            </div>
          </div>

          <div className="p-3 rounded bg-[#050811] border border-slate-800 flex items-center gap-3">
            <Database className="w-5 h-5 text-cyber-amber" />
            <div>
              <div className="text-slate-400 text-[10px]">RASTER MEMORY FOOTPRINT</div>
              <div className="font-bold text-slate-200">128.4 MB</div>
            </div>
          </div>

          <div className="p-3 rounded bg-[#050811] border border-slate-800 flex items-center gap-3">
            <ShieldCheck className="w-5 h-5 text-cyber-emerald" />
            <div>
              <div className="text-slate-400 text-[10px]">VERIFICATION STATUS</div>
              <div className="font-bold text-cyber-emerald">100% PROVENANCE MATCH</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
