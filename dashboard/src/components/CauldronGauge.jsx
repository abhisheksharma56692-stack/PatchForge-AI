import React from 'react';

export default function CauldronGauge({
  label = "Cauldron Gauge",
  value = 85.0,
  max = 100,
  unit = "%",
  color = "#ff6b00",
}) {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));
  const strokeDashoffset = 283 - (283 * percentage) / 100;

  return (
    <div className="flex flex-col items-center justify-center p-4 bg-deepGrave border border-cobwebGray/50 rounded-xl relative overflow-hidden group">
      <div className="relative w-28 h-28 flex items-center justify-center">
        {/* SVG Circular Progress */}
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r="45"
            stroke="#1a0a2e"
            strokeWidth="8"
            fill="transparent"
          />
          <circle
            cx="50"
            cy="50"
            r="45"
            stroke={color}
            strokeWidth="8"
            strokeDasharray="283"
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center Cauldron Icon & Value */}
        <div className="absolute flex flex-col items-center justify-center">
          <span className="text-xl animate-cauldron-bubble">🧙‍♂️</span>
          <span className="font-mono text-sm font-bold text-boneWhite">
            {value}
            <span className="text-xs text-boneWhite/60">{unit}</span>
          </span>
        </div>
      </div>

      <div className="mt-3 text-center">
        <span className="text-xs font-mono uppercase tracking-wider text-boneWhite/70">
          {label}
        </span>
      </div>
    </div>
  );
}

