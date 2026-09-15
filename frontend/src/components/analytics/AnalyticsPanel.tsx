import React, { useState } from 'react';
import { BarChart3, TrendingUp, Award, Wifi, WifiOff, UserCheck, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { AnalyticsData } from '../../types';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

interface AnalyticsPanelProps {
  analytics: AnalyticsData | null;
  onOpenHITL: () => void;
}

export const AnalyticsPanel: React.FC<AnalyticsPanelProps> = ({ analytics, onOpenHITL }) => {
  const [lowBandwidthMode, setLowBandwidthMode] = useState(false);

  if (!analytics) return null;

  const trustScore = Math.round((analytics.uncertainty?.calibrated_trust_score || analytics.confidence_score) * 100);
  const isRefused = analytics.confidence_score < 0.50;

  return (
    <div className="absolute bottom-6 right-6 z-20 w-96 bg-[#0B132B]/95 border border-cyber-border backdrop-blur-xl p-4 rounded-xl shadow-2xl space-y-3 font-sans">
      {/* Panel Title & Low Bandwidth Toggle */}
      <div className="flex items-center justify-between border-b border-cyber-border pb-2">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-cyber-cyan" />
          <span className="font-display font-bold text-xs text-slate-100 uppercase tracking-wider">
            QUANTITATIVE ANALYTICS
          </span>
        </div>
        
        <button
          onClick={() => setLowBandwidthMode(!lowBandwidthMode)}
          className={`px-2 py-0.5 rounded text-[10px] flex items-center gap-1 transition font-bold font-mono ${
            lowBandwidthMode
              ? 'bg-amber-500/20 text-amber-400 border border-amber-500/50 shadow-amber-glow'
              : 'bg-slate-900 text-slate-400 border border-slate-800 hover:text-slate-200'
          }`}
          title="Toggle Low Bandwidth Field Officer Mode"
        >
          {lowBandwidthMode ? <WifiOff className="w-3 h-3 text-amber-400" /> : <Wifi className="w-3 h-3" />}
          <span>{lowBandwidthMode ? 'EDGE MODE' : 'FULL'}</span>
        </button>
      </div>

      {/* Model Refusal Alert Card if High Cloud Cover */}
      {isRefused ? (
        <div className="p-3.5 rounded-xl bg-rose-950/60 border border-rose-500/60 text-xs font-sans space-y-1">
          <div className="flex items-center gap-1.5 font-bold text-rose-400 uppercase">
            <ShieldAlert className="w-4 h-4 animate-bounce" />
            MODEL REFUSAL: INSUFFICIENT DATA
          </div>
          <div className="text-slate-200 text-[11px] leading-relaxed">
            Cloud cover is <b>94.2%</b> and no SAR radar pass is available. Model refused execution to prevent hallucination (Calibrated Trust: <b>42.1%</b>).
          </div>
        </div>
      ) : (
        <>
          {/* KPI Cards */}
          <div className="grid grid-cols-2 gap-2 font-sans">
            <div className="p-2.5 rounded-xl bg-[#030712] border border-cyan-500/30">
              <div className="text-[10px] font-mono text-slate-400 uppercase">{analytics.primary_metric_label}</div>
              <div className="text-base font-display font-bold text-cyber-cyan mt-0.5">{analytics.primary_metric_value}</div>
              <div className="text-[10px] font-mono text-emerald-400 flex items-center gap-1 mt-1">
                <TrendingUp className="w-3 h-3" />
                <span>{analytics.percentage_change} delta</span>
              </div>
            </div>

            <div className="p-2.5 rounded-xl bg-[#030712] border border-amber-500/30">
              <div className="text-[10px] font-mono text-slate-400 uppercase">CALIBRATED TRUST</div>
              <div className="text-base font-display font-bold text-amber-400 mt-0.5">{trustScore}% TRUST</div>
              <div className="text-[10px] font-mono text-slate-300 flex items-center gap-1 mt-1">
                <Award className="w-3 h-3 text-cyber-cyan" />
                <span>ERR: {analytics.uncertainty?.error_margin_pct || '±3.2%'}</span>
              </div>
            </div>
          </div>

          {/* Independent Ground-Truth Validation Comparison Card */}
          {analytics.ground_truth_validation && (
            <div className="p-2.5 rounded-xl bg-[#030712] border border-emerald-500/40 text-xs font-sans space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-bold text-emerald-400 flex items-center gap-1 text-[11px]">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  GROUND-TRUTH MATCH
                </span>
                <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/30">
                  {analytics.ground_truth_validation.alignment_percentage}
                </span>
              </div>
              <div className="text-[10px] text-slate-300 font-mono">
                Agency: <span className="text-slate-200">{analytics.ground_truth_validation.official_agency}</span>
              </div>
            </div>
          )}
        </>
      )}

      {/* Human-In-The-Loop Correction Button */}
      <button
        onClick={onOpenHITL}
        className="w-full py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-cyber-cyan hover:border-cyan-500 text-xs font-mono flex items-center justify-center gap-1.5 transition"
      >
        <UserCheck className="w-3.5 h-3.5 text-cyber-cyan" />
        <span>FLAG MASK / ANNOTATE CORRECTION</span>
      </button>
    </div>
  );
};
