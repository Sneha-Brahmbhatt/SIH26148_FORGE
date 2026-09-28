import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { HardDrive, Cpu, Wrench, FileText, ShieldAlert, Globe, Key } from 'lucide-react';

export const ComputerForensicsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'host' | 'processes' | 'services' | 'files' | 'events' | 'registry' | 'browser'>('host');
  const [host, setHost] = useState<any>(null);
  const [processes, setProcesses] = useState<any[]>([]);
  const [services, setServices] = useState<any[]>([]);
  const [files, setFiles] = useState<any[]>([]);
  const [events, setEvents] = useState<any[]>([]);
  const [eventSource, setEventSource] = useState('System');

  useEffect(() => {
    const loadComputerData = async () => {
      try {
        const [hData, pData, sData, fData] = await Promise.all([
          apiClient.getHosts(),
          apiClient.getProcesses(),
          apiClient.getServices(),
          apiClient.getFiles()
        ]);
        setHost(hData[0] || null);
        setProcesses(pData || []);
        setServices(sData || []);
        setFiles(fData || []);
      } catch (err) {
        console.error(err);
      }
    };
    loadComputerData();
  }, []);

  useEffect(() => {
    if (activeTab === 'events') {
      apiClient.getEvents(eventSource).then(setEvents).catch(console.error);
    }
  }, [activeTab, eventSource]);

  return (
    <div className="p-6 space-y-6 font-mono">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <HardDrive className="w-5 h-5 text-cyan-400" />
            <span>Computer Forensics Subsystem</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Host metadata, process trees, services, file system baselines, event logs, and registry persistence.
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 space-x-4 overflow-x-auto">
        {[
          { key: 'host', label: 'Host & System Metadata', icon: HardDrive },
          { key: 'processes', label: `Processes (${processes.length})`, icon: Cpu },
          { key: 'services', label: `Services (${services.length})`, icon: Wrench },
          { key: 'files', label: `Controlled Files (${files.length})`, icon: FileText },
          { key: 'events', label: 'Windows Event Logs', icon: ShieldAlert },
          { key: 'registry', label: 'Registry & Persistence', icon: Key },
          { key: 'browser', label: 'Browser History', icon: Globe },
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as any)}
              className={`flex items-center space-x-2 pb-3 text-xs transition border-b-2 whitespace-nowrap ${
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
        {activeTab === 'host' && host && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="bg-slate-950 p-4 rounded border border-slate-800 space-y-2">
              <span className="text-slate-500 font-bold">HOST IDENTIFICATION</span>
              <div className="text-slate-200"><strong>Hostname:</strong> {host.hostname}</div>
              <div className="text-slate-200"><strong>OS:</strong> {host.os}</div>
              <div className="text-slate-200"><strong>Architecture:</strong> {host.architecture}</div>
              <div className="text-slate-200"><strong>Domain:</strong> {host.domain}</div>
            </div>
            <div className="bg-slate-950 p-4 rounded border border-slate-800 space-y-2">
              <span className="text-slate-500 font-bold">NETWORK & BOOT PARAMETERS</span>
              <div className="text-slate-200"><strong>IP Address:</strong> {host.ip_address}</div>
              <div className="text-slate-200"><strong>MAC Address:</strong> {host.mac_address}</div>
              <div className="text-slate-200"><strong>Timezone:</strong> {host.timezone}</div>
              <div className="text-slate-200"><strong>Boot Time (UTC):</strong> {host.boot_time_utc}</div>
            </div>
          </div>
        )}

        {activeTab === 'processes' && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400">
                  <th className="py-2">PID</th>
                  <th className="py-2">PPID</th>
                  <th className="py-2">NAME</th>
                  <th className="py-2">USER</th>
                  <th className="py-2">START TIME (UTC)</th>
                  <th className="py-2">COMMAND LINE</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {processes.map((p) => (
                  <tr key={p.pid} className="hover:bg-slate-800/40">
                    <td className="py-2 text-cyan-400 font-bold">{p.pid}</td>
                    <td className="py-2 text-slate-400">{p.ppid}</td>
                    <td className="py-2 text-slate-200 font-semibold">{p.name}</td>
                    <td className="py-2 text-slate-300">{p.user}</td>
                    <td className="py-2 text-slate-400">{p.start_time_utc}</td>
                    <td className="py-2 text-purple-300 font-mono text-[11px]">{p.cmdline}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'services' && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400">
                  <th className="py-2">SERVICE NAME</th>
                  <th className="py-2">DISPLAY NAME</th>
                  <th className="py-2">STATE</th>
                  <th className="py-2">START TYPE</th>
                  <th className="py-2">BINARY PATH</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {services.map((s, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40">
                    <td className="py-2 text-cyan-400 font-bold">{s.name}</td>
                    <td className="py-2 text-slate-200">{s.display_name}</td>
                    <td className="py-2">
                      <span className="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded text-[10px]">
                        {s.state}
                      </span>
                    </td>
                    <td className="py-2 text-slate-400">{s.start_type}</td>
                    <td className="py-2 text-purple-300 font-mono text-[11px]">{s.binary_path}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'files' && (
          <div className="space-y-2">
            <h3 className="text-xs font-bold text-slate-300">Controlled Target Files</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
              {files.map((f, idx) => (
                <div key={idx} className="bg-slate-950 p-2.5 rounded border border-slate-800 flex items-center justify-between">
                  <span className="text-slate-200 font-semibold">{f.filename}</span>
                  <code className="text-slate-500 text-[10px]">{f.path}</code>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'events' && (
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <span className="text-xs text-slate-400">Log Source Channel:</span>
              {['System', 'Security', 'Application'].map((src) => (
                <button
                  key={src}
                  onClick={() => setEventSource(src)}
                  className={`px-3 py-1 rounded text-xs transition ${
                    eventSource === src ? 'bg-cyan-500 text-slate-950 font-bold' : 'bg-slate-800 text-slate-300'
                  }`}
                >
                  {src}
                </button>
              ))}
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400">
                    <th className="py-2">EVENT ID</th>
                    <th className="py-2">TASK / PROVIDER</th>
                    <th className="py-2">TIMESTAMP (UTC)</th>
                    <th className="py-2">MESSAGE</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {events.map((e, idx) => (
                    <tr key={idx} className="hover:bg-slate-800/40">
                      <td className="py-2 text-purple-400 font-bold">{e.event_id}</td>
                      <td className="py-2 text-slate-300">{e.task || e.provider}</td>
                      <td className="py-2 text-slate-400">{e.timestamp_utc}</td>
                      <td className="py-2 text-slate-200">{e.message}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'registry' && (
          <div className="space-y-3">
            <h3 className="text-xs font-bold text-slate-300">Persistence Leads & Run Keys</h3>
            <div className="bg-slate-950 p-3 rounded border border-slate-800 space-y-2 text-xs">
              <div className="flex items-center justify-between">
                <span className="font-bold text-purple-400">HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce</span>
                <span className="bg-rose-950 text-rose-400 border border-rose-800 text-[10px] px-2 py-0.5 rounded">HIGH PRIORITY LEAD</span>
              </div>
              <p className="text-slate-300">Value Name: <code>UpdateFix</code></p>
              <p className="text-cyan-300">Value Data: <code>C:\Users\Public\Downloads\updater_svc.exe</code></p>
            </div>
          </div>
        )}

        {activeTab === 'browser' && (
          <div className="space-y-3">
            <h3 className="text-xs font-bold text-slate-300">Browser History Artifacts</h3>
            <div className="space-y-2 text-xs">
              <div className="bg-slate-950 p-2.5 rounded border border-slate-800 flex justify-between items-center">
                <div>
                  <div className="text-slate-200 font-bold">Pastebin Raw Content</div>
                  <div className="text-cyan-400 text-[11px]">https://pastebin.org/raw/temp89342</div>
                </div>
                <span className="text-slate-500 text-[10px]">2026-09-25T14:14:02Z</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
