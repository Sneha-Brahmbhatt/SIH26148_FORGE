import React from 'react';
import { ShieldAlert } from 'lucide-react';

export const SafetyBanner: React.FC = () => {
  return (
    <div className="bg-amber-950/80 border-b border-amber-600/40 text-amber-200 px-4 py-2 text-xs font-mono flex items-center justify-between shadow-sm">
      <div className="flex items-center space-x-2">
        <ShieldAlert className="w-4 h-4 text-amber-400 flex-shrink-0" />
        <span>
          <strong className="text-amber-400">MANDATORY SAFETY BOUNDARY:</strong> FORGE is intended only for authorized digital-forensic investigations and controlled security environments. It does not bypass, disable, evade, or interfere with endpoint security controls.
        </span>
      </div>
      <span className="hidden lg:inline-block bg-amber-900/60 border border-amber-700/50 px-2 py-0.5 rounded text-[10px] text-amber-300">
        READ-ONLY & CAPABILITY GOVERNED
      </span>
    </div>
  );
};
