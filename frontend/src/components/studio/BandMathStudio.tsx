import React, { useState } from 'react';
import { Layers, Sliders, Activity, Sparkles, RefreshCw } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

export const BandMathStudio: React.FC = () => {
  const [ndviThreshold, setNdviThreshold] = useState(0.45);
  const [ndwiThreshold, setNdwiThreshold] = useState(0.20);
  const [selectedProfile, setSelectedProfile] = useState('DENSE_FOREST');

  const spectralProfiles = [
    { band: 'B02 (Blue)', wavelength: '490nm', DENSE_FOREST: 0.03, URBAN_BUILDING: 0.18, OPEN_WATER: 0.08 },
    { band: 'B03 (Green)', wavelength: '560nm', DENSE_FOREST: 0.06, URBAN_BUILDING: 0.22, OPEN_WATER: 0.06 },
    { band: 'B04 (Red)', wavelength: '665nm', DENSE_FOREST: 0.04, URBAN_BUILDING: 0.26, OPEN_WATER: 0.02 },
    { band: 'B08 (NIR)', wavelength: '842nm', DENSE_FOREST: 0.55, URBAN_BUILDING: 0.30, OPEN_WATER: 0.01 },
    { band: 'B11 (SWIR1)', wavelength: '1610nm', DENSE_FOREST: 0.22, URBAN_BUILDING: 0.38, OPEN_WATER: 0.00 },
    { band: 'B12 (SWIR2)', wavelength: '2190nm', DENSE_FOREST: 0.10, URBAN_BUILDING: 0.34, OPEN_WATER: 0.00 }
  ];

  return (
    <div className="w-full h-full bg-[#030712] p-6 overflow-y-auto space-y-6 font-sans select-none">
      {/* Studio Header */}
      <div className="flex items-center justify-between border-b border-cyber-border pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Layers className="w-6 h-6 text-cyber-cyan" />
            <h2 className="font-display font-extrabold text-xl text-slate-100 uppercase tracking-wider">
              SPECTRAL BAND PROFILE & BAND MATH STUDIO
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Multi-spectral band ratio math engine & surface material spectral reflectance curve profiler.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-cyan-500/10 text-cyber-cyan border border-cyan-500/30">
            SENTINEL-2A L2A • 10M RESOLUTION
          </span>
        </div>
      </div>

      {/* Grid Layout: Spectral Reflectance Curve + Band Ratio Math */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Card 1: Spectral Reflectance Curve Chart */}
        <div className="p-6 rounded-2xl bg-[#0B132B]/90 border border-cyber-border backdrop-blur-xl space-y-4 shadow-2xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-emerald-400" />
              <h3 className="font-display font-bold text-sm text-slate-100 uppercase">
                SPECTRAL REFLECTANCE CURVE (6 BANDS)
              </h3>
            </div>

            <div className="flex gap-2">
              {['DENSE_FOREST', 'URBAN_BUILDING', 'OPEN_WATER'].map(p => (
                <button
                  key={p}
                  onClick={() => setSelectedProfile(p)}
                  className={`px-2.5 py-1 rounded-lg text-[11px] font-mono font-bold transition ${
                    selectedProfile === p ? 'bg-cyan-500/20 text-cyber-cyan border border-cyan-500/40' : 'bg-slate-900 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {p.replace('_', ' ')}
                </button>
              ))}
            </div>
          </div>

          <div className="h-64 w-full bg-[#030712] p-4 rounded-xl border border-slate-800">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={spectralProfiles}>
                <XAxis dataKey="band" stroke="#64748B" fontSize={11} />
                <YAxis stroke="#64748B" fontSize={11} domain={[0, 0.6]} />
                <Tooltip
                  contentStyle={{ background: '#0B132B', border: '1px solid #00F0FF', borderRadius: '8px', fontSize: '12px' }}
                />
                <Line type="monotone" dataKey={selectedProfile} stroke="#00F0FF" strokeWidth={3} dot={{ r: 6, fill: '#00F0FF' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="text-xs text-slate-400 leading-relaxed bg-[#030712] p-3 rounded-xl border border-slate-800">
            High NIR reflectance (B08: 0.55) paired with low Red reflectance (B04: 0.04) confirms dense photosynthetically active chlorophyll vegetation.
          </div>
        </div>

        {/* Card 2: Interactive Band Math Ratio Calculator */}
        <div className="p-6 rounded-2xl bg-[#0B132B]/90 border border-cyber-border backdrop-blur-xl space-y-4 shadow-2xl">
          <div className="flex items-center gap-2">
            <Sliders className="w-5 h-5 text-amber-400" />
            <h3 className="font-display font-bold text-sm text-slate-100 uppercase">
              MULTI-SPECTRAL BAND RATIO CALCULATORS
            </h3>
          </div>

          <div className="space-y-4 text-xs font-mono">
            {/* NDVI Formula Box */}
            <div className="p-4 rounded-xl bg-[#030712] border border-cyan-500/30 space-y-2">
              <div className="flex justify-between font-bold text-cyber-cyan">
                <span>NDVI (Normalized Difference Vegetation Index)</span>
                <span>Threshold: {ndviThreshold}</span>
              </div>
              <div className="text-[11px] text-slate-400">Formula: (B08 NIR - B04 Red) / (B08 NIR + B04 Red)</div>
              <input
                type="range"
                min="0.1"
                max="0.8"
                step="0.05"
                value={ndviThreshold}
                onChange={(e) => setNdviThreshold(Number(e.target.value))}
                className="w-full accent-cyber-cyan cursor-pointer h-1.5 bg-slate-800 rounded"
              />
            </div>

            {/* NDWI Formula Box */}
            <div className="p-4 rounded-xl bg-[#030712] border border-amber-500/30 space-y-2">
              <div className="flex justify-between font-bold text-amber-400">
                <span>NDWI (Normalized Difference Water Index)</span>
                <span>Threshold: {ndwiThreshold}</span>
              </div>
              <div className="text-[11px] text-slate-400">Formula: (B03 Green - B08 NIR) / (B03 Green + B08 NIR)</div>
              <input
                type="range"
                min="0.05"
                max="0.5"
                step="0.05"
                value={ndwiThreshold}
                onChange={(e) => setNdwiThreshold(Number(e.target.value))}
                className="w-full accent-amber-400 cursor-pointer h-1.5 bg-slate-800 rounded"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
