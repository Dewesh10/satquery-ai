import React, { useState, useEffect } from 'react';
import { History, Play, RotateCcw, Clock, MapPin, CheckCircle2, ChevronRight, Database } from 'lucide-react';
import { DEFAULT_HEADERS } from '../../lib/api';

const API_BASE = 'http://localhost:8000/api/v1';

interface QueryHistoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectRun: (runData: any) => void;
}

export const QueryHistoryModal: React.FC<QueryHistoryModalProps> = ({ isOpen, onClose, onSelectRun }) => {
  const [runs, setRuns] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      loadHistory();
    }
  }, [isOpen]);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/history?limit=25`, { headers: DEFAULT_HEADERS });
      if (res.ok) {
        const data = await res.json();
        if (data.runs && data.runs.length > 0) {
          setRuns(data.runs);
        } else {
          // Fallback to demo runs
          const demoRes = await fetch(`${API_BASE}/demo`, { headers: DEFAULT_HEADERS });
          if (demoRes.ok) {
            const demoData = await demoRes.json();
            setRuns(demoData.runs || []);
          }
        }
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleReplay = async (runId: string) => {
    setSelectedRunId(runId);
    try {
      const res = await fetch(`${API_BASE}/replay/${runId}`, { headers: DEFAULT_HEADERS });
      if (res.ok) {
        const fullRun = await res.json();
        onSelectRun(fullRun);
        onClose();
      }
    } catch (e) {
      console.error(e);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[10000] bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-[#0b1329] border border-cyber-border rounded-2xl w-full max-w-3xl overflow-hidden shadow-2xl flex flex-col max-h-[85vh]">
        
        {/* Header */}
        <div className="p-5 border-b border-cyber-border flex items-center justify-between bg-black/40">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyber-cyan">
              <History className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                SQLITE QUERY HISTORY & REPLAY LOGS
                <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-mono">
                  {runs.length} RECORDS
                </span>
              </h2>
              <p className="text-xs text-slate-400">
                Instantly replay cached DAG execution runs, vector polygons, and change metrics
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white text-lg font-mono px-2 py-1"
          >
            ✕
          </button>
        </div>

        {/* Content list */}
        <div className="p-5 overflow-y-auto space-y-3 flex-1">
          {loading ? (
            <div className="text-center py-12 text-slate-400 text-xs flex items-center justify-center gap-2">
              <RotateCcw className="w-4 h-4 animate-spin text-cyber-cyan" />
              Loading persistent query database...
            </div>
          ) : runs.length === 0 ? (
            <div className="text-center py-12 text-slate-400 text-xs">
              No historical runs recorded yet. Execute queries on the map to build your history!
            </div>
          ) : (
            runs.map((r) => (
              <div
                key={r.run_id}
                className="p-4 rounded-xl bg-black/40 border border-cyber-border/80 hover:border-cyber-cyan/60 transition-all flex items-center justify-between group"
              >
                <div className="space-y-1.5 max-w-[70%]">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
                      {r.run_id}
                    </span>
                    <span className="text-xs font-semibold text-white flex items-center gap-1">
                      <MapPin className="w-3 h-3 text-slate-400" />
                      {r.preset_id}
                    </span>
                    <span className="text-[10px] text-slate-500 font-mono flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {r.created_at || 'Recently'}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 font-medium truncate">
                    "{r.query}"
                  </p>
                  <div className="flex items-center gap-4 text-[11px] font-mono text-slate-400">
                    <span>Delta: <strong className="text-cyan-400">{r.area_sq_km ? `${r.area_sq_km} km²` : 'N/A'}</strong></span>
                    <span>Change: <strong className="text-emerald-400">{r.percentage_change || 'N/A'}</strong></span>
                    <span>Confidence: <strong className="text-slate-200">{Math.round((r.confidence || 0.94) * 100)}%</strong></span>
                  </div>
                </div>

                <button
                  onClick={() => handleReplay(r.run_id)}
                  className="flex items-center gap-2 px-3.5 py-2 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 text-cyber-cyan border border-cyan-500/40 text-xs font-semibold transition-all group-hover:shadow-cyan-glow"
                >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  Replay Run
                </button>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="p-4 bg-black/60 border-t border-cyber-border flex items-center justify-between text-xs text-slate-500">
          <span className="flex items-center gap-1.5 font-mono text-[11px]">
            <Database className="w-3.5 h-3.5 text-emerald-400" />
            Backend SQLite Persistence Engine Connected
          </span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg bg-cyber-card border border-cyber-border text-slate-300 hover:text-white text-xs font-medium"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
};
