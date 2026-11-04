import React from 'react';

export default function GhostParticles() {
  return (
    <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden opacity-30">
      <div className="absolute top-[20%] left-[10%] animate-ghost-float text-3xl">
        👻
      </div>
      <div
        className="absolute top-[60%] right-[15%] animate-ghost-float text-2xl"
        style={{ animationDelay: '1.5s', animationDuration: '5s' }}
      >
        👻
      </div>
      <div
        className="absolute top-[75%] left-[30%] animate-ghost-float text-xl"
        style={{ animationDelay: '2.5s', animationDuration: '6s' }}
      >
        👻
      </div>
      <div className="absolute top-10 left-0 w-full animate-bat-fly text-2xl">
        🦇
      </div>
    </div>
  );
}

