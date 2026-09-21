import React, { useState } from 'react';
import { Send, Cpu, CheckCircle2, Loader2, Sparkles, Terminal, Activity, ChevronLeft, ChevronRight, Mic, MicOff, Volume2, VolumeX } from 'lucide-react';
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
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  React.useEffect(() => {
    setPromptInput(currentPreset.suggested_prompt);
  }, [currentPreset.suggested_prompt]);

  const toggleVoiceInput = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Web Speech Recognition API is not supported in this browser.");
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = () => setIsListening(false);

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setPromptInput(transcript);
    };

    recognition.start();
  };

  const toggleSpeechSynthesis = (textToSpeak: string) => {
    if (!('speechSynthesis' in window)) {
      alert("Text-to-speech API is not supported in this browser.");
      return;
    }

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.rate = 1.0;
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    setIsSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

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
      <div className="p-4 border-b border-cyber-border flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Cpu className="w-5 h-5 text-cyber-cyan" />
          <span className="font-display font-bold text-sm text-slate-100 uppercase tracking-wider">
            QUERY PLANNER & VOICE COPILOT
          </span>
        </div>

        {/* Read Aloud Toggle */}
        <button
          onClick={() => toggleSpeechSynthesis("SatQuery AI autonomous satellite copilot ready for queries.")}
          className={`p-1.5 rounded transition ${isSpeaking ? 'bg-rose-500/20 text-rose-400' : 'text-slate-400 hover:text-white'}`}
          title="Read Aloud Voice Assistant"
        >
          {isSpeaking ? <VolumeX className="w-4 h-4 animate-pulse" /> : <Volume2 className="w-4 h-4" />}
        </button>
      </div>

      {/* Query Input & Suggested Prompts */}
      <div className="p-4 border-b border-cyber-border bg-[#030712]/50">
        <form onSubmit={handleSubmit} className="flex flex-col gap-2">
          <div className="flex items-center justify-between">
            <label className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              ASK SATELLITE COPILOT:
            </label>

            {/* Voice Input Button */}
            <button
              type="button"
              onClick={toggleVoiceInput}
              className={`p-1.5 rounded-lg border text-xs font-mono font-bold flex items-center gap-1 transition ${
                isListening
                  ? 'bg-rose-500/20 border-rose-500/50 text-rose-400 animate-pulse'
                  : 'bg-slate-900 border-slate-700 text-slate-300 hover:text-white'
              }`}
              title="Speak Query via Microphone"
            >
              {isListening ? <MicOff className="w-3.5 h-3.5 text-rose-400" /> : <Mic className="w-3.5 h-3.5 text-cyber-cyan" />}
              <span>{isListening ? 'LISTENING...' : 'VOICE'}</span>
            </button>
          </div>

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

        {/* Quick Suggestion Chips */}
        <div className="mt-3 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono text-slate-400 uppercase font-bold">Preset Benchmark Query:</span>
          </div>

          <button
            onClick={() => setPromptInput(currentPreset.suggested_prompt)}
            className="w-full text-left p-2.5 rounded-xl bg-[#0B132B] border border-cyber-border/60 hover:border-cyber-cyan/60 text-slate-300 text-xs font-mono transition line-clamp-2"
          >
            "{currentPreset.suggested_prompt}"
          </button>
        </div>
      </div>

      {/* Query Execution Plan DAG View */}
      <div className="flex-1 p-4 overflow-y-auto space-y-4 font-mono text-xs">
        {activePlan ? (
          <div className="space-y-3">
            <div className="flex items-center justify-between text-[11px] text-slate-400 border-b border-slate-800 pb-2">
              <span className="flex items-center gap-1.5">
                <Terminal className="w-3.5 h-3.5 text-cyber-cyan" />
                EXECUTION DAG PLAN
              </span>
              <span className="text-emerald-400 font-bold">{activePlan.intent}</span>
            </div>

            <div className="space-y-2">
              {activePlan.dag_steps.map((step, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-xl bg-[#030712] border border-slate-800 flex items-start gap-2.5 transition hover:border-cyber-cyan/40"
                >
                  <CheckCircle2 className="w-4 h-4 text-cyber-cyan shrink-0 mt-0.5" />
                  <div className="space-y-0.5">
                    <div className="font-bold text-slate-200">{step.name}</div>
                    <div className="text-[11px] text-slate-400">Tool: {step.tool} • Status: {step.status}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-500 space-y-2">
            <Activity className="w-8 h-8 text-slate-600 animate-pulse" />
            <div className="text-xs font-bold text-slate-400 uppercase">NO ACTIVE DAG PLAN</div>
            <p className="text-[11px] max-w-xs text-slate-500 font-sans">
              Enter a prompt above or use voice input to generate a multi-step satellite processing plan.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
