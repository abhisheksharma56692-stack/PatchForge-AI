import React from 'react';

export default function SkullRating({ count = 3, max = 5 }) {
  // Accepts either integer or "3_skulls" string
  let skullCount = 3;
  if (typeof count === 'number') {
    skullCount = count;
  } else if (typeof count === 'string') {
    const match = count.match(/\d+/);
    skullCount = match ? parseInt(match[0], 10) : 3;
  }

  return (
    <div className="flex items-center space-x-1" title={`${skullCount} of ${max} skulls`}>
      {Array.from({ length: max }).map((_, i) => (
        <span
          key={i}
          className={`text-sm select-none transition-all duration-300 ${
            i < skullCount
              ? 'opacity-100 scale-100 filter drop-shadow-[0_0_4px_#ff1a1a]'
              : 'opacity-20 grayscale'
          }`}
        >
          💀
        </span>
      ))}
      <span className="text-xs text-boneWhite/60 ml-1 font-mono">({skullCount}/{max})</span>
    </div>
  );
}

