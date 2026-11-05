import React from 'react';
import { Skull } from 'lucide-react';

export const SkullRating = ({
  count = 1,
  max = 5,
  size = 'md',
  interactive = false,
  onChange,
}) => {
  const sizeClasses = {
    sm: 'w-3.5 h-3.5',
    md: 'w-4 h-4',
    lg: 'w-5 h-5',
  };

  const getSkullColor = (index) => {
    if (index >= count) return 'text-coffinBorder opacity-40';
    if (count === 5) return 'text-red-500 drop-shadow-[0_0_8px_rgba(239,68,68,0.9)] animate-pulse';
    if (count >= 4) return 'text-orange-500 drop-shadow-[0_0_6px_rgba(249,115,22,0.7)]';
    if (count >= 3) return 'text-amber-400 drop-shadow-[0_0_4px_rgba(251,191,36,0.6)]';
    return 'text-cyan-400';
  };

  return (
    <div className="flex items-center gap-1 select-none" title={`Threat Severity: ${count} of ${max} skulls`}>
      {Array.from({ length: max }).map((_, i) => (
        <button
          key={i}
          type="button"
          disabled={!interactive}
          onClick={() => interactive && onChange && onChange(i + 1)}
          className={`transition-transform duration-200 ${
            interactive ? 'hover:scale-125 cursor-pointer focus:outline-none' : 'cursor-default'
          }`}
        >
          <Skull className={`${sizeClasses[size]} ${getSkullColor(i)}`} />
        </button>
      ))}
      <span className="ml-1 text-[11px] font-mono text-cryptGray">
        ({count}/{max})
      </span>
    </div>
  );
};

export default SkullRating;

