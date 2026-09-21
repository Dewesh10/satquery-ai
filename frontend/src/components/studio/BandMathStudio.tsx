import React, { useState } from 'react';
import { Layers, Sliders, Activity, Sparkles, Cpu, Calculator } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

export const BandMathStudio: React.FC = () => {
  const [ndviThreshold, setNdviThreshold] = useState(0.45);
  const [ndwiThreshold, setNdwiThreshold] = useState(0.20);
  const [selectedIndex, setSelectedIndex] = useState<'NDVI' | 'NDWI' | 'EVI' | 'NBR' | 'NDMI'>('EVI');
  const [selectedProfile, setSelectedProfile] = useState('DENSE_FOREST');

  const spectralProfiles = [
    { band: 'B02 (Blue)', wavelength: '490nm', DENSE_FOREST: 0.03, URBAN_BUILDING: 0.18, OPEN_WATER: 0.08 },
    { band: 'B03 (Green)', wavelength: '560nm', DENSE_FOREST: 0.06, URBAN_BUILDING: 0.22, OPEN_WATER: 0.06 },
    { band: 'B04 (Red)', wavelength: '665nm', DENSE_FOREST: 0.04, URBAN_BUILDING: 0.26, OPEN_WATER: 0.02 },
    { band: 'B08 (NIR)', wavelength: '842nm', DENSE_FOREST: 0.55, URBAN_BUILDING: 0.30, OPEN_WATER: 0.01 },
    { band: 'B11 (SWIR1)', wavelength: '1610nm', DENSE_FOREST: 0.22, URBAN_BUILDING: 0.38, OPEN_WATER: 0.00 },
    { band: 'B12 (SWIR2)', wavelength: '2190nm', DENSE_FOREST: 0.10, URBAN_BUILDING: 0.34, OPEN_WATER: 0.00 }
  ];

  // 5x5 Simulated Pixel Reflectance Matrix for Band Math calculation
  const generatePixelMatrix = () => {
    const matrix = [];
    for (let r = 0; r < 5; r++) {
      const row = [];
      for (let c = 0; c < 5; c++) {
        const nir = 0.45 + (r * 0.03) - (c * 0.02);
        const red = 0.05 + (c * 0.01);
        const blue = 0.04 + (r * 0.005);
        const swir1 = 0.15 + (r * 0.02);
        const swir2 = 0.08 + (c * 0.015);
        const green = 0.08 - (r * 0.01);

        let val = 0;
        if (selectedIndex === 'NDVI') val = (nir - red) / (nir + red);
        else if (selectedIndex === 'NDWI') val = (green - nir) / (green + nir);
        else if (selectedIndex === 'EVI') val = 2.5 * ((nir - red) / (nir + 6 * red - 7.5 * blue + 1));
        else if (selectedIndex === 'NBR') val = (nir - swir2) / (nir + swir2);
        else if (selectedIndex === 'NDMI') val = (nir - swir1) / (nir + swir1);

        row.push(Number(val.toFixed(3)));
      }
      matrix.push(row);
    }
    return matrix;
  };

  const pixelMatrix = generatePixelMatrix();

  return (
    <div className="w-full h-full bg-[#030712] p-6 overflow-y-auto space-y-6 font-sans select-none">
      {/* Studio Header */}
      <div className="flex items-center justify-between border-b border-cyber-border pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Layers className="w-6 h-6 text-cyber-cyan" />
            <h2 className="font-display font-extrabold text-xl text-slate-100 uppercase tracking-wider">
              SPECTRAL BAND PROFILE & LIVE BAND MATH SANDBOX
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Real-time multi-spectral band index calculator, formula sandbox & surface material reflectance curve engine.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-cyan-500/10 text-cyber-cyan border border-cyan-500/30">
            SENTINEL-2A L2A • 10M GSD
          </span>
        </div>
      </div>

      {/* Grid Layout: Spectral Reflectance Curve + Live Formula Sandbox */}
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

        {/* Card 2: Live Custom Band Math Matrix Sandbox */}
        <div className="p-6 rounded-2xl bg-[#0B132B]/90 border border-cyber-border backdrop-blur-xl space-y-4 shadow-2xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Calculator className="w-5 h-5 text-purple-400" />
              <h3 className="font-display font-bold text-sm text-slate-100 uppercase">
                LIVE 5x5 PIXEL MATRIX BAND MATH SANDBOX
              </h3>
            </div>

            {/* Formula Selector Tabs */}
            <div className="flex gap-1.5 font-mono text-[10px]">
              {(['NDVI', 'NDWI', 'EVI', 'NBR', 'NDMI'] as const).map(idx => (
                <button
                  key={idx}
                  onClick={() => setSelectedIndex(idx)}
                  className={`px-2 py-1 rounded font-bold transition ${
                    selectedIndex === idx ? 'bg-purple-500 text-white shadow-purple-950/50 shadow-lg' : 'bg-slate-900 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {idx}
                </button>
              ))}
            </div>
          </div>

          {/* Active Formula Explanation */}
          <div className="p-3 rounded-xl bg-[#030712] border border-purple-500/40 font-mono text-xs space-y-1">
            <div className="font-bold text-purple-400">Selected Formula: {selectedIndex}</div>
            <div className="text-[11px] text-slate-300">
              {selectedIndex === 'EVI' && 'EVI = 2.5 * ((NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1))'}
              {selectedIndex === 'NDVI' && 'NDVI = (NIR - Red) / (NIR + Red)'}
              {selectedIndex === 'NDWI' && 'NDWI = (Green - NIR) / (Green + NIR)'}
              {selectedIndex === 'NBR' && 'NBR = (NIR - SWIR2) / (NIR + SWIR2)'}
              {selectedIndex === 'NDMI' && 'NDMI = (NIR - SWIR1) / (NIR + SWIR1)'}
            </div>
          </div>

          {/* 5x5 Matrix Visualizer */}
          <div className="p-4 rounded-xl bg-[#030712] border border-slate-800 space-y-2">
            <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
              COMPUTED 5x5 SPECTRAL INDEX MATRIX VALUES
            </div>
            <div className="grid grid-cols-5 gap-2 font-mono text-xs text-center">
              {pixelMatrix.map((row, rIdx) =>
                row.map((val, cIdx) => (
                  <div
                    key={`${rIdx}-${cIdx}`}
                    className="p-2 rounded bg-[#0A101D] border border-purple-500/30 text-purple-300 font-bold transition hover:bg-purple-500/20"
                  >
                    {val}
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Interactive Threshold Sliders */}
          <div className="space-y-3 text-xs font-mono">
            <div className="p-3 rounded-xl bg-[#030712] border border-cyan-500/30 space-y-1">
              <div className="flex justify-between font-bold text-cyber-cyan">
                <span>NDVI Vegetation Mask Threshold</span>
                <span>{ndviThreshold}</span>
              </div>
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
          </div>
        </div>
      </div>
    </div>
  );
};
