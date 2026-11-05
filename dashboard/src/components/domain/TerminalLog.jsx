import React, { useEffect, useRef } from 'react';
import { Terminal, Copy, Check, Trash2 } from 'lucide-react';

export const TerminalLog = ({
  logs = [],
  title = 'Hermetic Sandbox Execution Console',
  maxHeight = 'max-h-96',
  onClear,
}) => {
  const terminalEndRef = useRef(null);
  const [copied, setCopied] = React.useState(false);

  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const handleCopy = () => {
    navigator.clipboard.writeText(logs.join('\n'));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getLineStyle = (line) => {
    if (line.includes('[ERROR]') || line.includes('FAILED') || line.includes('FAIL')) {
      return 'text-red-400 font-semibold';
    }
    if (line.includes('[PASS]') || line.includes('PASSED') || line.includes('DEFENDED') || line.includes('CLEAN')) {
      return 'text-ghostGreen font-semibold';
    }
    if (line.includes('[Z3]') || line.includes('INVARIANT') || line.includes('FORMAL')) {
      return 'text-cauldronGold';
    }
    if (line.includes('[AGENT]') || line.includes('CODER') || line.includes('SYNTH')) {
      return 'text-pumpkinOrange';
    }
    return 'text-slimeLime/90';
  };

  return (
    <div className="rounded-xl border border-coffinBorder bg-[#08040d] overflow-hidden shadow-2xl flex flex-col font-mono text-xs">
      {/* Terminal Title Bar */}
      <div className="h-9 px-4 bg-[#140b1c] border-b border-coffinBorder/60 flex items-center justify-between select-none">
        <div className="flex items-center gap-2 text-cryptGray">
          <Terminal className="w-3.5 h-3.5 text-slimeLime" />
          <span className="font-semibold text-boneWhite text-xs">{title}</span>
        </div>

        <div className="flex items-center gap-2">
          {onClear && (
            <button
              onClick={onClear}
              className="p-1 rounded text-cryptGray hover:text-boneWhite hover:bg-coffinPurple transition-colors"
              title="Clear Console"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          )}
          <button
            onClick={handleCopy}
            className="p-1 rounded text-cryptGray hover:text-pumpkinOrange hover:bg-coffinPurple transition-colors"
            title="Copy Logs"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-ghostGreen" /> : <Copy className="w-3.5 h-3.5" />}
          </button>
        </div>
      </div>

      {/* Terminal Log Output Window */}
      <div className={`p-4 overflow-y-auto ${maxHeight} space-y-1 bg-black/60`}>
        {logs.length === 0 ? (
          <div className="text-cryptGray/50 italic py-4 text-center">
            &gt; Waiting for execution telemetry stream...
          </div>
        ) : (
          logs.map((log, index) => (
            <div key={index} className={`leading-relaxed whitespace-pre-wrap break-all ${getLineStyle(log)}`}>
              <span className="text-cryptGray/40 select-none mr-2 font-light">[{index + 1}]</span>
              {log}
            </div>
          ))
        )}
        <div ref={terminalEndRef} />
      </div>

      {/* Terminal Footer Indicator */}
      <div className="h-6 px-4 bg-[#0d0714] border-t border-coffinBorder/30 flex items-center justify-between text-[10px] text-cryptGray">
        <span className="flex items-center gap-1.5 text-slimeLime">
          <span className="w-2 h-2 rounded-full bg-slimeLime animate-ping" />
          <span>LIVE STDOUT STREAM</span>
        </span>
        <span>{logs.length} Lines Captured</span>
      </div>
    </div>
  );
};

export default TerminalLog;

