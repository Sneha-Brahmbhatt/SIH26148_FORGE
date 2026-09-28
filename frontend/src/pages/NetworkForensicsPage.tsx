import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { Network, Activity, Globe, ArrowUpRight, BarChart2 } from 'lucide-react';

export const NetworkForensicsPage: React.FC = () => {
  const [flows, setFlows] = useState<any[]>([]);
  const [dns, setDns] = useState<any[]>([]);
  const [protocols, setProtocols] = useState<any[]>([]);
  const [mode, setMode] = useState('PCAP Mode: SYNTHETIC NETWORK DATASET');

  useEffect(() => {
    const loadNetworkData = async () => {
      try {
        const [fData, dData, pData] = await Promise.all([
          apiClient.getNetworkFlows(),
          apiClient.getNetworkDNS(),
          apiClient.getNetworkProtocols()
        ]);
        setFlows(fData || []);
        setDns(dData || []);
        setProtocols(pData || []);
      } catch (err) {
        console.error(err);
      }
    };
    loadNetworkData();
  }, []);

  return (
    <div className="p-6 space-y-6 font-mono">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Network className="w-5 h-5 text-cyan-400" />
            <span>Network Forensics Subsystem</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            PCAP & network telemetry analysis, flow summaries, DNS NXDOMAIN query frequency, and protocol stats.
          </p>
        </div>

        {/* Mode Badge */}
        <span className="bg-gradient-to-r from-purple-900 to-indigo-900 border border-purple-600/50 text-purple-200 font-bold px-3 py-1.5 rounded text-xs shadow-sm flex items-center space-x-2">
          <Activity className="w-4 h-4 text-purple-400" />
          <span>{mode}</span>
        </span>
      </div>

      {/* Protocol Statistics Summary */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-5 space-y-3">
        <h2 className="text-xs font-bold text-slate-200 flex items-center space-x-2">
          <BarChart2 className="w-4 h-4 text-cyan-400" />
          <span>Protocol Distribution Analysis</span>
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {protocols.map((p, idx) => (
            <div key={idx} className="bg-slate-950 p-3 rounded border border-slate-800">
              <span className="text-xs text-slate-400 font-bold">{p.protocol}</span>
              <div className="text-lg font-bold text-slate-100 mt-1">{p.count} Packets</div>
              <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                <div
                  className="bg-cyan-500 h-full"
                  style={{ width: `${p.percentage}%` }}
                />
              </div>
              <span className="text-[10px] text-slate-500 mt-1 inline-block">{p.percentage}% of total</span>
            </div>
          ))}
        </div>
      </div>

      {/* Main Grid: Flow Summary & DNS Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Network Flow Summaries */}
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-5">
          <h2 className="text-xs font-bold text-slate-200 mb-3 flex items-center space-x-2">
            <ArrowUpRight className="w-4 h-4 text-cyan-400" />
            <span>Connection Flow Summaries</span>
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400">
                  <th className="py-2">FLOW KEY</th>
                  <th className="py-2">TOTAL BYTES</th>
                  <th className="py-2">CONNS</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {flows.map((f, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40">
                    <td className="py-2 text-cyan-400 font-bold">{f.flow_key}</td>
                    <td className="py-2 text-slate-300">{f.total_bytes} B</td>
                    <td className="py-2 text-slate-400">{f.connection_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* DNS Activity */}
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-5">
          <h2 className="text-xs font-bold text-slate-200 mb-3 flex items-center space-x-2">
            <Globe className="w-4 h-4 text-emerald-400" />
            <span>DNS Telemetry & Query Anomalies</span>
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400">
                  <th className="py-2">QUERY DOMAIN</th>
                  <th className="py-2">RESPONSE</th>
                  <th className="py-2">RESOLVED IP</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {dns.map((d, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40">
                    <td className="py-2 text-slate-200 font-semibold">{d.query_domain}</td>
                    <td className="py-2">
                      {d.response_code === 'NXDOMAIN' ? (
                        <span className="bg-rose-950 text-rose-400 border border-rose-800 px-2 py-0.5 rounded text-[10px] font-bold">
                          NXDOMAIN
                        </span>
                      ) : (
                        <span className="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded text-[10px]">
                          NOERROR
                        </span>
                      )}
                    </td>
                    <td className="py-2 text-slate-400">{d.resolved_ip || 'None'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
