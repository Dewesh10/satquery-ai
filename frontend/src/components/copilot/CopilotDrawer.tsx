import React, { useState } from 'react';
import { Send, Cpu, CheckCircle2, Loader2, Sparkles, Terminal, Activity, ChevronLeft, ChevronRight } from 'lucide-react';
import { QueryPlan, PresetLocation } from '../../types';

interface CopilotDrawerProps {
  currentPreset: PresetLocation;
  onExecuteQuery: (prompt: string) => void;
  isProcessing: boolean;
  activePlan: QueryPlan | null;
  collapsed: boolean;
  onToggleCollapse: () => void;
}

export const CopilotDrawer: React.FC<CopilotDrawerProps> = ({
  currentPreset,
  onExecuteQuery,
  isProcessing,
  activePlan,
  collapsed,
  onToggleCollapse
}) => {
  const [promptInput, setPromptInput] = useState(currentPreset.suggested_prompt);

  React.useEffect(() => {
    setPromptInput(currentPreset.suggested_prompt);
  }, [currentPreset.suggested_prompt]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!promptInput.trim() || isProcessing) return;
    onExecuteQuery(promptInput);
  };

  if (collapsed) {
    return (
      <div className="w-12 h-full bg-[#0B132B]/90 border-r border-cyber-border flex flex-col items-center py-4 z-20 shrink-0 select-none font-sans">
        <button
          onClick={onToggleCollapse}
          className="p-2 rounded hover:bg-slate-800 text-cyber-cyan transition"
          title="Expand Copilot Panel"
        >
          <ChevronRight className="w-5 h-5" />
        </button>
        <div className="mt-8 text-[11px] font-display font-bold text-slate-400 rotate-90 whitespace-nowrap uppercase tracking-widest">
          QUERY COPILOT
        </div>
      </div>
    );
  }

  return (
    <div className="w-96 h-full bg-[#0B132B]/90 border-r border-cyber-border backdrop-blur-xl flex flex-col z-20 shrink-0 relative transition-all font-sans">
      {/* Collapse Button */}
      <button
        onClick={onToggleCollapse}
        className="absolute top-4 right-3 p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition"
        title="Collapse Panel"
      >
        <ChevronLeft className="w-4 h-4" />
      </button>

      {/* Drawer Header */}
      <div className="p-4 border-b border-cyber-border flex items-center gap-2">
        <Cpu className="w-5 h-5 text-cyber-cyan" />
        <span className="font-display font-bold text-sm text-slate-100 uppercase tracking-wider">
          QUERY PLANNER & COPILOT
        </span>
      </div>

      {/* Query Input & Suggested Prompts */}
      <div className="p-4 border-b border-cyber-border bg-[#030712]/50">
        <form onSubmit={handleSubmit} className="flex flex-col gap-2">
          <label className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            ASK SATELLITE COPILOT:
          </label>
          <div className="relative">
            <textarea
              rows={3}
              value={promptInput}
              onChange={(e) => setPromptInput(e.target.value)}
              placeholder="e.g. Show built-up growth between two dates..."
              className="w-full bg-[#0B132B] border border-cyber-border rounded-xl p-3 text-xs font-sans text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyber-cyan focus:ring-1 focus:ring-cyber-cyan resize-none shadow-inner"
            />
            <button
              type="submit"
              disabled={isProcessing || !promptInput.trim()}
              className="absolute bottom-2.5 right-2.5 px-3 py-1.5 bg-cyber-cyan text-black font-sans text-xs font-bold rounded-lg flex items-center gap-1.5 hover:bg-cyan-300 disabled:opacity-50 transition shadow-cyan-glow"
            >
              {isProcessing ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Send className="w-3.5 h-3.5" />}
              <span>RUN</span>
            </button>
          </div>
        </form>

        {/* Quick Suggestion Chips & Refusal Demo Trigger */}
        <div className="mt-3 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono text-slate-400 uppercase font-bold">Preset Benchmark Query:</span>
            <button
              onClick={() => {
                const prompt = "Show vegetation change during heavy cloud cover refusal scenario in Assam";
                setPromptInput(prompt);
                onExecuteQuery(prompt);
              }}
              className="text-[10px] font-mono font-bold text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/30 hover:bg-rose-500/20 transition flex items-center gap-1"
              title="Test Zero-Hallucination Model Refusal Feature"
            >
              <span>☁️ TEST CLOUD REFUSAL</span>
            </button>
          </div>
          <button
            onClick={() => {
              setPromptInput(currentPreset.suggested_prompt);
              onExecuteQuery(currentPreset.suggested_prompt);
            }}
            className="w-full text-left p-2.5 rounded-lg bg-[#0F172A] border border-slate-700 text-xs font-sans text-cyber-cyan hover:border-cyan-400 transition line-clamp-2"
          >
            "{currentPreset.suggested_prompt}"
          </button>
        </div>
      </div>

      {/* AI Transparency execution trace DAG */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-xs font-display font-bold text-slate-200 flex items-center gap-1.5">
            <Activity className="w-4 h-4 text-cyber-cyan" />
            EXECUTION DAG TRACE
          </span>
          {activePlan && (
            <span className="text-[10px] font-mono text-slate-400">
              {activePlan.execution_time_ms}ms
            </span>
          )}
        </div>

        {isProcessing && (
          <div className="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyber-cyan text-xs font-sans flex items-center gap-3 animate-pulse">
            <Loader2 className="w-5 h-5 animate-spin" />
            <div>
              <div className="font-bold">COMPILING GEOSPATIAL DAG...</div>
              <div className="text-[10px] text-slate-400">Fetching STAC scenes & running CV pipelines</div>
            </div>
          </div>
        )}

        {activePlan ? (
          <div className="space-y-2.5">
            {activePlan.dag_steps.map((step) => (
              <div
                key={step.step_id}
                className="p-3 rounded-xl bg-[#0F172A]/70 border border-cyber-border text-xs font-sans space-y-1"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    <span className="font-semibold text-slate-200">{step.name}</span>
                  </div>
                  <span className="text-[10px] font-mono text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/30">
                    #{step.step_id}
                  </span>
                </div>
                <div className="text-[11px] text-slate-400 font-sans">
                  Tool: <span className="text-slate-300 font-mono">{step.tool}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-6 text-center text-xs font-sans text-slate-500 border border-dashed border-slate-800 rounded-xl">
            <Terminal className="w-6 h-6 mx-auto mb-2 opacity-40 text-cyber-cyan" />
            Enter a prompt above to compile natural language into structured geospatial operations.
          </div>
        )}
      </div>
    </div>
  );
};
