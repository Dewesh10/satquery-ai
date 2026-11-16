import React, { useState } from 'react';
import { Layers, Sliders, Activity, Sparkles, Cpu, Calculator, Play, CheckCircle2, AlertCircle } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, BarChart, Bar } from 'recharts';
import { DEFAULT_HEADERS } from '../../lib/api';

const API_BASE = 'http://localhost:8000/api/v1';

export const BandMathStudio: React.FC = () => {
  const [ndviThreshold, setNdviThreshold] = useState(0.45);
  const [selectedIndex, setSelectedIndex] = useState<'NDVI' | 'NDWI' | 'EVI' | 'NBR' | 'NDMI'>('EVI');
  const [selectedProfile, setSelectedProfile] = useState('DENSE_FOREST');

  // Custom Formula Evaluator States
  const [customFormula, setCustomFormula] = useState('(B08 - B04) / (B08 + B04 + 0.5) * 1.5');
  const [evalResult, setEvalResult] = useState<any | null>(null);
  const [evalLoading, setEvalLoading] = useState(false);
  const [evalError, setEvalError] = useState<string | null>(null);

  const spectralProfiles = [
    { band: 'B02 (Blue)', wavelength: '490nm', DENSE_FOREST: 0.03, URBAN_BUILDING: 0.18, OPEN_WATER: 0.08 },
    { band: 'B03 (Green)', wavelength: '560nm', DENSE_FOREST: 0.06, URBAN_BUILDING: 0.22, OPEN_WATER: 0.06 },
    { band: 'B04 (Red)', wavelength: '665nm', DENSE_FOREST: 0.04, URBAN_BUILDING: 0.26, OPEN_WATER: 0.02 },
    { band: 'B08 (NIR)', wavelength: '842nm', DENSE_FOREST: 0.55, URBAN_BUILDING: 0.30, OPEN_WATER: 0.01 },
    { band: 'B11 (SWIR1)', wavelength: '1610nm', DENSE_FOREST: 0.22, URBAN_BUILDING: 0.38, OPEN_WATER: 0.00 },
    { band: 'B12 (SWIR2)', wavelength: '2190nm', DENSE_FOREST: 0.10, URBAN_BUILDING: 0.34, OPEN_WATER: 0.00 }
  ];

  const handleEvaluateCustomFormula = async () => {
    if (!customFormula.trim()) return;
    setEvalLoading(true);
    setEvalError(null);
    try {
      const res = await fetch(`${API_BASE}/raster/eval-formula`, {
        method: 'POST',
        headers: { ...DEFAULT_HEADERS, 'Content-Type': 'application/json' },
        body: JSON.stringify({ formula: customFormula.trim() })
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Evaluation failed');
      }
      const data = await res.json();
      setEvalResult(data);
    } catch (err: any) {
      setEvalError(err.message || 'Formula syntax error');
    } finally {
      setEvalLoading(false);
    }
  };

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
              SPECTRAL BAND PROFILE & CUSTOM FORMULA ENGINE
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Real-time multi-spectral band index calculator, arbitrary formula evaluator & surface reflectance curve engine.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-cyan-500/10 text-cyber-cyan border border-cyan-500/30">
            NUMPY VECTORIZED • 10M GSD
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
            
            <div className="flex gap-1.5">
              {['DENSE_FOREST', 'URBAN_BUILDING', 'OPEN_WATER'].map(p => (
                <button
                  key={p}
                  onClick={() => setSelectedProfile(p)}
                  className={`px-2.5 py-1 rounded text-[10px] font-mono font-bold transition ${
                    selectedProfile === p
                      ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                      : 'text-slate-400 hover:bg-slate-800'
                  }`}
                >
                  {p.replace('_', ' ')}
                </button>
              ))}
            </div>
          </div>

          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={spectralProfiles}>
                <XAxis dataKey="band" stroke="#64748B" fontSize={10} tickLine={false} />
                <YAxis stroke="#64748B" fontSize={10} tickLine={false} domain={[0, 0.6]} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#030712', border: '1px solid #1E293B', borderRadius: '8px', fontSize: '11px' }}
                />
                <Line
                  type="monotone"
                  dataKey={selectedProfile}
                  stroke="#10B981"
                  strokeWidth={2.5}
                  dot={{ r: 4, fill: '#10B981', strokeWidth: 1.5, stroke: '#FFFFFF' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Interactive Threshold Slider */}
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

        {/* Card 2: Custom Spectral Index Formula Evaluator */}
        <div className="p-6 rounded-2xl bg-[#0B132B]/90 border border-cyber-border backdrop-blur-xl space-y-4 shadow-2xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Calculator className="w-5 h-5 text-purple-400" />
              <h3 className="font-display font-bold text-sm text-slate-100 uppercase">
                ARBITRARY SPECTRAL FORMULA EVALUATOR
              </h3>
            </div>
            <span className="text-[10px] px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 font-mono">
              NUMPY AST
            </span>
          </div>

          <p className="text-xs text-slate-300">
            Write any mathematical formula using Sentinel-2 bands (<span className="text-purple-300 font-mono font-bold">B02, B03, B04, B08, B11, B12</span>). The backend evaluates the equation on real pixel tensors in real-time.
          </p>

          <div className="flex gap-2">
            <input
              type="text"
              value={customFormula}
              onChange={(e) => setCustomFormula(e.target.value)}
              placeholder="e.g. (B08 - B04) / (B08 + B04)"
              className="flex-1 px-3 py-2 rounded-xl bg-black/60 border border-cyber-border text-white text-xs font-mono focus:outline-none focus:border-purple-400 shadow-inner"
            />
            <button
              onClick={handleEvaluateCustomFormula}
              disabled={evalLoading}
              className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold font-mono transition flex items-center gap-1.5 shadow-purple-glow"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              {evalLoading ? 'Eval...' : 'Run'}
            </button>
          </div>

          {/* Quick presets */}
          <div className="flex flex-wrap gap-1.5 pt-1">
            <span className="text-[10px] text-slate-400 font-mono py-0.5">Presets:</span>
            {[
              { name: 'SAVI (Soil Adjusted)', expr: '(B08 - B04) / (B08 + B04 + 0.5) * 1.5' },
              { name: 'NBR (Burn Ratio)', expr: '(B08 - B12) / (B08 + B12)' },
              { name: 'MNDWI (Turbid Water)', expr: '(B03 - B11) / (B03 + B11)' },
              { name: 'NDVI Standard', expr: '(B08 - B04) / (B08 + B04)' }
            ].map(p => (
              <button
                key={p.name}
                onClick={() => setCustomFormula(p.expr)}
                className="text-[10px] font-mono px-2 py-0.5 rounded bg-black/50 border border-cyber-border/70 hover:border-purple-400 text-slate-300 transition"
              >
                {p.name}
              </button>
            ))}
          </div>

          {evalError && (
            <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/40 text-rose-300 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{evalError}</span>
            </div>
          )}

          {evalResult && (
            <div className="p-4 rounded-xl bg-black/50 border border-purple-500/40 space-y-3">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="text-slate-400">MEAN VALUE: <strong className="text-purple-300 text-sm">{evalResult.mean_index_value}</strong></span>
                <span className="text-slate-400">STD DEV: <strong className="text-cyan-300">{evalResult.std_deviation}</strong></span>
                <span className="text-slate-400">RANGE: <strong className="text-emerald-300">[{evalResult.min_index_value}, {evalResult.max_index_value}]</strong></span>
              </div>

              <div className="h-28 w-full pt-1">
                <div className="text-[10px] font-mono text-slate-400 mb-1">INDEX VALUE DISTRIBUTION HISTOGRAM:</div>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={evalResult.histogram}>
                    <XAxis dataKey="bin" hide />
                    <YAxis hide />
                    <Tooltip contentStyle={{ backgroundColor: '#030712', border: '1px solid #1E293B', fontSize: '10px' }} />
                    <Bar dataKey="count" fill="#A855F7" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* 5x5 Matrix Visualizer */}
          <div className="p-3 rounded-xl bg-[#030712] border border-slate-800 space-y-2">
            <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider flex justify-between">
              <span>REFERENCE 5x5 TENSOR CHIP</span>
              <span className="text-purple-400">{selectedIndex}</span>
            </div>
            <div className="grid grid-cols-5 gap-1.5 font-mono text-[11px] text-center">
              {pixelMatrix.map((row, rIdx) =>
                row.map((val, cIdx) => (
                  <div
                    key={`${rIdx}-${cIdx}`}
                    className="p-1.5 rounded bg-[#0A101D] border border-purple-500/30 text-purple-300 font-bold transition hover:bg-purple-500/20"
                  >
                    {val}
                  </div>
                ))
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};
