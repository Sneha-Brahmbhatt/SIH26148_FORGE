import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { ReportItem } from '../types';
import { FileText, Download, Hash, RefreshCw } from 'lucide-react';

export const ReportsPage: React.FC = () => {
  const [reports, setReports] = useState<ReportItem[]>([]);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const res = await apiClient.getReports();
        setReports(res);
      } catch (err) {
        console.error(err);
      }
    };
    fetchReports();
  }, []);

  return (
    <div className="p-6 space-y-6 font-mono">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <FileText className="w-5 h-5 text-cyan-400" />
            <span>Forensic Report Archive</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Generated JSON, CSV, and HTML forensic reports bound to execution provenance and SHA-256 integrity hashes.
          </p>
        </div>
        <button
          onClick={() => apiClient.getReports().then(setReports)}
          className="flex items-center space-x-1.5 bg-slate-800 hover:bg-slate-700 text-cyan-400 font-mono text-xs font-semibold px-4 py-2 rounded border border-cyan-500/30 transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh</span>
        </button>
      </div>

      {reports.length === 0 ? (
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-8 text-center">
          <FileText className="w-12 h-12 text-slate-600 mx-auto mb-3" />
          <p className="text-sm text-slate-400">No reports generated yet. Execute a forensic script to produce reports.</p>
        </div>
      ) : (
        <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-950 text-slate-400 text-[11px]">
                <th className="py-3 px-4">REPORT ID</th>
                <th className="py-3 px-4">FILENAME</th>
                <th className="py-3 px-4">FORMAT</th>
                <th className="py-3 px-4">SIZE</th>
                <th className="py-3 px-4">SHA-256</th>
                <th className="py-3 px-4">ACTIONS</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {reports.map((rpt) => {
                const ext = rpt.filename.split('.').pop()?.toUpperCase() || 'FILE';
                return (
                  <tr key={rpt.report_id} className="hover:bg-slate-800/40">
                    <td className="py-3 px-4 text-cyan-400 font-bold">{rpt.report_id}</td>
                    <td className="py-3 px-4 text-slate-200 font-semibold">{rpt.filename}</td>
                    <td className="py-3 px-4">
                      <span className={`text-[10px] px-2 py-0.5 rounded font-bold border ${
                        ext === 'HTML' ? 'bg-blue-950 text-blue-400 border-blue-800' :
                        ext === 'JSON' ? 'bg-emerald-950 text-emerald-400 border-emerald-800' :
                        ext === 'CSV' ? 'bg-amber-950 text-amber-400 border-amber-800' :
                        'bg-slate-800 text-slate-300 border-slate-700'
                      }`}>
                        {ext}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-400">
                      {(rpt.size_bytes / 1024).toFixed(1)} KB
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-1 text-cyan-300 text-[11px]">
                        <Hash className="w-3 h-3 text-emerald-400 flex-shrink-0" />
                        <span className="truncate max-w-[160px]" title={rpt.sha256}>
                          {rpt.sha256?.substring(0, 24)}...
                        </span>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <a
                        href={`/api/v1/reports/${rpt.filename}/download`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center space-x-1 text-cyan-400 hover:text-cyan-300 transition"
                      >
                        <Download className="w-3.5 h-3.5" />
                        <span>Download</span>
                      </a>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
