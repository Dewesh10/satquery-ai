import React, { useState } from 'react';
import { Globe, Radio, Layers, Network, Download, Bell, Cpu, ChevronDown, Zap, Award, Languages, MapPin, Activity, History } from 'lucide-react';
import { PresetLocation } from '../types';
import { soundEngine } from '../lib/sound';

interface NavbarProps {
  presets: Record<string, PresetLocation>;
  selectedPreset: string;
  onSelectPreset: (presetId: string) => void;
  activeLayer: string;
  onChangeLayer: (layer: string) => void;
  splitScreenMode: boolean;
  onToggleSplitScreen: () => void;
  onOpenExport: () => void;
  onOpenBenchmarking: () => void;
  onOpenRoadmap: () => void;
  onOpenHistory: () => void;
  selectedLang: string;
  onChangeLang: (lang: string) => void;
  activeTab: string;
  onChangeTab: (tab: string) => void;
  isProcessing: boolean;
}

export const WORKBENCH_TABS = [
  { id: 'WORKSPACE', label: '3D MAP WORKSPACE', icon: Globe },
  { id: 'BAND_MATH', label: 'BAND MATH STUDIO', icon: Layers },
  { id: 'DAG_STUDIO', label: 'AGENT DAG STUDIO', icon: Network },
  { id: 'PIPELINE_OPS', label: 'PIPELINE & OPS', icon: Activity },
  { id: 'WATCHTOWER', label: 'SENTINEL WATCHTOWER', icon: Bell },
  { id: 'GOVT_DIRECTIVE', label: 'ISRO BHUVAN DIRECTIVE', icon: MapPin },
  { id: 'HITL_STUDIO', label: 'HITL RETRAINING', icon: Cpu }
];

export const Navbar: React.FC<NavbarProps> = ({
  presets,
  selectedPreset,
  onSelectPreset,
  activeLayer,
  onChangeLayer,
  splitScreenMode,
  onToggleSplitScreen,
  onOpenExport,
  onOpenBenchmarking,
  onOpenRoadmap,
  onOpenHistory,
  selectedLang,
  onChangeLang,
  activeTab,
  onChangeTab,
  isProcessing
}) => {
  const [isBandsOpen, setIsBandsOpen] = useState(false);
  const [isLangOpen, setIsLangOpen] = useState(false);

  return (
    <>
      {/* Demo disclaimer banner — always visible at the very top */}
      <div className="w-full bg-amber-500/10 border-b border-amber-500/30 px-4 py-1 flex items-center justify-center gap-2 text-[11px] font-mono text-amber-300 select-none z-[10000]">
        <span className="font-bold text-amber-400">⚠ DEMO</span>
        <span>·</span>
        <span>Synthetic pipeline validation only — not for operational or safety-critical use.</span>
        <span>·</span>
        <span>Benchmarks are computed on simulated arrays, not real Sen1Floods11 / OSCD chips.</span>
      </div>
    <header className="h-16 bg-[#030712]/95 border-b border-cyber-border backdrop-blur-xl px-5 flex items-center justify-between z-[9999] relative shrink-0 select-none font-sans">
      {/* Brand & ROI Efficiency Banner */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-3">
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/40 shadow-cyan-glow">
            <Globe className="w-5 h-5 text-cyber-cyan animate-pulse" />
            <div className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-black animate-ping" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-display font-black text-lg tracking-wider text-white">
                SatQuery<span className="text-cyber-cyan">.AI</span>
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyber-cyan border border-cyan-500/30 uppercase tracking-widest font-semibold">
                ENTERPRISE
              </span>
            </div>
            <div className="text-[10px] font-mono text-slate-400 flex items-center gap-2">
              <span className="text-emerald-400 flex items-center gap-1 font-semibold">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                STAC BOA ONLINE
              </span>
              <span>•</span>
              <span>Z-SCORE CALIBRATED</span>
            </div>
          </div>
        </div>
      </div>

      {/* Center Tabs Navigation */}
      <div className="flex items-center gap-1 bg-[#0B132B]/60 p-1 rounded-xl border border-cyber-border/80">
        {WORKBENCH_TABS.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => {
                soundEngine.playTabSwitch();
                onChangeTab(tab.id);
              }}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                isActive
                  ? 'bg-cyan-500/20 text-cyber-cyan border border-cyan-500/50 shadow-cyan-glow'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Action Controls */}
      <div className="flex items-center gap-2.5 relative z-[10000]">
        {/* History Replay Button */}
        <button
          onClick={onOpenHistory}
          className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-[#0B132B] border border-cyan-500/40 text-cyber-cyan text-xs font-semibold hover:bg-cyan-500/10 transition shadow-cyan-glow"
          title="Open SQLite Query History & Replay Runs"
        >
          <History className="w-3.5 h-3.5" />
          <span>REPLAY</span>
        </button>

        {/* Multi-Language Selector Dropdown */}
        <div className="relative">
          <button
            onClick={() => { setIsLangOpen(!isLangOpen); setIsBandsOpen(false); }}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#0B132B] border border-cyan-500/40 text-cyber-cyan text-xs font-mono font-bold hover:bg-cyan-500/10 transition shadow-cyan-glow"
          >
            <Languages className="w-4 h-4" />
            <span>{selectedLang}</span>
            <ChevronDown className="w-3.5 h-3.5 opacity-70" />
          </button>

          {isLangOpen && (
            <div className="absolute right-0 top-full mt-2 w-44 bg-[#0B132B] border border-cyber-border rounded-xl shadow-2xl p-2 z-[10000] font-sans space-y-1 backdrop-blur-xl">
              {[
                { id: 'EN', label: 'ENGLISH' },
                { id: 'HI', label: 'हिंदी (HINDI)' },
                { id: 'AS', label: 'অসমীয়া (ASSAMESE)' }
              ].map(l => (
                <button
                  key={l.id}
                  onClick={() => { onChangeLang(l.id); setIsLangOpen(false); }}
                  className={`w-full text-left px-3 py-2 rounded-lg text-xs font-medium transition ${
                    selectedLang === l.id ? 'bg-cyan-500/20 text-cyber-cyan font-bold border border-cyan-500/40' : 'text-slate-300 hover:bg-slate-800'
                  }`}
                >
                  {l.label}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Benchmarking & Roadmap Trigger Buttons */}
        <button
          onClick={onOpenBenchmarking}
          className="p-2 rounded-lg bg-[#0B132B] border border-cyber-border text-slate-300 hover:text-cyber-cyan transition"
          title="Model Benchmarking & Evaluation Specs"
        >
          <Award className="w-4 h-4" />
        </button>

        <button
          onClick={onOpenRoadmap}
          className="p-2 rounded-lg bg-[#0B132B] border border-cyber-border text-slate-300 hover:text-amber-400 transition"
          title="System Implementation Scope & Roadmap"
        >
          <Cpu className="w-4 h-4" />
        </button>

        {/* Spectral Band Selector */}
        <div className="relative">
          <button
            onClick={() => { setIsBandsOpen(!isBandsOpen); setIsLangOpen(false); }}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-[#0B132B] border border-cyber-border text-xs font-semibold text-slate-200 hover:text-cyber-cyan transition"
          >
            <Layers className="w-4 h-4 text-cyber-cyan" />
            <span className="uppercase">{activeLayer}</span>
            <ChevronDown className="w-3.5 h-3.5 opacity-70" />
          </button>
          
          {isBandsOpen && (
            <div className="absolute right-0 top-full mt-2 w-52 bg-[#0B132B] border border-cyber-border rounded-xl shadow-2xl p-2 z-[10000] font-sans backdrop-blur-xl space-y-1">
              <div className="text-[10px] font-mono text-slate-400 uppercase px-2 py-1 font-bold">Spectral Layers</div>
              {[
                { id: 'RGB', label: 'True Color (RGB)' },
                { id: 'INFRARED', label: 'False Color IR' },
                { id: 'NDVI', label: 'NDVI Vegetation' },
                { id: 'NDWI', label: 'NDWI Water' },
                { id: 'SAR', label: 'SAR Radar' },
                { id: 'DARK', label: 'Dark Canvas Vector' }
              ].map(l => (
                <button
                  key={l.id}
                  onClick={() => { onChangeLayer(l.id); setIsBandsOpen(false); }}
                  className={`w-full text-left px-3 py-2 rounded-lg text-xs font-medium transition ${
                    activeLayer === l.id ? 'bg-cyan-500/20 text-cyber-cyan font-bold border border-cyan-500/40' : 'text-slate-300 hover:bg-slate-800'
                  }`}
                >
                  {l.label}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Split Screen Toggle */}
        <button
          onClick={onToggleSplitScreen}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition border ${
            splitScreenMode
              ? 'bg-amber-500/20 text-amber-400 border-amber-500/50 shadow-amber-glow'
              : 'bg-[#0B132B] text-slate-200 border-cyber-border hover:border-slate-500'
          }`}
        >
          <Radio className="w-4 h-4" />
          <span>SPLIT</span>
        </button>

        {/* Export Button */}
        <button
          onClick={onOpenExport}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyan-500/10 border border-cyan-500/40 text-cyber-cyan text-xs font-semibold hover:bg-cyan-500/20 transition shadow-cyan-glow"
        >
          <Download className="w-4 h-4" />
          <span>EXPORT</span>
        </button>
      </div>
    </header>
    </>
  );
};
