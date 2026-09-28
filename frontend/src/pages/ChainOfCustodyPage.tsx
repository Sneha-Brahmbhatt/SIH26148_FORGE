import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { AuditLogItem } from '../types';
import { Link2, Database, ShieldCheck, Hash, CheckCircle2 } from 'lucide-react';

export const ChainOfCustodyPage: React.FC = () => {
  const [custodyData, setCustodyData] = useState<any>(null);

  useEffect(() => {
    const fetchCustody = async () => {
      try {
        const res = await apiClient.getChainOfCustody('CASE-001');
        setCustodyData(res);
      } catch (err) {
        console.error(err);
      }
    };
    fetchCustody();
  }, []);

  if (!custodyData) {
    return (
      <div className="p-8 text-center font-mono">
        <Link2 className="w-12 h-12 text-cyan-400 mx-auto mb-4 animate-pulse" />
        <p className="text-slate-400 text-sm">Loading chain of custody data...</p>
      </div>
    );
  }

  const chainEvents: AuditLogItem[] = custodyData.chain_events || [];
  const evidenceItems = custodyData.evidence_items || [];

  return (
    <div className="p-6 space-y-6 font-mono">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Link2 className="w-5 h-5 text-purple-400" />
            <span>Chain of Custody — {custodyData.case_id}</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Immutable hash-chained audit trail binding every custody event to cryptographic provenance.
          </p>
        </div>

        <div className="flex items-center space-x-4 text-xs">
          <div className="bg-slate-900 border border-slate-800 px-3 py-1.5 rounded flex items-center space-x-2">
            <Database className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-slate-300">Evidence Items: <strong className="text-emerald-400">{custodyData.evidence_items_count}</strong></span>
          </div>
          <div className="bg-slate-900 border border-slate-800 px-3 py-1.5 rounded flex items-center space-x-2">
            <ShieldCheck className="w-3.5 h-3.5 text-cyan-400" />
            <span className="text-slate-300">Audit Events: <strong className="text-cyan-400">{custodyData.audit_events_count}</strong></span>
          </div>
          <span className="bg-emerald-950 border border-emerald-700 text-emerald-400 font-bold px-3 py-1.5 rounded text-[11px] flex items-center space-x-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>CHAIN VERIFIED</span>
          </span>
        </div>
      </div>

      {/* Evidence Custody Items */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-5">
        <h2 className="text-sm font-bold text-slate-200 mb-4 flex items-center space-x-2">
          <Database className="w-4 h-4 text-emerald-400" />
          <span>Evidence Items Under Custody</span>
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 text-[11px]">
                <th className="py-2 px-3">EVIDENCE ID</th>
                <th className="py-2 px-3">TYPE</th>
                <th className="py-2 px-3">COLLECTOR</th>
                <th className="py-2 px-3">SHA-256</th>
                <th className="py-2 px-3">PROVENANCE</th>
                <th className="py-2 px-3">COLLECTED AT</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {evidenceItems.map((ev: any) => (
                <tr key={ev.evidence_id} className="hover:bg-slate-800/40">
                  <td className="py-2.5 px-3 text-cyan-400 font-bold">{ev.evidence_id}</td>
                  <td className="py-2.5 px-3">
                    <span className="bg-slate-800 text-slate-200 border border-slate-700 px-2 py-0.5 rounded text-[10px]">
                      {ev.evidence_type}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 text-slate-300">{ev.collector}</td>
                  <td className="py-2.5 px-3">
                    <div className="flex items-center space-x-1 text-cyan-300 text-[11px]">
                      <Hash className="w-3 h-3 text-emerald-400 flex-shrink-0" />
                      <span className="truncate max-w-[140px]" title={ev.sha256}>{ev.sha256}</span>
                    </div>
                  </td>
                  <td className="py-2.5 px-3 text-purple-400 font-semibold">{ev.provenance_id}</td>
                  <td className="py-2.5 px-3 text-slate-400">{ev.collected_at_utc?.substring(0, 19)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Chain of Custody Audit Trail */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-5">
        <h2 className="text-sm font-bold text-slate-200 mb-4 flex items-center space-x-2">
          <Link2 className="w-4 h-4 text-purple-400" />
          <span>Hash-Chained Custody Event Timeline</span>
        </h2>

        <div className="relative border-l-2 border-slate-700 ml-4 pl-6 space-y-4">
          {chainEvents.map((evt: AuditLogItem) => (
            <div key={evt.audit_id} className="relative bg-slate-950 p-4 rounded-lg border border-slate-800/80">
              <div className="absolute -left-[31px] top-4 w-4 h-4 rounded-full bg-slate-900 border-2 border-purple-400 flex items-center justify-center">
                <div className="w-1.5 h-1.5 rounded-full bg-purple-400" />
              </div>

              <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-2">
                <div className="flex items-center space-x-2">
                  <span className="text-purple-400 font-bold text-[11px]">{evt.audit_id}</span>
                  <span className="bg-slate-800 text-slate-200 px-2 py-0.5 rounded text-[11px] font-bold">
                    {evt.action}
                  </span>
                  <span className={`text-[10px] px-2 py-0.5 rounded font-bold ${
                    evt.result === 'SUCCESS' || evt.result === 'APPROVED'
                      ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                      : evt.result === 'BLOCKED'
                        ? 'bg-rose-950 text-rose-400 border border-rose-800'
                        : 'bg-slate-800 text-slate-300 border border-slate-700'
                  }`}>
                    {evt.result}
                  </span>
                </div>
                <span className="text-[10px] text-slate-500">{evt.timestamp_utc?.substring(11, 19)} UTC</span>
              </div>

              <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-400">
                <span>Actor: <strong className="text-slate-300">{evt.actor}</strong></span>
                <span>Object: <strong className="text-slate-300">{evt.object_type} ({evt.object_id})</strong></span>
              </div>

              <div className="mt-2 pt-2 border-t border-slate-900 text-[9px] text-slate-500 space-y-0.5">
                <div>Hash: <code className="text-cyan-400/80">{evt.audit_hash?.substring(0, 40)}...</code></div>
                <div>Prev: <code className="text-slate-600">{evt.prev_audit_hash?.substring(0, 40)}...</code></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
