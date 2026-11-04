import React, { useEffect, useState } from 'react';
import PipelineNode from '../components/PipelineNode';
import { connectPipelineWebSocket } from '../services/websocket';

export default function PatchWorkbench() {
  const [activeStep, setActiveStep] = useState('solve');
  const [wsStatus, setWsStatus] = useState('DISCONNECTED');
  const [liveLogs, setLiveLogs] = useState([
    '🕷️ [SARIF] Ingested 1 finding from semgrep_cwe89_sqli.sarif.json',
    '🔬 [SLICING] Reduced 33 lines -> 7 lines (78.8% context reduction)',
    '🔮 [Z3 SMT] Formal invariant proved: MUST_USE_PARAMETERIZED_QUERY',
  ]);

  useEffect(() => {
    const ws = connectPipelineWebSocket(
      (msg) => {
        if (msg.event === 'NODE_TRANSITION') {
          setActiveStep(msg.data.step);
          setLiveLogs((prev) => [
            `🎃 [${msg.data.step.toUpperCase()}] ${msg.data.status}`,
            ...prev.slice(0, 15),
          ]);
        }
      },
      (status) => setWsStatus(status)
    );

    return () => ws.disconnect();
  }, []);

  const getStepStatus = (stepName) => {
    const steps = ['ingest', 'slice', 'solve', 'synthesize', 'audit', 'sandbox', 'dispatch'];
    const activeIdx = steps.indexOf(activeStep);
    const thisIdx = steps.indexOf(stepName);

    if (thisIdx < activeIdx) return 'passed';
    if (thisIdx === activeIdx) return 'active';
    return 'idle';
  };

  return (
    <div className="space-y-6">
      {/* Workbench Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="font-creepster text-3xl text-boneWhite tracking-wide">
            🔬 The Patch Forge Workbench
          </h2>
          <p className="text-xs font-mono text-boneWhite/60 mt-1">
            Real-time multi-agent closed loop pipeline with automated Z3 proofs and hermetic container verification.
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono">
          <span className="w-2.5 h-2.5 rounded-full bg-ghostGreen animate-pulse"></span>
          <span className="text-boneWhite/70">WebSocket:</span>
          <span className="text-ghostGreen font-bold">{wsStatus}</span>
        </div>
      </div>

      {/* Animated Pipeline Nodes Flow */}
      <div className="p-6 bg-deepGrave border border-cobwebGray/60 rounded-2xl overflow-x-auto">
        <div className="flex items-center space-x-4 min-w-[1100px] justify-between">
          <PipelineNode
            title="1. SARIF Ingestion"
            icon="🕷️"
            status={getStepStatus('ingest')}
            description="Schema validation & skull severity rating"
          />
          <span className="text-pumpkinOrange text-xl font-bold">➔</span>

          <PipelineNode
            title="2. AST Taint Slicing"
            icon="🔬"
            status={getStepStatus('slice')}
            description="Tree-sitter PDG backwards reachability"
          />
          <span className="text-pumpkinOrange text-xl font-bold">➔</span>

          <PipelineNode
            title="3. Z3 Invariant Prover"
            icon="🔮"
            status={getStepStatus('solve')}
            description="First-Order Logic SAT boundary proof"
          />
          <span className="text-pumpkinOrange text-xl font-bold">➔</span>

          <PipelineNode
            title="4. Adversarial Agents"
            icon="⚔️"
            status={getStepStatus('synthesize')}
            description="Alpha (PoC test) vs Beta (patch synthesis)"
          />
          <span className="text-pumpkinOrange text-xl font-bold">➔</span>

          <PipelineNode
            title="5. Anti-Tamper Audit"
            icon="⚖️"
            status={getStepStatus('audit')}
            description="Agent Gamma AST boundary inspection"
          />
          <span className="text-pumpkinOrange text-xl font-bold">➔</span>

          <PipelineNode
            title="6. Hermetic Sandbox"
            icon="🧪"
            status={getStepStatus('sandbox')}
            description="Air-gapped container test runner & mutation"
          />
          <span className="text-pumpkinOrange text-xl font-bold">➔</span>

          <PipelineNode
            title="7. PR Dispatch"
            icon="⚰️"
            status={getStepStatus('dispatch')}
            description="GPG-signed branch & V-BOM delivery"
          />
        </div>
      </div>

      {/* Live Telemetry Terminal */}
      <div className="p-4 bg-midnightBlack border border-cobwebGray/80 rounded-xl font-mono text-xs">
        <div className="flex items-center justify-between pb-2 border-b border-cobwebGray/40 text-boneWhite/50 mb-3">
          <span className="text-pumpkinOrange font-bold">⚡ Live Pipeline Telemetry Stream</span>
          <span>Buffer: {liveLogs.length} events</span>
        </div>
        <div className="space-y-1.5 text-boneWhite/80 max-h-48 overflow-y-auto">
          {liveLogs.map((log, idx) => (
            <div key={idx} className="flex items-center space-x-2">
              <span className="text-pumpkinOrange font-bold">&gt;</span>
              <span>{log}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

