import React from 'react';
import CauldronGauge from '../components/CauldronGauge';

export default function SandboxDungeon() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="font-creepster text-3xl text-boneWhite tracking-wide">
          🧪 The Sandbox Dungeon
        </h2>
        <p className="text-xs font-mono text-boneWhite/60 mt-1">
          Rootless ephemeral micro-container telemetry with strictly enforced cgroups and air-gapped network isolation.
        </p>
      </div>

      {/* Isolation Badges */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 bg-deepGrave border border-ghostGreen/40 rounded-xl">
          <div className="text-xs font-mono text-boneWhite/60 uppercase">Air-Gap Status</div>
          <div className="mt-1 text-lg font-mono font-bold text-ghostGreen flex items-center space-x-1">
            <span>🔒</span>
            <span>--network none</span>
          </div>
          <div className="text-[11px] font-mono text-boneWhite/40 mt-1">Zero outbound sockets</div>
        </div>

        <div className="p-4 bg-deepGrave border border-pumpkinOrange/40 rounded-xl">
          <div className="text-xs font-mono text-boneWhite/60 uppercase">Cgroup RAM Limit</div>
          <div className="mt-1 text-lg font-mono font-bold text-pumpkinOrange">
            2048 MB Hard Cap
          </div>
          <div className="text-[11px] font-mono text-boneWhite/40 mt-1">OOM Killer Guarded</div>
        </div>

        <div className="p-4 bg-deepGrave border border-cauldronYellow/40 rounded-xl">
          <div className="text-xs font-mono text-boneWhite/60 uppercase">CPU Core Quota</div>
          <div className="mt-1 text-lg font-mono font-bold text-cauldronYellow">
            2.0 VCPUs Max
          </div>
          <div className="text-[11px] font-mono text-boneWhite/40 mt-1">Fork-bomb PID limit: 100</div>
        </div>

        <div className="p-4 bg-deepGrave border border-bloodVibrant/40 rounded-xl">
          <div className="text-xs font-mono text-boneWhite/60 uppercase">Rootfs Protection</div>
          <div className="mt-1 text-lg font-mono font-bold text-bloodVibrant">
            --read-only rootfs
          </div>
          <div className="text-[11px] font-mono text-boneWhite/40 mt-1">Ephemeral tmpfs mounts</div>
        </div>
      </div>

      {/* Cauldron Resource Gauges */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <CauldronGauge
          label="Memory Consumption"
          value={342}
          max={2048}
          unit="MB"
          color="#ff6b00"
        />
        <CauldronGauge
          label="CPU Core Load"
          value={1.1}
          max={2.0}
          unit="cores"
          color="#ffd700"
        />
        <CauldronGauge
          label="Execution Timeout Timer"
          value={14.5}
          max={60}
          unit="s / 60s"
          color="#00ff88"
        />
      </div>
    </div>
  );
}

