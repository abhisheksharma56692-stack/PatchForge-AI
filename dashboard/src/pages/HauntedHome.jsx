import React, { useEffect, useState } from 'react';
import CauldronGauge from '../components/CauldronGauge';
import { fetchDashboardSummary } from '../services/api';

export default function HauntedHome() {
  const [summary, setSummary] = useState({
    total_vulnerabilities: 14,
    open_skulls: 4,
    in_progress_bats: 2,
    remediated_ghosts: 8,
    mean_time_to_remediate_sec: 172.0,
    pipeline_health_percent: 98.8,
  });

  useEffect(() => {
    fetchDashboardSummary().then(setSummary);
  }, []);

  return (
    <div className="space-y-6">
      {/* Hero Banner with Graveyard SVG */}
      <div className="relative rounded-2xl overflow-hidden border border-cobwebGray/60 bg-gradient-to-r from-deepGrave via-coffinPurple to-deepGrave p-6">
        <img
          src="/assets/graveyard-hero.svg"
          alt="Graveyard Scene"
          className="absolute inset-0 w-full h-full object-cover opacity-35 mix-blend-screen pointer-events-none"
        />
        <div className="relative z-10 max-w-xl">
          <span className="text-xs font-mono px-3 py-1 bg-pumpkinOrange/20 border border-pumpkinOrange/50 text-pumpkinOrange rounded-full uppercase tracking-wider">
            🏚️ Operations Command Center
          </span>
          <h2 className="font-creepster text-4xl text-boneWhite mt-3 tracking-wide drop-shadow-md">
            The Haunted Codebase Overview
          </h2>
          <p className="text-sm font-mono text-boneWhite/80 mt-2 leading-relaxed">
            Autonomous static analysis ingestion, Tree-sitter taint slicing, and Microsoft Z3 formal verification turning security horrors into harmless ghosts.
          </p>
        </div>
      </div>

      {/* Top Telemetry Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 bg-deepGrave border border-bloodRed/40 rounded-xl relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-boneWhite/60 uppercase">Active Skulls</span>
            <span className="text-2xl">💀</span>
          </div>
          <div className="mt-2 font-mono text-3xl font-bold text-bloodVibrant">
            {summary.open_skulls}
          </div>
          <div className="text-[11px] font-mono text-boneWhite/40 mt-1">
            Critical & High Severity
          </div>
        </div>

        <div className="p-4 bg-deepGrave border border-cauldronYellow/40 rounded-xl relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-boneWhite/60 uppercase">Dueling Bats</span>
            <span className="text-2xl">🦇</span>
          </div>
          <div className="mt-2 font-mono text-3xl font-bold text-cauldronYellow">
            {summary.in_progress_bats}
          </div>
          <div className="text-[11px] font-mono text-boneWhite/40 mt-1">
            Synthesizing & In Sandbox
          </div>
        </div>

        <div className="p-4 bg-deepGrave border border-ghostGreen/40 rounded-xl relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-boneWhite/60 uppercase">Remediated Ghosts</span>
            <span className="text-2xl">👻</span>
          </div>
          <div className="mt-2 font-mono text-3xl font-bold text-ghostGreen">
            {summary.remediated_ghosts}
          </div>
          <div className="text-[11px] font-mono text-boneWhite/40 mt-1">
            Verified In Graveyard
          </div>
        </div>

        <div className="p-4 bg-deepGrave border border-pumpkinOrange/40 rounded-xl relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-boneWhite/60 uppercase">MTTR Speed</span>
            <span className="text-2xl">⚡</span>
          </div>
          <div className="mt-2 font-mono text-3xl font-bold text-pumpkinOrange">
            {Math.round(summary.mean_time_to_remediate_sec)}s
          </div>
          <div className="text-[11px] font-mono text-ghostGreen mt-1">
            ↓ 99.8% vs 60 days industry MTTR
          </div>
        </div>
      </div>

      {/* Cauldron Gauges Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <CauldronGauge
          label="Pipeline Cauldron Health"
          value={summary.pipeline_health_percent}
          color="#00ff88"
          unit="%"
        />
        <CauldronGauge
          label="Mutation Test Kill Rate"
          value={91.5}
          color="#ff6b00"
          unit="%"
        />
        <CauldronGauge
          label="Delta-SAST Clearance"
          value={100}
          color="#ffd700"
          unit="%"
        />
      </div>
    </div>
  );
}

