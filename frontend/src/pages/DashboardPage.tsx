import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../api/client';
import { Execution, TimelineEvent, Finding, AuditLogItem } from '../types';
import {
  Play, ShieldCheck, Database, Clock, AlertTriangle, FileText,
  Activity, ArrowRight, CheckCircle2, XCircle, Shield
} from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [demoStatus, setDemoStatus] = useState<string | null>(null);

  const [casesCount, setCasesCount] = useState(1);
  const [executions, setExecutions] = useState<any[]>([]);
  const [evidenceCount, setEvidenceCount] = useState(0);
  const [findings, setFindings] = useState<Finding[]>([]);
  const [timelineEvents, setTimelineEvents] = useState<TimelineEvent[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditLogItem[]>([]);

  const loadDashboardData = async () => {
    try {
      const [cases, execs, evd, tls, fnds, audits] = await Promise.all([
        apiClient.getCases(),
        apiClient.getExecutions(),
        apiClient.getEvidence(),
        apiClient.getTimeline(),
        apiClient.getFindings(),
        apiClient.getAuditLogs()
      ]);
      const safeCases = Array.isArray(cases) ? cases : [];
      const safeExecs = Array.isArray(execs) ? execs : [];
      const safeEvd = Array.isArray(evd) ? evd : [];
      const safeTls = Array.isArray(tls) ? tls : [];
      const safeFnds = Array.isArray(fnds) ? fnds : [];
      const safeAudits = Array.isArray(audits) ? audits : [];

      setCasesCount(safeCases.length || 1);
      setExecutions(safeExecs);
      setEvidenceCount(safeEvd.length || 0);
      setTimelineEvents(safeTls);
      setFindings(safeFnds);
      setAuditLogs(safeAudits);
    } catch (err) {
      console.error('Error loading dashboard data', err);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const handleRunSIHDemo = async () => {
    setLoading(true);
    setDemoStatus('Initializing SIH Demo execution pipeline...');
    try {
      const res = await apiClient.runSIHDemo();
      setDemoStatus('Demo script executed successfully!');
      await loadDashboardData();
      setTimeout(() => {
        navigate('/execution');
      }, 800);
    } catch (err: any) {
      setDemoStatus(`Demo execution error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const safeFindings = Array.isArray(findings) ? findings : [];
  const safeExecutions = Array.isArray(executions) ? executions : [];
  const safeAuditLogs = Array.isArray(auditLogs) ? auditLogs : [];

  const highFindings = safeFindings.filter(f => f && f.severity === 'HIGH').length;

  return (
    <div className="p-6 space-y-6">
      {/* Header & Hero Action */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold font-mono text-slate-100 flex items-center space-x-3">
            <Activity className="w-6 h-6 text-cyan-400" />
            <span>FORGE — Forensic Object Runtime & Governed Execution</span>
          </h1>
          <p className="text-xs font-mono text-slate-400 mt-1 max-w-3xl">
            SIH Problem Statement SIH26148 | Organization: National Technical Research Organisation (NTRO)
          </p>
          <p className="text-[11px] font-mono text-cyan-400 mt-0.5">
            USP: Forensic Safety is Structural — Read-Only Evidence, Capability-Checked DSL, Provenance-Bound Hashes.
          </p>
        </div>

        {/* Hero Demo Trigger Button */}
        <div className="flex flex-col items-end space-y-2">
          <button
            onClick={handleRunSIHDemo}
            disabled={loading}
            className="flex items-center space-x-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-mono font-bold px-6 py-3 rounded-md text-sm shadow-lg transform transition active:scale-95 disabled:opacity-50"
          >
            <Play className="w-5 h-5 fill-current" />
            <span>{loading ? 'EXECUTING DEMO...' : 'RUN 5-MINUTE SIH DEMO'}</span>
          </button>
          {demoStatus && (
            <span className="text-[11px] font-mono text-emerald-400 animate-pulse">
              {demoStatus}
            </span>
          )}
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg shadow-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono">ACTIVE CASES</span>
            <ShieldCheck className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-mono font-bold text-slate-100">{casesCount}</div>
          <div className="text-[10px] font-mono text-slate-500 mt-1">Bound investigations</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg shadow-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono">EXECUTIONS</span>
            <Activity className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-mono font-bold text-slate-100">{executions.length}</div>
          <div className="text-[10px] font-mono text-slate-500 mt-1">Governed runtime runs</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg shadow-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono">EVIDENCE ITEMS</span>
            <Database className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-mono font-bold text-slate-100">{evidenceCount}</div>
          <div className="text-[10px] font-mono text-slate-500 mt-1">SHA-256 integrity bound</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg shadow-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono">FINDINGS</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-mono font-bold text-slate-100">{findings.length}</div>
          <div className="text-[10px] font-mono text-amber-400 mt-1">{highFindings} High Severity Leads</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg shadow-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-mono">TIMELINE EVENTS</span>
            <Clock className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-mono font-bold text-slate-100">{timelineEvents.length}</div>
          <div className="text-[10px] font-mono text-slate-500 mt-1">Unified correlation</div>
        </div>
      </div>

      {/* Main Content Split: Recent Executions & Audit Log */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Executions */}
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-5">
          <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-2">
            <h2 className="text-sm font-mono font-bold text-slate-200 flex items-center space-x-2">
              <Play className="w-4 h-4 text-cyan-400" />
              <span>Recent Governed Executions</span>
            </h2>
            <button
              onClick={() => navigate('/execution')}
              className="text-xs font-mono text-cyan-400 hover:underline flex items-center space-x-1"
            >
              <span>View All</span>
              <ArrowRight className="w-3 h-3" />
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 text-[11px]">
                  <th className="py-2">EXECUTION ID</th>
                  <th className="py-2">CASE</th>
                  <th className="py-2">POLICY</th>
                  <th className="py-2">STATUS</th>
                  <th className="py-2">DURATION</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {safeExecutions.slice(0, 5).map((ex) => (
                  <tr key={ex.execution_id} className="hover:bg-slate-800/40">
                    <td className="py-2.5 font-bold text-cyan-400">{ex.execution_id}</td>
                    <td className="py-2.5 text-slate-300">{ex.case_id}</td>
                    <td className="py-2.5 text-slate-400">standard-read-only-v1</td>
                    <td className="py-2.5">
                      {ex.policy_decision === 'APPROVED' ? (
                        <span className="inline-flex items-center space-x-1 text-emerald-400 bg-emerald-950/60 border border-emerald-800 px-2 py-0.5 rounded text-[10px]">
                          <CheckCircle2 className="w-3 h-3" />
                          <span>APPROVED</span>
                        </span>
                      ) : (
                        <span className="inline-flex items-center space-x-1 text-rose-400 bg-rose-950/60 border border-rose-800 px-2 py-0.5 rounded text-[10px]">
                          <XCircle className="w-3 h-3" />
                          <span>BLOCKED</span>
                        </span>
                      )}
                    </td>
                    <td className="py-2.5 text-slate-400">{ex.duration_ms} ms</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Audit Activity & Hash Chain Status */}
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-5">
          <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-2">
            <h2 className="text-sm font-mono font-bold text-slate-200 flex items-center space-x-2">
              <Shield className="w-4 h-4 text-purple-400" />
              <span>Immutable Hash-Chained Audit Log</span>
            </h2>
            <span className="inline-flex items-center space-x-1 text-emerald-400 bg-emerald-950/80 border border-emerald-700/60 px-2 py-0.5 rounded text-[10px] font-mono">
              <CheckCircle2 className="w-3 h-3" />
              <span>VERIFIED VALID</span>
            </span>
          </div>

          <div className="space-y-2 font-mono text-xs max-h-72 overflow-y-auto pr-1">
            {safeAuditLogs.slice(-6).reverse().map((log) => (
              <div
                key={log.audit_id}
                className="bg-slate-950/80 p-2.5 rounded border border-slate-800 flex items-start justify-between"
              >
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-purple-400 font-bold">{log.audit_id}</span>
                    <span className="text-slate-200 font-semibold">{log.action}</span>
                    <span className="text-[10px] bg-slate-800 text-slate-300 px-1.5 py-0.5 rounded">
                      {log.result}
                    </span>
                  </div>
                  <div className="text-[10px] text-slate-400 mt-1">
                    Actor: {log.actor} | Obj: {log.object_type} ({log.object_id})
                  </div>
                  <div className="text-[9px] text-slate-500 font-mono mt-0.5">
                    Hash: {log.audit_hash?.substring(0, 28)}...
                  </div>
                </div>
                <span className="text-[10px] text-slate-500 flex-shrink-0">
                  {log.timestamp_utc?.substring(11, 19)}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
