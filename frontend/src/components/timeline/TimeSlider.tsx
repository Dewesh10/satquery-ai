import React, { useState } from 'react';
import { Play, Pause, RotateCcw, Calendar, Clock } from 'lucide-react';
import { PresetLocation } from '../../types';

interface TimeSliderProps {
  preset: PresetLocation;
  onTimeChange?: (dateStr: string) => void;
}

export const TimeSlider: React.FC<TimeSliderProps> = ({ preset, onTimeChange }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(1);

  const dates = [
    preset.dates[0],
    '2020-06-15',
    '2022-01-10',
    preset.dates[1]
  ];

  const handlePlayToggle = () => {
    setIsPlaying(!isPlaying);
  };

  return (
    <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 bg-[#0A101D]/90 border border-cyber-border backdrop-blur-md px-4 py-2.5 rounded-xl shadow-2xl flex items-center gap-4 font-mono select-none">
      {/* Play/Pause Button */}
      <button
        onClick={handlePlayToggle}
        className="w-8 h-8 rounded-full bg-cyber-cyan/20 border border-cyber-cyan text-cyber-cyan hover:bg-cyber-cyan/30 flex items-center justify-center transition shadow-cyan-glow"
      >
        {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 ml-0.5" />}
      </button>

      {/* Scrubber Controls */}
      <div className="flex flex-col gap-1 w-64 sm:w-80">
        <div className="flex items-center justify-between text-[11px]">
          <span className="text-slate-400 flex items-center gap-1">
            <Calendar className="w-3 h-3 text-cyber-amber" /> TEMPORAL STEP:
          </span>
          <span className="text-cyber-cyan font-bold">{dates[currentIndex]}</span>
        </div>

        <input
          type="range"
          min="0"
          max={dates.length - 1}
          value={currentIndex}
          onChange={(e) => {
            const idx = Number(e.target.value);
            setCurrentIndex(idx);
            if (onTimeChange) onTimeChange(dates[idx]);
          }}
          className="w-full accent-cyber-cyan cursor-pointer h-1.5 bg-slate-800 rounded-lg"
        />

        <div className="flex justify-between text-[9px] text-slate-500 font-mono">
          <span>{dates[0]}</span>
          <span>{dates[dates.length - 1]}</span>
        </div>
      </div>
    </div>
  );
};
