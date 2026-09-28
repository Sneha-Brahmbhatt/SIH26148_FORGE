import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { Finding } from '../types';
import { AlertTriangle, ShieldCheck, CheckCircle2, FileSearch, Filter } from 'lucide-react';

export const FindingsPage: React.FC = () => {
  const [findings, setFindings] = useState<Finding[]>([]);
  const [categoryFilter, setCategoryFilter] = useState('ALL');

  useEffect(() => {
    const fetchFindings = async () => {
      try {
        const res = await apiClient.getFindings();
        setFindings(res);
      } catch (err) {
        console.error(err);
      }
    };
    fetchFindings();
  }, []);

  const categories = Array.from(new Set(findings.map((f) => f.category)));

  const filteredFindings = findings.filter(
    (f) => categoryFilter === 'ALL' || f.category === categoryFilter
  );

  return (
    <div className="p-6 space-y-6 font-mono">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            <span>Correlated Forensic Findings</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Evidence-backed findings with strict separation between Observed Evidence, Derived Analysis, and Investigator Action.
          </p>
        </div>

        {/* Category Filter */}
        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 rounded px-3 py-1.5 text-xs">
          <Filter className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-slate-400">Category:</span>
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="bg-transparent text-slate-200 focus:outline-none"
          >
            <option value="ALL">All Categories</option>
            {categories.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Findings Cards */}
      <div className="space-y-4">
        {filteredFindings.map((fnd) => (
          <div
            key={fnd.finding_id}
            className="bg-slate-900 border border-slate-800 rounded-lg p-5 space-y-4 shadow-md"
          >
            {/* Finding Title & Badges */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-slate-800 pb-3">
              <div className="flex items-center space-x-3">
                <span className="text-cyan-400 font-bold text-xs">{fnd.finding_id}</span>
                <h3 className="text-slate-100 font-bold text-sm">{fnd.title}</h3>
              </div>
              <div className="flex items-center space-x-2">
                <span className="bg-slate-800 text-slate-300 border border-slate-700 text-[10px] px-2 py-0.5 rounded">
                  {fnd.category}
                </span>
                {fnd.severity === 'HIGH' ? (
                  <span className="bg-rose-950 text-rose-400 border border-rose-800 text-[10px] px-2 py-0.5 rounded font-bold">
                    HIGH SEVERITY
                  </span>
                ) : (
                  <span className="bg-amber-950 text-amber-400 border border-amber-800 text-[10px] px-2 py-0.5 rounded font-bold">
                    MEDIUM SEVERITY
                  </span>
                )}
                <span className="text-[10px] text-slate-500">{fnd.confidence}</span>
              </div>
            </div>

            {/* MANDATORY THREE-PART EVIDENCE BREAKDOWN */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              {/* Part 1: Observed Evidence */}
              <div className="bg-slate-950 p-3.5 rounded border border-slate-800/80 space-y-1.5">
                <div className="flex items-center space-x-1.5 text-cyan-400 font-bold text-[11px]">
                  <FileSearch className="w-3.5 h-3.5" />
                  <span>1. OBSERVED EVIDENCE</span>
                </div>
                <p className="text-slate-300 text-[11px] leading-relaxed">
                  {fnd.observed_evidence || fnd.description}
                </p>
              </div>

              {/* Part 2: Derived Analysis */}
              <div className="bg-slate-950 p-3.5 rounded border border-slate-800/80 space-y-1.5">
                <div className="flex items-center space-x-1.5 text-purple-400 font-bold text-[11px]">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  <span>2. DERIVED ANALYSIS</span>
                </div>
                <p className="text-slate-300 text-[11px] leading-relaxed">
                  {fnd.derived_analysis || 'Automated technical correlation based on forensic rules.'}
                </p>
              </div>

              {/* Part 3: Investigator Action */}
              <div className="bg-slate-950 p-3.5 rounded border border-slate-800/80 space-y-1.5">
                <div className="flex items-center space-x-1.5 text-amber-400 font-bold text-[11px]">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>3. INVESTIGATOR REVIEW REQUIRED</span>
                </div>
                <p className="text-amber-200 text-[11px] leading-relaxed">
                  {fnd.analyst_interpretation_required || 'Review associated evidence artifacts to confirm authorization.'}
                </p>
              </div>
            </div>

            {/* Footer Ref */}
            <div className="flex items-center justify-between text-[10px] text-slate-500 pt-1">
              <span>Timestamp: {fnd.timestamp_utc}</span>
              <span>Analysis Type: {fnd.analysis_type}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
