import React from 'react';
import { Network, X, CheckCircle2, Clock, ShieldCheck, AlertCircle } from 'lucide-react';

interface SystemRoadmapModalProps {
  onClose: () => void;
}

export const SystemRoadmapModal: React.FC<SystemRoadmapModalProps> = ({ onClose }) => {
  return (
    <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4 font-sans select-none">
      <div className="w-full max-w-2xl bg-[#0B132B] border border-cyber-cyan rounded-xl shadow-2xl p-6 relative space-y-5">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-cyber-border pb-3">
          <div className="flex items-center gap-2">
            <Network className="w-5 h-5 text-cyber-cyan animate-pulse" />
            <h3 className="font-display font-bold text-sm text-slate-100 uppercase tracking-wider">
              SYSTEM IMPLEMENTATION SCOPE & ENGINEERING ROADMAP
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Feature Status Grid */}
        <div className="space-y-3 font-mono text-xs">
          {/* Fully Implemented Features */}
          <div className="p-4 bg-[#030712] border border-emerald-500/40 rounded-xl space-y-2">
            <div className="font-bold text-emerald-400 flex items-center gap-1.5 uppercase">
              <CheckCircle2 className="w-4 h-4" /> FULLY IMPLEMENTED & LIVE (100% PRODUCTION)
            </div>
            <ul className="text-[11px] text-slate-300 space-y-1 list-disc list-inside">
              <li>STAC Satellite Catalog Querying & Metadata Normalization</li>
              <li>Multi-Sensor Optical + SAR Radar Specular Fusion (100% Cloud Penetration)</li>
              <li>Bayesian Uncertainty Quantification Engine (Calibrated Trust Scores)</li>
              <li>Vision-Language Grounded Evidence Generator & Spatial Fly-to</li>
              <li>ISRO NRSC Bhuvan Directive Generator & Workflow Accountability Bar</li>
              <li>Multi-Format Exporter (GeoJSON, CSV, PDF Reports)</li>
            </ul>
          </div>

          {/* Roadmap & In-Flight Stubs */}
          <div className="p-4 bg-[#030712] border border-amber-500/40 rounded-xl space-y-2">
            <div className="font-bold text-amber-400 flex items-center gap-1.5 uppercase">
              <Clock className="w-4 h-4" /> IN-FLIGHT / ACTIVE LEARNING ROADMAP
            </div>
            <ul className="text-[11px] text-slate-300 space-y-1 list-disc list-inside">
              <li><b>Active Learning Gradient Update</b>: HITL annotations are logged to queue; full GPU backpropagation is triggered in offline batch jobs.</li>
              <li><b>ISRO Bhuvan Live Portal Sync</b>: Direct REST API sync to Bhuvan servers operates via local mock gateway.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
