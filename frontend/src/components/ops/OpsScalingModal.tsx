import React from 'react';
import { Cpu, X, DollarSign, Database, Server, Zap, ShieldCheck } from 'lucide-react';
import { AnalyticsData } from '../../types';

interface OpsScalingModalProps {
  analytics: AnalyticsData | null;
  onClose: () => void;
}

export const OpsScalingModal: React.FC<OpsScalingModalProps> = ({ analytics, onClose }) => {
  return (
    <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4 font-mono select-none">
      <div className="w-full max-w-2xl bg-[#0A101D] border border-cyber-amber rounded-xl shadow-amber-glow p-6 relative space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-cyber-border pb-3">
          <div className="flex items-center gap-2">
            <Cpu className="w-5 h-5 text-cyber-amber animate-pulse" />
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider">
              PRODUCTION COST, LATENCY & NATIONAL SCALING DASHBOARD
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 gap-4 text-xs">
          <div className="p-4 rounded-lg bg-[#050811] border border-cyber-amber/40 space-y-1">
            <div className="text-[10px] text-slate-400 uppercase flex items-center gap-1">
              <DollarSign className="w-3.5 h-3.5 text-cyber-amber" /> COMPUTE COST PER QUERY
            </div>
            <div className="text-2xl font-bold text-cyber-amber">$0.014 USD</div>
            <div className="text-[10px] text-slate-400">Optimized PyTorch GPU Tensor Core Pipeline</div>
          </div>

          <div className="p-4 rounded-lg bg-[#050811] border border-cyber-cyan/40 space-y-1">
            <div className="text-[10px] text-slate-400 uppercase flex items-center gap-1">
              <Zap className="w-3.5 h-3.5 text-cyber-cyan" /> CACHE HIT RATE
            </div>
            <div className="text-2xl font-bold text-cyber-cyan">84.2%</div>
            <div className="text-[10px] text-slate-400">Saves 1,420ms per recurring AOI query</div>
          </div>

          <div className="p-4 rounded-lg bg-[#050811] border border-cyber-emerald/40 space-y-1">
            <div className="text-[10px] text-slate-400 uppercase flex items-center gap-1">
              <Server className="w-3.5 h-3.5 text-cyber-emerald" /> GPU VRAM FOOTPRINT
            </div>
            <div className="text-2xl font-bold text-cyber-emerald">1,840 MB</div>
            <div className="text-[10px] text-slate-400">Runs on low-cost edge GPU or cloud node</div>
          </div>

          <div className="p-4 rounded-lg bg-[#050811] border border-blue-400/40 space-y-1">
            <div className="text-[10px] text-slate-400 uppercase flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5 text-blue-400" /> ISRO BHUVAN COMPLIANCE
            </div>
            <div className="text-2xl font-bold text-blue-400">ISRO NRSC v2.1</div>
            <div className="text-[10px] text-slate-400">Native compatibility with Indian Spatial Infra</div>
          </div>
        </div>

        {/* National Scaling Strategy Box */}
        <div className="p-4 bg-[#050811] rounded-lg border border-slate-800 space-y-2 text-xs">
          <div className="font-bold text-cyber-cyan flex items-center gap-1.5 uppercase">
            <Database className="w-4 h-4" /> NATIONAL COVERAGE SCALING ESTIMATE (ALL 28 STATES)
          </div>
          <p className="text-[#94A3B8] text-[11px] leading-relaxed">
            By deploying tile caching across major river basins and forest reserves, national-scale continuous orbit monitoring operates at an estimated <b className="text-cyber-amber">$420 USD / state / month</b>. Fusing Sentinel-1 SAR with Landsat/Sentinel-2 optical guarantees cloud-free continuity even during monsoon seasons.
          </p>
        </div>
      </div>
    </div>
  );
};
