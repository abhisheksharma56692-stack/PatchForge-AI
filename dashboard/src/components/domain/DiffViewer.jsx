import React from 'react';
import { GitCommit, FileCode, Check } from 'lucide-react';

export const DiffViewer = ({
  diffContent = '',
  language = 'python',
  originalPath = 'backend/views/user.py',
  newPath = 'backend/views/user.py',
  astSliceRange = [35, 68],
}) => {
  const lines = diffContent.split('\n');

  return (
    <div className="rounded-xl border border-coffinBorder bg-[#08040d] overflow-hidden shadow-2xl font-mono text-xs">
      {/* Diff Header */}
      <div className="h-10 px-4 bg-[#140b1c] border-b border-coffinBorder/60 flex items-center justify-between select-none">
        <div className="flex items-center gap-2">
          <FileCode className="w-4 h-4 text-pumpkinOrange" />
          <span className="font-semibold text-boneWhite text-xs">{originalPath}</span>
          <span className="px-2 py-0.5 rounded text-[10px] bg-coffinPurple text-cryptGray">
            {language}
          </span>
        </div>

        <div className="flex items-center gap-3 text-[11px] text-cryptGray">
          <span>AST Slice: L{astSliceRange[0]}–L{astSliceRange[1]}</span>
          <span className="flex items-center gap-1 text-ghostGreen">
            <Check className="w-3.5 h-3.5" />
            <span>Anti-Tamper Approved</span>
          </span>
        </div>
      </div>

      {/* Code Lines Container */}
      <div className="overflow-x-auto max-h-[420px] divide-y divide-white/5 py-1">
        {lines.map((line, idx) => {
          let lineType = 'context';
          if (line.startsWith('+') && !line.startsWith('+++')) lineType = 'addition';
          else if (line.startsWith('-') && !line.startsWith('---')) lineType = 'deletion';
          else if (line.startsWith('@@')) lineType = 'header';

          const bgStyle =
            lineType === 'addition'
              ? 'bg-emerald-950/40 text-ghostGreen hover:bg-emerald-950/60'
              : lineType === 'deletion'
              ? 'bg-red-950/40 text-red-300 hover:bg-red-950/60'
              : lineType === 'header'
              ? 'bg-coffinPurple/50 text-pumpkinAmber font-semibold'
              : 'text-boneWhite/80 hover:bg-white/[0.02]';

          return (
            <div key={idx} className={`flex items-start px-3 py-0.5 ${bgStyle} transition-colors font-mono`}>
              <span className="w-10 select-none text-cryptGray/50 text-right pr-3 flex-shrink-0 text-[11px]">
                {idx + 1}
              </span>
              <span className="w-4 select-none flex-shrink-0 font-bold">
                {lineType === 'addition' ? '+' : lineType === 'deletion' ? '-' : ' '}
              </span>
              <span className="whitespace-pre leading-relaxed">{line.replace(/^[+-]/, '')}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DiffViewer;

