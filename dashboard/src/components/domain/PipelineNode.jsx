import React from 'react';
import { CheckCircle2, AlertOctagon, Loader2, Circle } from 'lucide-react';

export const PipelineNode = ({
  title,
  stage,
  status = 'idle', // 'idle' | 'running' | 'active' | 'completed' | 'passed' | 'failed'
  latencyMs,
  agentName,
  icon: Icon,
  activeMessage,
}) => {
  const isRunning = status === 'running' || status === 'active';
  const isPassed = status === 'completed' || status === 'passed';
  const isFailed = status === 'failed';

  const statusBorder = isRunning
    ? 'border-pumpkinOrange shadow-[0_0_20px_rgba(255,106,0,0.4)] animate-candle-flicker'
    : isPassed
    ? 'border-ghostGreen/80 shadow-[0_0_15px_rgba(0,255,157,0.25)]'
    : isFailed
    ? 'border-bloodRed shadow-[0_0_20px_rgba(220,38,38,0.5)]'
    : 'border-coffinBorder/60 opacity-60';

  const statusBg = isRunning
    ? 'bg-gradient-to-b from-[#29133b] to-[#160a22]'
    : isPassed
    ? 'bg-[#101c18]'
    : isFailed
    ? 'bg-[#20080c]'
    : 'bg-coffinDark';

  return (
    <div
      className={`relative rounded-xl border-2 ${statusBorder} ${statusBg} p-4 transition-all duration-300 min-w-[210px] flex-1 select-none`}
    >
      {/* Node Header */}
      <div className="flex items-center justify-between gap-2 pb-2 mb-2 border-b border-coffinBorder/40">
        <div className="flex items-center gap-2">
          {Icon && (
            <div
              className={`p-1.5 rounded-lg ${
                isRunning
                  ? 'bg-pumpkinOrange/20 text-pumpkinOrange'
                  : isPassed
                  ? 'bg-ghostGreen/20 text-ghostGreen'
                  : 'bg-coffinPurple text-cryptGray'
              }`}
            >
              <Icon className="w-4 h-4" />
            </div>
          )}
          <span className="font-mono text-xs font-semibold text-boneWhite tracking-wide">{title}</span>
        </div>

        <div>
          {isRunning && <Loader2 className="w-4 h-4 text-pumpkinOrange animate-spin" />}
          {isPassed && <CheckCircle2 className="w-4 h-4 text-ghostGreen" />}
          {isFailed && <AlertOctagon className="w-4 h-4 text-bloodRed animate-pulse" />}
          {!isRunning && !isPassed && !isFailed && <Circle className="w-3.5 h-3.5 text-cryptGray opacity-40" />}
        </div>
      </div>

      {/* Stage & Agent Metadata */}
      <div className="space-y-1 text-xs font-mono">
        <div className="flex items-center justify-between text-cryptGray text-[11px]">
          <span>Stage: {stage}</span>
          {latencyMs !== undefined && <span>{latencyMs}ms</span>}
        </div>

        {agentName && (
          <div className="text-[11px] text-pumpkinAmber font-medium truncate" title={agentName}>
            🤖 {agentName}
          </div>
        )}

        {/* Active Live Status Message */}
        {activeMessage && (
          <div className="text-[10px] text-boneWhite/90 pt-1 line-clamp-2 leading-tight">
            {activeMessage}
          </div>
        )}
      </div>

      {/* Glow pulse bar for active state */}
      {isRunning && (
        <div className="absolute -bottom-0.5 left-2 right-2 h-0.5 bg-pumpkinOrange shadow-pumpkin" />
      )}
    </div>
  );
};

export default PipelineNode;

