import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('FORGE UI Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center p-6 font-mono">
          <div className="max-w-lg w-full bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-4 shadow-2xl">
            <div className="flex items-center space-x-3 border-b border-slate-800 pb-3">
              <AlertTriangle className="w-6 h-6 text-amber-400 flex-shrink-0" />
              <h1 className="text-base font-bold text-slate-100">FORGE UI Error Boundary Triggered</h1>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              An unexpected render error occurred in the component tree.
            </p>
            {this.state.error && (
              <pre className="bg-slate-950 p-3 rounded border border-slate-800 text-[11px] text-rose-300 overflow-x-auto whitespace-pre-wrap">
                {this.state.error.toString()}
              </pre>
            )}
            <div className="pt-2 flex justify-end">
              <button
                onClick={() => window.location.reload()}
                className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-4 py-2 rounded text-xs flex items-center space-x-2 transition"
              >
                <RefreshCw className="w-4 h-4" />
                <span>Reload Application</span>
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
