import React from 'react';

export default function PipelineNode({
  title,
  icon,
  status = "idle", // "idle", "active", "passed", "failed"
  description,
}) {
  let borderColor = "border-cobwebGray/50";
  let glowClass = "";
  let badgeColor = "bg-cobwebGray/30 text-boneWhite/50";
  let statusText = "Idle";

  if (status === "active") {
    borderColor = "border-pumpkinOrange";
    glowClass = "animate-candle-flicker shadow-pumpkin-glow";
    badgeColor = "bg-pumpkinOrange text-midnightBlack font-bold animate-pulse";
    statusText = "Conjuring...";
  } else if (status === "passed") {
    borderColor = "border-ghostGreen";
    glowClass = "shadow-ghost-glow";
    badgeColor = "bg-ghostGreen/20 text-ghostGreen border border-ghostGreen";
    statusText = "Passed";
  } else if (status === "failed") {
    borderColor = "border-bloodVibrant";
    glowClass = "shadow-blood-glow animate-blood-drip";
    badgeColor = "bg-bloodRed text-boneWhite";
    statusText = "Failed";
  }

  return (
    <div
      className={`relative flex flex-col p-4 rounded-xl bg-coffinPurple/90 border-2 ${borderColor} ${glowClass} transition-all duration-300 w-52 min-h-[140px] justify-between`}
    >
      <div className="flex items-center justify-between">
        <span className="text-2xl">{icon}</span>
        <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full uppercase ${badgeColor}`}>
          {statusText}
        </span>
      </div>

      <div className="my-2">
        <h4 className="font-mono text-sm font-bold text-boneWhite">{title}</h4>
        {description && (
          <p className="text-[11px] text-boneWhite/60 font-mono mt-1 line-clamp-2">
            {description}
          </p>
        )}
      </div>

      <div className="text-[10px] text-boneWhite/40 font-mono flex items-center justify-between border-t border-cobwebGray/30 pt-1">
        <span>Node Gate</span>
        <span>{status === 'passed' ? '✓ Safe' : '• Guarded'}</span>
      </div>
    </div>
  );
}

