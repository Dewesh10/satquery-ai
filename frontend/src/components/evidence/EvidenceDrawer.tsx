import React from 'react';
import { ShieldCheck, MapPin, ZoomIn, FileText, ChevronRight, ChevronLeft } from 'lucide-react';
import { EvidenceData, EvidenceCard } from '../../types';

interface EvidenceDrawerProps {
  evidence: EvidenceData | null;
  onFlyToEvidence: (coords: [number, number]) => void;
  onInspectChip: (card: EvidenceCard) => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
}

// Helper to format raw markdown **bold** text into clean HTML spans
function renderFormattedAnswer(text: string) {
  const parts = text.split(/(\*\*.*?\*\*)/g);
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i} className="text-cyber-cyan font-bold">{part.slice(2, -2)}</strong>;
    }
    return part;
  });
}

export const EvidenceDrawer: React.FC<EvidenceDrawerProps> = ({
  evidence,
  onFlyToEvidence,
  onInspectChip,
  collapsed,
  onToggleCollapse
}) => {
  if (collapsed) {
    return (
      <div className="w-12 h-full bg-[#0B132B]/90 border-l border-cyber-border flex flex-col items-center py-4 z-20 shrink-0 select-none font-sans">
        <button
          onClick={onToggleCollapse}
          className="p-2 rounded hover:bg-slate-800 text-emerald-400 transition"
          title="Expand Evidence Panel"
        >
          <ChevronLeft className="w-5 h-5" />
        </button>
        <div className="mt-8 text-[11px] font-display font-bold text-slate-400 rotate-90 whitespace-nowrap uppercase tracking-widest">
          EVIDENCE PANEL
        </div>
      </div>
    );
  }

  if (!evidence) {
    return (
      <div className="w-80 h-full bg-[#0B132B]/90 border-l border-cyber-border backdrop-blur-xl p-4 flex flex-col items-center justify-center text-center z-20 shrink-0 select-none relative font-sans">
        <button
          onClick={onToggleCollapse}
          className="absolute top-4 left-3 p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition"
          title="Collapse Panel"
        >
          <ChevronRight className="w-4 h-4" />
        </button>
        <ShieldCheck className="w-10 h-10 text-cyber-cyan/30 mb-2" />
        <span className="text-xs font-mono text-slate-500">
          EVIDENCE PANEL WAITING FOR QUERY INVOCATION
        </span>
      </div>
    );
  }

  return (
    <div className="w-80 h-full bg-[#0B132B]/90 border-l border-cyber-border backdrop-blur-xl flex flex-col z-20 shrink-0 overflow-y-auto relative font-sans">
      {/* Collapse Button */}
      <button
        onClick={onToggleCollapse}
        className="absolute top-4 left-3 p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition"
        title="Collapse Panel"
      >
        <ChevronRight className="w-4 h-4" />
      </button>

      {/* Evidence Header */}
      <div className="p-4 border-b border-cyber-border flex items-center justify-between pl-10">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          <span className="font-display font-bold text-sm text-slate-100 uppercase tracking-wider">
            EVIDENCE GROUNDING
          </span>
        </div>
      </div>

      {/* Grounded VLM Answer Explanation with clean typography */}
      <div className="p-4 border-b border-cyber-border bg-[#030712]/50 space-y-2">
        <div className="text-xs font-semibold text-cyber-cyan flex items-center gap-1.5 uppercase">
          <FileText className="w-4 h-4" />
          VLM EXECUTIVE STATEMENT:
        </div>
        <p className="text-xs font-sans text-slate-200 leading-relaxed bg-[#0F172A]/80 p-3.5 rounded-xl border border-cyan-500/20 shadow-inner">
          {renderFormattedAnswer(evidence.answer)}
        </p>
      </div>

      {/* Supporting Evidence Cards */}
      <div className="p-4 space-y-3">
        <div className="text-xs font-display font-bold text-slate-400 uppercase tracking-wider">
          CITATIONS & SCENE FOOTPRINTS ({evidence.evidence_cards.length})
        </div>

        {evidence.evidence_cards.map((card) => (
          <div
            key={card.id}
            className="p-3.5 rounded-xl bg-[#0F172A] border border-cyan-500/30 hover:border-cyan-400 transition-all space-y-2.5 group shadow-cyan-glow"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-display font-bold text-cyber-cyan">{card.title}</span>
              <span className="text-[10px] font-mono font-bold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded-md border border-amber-500/30">
                CONF: {card.confidence}
              </span>
            </div>

            <div 
              onClick={() => onInspectChip(card)}
              className="relative h-28 rounded-lg overflow-hidden border border-slate-700 cursor-pointer group-hover:border-cyan-400 transition"
            >
              <img src={card.thumbnail} alt="Scene chip" className="w-full h-full object-cover group-hover:scale-105 transition" />
              <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-cyber-cyan text-xs font-semibold gap-1.5">
                <ZoomIn className="w-4 h-4" /> 4X MAGNIFIER
              </div>
            </div>

            <div className="space-y-1 text-xs font-sans text-slate-300">
              <div className="flex justify-between"><span className="text-slate-400">SCENE ID:</span> <span className="font-mono text-slate-200 text-[11px]">{card.scene_id}</span></div>
              <div className="flex justify-between"><span className="text-slate-400">METRIC:</span> <span className="text-emerald-400 font-bold">{card.metric}</span></div>
            </div>

            <div className="grid grid-cols-2 gap-2 mt-2">
              <button
                onClick={() => onFlyToEvidence(card.coordinates)}
                className="py-1.5 rounded-lg bg-cyan-500/10 border border-cyan-500/40 text-cyber-cyan hover:bg-cyan-500/20 text-xs font-semibold flex items-center justify-center gap-1 transition"
              >
                <MapPin className="w-3.5 h-3.5" />
                <span>FLY TO MAP</span>
              </button>

              <button
                onClick={() => onInspectChip(card)}
                className="py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/40 text-amber-400 hover:bg-amber-500/20 text-xs font-semibold flex items-center justify-center gap-1 transition"
              >
                <ZoomIn className="w-3.5 h-3.5" />
                <span>INSPECT</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
