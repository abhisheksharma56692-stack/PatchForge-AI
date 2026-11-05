import React from 'react';
import { GitBranch, ShieldCheck, Terminal } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="h-9 border-t border-coffinBorder/50 bg-[#0b0512]/90 px-6 flex items-center justify-between text-[11px] font-mono text-cryptGray z-20 select-none">
      <div className="flex items-center gap-4">
        <span className="flex items-center gap-1.5 text-boneWhite">
          <GitBranch className="w-3 h-3 text-pumpkinOrange" />
          <span>branch: patchforge/remediate-cwe89-main</span>
        </span>
        <span className="hidden sm:inline text-coffinBorder">|</span>
        <span className="hidden sm:inline">MTTR Benchmark: &lt; 180s (Target 99.8% SLA)</span>
      </div>

      <div className="flex items-center gap-4">
        <span className="flex items-center gap-1.5 text-ghostGreen">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Air-Gap Isolated Sandbox</span>
        </span>
        <span className="hidden md:inline text-coffinBorder">|</span>
        <span className="hidden md:flex items-center gap-1 text-pumpkinOrange">
          <Terminal className="w-3 h-3" />
          <span>v1.0.0-cyber-gothic</span>
        </span>
      </div>
    </footer>
  );
};

export default Footer;

