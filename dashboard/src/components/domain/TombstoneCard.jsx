import React from 'react';
import { GitPullRequest, ShieldCheck, Clock, FileText } from 'lucide-react';

export const TombstoneCard = ({ vulnerability, onInspectDiff }) => {
  const {
    id,
    cwe_id = 'CWE-89',
    title = 'SQL Injection Vulnerability',
    file_path = 'backend/views/user.py',
    resolved_at = '2026-11-04',
    mttr_seconds = 145,
    pr_url = '#',
    pr_number = 104,
    mutation_score = 92.4,
  } = vulnerability || {};

  return (
    <div className="relative group bg-[#160c22] border-2 border-coffinBorder hover:border-pumpkinOrange rounded-t-3xl rounded-b-xl p-5 shadow-2xl transition-all duration-300 transform hover:-translate-y-2 hover:shadow-[0_15px_30px_rgba(255,106,0,0.25)] flex flex-col justify-between">
      {/* Tombstone Stone Arch Top */}
      <div className="text-center border-b border-coffinBorder/60 pb-3 mb-2">
        <span className="font-creepster text-3xl tracking-widest text-pumpkinOrange drop-shadow-[0_0_8px_rgba(255,106,0,0.6)]">
          R. I. P.
        </span>
        <div className="text-[10px] font-mono text-cryptGray uppercase tracking-widest mt-0.5">
          Neutralized & Buried
        </div>
      </div>

      {/* Epitaph Details */}
      <div className="space-y-2 my-2 flex-1">
        <div className="inline-block px-2.5 py-0.5 rounded text-xs font-bold font-mono bg-red-950/70 text-red-400 border border-red-800/40">
          {cwe_id}
        </div>
        <h4 className="text-sm font-semibold text-boneWhite leading-snug group-hover:text-pumpkinAmber transition-colors line-clamp-2">
          {title}
        </h4>
        <p className="text-xs font-mono text-cryptGray truncate" title={file_path}>
          📍 {file_path}
        </p>
      </div>

      {/* Verification Metrics Bar */}
      <div className="grid grid-cols-2 gap-2 my-3 pt-3 border-t border-coffinBorder/40 text-xs font-mono">
        <div className="flex items-center gap-1.5 text-ghostGreen" title="Mutation Test Kill Rate">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>{mutation_score}% Killed</span>
        </div>
        <div className="flex items-center gap-1.5 text-cauldronGold" title="Mean Time To Remediate">
          <Clock className="w-3.5 h-3.5" />
          <span>{Math.round(mttr_seconds)}s MTTR</span>
        </div>
      </div>

      {/* Card Actions */}
      <div className="flex items-center justify-between gap-2 pt-2">
        <a
          href={pr_url}
          target="_blank"
          rel="noreferrer"
          className="flex-1 flex items-center justify-center gap-1.5 bg-[#25133b] hover:bg-pumpkinOrange hover:text-midnightBlack text-xs font-mono font-semibold py-1.5 px-3 rounded text-boneWhite border border-[#4d2875] hover:border-pumpkinOrange transition-all"
        >
          <GitPullRequest className="w-3.5 h-3.5" />
          <span>PR #{pr_number}</span>
        </a>
        <button
          onClick={() => onInspectDiff && onInspectDiff(id)}
          className="px-3 py-1.5 bg-[#120720] hover:bg-coffinPurple text-xs font-mono text-cryptGray hover:text-boneWhite rounded border border-coffinBorder transition-colors flex items-center gap-1"
          title="Inspect V-BOM & Diff"
        >
          <FileText className="w-3.5 h-3.5" />
          <span>Proofs</span>
        </button>
      </div>
    </div>
  );
};

export default TombstoneCard;

