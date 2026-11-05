import React from 'react';

export const CauldronGauge = ({
  value = 50,
  label = 'Resource Quota',
  metric = '50%',
  threshold = 85,
  colorScheme = 'orange',
}) => {
  // Clamped percentage
  const pct = Math.min(Math.max(value, 0), 100);

  const colors = {
    green: {
      liquid: '#00ff9d',
      glow: 'rgba(0, 255, 157, 0.45)',
      fill: 'from-emerald-900 to-ghostGreen',
    },
    orange: {
      liquid: '#ff6a00',
      glow: 'rgba(255, 106, 0, 0.45)',
      fill: 'from-amber-900 to-pumpkinOrange',
    },
    blood: {
      liquid: '#dc2626',
      glow: 'rgba(220, 38, 38, 0.55)',
      fill: 'from-red-950 to-bloodVibrant',
    },
    purple: {
      liquid: '#a855f7',
      glow: 'rgba(168, 85, 247, 0.45)',
      fill: 'from-purple-950 to-purple-500',
    },
  };

  const activeColor = colors[colorScheme] || colors.orange;

  // Cauldron potion fill height (from y=75 to y=30)
  const fillY = 75 - (pct / 100) * 45;

  return (
    <div className="flex flex-col items-center p-4 rounded-xl border border-coffinBorder bg-coffinDark/90 backdrop-blur-md shadow-coffin">
      {/* SVG Cauldron */}
      <div className="relative w-28 h-28 flex items-center justify-center">
        <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-md">
          <defs>
            <linearGradient id={`liquidGrad-${label}`} x1="0%" y1="100%" x2="0%" y2="0%">
              <stop offset="0%" stop-color="#120720" />
              <stop offset="100%" stop-color={activeColor.liquid} />
            </linearGradient>
            <filter id={`cauldronGlow-${label}`}>
              <feDropShadow dx="0" dy="0" stdDeviation="3" floodColor={activeColor.liquid} floodOpacity="0.6" />
            </filter>
          </defs>

          {/* Cauldron Iron Body */}
          <ellipse cx="50" cy="85" rx="32" ry="7" fill="#0a050f" opacity="0.6" />
          <path
            d="M20,35 C15,65 25,82 50,82 C75,82 85,65 80,35 Z"
            fill="#12091c"
            stroke="#3b1d5c"
            strokeWidth="3.5"
          />

          {/* Pot Leg Left & Right */}
          <path d="M26,75 L20,86 L28,84 Z" fill="#201030" />
          <path d="M74,75 L80,86 L72,84 Z" fill="#201030" />

          {/* Potion Liquid Fill (Clipped inside cauldron) */}
          <clipPath id={`cauldronClip-${label}`}>
            <path d="M22,38 C18,63 27,80 50,80 C73,80 82,63 78,38 Z" />
          </clipPath>

          <g clipPath={`url(#cauldronClip-${label})`}>
            {/* Liquid Body */}
            <rect x="15" y={fillY} width="70" height="70" fill={`url(#liquidGrad-${label})`} />
            {/* Bubbling Surface Wave */}
            <ellipse
              cx="50"
              cy={fillY}
              rx="28"
              ry="5"
              fill={activeColor.liquid}
              filter={`url(#cauldronGlow-${label})`}
              opacity="0.85"
            />
          </g>

          {/* Cauldron Iron Rim */}
          <ellipse cx="50" cy="35" rx="32" ry="6" fill="#1d0e2e" stroke="#3b1d5c" strokeWidth="3" />
          {/* Iron Handles */}
          <path d="M16,35 C10,35 10,45 16,45" fill="none" stroke="#3b1d5c" strokeWidth="2.5" />
          <path d="M84,35 C90,35 90,45 84,45" fill="none" stroke="#3b1d5c" strokeWidth="2.5" />

          {/* Animated Rising Bubbles */}
          <circle cx="42" cy="28" r="2.5" fill={activeColor.liquid} opacity="0.8" className="animate-ping" />
          <circle cx="58" cy="22" r="2" fill={activeColor.liquid} opacity="0.6" />
          <circle cx="50" cy="18" r="1.5" fill={activeColor.liquid} opacity="0.5" />
        </svg>

        {/* Center Percentage / Value */}
        <div className="absolute inset-0 flex items-center justify-center pt-2 pointer-events-none">
          <span className="font-mono text-base font-bold text-boneWhite drop-shadow-[0_2px_4px_rgba(0,0,0,0.9)]">
            {metric}
          </span>
        </div>
      </div>

      {/* Label & Status */}
      <div className="mt-2 text-center">
        <h4 className="text-xs font-mono font-medium text-boneWhite tracking-wide">{label}</h4>
        <div className="flex items-center justify-center gap-1.5 mt-0.5 text-[10px] font-mono text-cryptGray">
          <span>Target: &gt;={threshold}%</span>
          {pct >= threshold ? (
            <span className="text-ghostGreen font-bold">PASS</span>
          ) : (
            <span className="text-bloodVibrant font-bold">EVAL</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default CauldronGauge;

