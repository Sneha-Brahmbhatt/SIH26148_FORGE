import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ScriptValidationResponse } from '../types';
import {
  CheckCircle2, XCircle, ShieldCheck, FileCode, Layers, ListChecks, Play, AlertOctagon
} from 'lucide-react';

export const ValidationPipelinePage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'policy' | 'semantic' | 'ast' | 'tokens'>('policy');

  const validationResult: ScriptValidationResponse | null = location.state?.validationResult || null;

  if (!validationResult) {
    return (
      <div className="p-8 text-center space-y-4">
        <AlertOctagon className="w-12 h-12 text-amber-400 mx-auto" />
        <h2 className="text-lg font-mono font-bold text-slate-200">No Validation Result Available</h2>
        <p className="text-xs font-mono text-slate-400">Please validate a script in the Script Editor first.</p>
        <button
          onClick={() => navigate('/editor')}
          className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-mono font-bold px-4 py-2 rounded text-xs"
        >
          Go to Script Editor
        </button>
      </div>
    );
  }

  const { policy, semantic, parser, lexer, valid, script_sha256 } = validationResult;

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold font-mono text-slate-100 flex items-center space-x-2">
            <ShieldCheck className="w-5 h-5 text-cyan-400" />
            <span>FORGE Validation Pipeline & Policy Engine</span>
          </h1>
          <p className="text-xs font-mono text-slate-400 mt-1">
            Lexer → Parser → AST → Semantic Validation → Capability Policy Decision
          </p>
        </div>

        {/* Status Badge & Actions */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 font-mono text-xs">
            <span className="text-slate-400">Policy Decision:</span>
            {policy.decision === 'APPROVED' ? (
              <span className="bg-emerald-950 border border-emerald-700 text-emerald-400 font-bold px-3 py-1 rounded flex items-center space-x-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>APPROVED</span>
              </span>
            ) : (
              <span className="bg-rose-950 border border-rose-700 text-rose-400 font-bold px-3 py-1 rounded flex items-center space-x-1.5">
                <XCircle className="w-4 h-4" />
                <span>BLOCKED</span>
              </span>
            )}
          </div>

          {policy.decision === 'APPROVED' && (
            <button
              onClick={() => navigate('/editor')}
              className="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-mono font-bold px-4 py-2 rounded text-xs flex items-center space-x-1"
            >
              <Play className="w-4 h-4 fill-current" />
              <span>Ready for Execution</span>
            </button>
          )}
        </div>
      </div>

      {/* Script SHA-256 Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-3 px-4 flex items-center justify-between font-mono text-xs">
        <div className="flex items-center space-x-2 text-slate-300">
          <FileCode className="w-4 h-4 text-cyan-400" />
          <span>SCRIPT SHA-256:</span>
          <code className="text-cyan-300 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">{script_sha256}</code>
        </div>
        <div className="text-[11px] text-slate-500">
          Tokens: {lexer.token_count} | Policy: standard-read-only-v1
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 space-x-4">
        {[
          { key: 'policy', label: 'Capability & Policy Checks', icon: ShieldCheck },
          { key: 'semantic', label: `Semantic Diagnostics (${semantic.errors.length})`, icon: ListChecks },
          { key: 'ast', label: 'Abstract Syntax Tree (AST)', icon: Layers },
          { key: 'tokens', label: `Lexer Tokens (${lexer.token_count})`, icon: FileCode },
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as any)}
              className={`flex items-center space-x-2 pb-3 font-mono text-xs transition border-b-2 ${
                activeTab === tab.key
                  ? 'border-cyan-400 text-cyan-400 font-bold'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab Content */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-5">
        {activeTab === 'policy' && (
          <div className="space-y-6">
            {/* Policy Decision Summary */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-slate-950 p-4 rounded border border-slate-800">
                <h3 className="text-xs font-mono font-bold text-slate-300 mb-2">Declared Capabilities</h3>
                <div className="flex flex-wrap gap-1.5">
                  {policy.required_capabilities.map((cap) => (
                    <span key={cap} className="bg-slate-800 text-cyan-400 border border-slate-700 text-[11px] font-mono px-2 py-0.5 rounded">
                      {cap}
                    </span>
                  ))}
                  {policy.required_capabilities.length === 0 && (
                    <span className="text-xs text-slate-500 font-mono">None declared</span>
                  )}
                </div>
              </div>

              <div className="bg-slate-950 p-4 rounded border border-slate-800">
                <h3 className="text-xs font-mono font-bold text-slate-300 mb-2">Prohibited / Denied Capabilities</h3>
                <div className="flex flex-wrap gap-1.5">
                  {policy.denied_capabilities.map((cap) => (
                    <span key={cap} className="bg-rose-950 text-rose-400 border border-rose-800 text-[11px] font-mono px-2 py-0.5 rounded font-bold">
                      ✗ {cap}
                    </span>
                  ))}
                  {policy.denied_capabilities.length === 0 && (
                    <span className="text-xs text-emerald-400 font-mono">✓ Zero prohibited capabilities requested</span>
                  )}
                </div>
              </div>
            </div>

            {/* Blocked Violations if any */}
            {policy.violations && policy.violations.length > 0 && (
              <div className="bg-rose-950/60 border border-rose-800/80 p-4 rounded-lg space-y-2">
                <h3 className="text-xs font-mono font-bold text-rose-300 flex items-center space-x-2">
                  <XCircle className="w-4 h-4 text-rose-400" />
                  <span>POLICY BLOCKED REASONS</span>
                </h3>
                <ul className="list-disc list-inside text-xs font-mono text-rose-200 space-y-1">
                  {policy.violations.map((v, i) => (
                    <li key={i}>{v}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Command-by-Command Checks Table */}
            <div>
              <h3 className="text-xs font-mono font-bold text-slate-300 mb-3">Command-by-Command Capability Evaluation</h3>
              <table className="w-full text-left text-xs font-mono">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400">
                    <th className="py-2">COMMAND</th>
                    <th className="py-2">REQUIRED CAPABILITY</th>
                    <th className="py-2">STATUS</th>
                    <th className="py-2">EVALUATION REASON</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {policy.command_checks.map((chk, idx) => (
                    <tr key={idx} className="hover:bg-slate-800/40">
                      <td className="py-2 text-cyan-400 font-bold">{chk.command}</td>
                      <td className="py-2 text-slate-300">{chk.required_capability}</td>
                      <td className="py-2">
                        {chk.status === 'GRANTED' ? (
                          <span className="text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded text-[10px]">GRANTED</span>
                        ) : (
                          <span className="text-rose-400 bg-rose-950 px-2 py-0.5 rounded text-[10px] font-bold">DENIED</span>
                        )}
                      </td>
                      <td className="py-2 text-slate-400">{chk.reason}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'semantic' && (
          <div className="space-y-4 font-mono text-xs">
            {semantic.errors.length === 0 ? (
              <div className="p-4 bg-emerald-950/40 border border-emerald-800 rounded text-emerald-400 flex items-center space-x-2">
                <CheckCircle2 className="w-5 h-5" />
                <span>Zero semantic errors detected. AST is semantically valid.</span>
              </div>
            ) : (
              semantic.errors.map((err, idx) => (
                <div key={idx} className="p-3 bg-rose-950/40 border border-rose-800 rounded text-rose-300 space-y-1">
                  <div className="font-bold flex items-center space-x-2">
                    <XCircle className="w-4 h-4 text-rose-400" />
                    <span>[{err.code}] Line {err.line}, Col {err.column}</span>
                  </div>
                  <p className="text-slate-300">{err.message}</p>
                </div>
              ))
            )}
          </div>
        )}

        {activeTab === 'ast' && (
          <pre className="bg-slate-950 p-4 rounded border border-slate-800 text-cyan-300 font-mono text-xs overflow-x-auto max-h-96">
            {JSON.stringify(parser.ast, null, 2)}
          </pre>
        )}

        {activeTab === 'tokens' && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400">
                  <th className="py-2">TOKEN TYPE</th>
                  <th className="py-2">VALUE</th>
                  <th className="py-2">POSITION</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {lexer.tokens.map((tok: any, idx: number) => (
                  <tr key={idx} className="hover:bg-slate-800/40">
                    <td className="py-2 text-purple-400 font-bold">{tok.type}</td>
                    <td className="py-2 text-cyan-300"><code>{JSON.stringify(tok.value)}</code></td>
                    <td className="py-2 text-slate-500">L{tok.line}:C{tok.column}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
