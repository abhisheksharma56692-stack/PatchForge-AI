import React, { useState } from 'react';
import { PageContainer } from '../components/layout/PageContainer';
import { PipelineNode } from '../components/domain/PipelineNode';
import { DiffViewer } from '../components/domain/DiffViewer';
import { TerminalLog } from '../components/domain/TerminalLog';
import { Z3ProofViewer } from '../components/domain/Z3ProofViewer';
import { Tabs } from '../components/common/Tabs';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { useWebSocket } from '../context/WebSocketContext';
import { useAudio } from '../context/AudioContext';
import { mockSampleDiff } from '../services/mockData';
import {
  FileSearch,
  Scissors,
  Sparkles,
  Bot,
  Box,
  GitPullRequest,
  RotateCcw,
  Play,
  CheckCircle,
} from 'lucide-react';

export const PatchWorkbench = () => {
  const { pipelineState, liveLogs, clearLogs, addLog } = useWebSocket();
  const { playClick, playRemediationSuccess } = useAudio();

  const [activeTab, setActiveTab] = useState('diff');
  const [currentStep, setCurrentStep] = useState('synthesize');
  const [iteration, setIteration] = useState(1);
  const [prCreated, setPrCreated] = useState(false);

  const steps = [
    { id: 'ingest', title: 'SARIF Ingest', stage: 'Stage 1', icon: FileSearch, agent: 'Parser' },
    { id: 'slice', title: 'AST Slice', stage: 'Stage 2', icon: Scissors, agent: 'Tree-sitter' },
    { id: 'solve', title: 'Z3 Invariant', stage: 'Stage 3', icon: Sparkles, agent: 'SMT Solver' },
    { id: 'synthesize', title: 'Agent Duel', stage: 'Stage 4', icon: Bot, agent: 'Alpha vs Beta' },
    { id: 'sandbox', title: 'Hermetic Box', stage: 'Stage 5', icon: Box, agent: 'Docker Air-Gap' },
    { id: 'dispatch', title: 'PR Delivery', stage: 'Stage 6', icon: GitPullRequest, agent: 'GPG Signer' },
  ];

  const getStepStatus = (stepId) => {
    const stepOrder = ['ingest', 'slice', 'solve', 'synthesize', 'sandbox', 'dispatch'];
    const activeIdx = stepOrder.indexOf(currentStep);
    const thisIdx = stepOrder.indexOf(stepId);

    if (prCreated && thisIdx <= stepOrder.indexOf('dispatch')) return 'completed';
    if (thisIdx < activeIdx) return 'completed';
    if (thisIdx === activeIdx) return 'running';
    return 'idle';
  };

  const handleNextStep = () => {
    playClick();
    const stepOrder = ['ingest', 'slice', 'solve', 'synthesize', 'sandbox', 'dispatch'];
    const currentIdx = stepOrder.indexOf(currentStep);

    if (currentIdx < stepOrder.length - 1) {
      const nextStep = stepOrder[currentIdx + 1];
      setCurrentStep(nextStep);
      addLog(`🎃 [PIPELINE] Advanced state machine transition -> ${nextStep.toUpperCase()}`);
      if (nextStep === 'dispatch') {
        setPrCreated(true);
        playRemediationSuccess();
      }
    }
  };

  const handleReset = () => {
    playClick();
    setCurrentStep('ingest');
    setIteration(1);
    setPrCreated(false);
    clearLogs();
    addLog('🔄 [RESET] Initialized state machine graph to Stage 1');
  };

  const tabs = [
    { id: 'diff', label: 'Candidate Patch Diff' },
    { id: 'z3', label: 'Z3 Formal Proofs' },
    { id: 'slice', label: 'Isolated AST Slice' },
  ];

  return (
    <PageContainer
      title="🔬 The Patch Forge Workbench"
      subtitle="Closed-loop autonomous remediation engine: AST slicing, First-Order Logic constraints & hermetic sandbox validation"
      action={
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" icon={RotateCcw} onClick={handleReset}>
            Reset Loop
          </Button>
          <Button variant="pumpkin" size="sm" icon={Play} onClick={handleNextStep}>
            Step Forward
          </Button>
        </div>
      }
    >
      {/* Top Section: Multi-Agent State Graph Horizontal Nodes */}
      <div className="p-4 rounded-xl border border-coffinBorder bg-coffinDark/95 backdrop-blur-md shadow-coffin">
        <div className="flex items-center justify-between pb-3 mb-3 border-b border-coffinBorder/50">
          <div className="flex items-center gap-2 font-mono text-xs">
            <span className="font-semibold text-boneWhite">Active State Graph:</span>
            <Badge variant="high">Iteration k = {iteration} / 5</Badge>
            <span className="text-cryptGray">Target: CWE-89 (SQL Injection)</span>
          </div>
          {prCreated && (
            <Badge variant="neutralized" icon={CheckCircle}>
              PR #104 Published & GPG Signed
            </Badge>
          )}
        </div>

        {/* State Graph Horizontal Sequence */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin">
          {steps.map((st) => (
            <PipelineNode
              key={st.id}
              title={st.title}
              stage={st.stage}
              status={getStepStatus(st.id)}
              agentName={st.agent}
              icon={st.icon}
            />
          ))}
        </div>
      </div>

      {/* Main Split Workbench Screen (2 Columns) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column (7/12): Code Diff & Proofs */}
        <div className="lg:col-span-7 space-y-4">
          <div className="p-4 rounded-xl border border-coffinBorder bg-coffinDark/90 backdrop-blur-md">
            <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="mb-4" />

            {activeTab === 'diff' && (
              <DiffViewer
                diffContent={mockSampleDiff}
                language="python"
                originalPath="backend/views/user.py"
                newPath="backend/views/user.py"
                astSliceRange={[39, 48]}
              />
            )}

            {activeTab === 'z3' && (
              <Z3ProofViewer
                invariants={[
                  '∀ username ∈ String: length(username) <= 255',
                  '∀ query ∈ SQLStatements: is_parameterized(query) ∧ ¬has_concatenation(query)',
                  'Assert: connection.cursor().execute(query, [params]) == SAFE_EXECUTION',
                ]}
                status="UNCONDITIONALLY_SAFE"
                predicateFormula="Phi_path(username) ∧ ¬SafeParametric(query) == UNSAT"
              />
            )}

            {activeTab === 'slice' && (
              <div className="font-mono text-xs space-y-2">
                <div className="flex items-center justify-between text-cryptGray">
                  <span>Tree-sitter Backward Slice (PDG Ancestors of Tainted Sink):</span>
                  <span className="text-ghostGreen">33 lines reduced to 7 lines</span>
                </div>
                <pre className="p-4 rounded-xl bg-black/80 border border-coffinBorder text-ghostGreen overflow-x-auto max-h-[380px] leading-relaxed">
{`# File: backend/views/user.py (Program Dependence Graph Slice)
def get_user_profile(request, username):
    cursor = connection.cursor()
    # Taint propagates:
    query = f"SELECT id, username, email FROM users WHERE username = '{username}'"
    cursor.execute(query)  # SINK: Tainted Call`}
                </pre>
              </div>
            )}
          </div>
        </div>

        {/* Right Column (5/12): Terminal Stream & Telemetry */}
        <div className="lg:col-span-5 space-y-4">
          <TerminalLog
            logs={liveLogs}
            title="Real-Time Duel Telemetry (WebSocket)"
            maxHeight="max-h-[500px]"
            onClear={clearLogs}
          />
        </div>
      </div>
    </PageContainer>
  );
};

export default PatchWorkbench;
