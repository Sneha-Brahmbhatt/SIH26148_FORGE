import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { EvidenceItem } from '../types';
import { Database, Hash, ShieldCheck, CheckCircle2 } from 'lucide-react';

export const EvidencePage: React.FC = () => {
  const [evidence, setEvidence] = useState<EvidenceItem[]>([]);
  const [search, setSearch] = useState('');
  const [selectedEv, setSelectedEv] = useState<EvidenceItem | null>(null);

  useEffect(() => {
    const fetchEvidence = async () => {
      try {
        const res = await apiClient.getEvidence();
        setEvidence(res);
      } catch (err) {
        console.error(err);
      }
    };
    fetchEvidence();
  }, []);

  const filteredEvidence = evidence.filter(
    (ev) =>
      ev.evidence_id.toLowerCase().includes(search.toLowerCase()) ||
      ev.evidence_type.toLowerCase().includes(search.toLowerCase()) ||
      ev.source.toLowerCase().includes(search.toLowerCase()) ||
      ev.sha256.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6 space-y-6 font-mono">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Database className="w-5 h-5 text-emerald-400" />
            <span>Evidence Inventory & SHA-256 Provenance</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Read-only evidence artifacts cryptographically bound to provenance records and immutable audit trail.
          </p>
        </div>

        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Filter evidence by ID, type, source, or SHA-256..."
          className="bg-slate-900 border border-slate-800 rounded px-3 py-1.5 text-xs text-slate-200 w-full md:w-80 focus:outline-none focus:border-cyan-500"
        />
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-950 text-slate-400 text-[11px]">
                <th className="py-3 px-4">EVIDENCE ID</th>
                <th className="py-3 px-4">TYPE</th>
                <th className="py-3 px-4">SOURCE / COLLECTOR</th>
                <th className="py-3 px-4">SHA-256 HASH</th>
                <th className="py-3 px-4">RECORDS</th>
                <th className="py-3 px-4">PROVENANCE</th>
                <th className="py-3 px-4">SYNTHETIC</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {filteredEvidence.map((ev) => (
                <tr
                  key={ev.evidence_id}
                  onClick={() => setSelectedEv(ev)}
                  className="hover:bg-slate-800/40 cursor-pointer transition"
                >
                  <td className="py-3 px-4 font-bold text-cyan-400">{ev.evidence_id}</td>
                  <td className="py-3 px-4">
                    <span className="bg-slate-800 text-slate-200 border border-slate-700 px-2 py-0.5 rounded text-[10px]">
                      {ev.evidence_type}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-300">{ev.source}</td>
                  <td className="py-3 px-4">
                    <div className="flex items-center space-x-1 font-mono text-cyan-300 text-[11px]">
                      <Hash className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                      <span className="truncate max-w-[160px]" title={ev.sha256}>{ev.sha256}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4 text-slate-400">{ev.record_count}</td>
                  <td className="py-3 px-4 text-purple-400 font-semibold">{ev.provenance_id}</td>
                  <td className="py-3 px-4">
                    {ev.synthetic ? (
                      <span className="text-[10px] text-amber-400 bg-amber-950/60 border border-amber-800 px-2 py-0.5 rounded">
                        SYNTHETIC
                      </span>
                    ) : (
                      <span className="text-[10px] text-emerald-400">REAL</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Selected Evidence Detail Modal */}
      {selectedEv && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-lg max-w-2xl w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="font-bold text-slate-100 flex items-center space-x-2">
                <Database className="w-4 h-4 text-emerald-400" />
                <span>Evidence Record: {selectedEv.evidence_id}</span>
              </h3>
              <button
                onClick={() => setSelectedEv(null)}
                className="text-slate-400 hover:text-slate-200 font-bold text-sm"
              >
                ✕
              </button>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div>
                <span className="text-slate-500">Case ID:</span>
                <div className="text-slate-200 font-bold">{selectedEv.case_id}</div>
              </div>
              <div>
                <span className="text-slate-500">Execution ID:</span>
                <div className="text-cyan-400 font-bold">{selectedEv.execution_id}</div>
              </div>
              <div>
                <span className="text-slate-500">Collector:</span>
                <div className="text-slate-300">{selectedEv.collector}</div>
              </div>
              <div>
                <span className="text-slate-500">Collected At (UTC):</span>
                <div className="text-slate-300">{selectedEv.collected_at_utc}</div>
              </div>
            </div>

            <div className="bg-slate-950 p-3 rounded border border-slate-800 space-y-1">
              <span className="text-[10px] text-slate-500 font-mono">CRYPTOGRAPHIC SHA-256 baseline:</span>
              <div className="text-cyan-300 font-mono text-xs break-all">{selectedEv.sha256}</div>
            </div>

            <div className="flex justify-end">
              <button
                onClick={() => setSelectedEv(null)}
                className="bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-1.5 rounded text-xs"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
