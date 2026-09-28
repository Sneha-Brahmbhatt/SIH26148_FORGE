import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { Case } from '../types';
import { FolderKanban, Plus, ShieldCheck, Calendar, User } from 'lucide-react';

export const CaseManagementPage: React.FC = () => {
  const [cases, setCases] = useState<Case[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const loadCases = async () => {
    try {
      const res = await apiClient.getCases();
      setCases(res);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadCases();
  }, []);

  const handleCreateCase = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title) return;
    setLoading(true);
    try {
      await apiClient.createCase(title, description);
      setTitle('');
      setDescription('');
      await loadCases();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold font-mono text-slate-100 flex items-center space-x-2">
            <FolderKanban className="w-5 h-5 text-cyan-400" />
            <span>Case Management</span>
          </h1>
          <p className="text-xs font-mono text-slate-400 mt-1">
            Authorized Digital Forensic Investigation Case Registry
          </p>
        </div>
      </div>

      {/* Create Case Form */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-5">
        <h2 className="text-sm font-mono font-bold text-slate-200 mb-3 flex items-center space-x-2">
          <Plus className="w-4 h-4 text-cyan-400" />
          <span>Register New Forensic Case</span>
        </h2>
        <form onSubmit={handleCreateCase} className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-mono text-slate-400 mb-1">Case Title</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g., CASE-2026-002 Network Anomaly Investigation"
              className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-500"
              required
            />
          </div>
          <div>
            <label className="block text-xs font-mono text-slate-400 mb-1">Description</label>
            <input
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Brief scope summary"
              className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-500"
            />
          </div>
          <div className="flex items-end">
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-mono font-bold py-2 rounded text-xs transition"
            >
              {loading ? 'Registering...' : 'Register Case'}
            </button>
          </div>
        </form>
      </div>

      {/* Case List */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-5">
        <h2 className="text-sm font-mono font-bold text-slate-200 mb-4">Active & Archived Cases</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {cases.map((c) => (
            <div key={c.case_id} className="bg-slate-950 border border-slate-800 rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-mono font-bold text-cyan-400 text-sm">{c.case_id}</span>
                <span className="bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-mono px-2 py-0.5 rounded">
                  {c.status}
                </span>
              </div>
              <h3 className="font-mono font-semibold text-slate-200 text-xs">{c.title}</h3>
              <p className="text-xs font-mono text-slate-400">{c.description}</p>
              <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono text-slate-400">
                <span className="flex items-center space-x-1">
                  <User className="w-3 h-3 text-slate-500" />
                  <span>{c.analyst_id}</span>
                </span>
                <span className="flex items-center space-x-1">
                  <Calendar className="w-3 h-3 text-slate-500" />
                  <span>{c.created_at_utc?.substring(0, 10)}</span>
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
