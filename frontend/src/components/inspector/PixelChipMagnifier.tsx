import React, { useState } from 'react';
import { ZoomIn, Sliders, X, Layers, Sun, ShieldAlert } from 'lucide-react';
import { EvidenceCard } from '../../types';

interface PixelChipMagnifierProps {
  card: EvidenceCard;
  onClose: () => void;
}

export const PixelChipMagnifier: React.FC<PixelChipMagnifierProps> = ({ card, onClose }) => {
  const [zoomLevel, setZoomLevel] = useState(2.5);
  const [contrast, setContrast] = useState(120);
  const [showMask, setShowMask] = useState(true);

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4 font-mono select-none">
      <div className="w-full max-w-2xl bg-[#0A101D] border border-cyber-cyan rounded-xl shadow-cyan-glow p-6 relative space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-cyber-border pb-3">
          <div className="flex items-center gap-2">
            <ZoomIn className="w-5 h-5 text-cyber-cyan animate-pulse" />
            <span className="font-bold text-sm text-slate-100 uppercase tracking-wider">
              OPTICAL CHIP INSPECTOR // 4X MAGNIFIER
            </span>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Image Magnifier Canvas Area */}
        <div className="relative h-72 rounded-lg overflow-hidden border border-cyber-cyan/40 bg-black flex items-center justify-center group">
          <img
            src={card.thumbnail}
            alt="Magnified chip"
            className="w-full h-full object-cover transition-all"
            style={{
              transform: `scale(${zoomLevel})`,
              filter: `contrast(${contrast}%) brightness(110%)`
            }}
          />

          {/* Mask Highlight Overlay */}
          {showMask && (
            <div className="absolute inset-0 bg-cyber-cyan/20 border-2 border-cyber-cyan pointer-events-none flex items-center justify-center">
              <div className="bg-black/80 px-3 py-1 rounded text-[11px] text-cyber-cyan border border-cyber-cyan/50 font-bold">
                EXTRACTED VECTOR MASK (CONFIDENCE: {card.confidence})
              </div>
            </div>
          )}

          {/* Crosshair Overlay */}
          <div className="absolute inset-0 pointer-events-none flex items-center justify-center opacity-40">
            <div className="w-full h-0.5 bg-cyber-cyan" />
            <div className="h-full w-0.5 bg-cyber-cyan absolute" />
          </div>

          <div className="absolute bottom-2 left-2 bg-black/80 px-2.5 py-1 rounded text-[10px] text-slate-300 border border-slate-700">
            GSD: 10m • COORDS: [{card.coordinates[0].toFixed(3)}, {card.coordinates[1].toFixed(3)}]
          </div>
        </div>

        {/* Control Sliders & Band Inspection */}
        <div className="grid grid-cols-2 gap-4 bg-[#050811] p-3 rounded-lg border border-slate-800 text-xs">
          <div className="space-y-2">
            <div className="flex justify-between text-slate-400 text-[11px]">
              <span>MAGNIFICATION LEVEL</span>
              <span className="text-cyber-cyan">{zoomLevel.toFixed(1)}x</span>
            </div>
            <input
              type="range"
              min="1"
              max="4"
              step="0.1"
              value={zoomLevel}
              onChange={(e) => setZoomLevel(Number(e.target.value))}
              className="w-full accent-cyber-cyan cursor-pointer h-1.5 bg-slate-800 rounded"
            />
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-slate-400 text-[11px]">
              <span>CONTRAST EQUALIZATION</span>
              <span className="text-cyber-amber">{contrast}%</span>
            </div>
            <input
              type="range"
              min="80"
              max="200"
              value={contrast}
              onChange={(e) => setContrast(Number(e.target.value))}
              className="w-full accent-cyber-amber cursor-pointer h-1.5 bg-slate-800 rounded"
            />
          </div>
        </div>

        {/* Footer Meta */}
        <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-800">
          <div>SCENE: <span className="text-slate-200">{card.scene_id}</span></div>
          <div>SENSOR: <span className="text-cyber-emerald">{card.sensor}</span></div>
          <button
            onClick={() => setShowMask(!showMask)}
            className="px-3 py-1 rounded bg-cyber-cyan/10 border border-cyber-cyan/40 text-cyber-cyan hover:bg-cyber-cyan/20 transition font-bold"
          >
            {showMask ? 'HIDE MASK' : 'SHOW MASK'}
          </button>
        </div>
      </div>
    </div>
  );
};
