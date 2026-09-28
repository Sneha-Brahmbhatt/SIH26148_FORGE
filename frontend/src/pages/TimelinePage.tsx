import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { TimelineEvent } from '../types';
import { Clock, Filter, Search, ShieldAlert, Cpu, Network, FileText, Globe, Key } from 'lucide-react';

export const TimelinePage: React.FC = () => {
  const [timeline, setTimeline] = useState<TimelineEvent[]>([]);
  const [typeFilter, setTypeFilter] = useState('ALL');
  const [severityFilter, setSeverityFilter] = useState('ALL');
  const [search, setSearch] = useState('');
  const [selectedEvent, setSelectedEvent] = useState<TimelineEvent | null>(null);

  useEffect(() => {
    const fetchTimeline = async () => {
      try {
        const res = await apiClient.getTimeline();
        setTimeline(res);
      } catch (err) {
        console.error(err);
      }
    };
    fetchTimeline();
  }, []);

  const filteredTimeline = timeline.filter((tl) => {
    if (typeFilter !== 'ALL' && tl.event_type !== typeFilter) return false;
    if (severityFilter !== 'ALL' && tl.severity !== severityFilter) return false;
    if (
      search &&
      !tl.title.toLowerCase().includes(search.toLowerCase()) &&
      !tl.description.toLowerCase().includes(search.toLowerCase()) &&
      !tl.source.toLowerCase().includes(search.toLowerCase())
    )
      return false;
    return true;
  });

  const getEventIcon = (type: string) => {
    switch (type) {
      case 'PROCESS': return <Cpu className="w-4 h-4 text-purple-400" />;
      case 'NETWORK': return <Network className="w-4 h-4 text-cyan-400" />;
      case 'DNS': return <Globe className="w-4 h-4 text-emerald-400" />;
      case 'FILE': return <FileText className="w-4 h-4 text-blue-400" />;
      case 'REGISTRY': return <Key className="w-4 h-4 text-amber-400" />;
      default: return <Clock className="w-4 h-4 text-slate-400" />;
    }
  };

  const getSeverityBadge = (sev: string) => {
    if (sev === 'HIGH' || sev === 'CRITICAL') {
      return <span className="bg-rose-950 text-rose-400 border border-rose-800 text-[10px] px-2 py-0.5 rounded font-bold">HIGH</span>;
    } else if (sev === 'MEDIUM') {
      return <span className="bg-amber-950 text-amber-400 border border-amber-800 text-[10px] px-2 py-0.5 rounded font-bold">MEDIUM</span>;
    }
    return <span className="bg-slate-800 text-slate-300 border border-slate-700 text-[10px] px-2 py-0.5 rounded">INFO</span>;
  };

  return (
    <div className="p-6 space-y-6 font-mono">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Clock className="w-5 h-5 text-cyan-400" />
            <span>Unified Forensic Timeline</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Chronologically correlated timeline across computer artifacts and network telemetry.
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 rounded px-2 py-1 text-xs">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-slate-400">Type:</span>
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="bg-transparent text-slate-200 focus:outline-none"
            >
              <option value="ALL">All Event Types</option>
              <option value="PROCESS">PROCESS</option>
              <option value="NETWORK">NETWORK</option>
              <option value="DNS">DNS</option>
              <option value="FILE">FILE</option>
              <option value="EVENT_LOG">EVENT_LOG</option>
              <option value="REGISTRY">REGISTRY</option>
              <option value="SYSTEM">SYSTEM</option>
            </select>
          </div>

          <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 rounded px-2 py-1 text-xs">
            <span className="text-slate-400">Severity:</span>
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              className="bg-transparent text-slate-200 focus:outline-none"
            >
              <option value="ALL">All Severities</option>
              <option value="HIGH">HIGH</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="INFO">INFO</option>
            </select>
          </div>

          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search timeline..."
              className="bg-slate-900 border border-slate-800 rounded pl-8 pr-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
            />
          </div>
        </div>
      </div>

      {/* Timeline Stream */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-5 space-y-4">
        <div className="relative border-l-2 border-slate-800 ml-4 pl-6 space-y-6">
          {filteredTimeline.map((tl) => (
            <div
              key={tl.timeline_event_id}
              onClick={() => setSelectedEvent(tl)}
              className="relative bg-slate-950 p-4 rounded-lg border border-slate-800/80 hover:border-cyan-500/50 cursor-pointer transition shadow-md group"
            >
              {/* Timeline Bullet */}
              <div className="absolute -left-[31px] top-4 w-4 h-4 rounded-full bg-slate-900 border-2 border-cyan-400 flex items-center justify-center">
                <div className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
              </div>

              {/* Event Content */}
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-slate-800/60 pb-2 mb-2">
                <div className="flex items-center space-x-2">
                  {getEventIcon(tl.event_type)}
                  <span className="font-bold text-slate-200 text-xs">{tl.title}</span>
                  <span className="text-[10px] bg-slate-800 text-slate-300 px-1.5 py-0.5 rounded">
                    {tl.event_type}
                  </span>
                </div>
                <div className="flex items-center space-x-3 text-xs">
                  {getSeverityBadge(tl.severity)}
                  <span className="text-slate-400 text-[11px]">{tl.timestamp_utc}</span>
                </div>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed">{tl.description}</p>

              <div className="mt-2 pt-2 border-t border-slate-900 flex items-center justify-between text-[10px] text-slate-500">
                <span>Source: {tl.source}</span>
                <span>Ref: {tl.evidence_id || 'EVD-BASE'}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Event Detail Modal */}
      {selectedEvent && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-lg max-w-xl w-full p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="font-bold text-slate-100 flex items-center space-x-2">
                <Clock className="w-4 h-4 text-cyan-400" />
                <span>Event Inspector: {selectedEvent.timeline_event_id}</span>
              </h3>
              <button
                onClick={() => setSelectedEvent(null)}
                className="text-slate-400 hover:text-slate-200 font-bold text-sm"
              >
                ✕
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <span className="text-slate-500">Title:</span>
                <div className="text-slate-100 font-bold">{selectedEvent.title}</div>
              </div>
              <div>
                <span className="text-slate-500">Description:</span>
                <div className="text-slate-300 bg-slate-950 p-2.5 rounded border border-slate-800">{selectedEvent.description}</div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <span className="text-slate-500">Timestamp (UTC):</span>
                  <div className="text-cyan-400 font-bold">{selectedEvent.timestamp_utc}</div>
                </div>
                <div>
                  <span className="text-slate-500">Severity:</span>
                  <div>{getSeverityBadge(selectedEvent.severity)}</div>
                </div>
              </div>
            </div>

            <div className="flex justify-end">
              <button
                onClick={() => setSelectedEvent(null)}
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
