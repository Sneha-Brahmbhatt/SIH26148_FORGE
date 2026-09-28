import React, { useEffect, useState } from 'react';
import { apiClient } from '../api/client';
import { DSLCommandReference } from '../types';
import { BookOpen, ShieldCheck, ShieldAlert, Code2 } from 'lucide-react';

export const LanguageReferencePage: React.FC = () => {
  const [refData, setRefData] = useState<any>(null);

  useEffect(() => {
    const fetchRef = async () => {
      try {
        const res = await apiClient.getLanguageReference();
        setRefData(res);
      } catch (err) {
        console.error(err);
      }
    };
    fetchRef();
  }, []);

  if (!refData) {
    return (
      <div className="p-8 text-center font-mono">
        <BookOpen className="w-12 h-12 text-cyan-400 mx-auto mb-3 animate-pulse" />
        <p className="text-slate-400 text-sm">Loading FORGE DSL reference documentation...</p>
      </div>
    );
  }

  const commands: DSLCommandReference[] = refData.commands || [];
  const prohibitedCaps: string[] = refData.prohibited_capabilities || [];

  return (
    <div className="p-6 space-y-6 font-mono">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <BookOpen className="w-5 h-5 text-cyan-400" />
            <span>FORGE Forensic DSL Reference Manual</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Formal language specification, command registry, arities, and capability mappings.
          </p>
        </div>

        <span className="bg-slate-900 border border-slate-800 text-cyan-400 text-xs px-3 py-1.5 rounded">
          Model: CAPABILITY_GOVERNED_ALLOWLIST
        </span>
      </div>

      {/* Prohibited Capabilities Warning Box */}
      <div className="bg-rose-950/60 border border-rose-800/80 p-4 rounded-lg space-y-2">
        <h2 className="text-xs font-bold text-rose-300 flex items-center space-x-2">
          <ShieldAlert className="w-4 h-4 text-rose-400" />
          <span>ALWAYS-DENIED PROHIBITED CAPABILITIES</span>
        </h2>
        <p className="text-xs text-rose-200">
          The following capabilities are permanently blocked by execution policy standard-read-only-v1 and cannot be requested by any script:
        </p>
        <div className="flex flex-wrap gap-2 pt-1">
          {prohibitedCaps.map((cap) => (
            <span key={cap} className="bg-rose-900/80 text-rose-200 border border-rose-700 px-2.5 py-1 rounded text-xs font-bold">
              ✗ {cap}
            </span>
          ))}
        </div>
      </div>

      {/* Commands Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden shadow-sm">
        <div className="p-4 border-b border-slate-800 bg-slate-950 flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
            <Code2 className="w-4 h-4 text-cyan-400" />
            <span>Allowed Forensic Commands Registry</span>
          </h2>
          <span className="text-xs text-slate-500">{commands.length} Commands Available</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 text-[11px]">
                <th className="py-3 px-4">COMMAND</th>
                <th className="py-3 px-4">REQUIRED CAPABILITY</th>
                <th className="py-3 px-4">PURPOSE & DESCRIPTION</th>
                <th className="py-3 px-4">USAGE SYNTAX</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {commands.map((cmd, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="py-3 px-4 font-bold text-cyan-400">{cmd.command}</td>
                  <td className="py-3 px-4">
                    <span className="bg-slate-800 text-slate-200 border border-slate-700 px-2 py-0.5 rounded text-[10px]">
                      {cmd.capability}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-300 max-w-xs">{cmd.purpose}</td>
                  <td className="py-3 px-4">
                    <code className="bg-slate-950 text-purple-300 px-2 py-1 rounded border border-slate-800 text-[11px]">
                      {cmd.syntax}
                    </code>
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
