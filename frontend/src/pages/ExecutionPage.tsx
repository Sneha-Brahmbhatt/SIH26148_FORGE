import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { apiClient } from '../api/client';
import { Execution } from '../types';
import { Play, CheckCircle2, XCircle, Clock, Database, AlertTriangle, ShieldCheck, ArrowRight } from 'lucide-react';

export const ExecutionPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [execution, setExecution] = useState<Execution | null>(location.state?.executionResult || null);
  const [executionsList, setExecutionsList] = useState<any[]>([]);

  useEffect(() => {
    const fetchLatest = async () => {
      try {
        const list = await apiClient.getExecutions();
        setExecutionsList(list);
        if (!execution && list.length > 0) {
          const details = await apiClient.getExecutionDetails(list[0].execution_id);
          setExecution(details);
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchLatest();
  }, []);

  if (!execution) {
    return (
      <div className="p-8 text-center font-mono space-y-4">
        <Play className="w-12 h-12 text-cyan-400 mx-auto" />
        <h2 className="text-lg font-bold text-slate-200">No Execution Record Loaded</h2>
        <p className="text-xs text-slate-400">Run a script from the Script Editor or click Run SIH Demo.</p>
      </div>
    );
  }

  const isBlocked = execution.status === 'BLOCKED' || execution.policy_decision === 'BLOCKED';

  return (
    <div className="p-6 space-y-6 font-mono">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Play className="w-5 h-5 text-cyan-400" />
            <span>Governed Execution Runtime</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Execution ID: <code className="text-cyan-400 font-bold">{execution.execution_id}</code> | Case: {execution.case_id}
          </p>
        </div>

        {/* Status Badge */}
        <div className="flex items-center space-x-3">
          {isBlocked ? (
            <span className="bg-rose-950 border border-rose-700 text-rose-400 font-bold px-4 py-1.5 rounded text-xs flex items-center space-x-2">
              <XCircle className="w-4 h-4" />
              <span>EXECUTION BLOCKED BY POLICY</span>
            </span>
          ) : (
            <span className="bg-emerald-950 border border-emerald-700 text-emerald-400 font-bold px-4 py-1.5 rounded text-xs flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4" />
              <span>EXECUTION COMPLETED SUCCESSFULLY</span>
            </span>
          )}
        </div>
      </div>

      {/* Metadata Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg">
          <span className="text-[11px] text-slate-400">POLICY DECISION</span>
          <div className="text-lg font-bold text-slate-100 mt-1">
            {execution.policy_decision}
          </div>
          <span className="text-[10px] text-slate-500">standard-read-only-v1</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg">
          <span className="text-[11px] text-slate-400">DURATION</span>
          <div className="text-lg font-bold text-slate-100 mt-1">{execution.duration_ms} ms</div>
          <span className="text-[10px] text-slate-500">Sandboxed execution</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg">
          <span className="text-[11px] text-slate-400">EVIDENCE PRODUCED</span>
          <div className="text-lg font-bold text-emerald-400 mt-1">
            {execution.evidence?.length || 0} Records
          </div>
          <span className="text-[10px] text-slate-500">SHA-256 bound</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg">
          <span className="text-[11px] text-slate-400">FINDINGS GENERATED</span>
          <div className="text-lg font-bold text-amber-400 mt-1">
            {execution.findings?.length || 0} Leads
          </div>
          <span className="text-[10px] text-slate-500">Correlation engine</span>
        </div>
      </div>

      {/* Blocked Explanation Alert */}
      {isBlocked && (
        <div className="bg-rose-950/80 border border-rose-800 p-5 rounded-lg space-y-3">
          <div className="flex items-center space-x-2 text-rose-300 font-bold text-sm">
            <XCircle className="w-5 h-5 text-rose-400" />
            <span>POLICY ENFORCEMENT PREVENTED UNTRUSTED OPERATION</span>
          </div>
          <p className="text-xs text-rose-200">
            {execution.error || 'The requested script requested capabilities or operations that violate execution policy standard-read-only-v1. Execution was stopped prior to runtime.'}
          </p>
          <div className="text-[11px] text-rose-300 font-semibold">
            Audit Event Created: <code className="bg-rose-900/60 px-2 py-0.5 rounded text-rose-200">POLICY_DENIED</code>
          </div>
        </div>
      )}

      {/* Execution Results Sections */}
      {!isBlocked && (
        <div className="space-y-6">
          {/* Quick Navigation Shortcuts */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button
              onClick={() => navigate('/evidence')}
              className="bg-slate-900 hover:bg-slate-800 border border-slate-800 p-4 rounded-lg flex items-center justify-between text-left transition group"
            >
              <div>
                <span className="text-xs text-slate-400 flex items-center space-x-1.5">
                  <Database className="w-4 h-4 text-emerald-400" />
                  <span>Inspect Evidence & Hashes</span>
                </span>
                <p className="text-sm font-bold text-slate-200 mt-1">
                  {execution.evidence?.length || 0} Evidence Items
                </p>
              </div>
              <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-cyan-400 transition" />
            </button>

            <button
              onClick={() => navigate('/timeline')}
              className="bg-slate-900 hover:bg-slate-800 border border-slate-800 p-4 rounded-lg flex items-center justify-between text-left transition group"
            >
              <div>
                <span className="text-xs text-slate-400 flex items-center space-x-1.5">
                  <Clock className="w-4 h-4 text-cyan-400" />
                  <span>View Unified Timeline</span>
                </span>
                <p className="text-sm font-bold text-slate-200 mt-1">
                  {execution.timeline?.length || 0} Chronological Events
                </p>
              </div>
              <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-cyan-400 transition" />
            </button>

            <button
              onClick={() => navigate('/findings')}
              className="bg-slate-900 hover:bg-slate-800 border border-slate-800 p-4 rounded-lg flex items-center justify-between text-left transition group"
            >
              <div>
                <span className="text-xs text-slate-400 flex items-center space-x-1.5">
                  <AlertTriangle className="w-4 h-4 text-amber-400" />
                  <span>Investigate Findings</span>
                </span>
                <p className="text-sm font-bold text-slate-200 mt-1">
                  {execution.findings?.length || 0} Correlated Leads
                </p>
              </div>
              <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-cyan-400 transition" />
            </button>
          </div>

          {/* Provenance Details */}
          {execution.provenance && (
            <div className="bg-slate-900 border border-slate-800 rounded-lg p-5 space-y-3">
              <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
                <ShieldCheck className="w-4 h-4 text-purple-400" />
                <span>Cryptographic Provenance Record</span>
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                <div>
                  <span className="text-slate-500">PROVENANCE ID:</span>
                  <div className="text-cyan-400 font-bold">{execution.provenance.provenance_id}</div>
                </div>
                <div>
                  <span className="text-slate-500">ANALYST:</span>
                  <div className="text-slate-300">{execution.provenance.analyst_id}</div>
                </div>
                <div>
                  <span className="text-slate-500">SCRIPT SHA-256:</span>
                  <div className="text-cyan-300 truncate">{execution.provenance.script_sha256}</div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
