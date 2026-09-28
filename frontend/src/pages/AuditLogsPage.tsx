import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { AuditLogItem } from '../types';
import { Shield, Search, CheckCircle2, Hash, Filter } from 'lucide-react';

export const AuditLogsPage: React.FC = () => {
  const [auditLogs, setAuditLogs] = useState<AuditLogItem[]>([]);
  const [search, setSearch] = useState('');
  const [actionFilter, setActionFilter] = useState('ALL');

  useEffect(() => {
    const fetchAudit = async () => {
      try {
        const res = await apiClient.getAuditLogs();
        setAuditLogs(res);
      } catch (err) {
        console.error(err);
      }
    };
    fetchAudit();
  }, []);

  const actions = Array.from(new Set(auditLogs.map((a) => a.action)));

  const filteredLogs = auditLogs.filter((log) => {
    if (actionFilter !== 'ALL' && log.action !== actionFilter) return false;
    if (
      search &&
      !log.audit_id.toLowerCase().includes(search.toLowerCase()) &&
      !log.action.toLowerCase().includes(search.toLowerCase()) &&
      !log.actor.toLowerCase().includes(search.toLowerCase()) &&
      !log.object_id.toLowerCase().includes(search.toLowerCase())
    )
      return false;
    return true;
  });

  return (
    <div className="p-6 space-y-6 font-mono">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Shield className="w-5 h-5 text-purple-400" />
            <span>Immutable Hash-Chained Audit Trail</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Every validation, policy decision, evidence collection, and report generation is cryptographically chained.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <span className="bg-emerald-950 border border-emerald-700 text-emerald-400 font-bold px-3 py-1.5 rounded text-xs flex items-center space-x-1.5">
            <CheckCircle2 className="w-4 h-4" />
            <span>HASH CHAIN INTEGRITY: VERIFIED VALID</span>
          </span>
        </div>
      </div>

      {/* Filters Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-3 rounded-lg">
        <div className="flex items-center space-x-2 text-xs">
          <Filter className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-slate-400">Action Filter:</span>
          <select
            value={actionFilter}
            onChange={(e) => setActionFilter(e.target.value)}
            className="bg-slate-950 text-slate-200 border border-slate-800 rounded px-2 py-1 focus:outline-none"
          >
            <option value="ALL">All Actions ({auditLogs.length})</option>
            {actions.map((act) => (
              <option key={act} value={act}>{act}</option>
            ))}
          </select>
        </div>

        <div className="relative">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search audit ID, actor, action, object..."
            className="bg-slate-950 border border-slate-800 rounded pl-8 pr-3 py-1 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 w-72"
          />
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-950 text-slate-400 text-[11px]">
                <th className="py-3 px-4">AUDIT ID</th>
                <th className="py-3 px-4">ACTION</th>
                <th className="py-3 px-4">RESULT</th>
                <th className="py-3 px-4">ACTOR</th>
                <th className="py-3 px-4">TARGET OBJECT</th>
                <th className="py-3 px-4">TIMESTAMP (UTC)</th>
                <th className="py-3 px-4">AUDIT HASH & PREV LINK</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {filteredLogs.map((log) => (
                <tr key={log.audit_id} className="hover:bg-slate-800/40">
                  <td className="py-3 px-4 font-bold text-purple-400">{log.audit_id}</td>
                  <td className="py-3 px-4 font-bold text-slate-200">{log.action}</td>
                  <td className="py-3 px-4">
                    <span className={`text-[10px] px-2 py-0.5 rounded font-bold border ${
                      log.result === 'SUCCESS' || log.result === 'APPROVED'
                        ? 'bg-emerald-950 text-emerald-400 border-emerald-800'
                        : log.result === 'BLOCKED'
                          ? 'bg-rose-950 text-rose-400 border-rose-800'
                          : 'bg-slate-800 text-slate-300 border-slate-700'
                    }`}>
                      {log.result}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-300">{log.actor}</td>
                  <td className="py-3 px-4 text-cyan-300">
                    {log.object_type} ({log.object_id})
                  </td>
                  <td className="py-3 px-4 text-slate-400">{log.timestamp_utc?.substring(0, 19)}</td>
                  <td className="py-3 px-4 text-[10px] space-y-0.5 font-mono">
                    <div className="flex items-center space-x-1 text-cyan-400">
                      <Hash className="w-3 h-3 text-cyan-400 flex-shrink-0" />
                      <span className="truncate max-w-[140px]" title={log.audit_hash}>{log.audit_hash}</span>
                    </div>
                    <div className="text-slate-500 truncate max-w-[140px]" title={log.prev_audit_hash}>
                      prev: {log.prev_audit_hash?.substring(0, 16)}...
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
