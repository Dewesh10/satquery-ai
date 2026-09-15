import React from 'react';
import { ShieldAlert, Trees, Building2, Waves, Anchor, Radio } from 'lucide-react';

interface MissionModeSelectorProps {
  currentPreset: string;
  onSelectMission: (presetId: string) => void;
}

export const MISSION_MODES = [
  { id: 'dubai_urban', label: 'URBAN GROWTH', icon: Building2, color: 'text-cyber-cyan', border: 'border-cyber-cyan' },
  { id: 'amazon_deforestation', label: 'AGRICULTURE', icon: Trees, color: 'text-cyber-emerald', border: 'border-cyber-emerald' },
  { id: 'lake_mead', label: 'WATER RESERVOIR', icon: Waves, color: 'text-blue-400', border: 'border-blue-400' },
  { id: 'assam_flood', label: 'DISASTER RESPONSE', icon: ShieldAlert, color: 'text-cyber-magenta', border: 'border-cyber-magenta' },
  { id: 'singapore_maritime', label: 'MARITIME PORT', icon: Anchor, color: 'text-cyber-amber', border: 'border-cyber-amber' }
];

export const MissionModeSelector: React.FC<MissionModeSelectorProps> = ({ currentPreset, onSelectMission }) => {
  return (
    <div className="flex items-center gap-1.5 bg-[#0A101D] border border-cyber-border rounded-lg p-1 font-mono">
      <span className="text-[10px] text-slate-400 px-2 flex items-center gap-1">
        <Radio className="w-3 h-3 text-cyber-cyan animate-pulse" /> MISSION:
      </span>

      {MISSION_MODES.map((m) => {
        const Icon = m.icon;
        const isActive = currentPreset === m.id;
        return (
          <button
            key={m.id}
            onClick={() => onSelectMission(m.id)}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded text-[11px] font-bold transition ${
              isActive
                ? `bg-slate-900 ${m.color} border ${m.border} shadow-lg`
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Icon className="w-3.5 h-3.5" />
            <span>{m.label}</span>
          </button>
        );
      })}
    </div>
  );
};
