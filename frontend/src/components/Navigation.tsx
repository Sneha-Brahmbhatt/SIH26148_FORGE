import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard, FolderKanban, Code2, CheckCircle2, Play,
  Database, HardDrive, Network, Clock, AlertTriangle, Link2,
  FileCheck, FileText, Shield, BookOpen, Terminal
} from 'lucide-react';

export const Navigation: React.FC = () => {
  const navItems = [
    { to: '/', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/cases', label: 'Case Management', icon: FolderKanban },
    { to: '/editor', label: 'Script Editor', icon: Code2 },
    { to: '/validation', label: 'Validation Pipeline', icon: CheckCircle2 },
    { to: '/execution', label: 'Execution', icon: Play },
    { to: '/evidence', label: 'Evidence & Hashes', icon: Database },
    { to: '/computer', label: 'Computer Forensics', icon: HardDrive },
    { to: '/network', label: 'Network Forensics', icon: Network },
    { to: '/timeline', label: 'Unified Timeline', icon: Clock },
    { to: '/findings', label: 'Findings', icon: AlertTriangle },
    { to: '/chain-of-custody', label: 'Chain of Custody', icon: Link2 },
    { to: '/reports', label: 'Reports', icon: FileText },
    { to: '/audit', label: 'Audit Logs', icon: Shield },
    { to: '/reference', label: 'Language Ref', icon: BookOpen },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col flex-shrink-0 h-screen sticky top-0 overflow-y-auto">
      {/* Brand Header */}
      <div className="p-4 border-b border-slate-800 flex items-center space-x-3">
        <div className="w-9 h-9 rounded bg-gradient-to-br from-cyan-500 to-purple-600 flex items-center justify-center font-bold text-slate-950 font-mono text-lg shadow-lg">
          F
        </div>
        <div>
          <h1 className="font-mono font-bold text-slate-100 tracking-wider text-base leading-tight">
            FORGE <span className="text-xs text-cyan-400 font-normal">v0.1</span>
          </h1>
          <p className="text-[10px] text-slate-400 font-mono leading-tight">
            NTRO SIH26148 Prototype
          </p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 p-2 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-3 py-2 rounded-md text-xs font-mono transition-colors ${
                  isActive
                    ? 'bg-slate-800 text-cyan-400 border-l-2 border-cyan-400 font-semibold shadow-inner'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`
              }
            >
              <Icon className="w-4 h-4 flex-shrink-0" />
              <span className="truncate">{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Footer System Status */}
      <div className="p-3 border-t border-slate-800 bg-slate-950/60 text-[11px] font-mono text-slate-400 space-y-1">
        <div className="flex items-center justify-between text-[10px]">
          <span className="text-slate-500">POLICY:</span>
          <span className="text-emerald-400 font-bold">READ-ONLY-V1</span>
        </div>
        <div className="flex items-center justify-between text-[10px]">
          <span className="text-slate-500">RUNTIME:</span>
          <span className="text-cyan-400">FORGE-0.1.0</span>
        </div>
      </div>
    </aside>
  );
};
