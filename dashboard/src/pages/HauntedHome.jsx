import React, { useState, useEffect } from 'react';
import { PageContainer } from '../components/layout/PageContainer';
import { CauldronGauge } from '../components/domain/CauldronGauge';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { fetchDashboardSummary, triggerRemediationRun } from '../services/api';
import { useAudio } from '../context/AudioContext';
import {
  Skull,
  Flame,
  Ghost,
  ShieldCheck,
  Upload,
  ArrowRight,
  Activity,
  CheckCircle2,
  Sparkles,
  Download,
} from 'lucide-react';

export const HauntedHome = ({ onNavigateToWorkbench }) => {
  const [summary, setSummary] = useState({
    total_vulnerabilities: 18,
    open_skulls: 4,
    in_progress_bats: 2,
    remediated_ghosts: 12,
    mean_time_to_remediate_sec: 142.5,
    pipeline_health_percent: 99.4,
    aws_bedrock_tokens_used: 124890,
    sandbox_containers_spawned: 36,
  });

  const [isUploading, setIsUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const { playClick, playRemediationSuccess } = useAudio();

  useEffect(() => {
    fetchDashboardSummary().then(setSummary);
  }, []);

  const handleSimulateRemediation = async () => {
    playClick();
    setIsUploading(true);
    await triggerRemediationRun({ file: 'semgrep_cwe89_sqli.sarif.json' });
    setTimeout(() => {
      setIsUploading(false);
      setUploadSuccess(true);
      playRemediationSuccess();
      setTimeout(() => setUploadSuccess(false), 3000);
      onNavigateToWorkbench?.();
    }, 1200);
  };

  return (
    <PageContainer>
      {/* Hero Banner with Graveyard Scene */}
      <div className="relative rounded-2xl overflow-hidden border border-coffinBorder bg-gradient-to-r from-deepGrave via-coffinPurple to-deepGrave p-6 sm:p-8 shadow-coffin">
        <div
          className="absolute inset-0 opacity-25 mix-blend-screen pointer-events-none bg-cover bg-center"
          style={{ backgroundImage: `url('/assets/graveyard-hero.svg')` }}
        />

        <div className="relative z-10 max-w-2xl">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xs font-mono px-3 py-1 bg-pumpkinOrange/20 border border-pumpkinOrange/60 text-pumpkinOrange rounded-full uppercase tracking-wider font-semibold">
              🎃 Autonomous DevSecOps Engine
            </span>
            <span className="text-xs font-mono text-ghostGreen flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5" />
              AWS Bedrock Active
            </span>
          </div>

          <h1 className="font-creepster text-4xl sm:text-5xl text-boneWhite tracking-wide drop-shadow-md">
            The Haunted Codebase Overview
          </h1>

          <p className="text-xs sm:text-sm font-mono text-cryptGray mt-3 leading-relaxed">
            Eliminating developer alert fatigue with symbolic Tree-sitter AST slicing, First-Order Logic Z3 proofs, and rootless hermetic container validation.
          </p>

          {/* Quick-Start Summon Button */}
          <div className="mt-5 flex flex-wrap items-center gap-3">
            <Button
              variant="pumpkin"
              size="md"
              icon={Flame}
              onClick={handleSimulateRemediation}
              disabled={isUploading}
            >
              {isUploading ? 'Summoning Agents...' : 'Summon Curse Breaker (Quick Run)'}
            </Button>
            <a
              href="/PatchForge_AI_Pitch_Deck.pptx"
              download="PatchForge_AI_Pitch_Deck.pptx"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-deepGrave hover:bg-coffinPurple/60 border border-phantomPurple/60 text-phantomPurple hover:text-white font-mono text-xs font-semibold transition-all shadow-sm"
              title="Download PowerPoint Presentation"
            >
              <Download className="w-4 h-4 text-pumpkinOrange" />
              <span>Download Pitch Deck (.pptx)</span>
            </a>
            {uploadSuccess && (
              <span className="flex items-center gap-1.5 text-xs font-mono text-ghostGreen font-semibold animate-bounce">
                <CheckCircle2 className="w-4 h-4" />
                Pipeline Dispatched to Workbench!
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Top 4 Cyber-Gothic Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Open Skulls */}
        <div className="p-5 bg-deepGrave border border-bloodRed/40 rounded-xl relative overflow-hidden shadow-blood">
          <div className="flex items-center justify-between text-xs font-mono text-cryptGray uppercase">
            <span>Active Curses</span>
            <Skull className="w-5 h-5 text-bloodRed animate-pulse" />
          </div>
          <div className="mt-2 font-mono text-3xl font-bold text-bloodVibrant">
            {summary.open_skulls} Skulls
          </div>
          <div className="text-[11px] font-mono text-cryptGray mt-1">
            4 Critical / High CVE Findings
          </div>
        </div>

        {/* Card 2: In-Progress Bats */}
        <div className="p-5 bg-deepGrave border border-cauldronGold/40 rounded-xl relative overflow-hidden shadow-pumpkin">
          <div className="flex items-center justify-between text-xs font-mono text-cryptGray uppercase">
            <span>Dueling Bats</span>
            <span className="text-xl">🦇</span>
          </div>
          <div className="mt-2 font-mono text-3xl font-bold text-cauldronGold">
            {summary.in_progress_bats} In-Flight
          </div>
          <div className="text-[11px] font-mono text-cryptGray mt-1">
            Red vs Blue Agent Synthesis Loop
          </div>
        </div>

        {/* Card 3: Remediated Ghosts */}
        <div className="p-5 bg-deepGrave border border-ghostGreen/40 rounded-xl relative overflow-hidden shadow-ghost">
          <div className="flex items-center justify-between text-xs font-mono text-cryptGray uppercase">
            <span>Spirits Exorcised</span>
            <Ghost className="w-5 h-5 text-ghostGreen animate-ghost-float" />
          </div>
          <div className="mt-2 font-mono text-3xl font-bold text-ghostGreen">
            {summary.remediated_ghosts} Neutralized
          </div>
          <div className="text-[11px] font-mono text-cryptGray mt-1">
            Autonomously Buried in Graveyard
          </div>
        </div>

        {/* Card 4: MTTR Velocity */}
        <div className="p-5 bg-deepGrave border border-coffinBorder rounded-xl relative overflow-hidden shadow-coffin">
          <div className="flex items-center justify-between text-xs font-mono text-cryptGray uppercase">
            <span>Mean Time To Remediate</span>
            <Activity className="w-5 h-5 text-pumpkinOrange" />
          </div>
          <div className="mt-2 font-mono text-3xl font-bold text-pumpkinOrange">
            {Math.round(summary.mean_time_to_remediate_sec)}s
          </div>
          <div className="text-[11px] font-mono text-cryptGray mt-1">
            99.2% Faster than 60-Day Industry MTTR
          </div>
        </div>
      </div>

      {/* Middle Section: Cauldron Gauges + Drag & Drop Ingress */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Cauldron Resource Gauges (2/3 width or 2 cauldrons) */}
        <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-3 gap-4">
          <CauldronGauge
            value={summary.pipeline_health_percent}
            label="Pipeline Health"
            metric={`${summary.pipeline_health_percent}%`}
            threshold={95}
            colorScheme="green"
          />
          <CauldronGauge
            value={93.4}
            label="Mutation Kill Rate"
            metric="93.4%"
            threshold={85}
            colorScheme="orange"
          />
          <CauldronGauge
            value={68.0}
            label="Container RAM Limit"
            metric="1392 / 2048 MB"
            threshold={80}
            colorScheme="blood"
          />
        </div>

        {/* SARIF File Ingress Dropzone */}
        <div className="p-5 rounded-xl border-2 border-dashed border-coffinBorder hover:border-pumpkinOrange bg-coffinDark/80 flex flex-col items-center justify-center text-center transition-all cursor-pointer group">
          <div className="w-12 h-12 rounded-full bg-coffinPurple flex items-center justify-center text-pumpkinOrange group-hover:scale-110 transition-transform mb-3 shadow-pumpkin">
            <Upload className="w-6 h-6" />
          </div>
          <h4 className="font-mono text-sm font-semibold text-boneWhite">
            Drop SARIF Report File Here
          </h4>
          <p className="text-xs font-mono text-cryptGray mt-1 max-w-xs">
            Supports Semgrep, Bandit, Snyk & CodeQL SARIF v2.1.0 diagnostics
          </p>
          <div className="mt-4">
            <Button variant="outline" size="sm" onClick={handleSimulateRemediation}>
              Browse Files (.sarif)
            </Button>
          </div>
        </div>
      </div>

      {/* Bottom Section: Live Multi-Agent Telemetry Feed */}
      <Card
        title="Live Agentic Duel Ticker"
        subtitle="Real-time multi-agent self-healing orchestration feed"
        icon={Sparkles}
        cornerCobweb={true}
        action={
          <Button variant="ghost-outline" size="sm" onClick={onNavigateToWorkbench}>
            <span>Open Workbench</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Button>
        }
      >
        <div className="space-y-2.5 font-mono text-xs">
          <div className="flex items-start gap-3 p-2.5 rounded-lg bg-[#140b1c] border border-coffinBorder/50">
            <span className="text-ghostGreen font-bold flex-shrink-0">16:42:10</span>
            <Badge variant="neutralized" size="sm">MUTATION PASSED</Badge>
            <span className="text-boneWhite truncate">
              Mutmut killed 13/14 mutants in <code className="text-pumpkinOrange">backend/views/user.py</code> (Score: 92.8%)
            </span>
          </div>

          <div className="flex items-start gap-3 p-2.5 rounded-lg bg-[#140b1c] border border-coffinBorder/50">
            <span className="text-cauldronGold font-bold flex-shrink-0">16:41:52</span>
            <Badge variant="purple" size="sm">Z3 INVARIANT</Badge>
            <span className="text-boneWhite truncate">
              Microsoft Z3 proved boundary theorem: <code className="text-cauldronGold">Phi_path(x) ∧ ¬Psi_safe(x) == UNSAT</code>
            </span>
          </div>

          <div className="flex items-start gap-3 p-2.5 rounded-lg bg-[#140b1c] border border-coffinBorder/50">
            <span className="text-pumpkinOrange font-bold flex-shrink-0">16:41:20</span>
            <Badge variant="high" size="sm">AGENT ALPHA</Badge>
            <span className="text-boneWhite truncate">
              Synthesized dynamic reproduction exploit fixture <code className="text-pumpkinAmber">test_cwe89_poc.py</code>
            </span>
          </div>
        </div>
      </Card>
    </PageContainer>
  );
};

export default HauntedHome;
