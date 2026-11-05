import React from 'react';
import { Sparkles, CheckCircle2, ShieldAlert } from 'lucide-react';

export const Z3ProofViewer = ({
  invariants = [
    '∀ offset ∈ ℤ: 0 <= offset < buffer_max',
    '∀ query ∈ String: ¬contains(query, "\'") ∧ is_parameterized(query)',
  ],
  status = 'UNCONDITIONALLY_SAFE',
  predicateFormula = 'Phi_path(x) ∧ ¬Psi_safe(x) == UNSAT',
}) => {
  const isSafe = status === 'UNCONDITIONALLY_SAFE' || status === 'SATISFIABLE_INVARIANT';

  return (
    <div className="rounded-xl border border-coffinBorder bg-[#0c0614] p-4 shadow-xl font-mono text-xs space-y-3">
      {/* Proof Header */}
      <div className="flex items-center justify-between pb-2 border-b border-coffinBorder/50">
        <div className="flex items-center gap-2 text-cauldronGold">
          <Sparkles className="w-4 h-4" />
          <span className="font-semibold text-boneWhite">Z3 SMT Invariant Verification</span>
        </div>

        <div className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-950/80 text-ghostGreen border border-ghostGreen/40">
          {isSafe ? <CheckCircle2 className="w-3.5 h-3.5" /> : <ShieldAlert className="w-3.5 h-3.5 text-bloodRed" />}
          <span>{status}</span>
        </div>
      </div>

      {/* Solver Target Theorem */}
      <div>
        <div className="text-[10px] uppercase tracking-wider text-cryptGray">Target Solver Theorem:</div>
        <div className="mt-1 p-2 rounded bg-midnightBlack border border-coffinBorder text-cauldronYellow font-bold">
          {predicateFormula}
        </div>
      </div>

      {/* Enforced Invariants List */}
      <div>
        <div className="text-[10px] uppercase tracking-wider text-cryptGray mb-1">
          Enforced Code Invariants (Non-Negotiable Bounds):
        </div>
        <ul className="space-y-1.5">
          {invariants.map((inv, idx) => (
            <li
              key={idx}
              className="flex items-start gap-2 p-2 rounded bg-[#160c22] border border-coffinBorder/80 text-ghostGreen"
            >
              <span className="text-pumpkinOrange font-bold">§{idx + 1}</span>
              <span className="leading-snug">{inv}</span>
            </li>
          ))}
        </ul>
      </div>

      <p className="text-[10px] text-cryptGray italic">
        * Invariant injected directly into Agent Beta prompt context to eliminate off-by-one and boundary overflow flaws.
      </p>
    </div>
  );
};

export default Z3ProofViewer;

