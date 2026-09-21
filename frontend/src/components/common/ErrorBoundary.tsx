import React, { Component, ErrorInfo, ReactNode } from 'react';
import { ShieldAlert, RefreshCw } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallbackTitle?: string;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught Studio Error:", error, errorInfo);
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="w-full h-full flex flex-col items-center justify-center bg-[#030712] p-8 text-center select-none font-sans">
          <div className="max-w-md bg-[#0B132B] border border-rose-500/50 rounded-2xl p-6 shadow-2xl space-y-4">
            <div className="flex justify-center">
              <div className="p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-400">
                <ShieldAlert className="w-8 h-8 animate-pulse" />
              </div>
            </div>
            
            <div className="space-y-1">
              <h3 className="text-base font-bold font-display text-slate-100 uppercase tracking-wider">
                {this.props.fallbackTitle || 'STUDIO RENDERING EXCEPTION'}
              </h3>
              <p className="text-xs text-slate-400 font-mono">
                An unexpected component rendering issue occurred. Studio state isolated.
              </p>
            </div>

            {this.state.error && (
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl font-mono text-[10px] text-rose-300 text-left overflow-x-auto max-h-24">
                {this.state.error.message || 'Render Exception'}
              </div>
            )}

            <button
              onClick={this.handleReset}
              className="w-full py-2.5 rounded-xl bg-cyan-500 text-black font-extrabold text-xs hover:bg-cyan-400 transition flex items-center justify-center gap-2 shadow-cyan-glow font-mono uppercase"
            >
              <RefreshCw className="w-4 h-4" />
              <span>RELOAD WORKSPACE</span>
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
