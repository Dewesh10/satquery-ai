import React, { useState } from 'react';
import { PresetLocation } from '../../types';
import { Sliders, Calendar, ArrowLeftRight } from 'lucide-react';

interface SplitScreenSliderProps {
  preset: PresetLocation;
  onClose: () => void;
}

export const SplitScreenSlider: React.FC<SplitScreenSliderProps> = ({ preset, onClose }) => {
  const [sliderPos, setSliderPos] = useState(50); // percentage 0 - 100

  return (
    <div className="relative w-full h-full bg-[#050811] overflow-hidden select-none">
      {/* Before Image Side (Left) */}
      <div 
        className="absolute inset-0 bg-cover bg-center transition-none border-r-2 border-cyber-cyan"
        style={{
          backgroundImage: `url('https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1600&q=80')`,
          clipPath: `polygon(0 0, ${sliderPos}% 0, ${sliderPos}% 100%, 0 100%)`
        }}
      >
        <div className="absolute top-6 left-6 bg-[#0A101D]/90 border border-cyber-cyan backdrop-blur-md px-3 py-1.5 rounded font-mono text-xs text-cyber-cyan shadow-cyan-glow flex items-center gap-2">
          <Calendar className="w-3.5 h-3.5" />
          <span>BEFORE: {preset.dates[0]} ({preset.sensors[0]})</span>
        </div>
      </div>

      {/* After Image Side (Right) */}
      <div 
        className="absolute inset-0 bg-cover bg-center transition-none"
        style={{
          backgroundImage: `url('https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1600&q=80')`,
          filter: 'hue-rotate(90deg) contrast(1.2)',
          clipPath: `polygon(${sliderPos}% 0, 100% 0, 100% 100%, ${sliderPos}% 100%)`
        }}
      >
        <div className="absolute top-6 right-6 bg-[#0A101D]/90 border border-cyber-amber backdrop-blur-md px-3 py-1.5 rounded font-mono text-xs text-cyber-amber shadow-amber-glow flex items-center gap-2">
          <Calendar className="w-3.5 h-3.5" />
          <span>AFTER: {preset.dates[1]} ({preset.sensors[1]})</span>
        </div>
      </div>

      {/* Interactive Swipe Control Bar */}
      <div 
        className="absolute top-0 bottom-0 w-1 bg-cyber-cyan cursor-ew-resize z-30 flex items-center justify-center shadow-cyan-glow"
        style={{ left: `${sliderPos}%` }}
      >
        <div className="w-8 h-8 rounded-full bg-cyber-cyan text-black font-bold flex items-center justify-center shadow-xl border-2 border-black">
          <ArrowLeftRight className="w-4 h-4" />
        </div>
      </div>

      {/* Range Input Overlay */}
      <input
        type="range"
        min="0"
        max="100"
        value={sliderPos}
        onChange={(e) => setSliderPos(Number(e.target.value))}
        className="absolute inset-0 opacity-0 cursor-ew-resize z-40 w-full h-full"
      />

      {/* Exit Split Screen Button */}
      <button
        onClick={onClose}
        className="absolute bottom-6 right-6 z-50 bg-[#0A101D] border border-cyber-border text-slate-300 hover:text-cyber-cyan px-4 py-2 rounded-lg font-mono text-xs shadow-xl"
      >
        EXIT SPLIT SCREEN
      </button>
    </div>
  );
};
