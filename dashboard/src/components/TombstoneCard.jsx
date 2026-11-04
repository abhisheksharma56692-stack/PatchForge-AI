import React from 'react';

export default function TombstoneCard({ record }) {
  const dateStr = record.timestamp
    ? new Date(record.timestamp * 1000).toLocaleDateString()
    : 'Unknown Date';

  return (
    <div className="relative group bg-coffinPurple/80 border-2 border-cobwebGray/60 hover:border-pumpkinOrange rounded-t-3xl rounded-b-md p-5 transition-all duration-300 hover:shadow-pumpkin-glow flex flex-col justify-between min-h-[220px]">
      {/* Tombstone Arch Header */}
      <div className="text-center border-b border-cobwebGray/40 pb-3">
        <div className="text-2xl mb-1 filter drop-shadow">⚰️</div>
        <h3 className="font-creepster text-2xl tracking-wider text-pumpkinOrange group-hover:text-pumpkinGlow">
          R.I.P.
        </h3>
        <p className="font-mono text-sm font-semibold text-ghostGreen">
          {record.cwe_id}
        </p>
      </div>

      {/* Body Inscription */}
      <div className="my-3 text-center">
        <p className="font-mono text-xs text-boneWhite/80 italic leading-relaxed">
          {record.tombstone_inscription || `Neutralized by PatchForge AI on ${dateStr}`}
        </p>
        <div className="mt-2 text-xs text-boneWhite/50 font-mono">
          Remediation Duration: <span className="text-pumpkinOrange">{record.duration}s</span>
        </div>
      </div>

      {/* Footer / Link */}
      <div className="pt-2 border-t border-cobwebGray/30 text-center">
        {record.pr_url && record.pr_url !== 'NONE' ? (
          <a
            href={record.pr_url}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center text-xs font-mono text-ghostGreen hover:underline"
          >
            👻 View Verified PR ↗
          </a>
        ) : (
          <span className="text-xs font-mono text-boneWhite/40">Verified Local Artifact</span>
        )}
      </div>
    </div>
  );
}

