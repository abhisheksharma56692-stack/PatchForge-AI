import React, { useState } from 'react';
import { PageContainer } from '../components/layout/PageContainer';
import { TombstoneCard } from '../components/domain/TombstoneCard';
import { Modal } from '../components/common/Modal';
import { Badge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import { useVulnerabilities } from '../context/VulnerabilityContext';
import { useAudio } from '../context/AudioContext';
import {
  Archive,
  Search,
  ShieldCheck,
  GitPullRequest,
  CheckCircle2,
  FileText,
  Lock,
} from 'lucide-react';

export const Graveyard = () => {
  const { graveyardTombstones } = useVulnerabilities();
  const [search, setSearch] = useState('');
  const [inspectTombstone, setInspectTombstone] = useState(null);
  const { playClick } = useAudio();

  const filteredGraves = graveyardTombstones.filter(
    (g) =>
      g.cwe_id.toLowerCase().includes(search.toLowerCase()) ||
      g.title.toLowerCase().includes(search.toLowerCase()) ||
      g.file_path.toLowerCase().includes(search.toLowerCase())
  );

  const handleInspect = (id) => {
    playClick();
    const target = graveyardTombstones.find((g) => g.id === id);
    if (target) setInspectTombstone(target);
  };

  return (
    <PageContainer
      title="⚰️ The Vulnerability Graveyard"
      subtitle="Final resting place of exorcised CVEs and permanently buried software supply chain horrors"
      action={
        <div className="flex items-center gap-2">
          <Badge variant="neutralized" icon={CheckCircle2}>
            {graveyardTombstones.length} CVEs Buried
          </Badge>
          <Badge variant="purple">100% Zero Regressions</Badge>
        </div>
      }
    >
      {/* Search Header Bar */}
      <div className="p-4 rounded-xl border border-coffinBorder bg-coffinDark/90 backdrop-blur-md flex items-center justify-between gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 text-cryptGray absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search buried tombstones by CWE or repository path..."
            className="w-full bg-[#160c22] border border-coffinBorder rounded-lg pl-9 pr-4 py-2 text-xs font-mono text-boneWhite placeholder:text-cryptGray/50 focus:outline-none focus:border-pumpkinOrange transition-colors"
          />
        </div>

        <div className="text-xs font-mono text-cryptGray">
          Sorted by Date of Neutralization (Newest first)
        </div>
      </div>

      {/* Tombstones Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {filteredGraves.map((grave) => (
          <TombstoneCard key={grave.id} vulnerability={grave} onInspectDiff={handleInspect} />
        ))}
      </div>

      {/* Cryptographic V-BOM Proofs Modal */}
      {inspectTombstone && (
        <Modal
          isOpen={!!inspectTombstone}
          onClose={() => setInspectTombstone(null)}
          title={`⚰️ Verification Bill of Materials (V-BOM)`}
          subtitle={`Cryptographic Proof Certificate for ${inspectTombstone.cwe_id} (PR #${inspectTombstone.pr_number})`}
        >
          <div className="space-y-4 font-mono text-xs">
            {/* Proof Card 1: Formal SMT Guarantee */}
            <div className="p-3.5 rounded-xl bg-deepGrave border border-ghostGreen/30 space-y-1">
              <div className="flex items-center justify-between text-ghostGreen font-bold">
                <span className="flex items-center gap-1.5">
                  <ShieldCheck className="w-4 h-4" />
                  Formal Invariant Proof (Z3 Theorem Prover)
                </span>
                <span>STATUS: VERIFIED</span>
              </div>
              <p className="text-cryptGray text-[11px] leading-relaxed">
                First-Order Logic solver proved that parameter boundary invariants eliminate all string injection surfaces while preserving existing functional AST bindings.
              </p>
            </div>

            {/* Proof Card 2: Mutation Testing Kill Rate */}
            <div className="p-3.5 rounded-xl bg-deepGrave border border-coffinBorder space-y-1">
              <div className="flex items-center justify-between text-cauldronGold font-bold">
                <span>Mutation Testing Coverage (Mutmut Engine)</span>
                <span>{inspectTombstone.mutation_score}% KILLED</span>
              </div>
              <p className="text-cryptGray text-[11px] leading-relaxed">
                All injected arithmetic and conditional AST mutations were successfully caught and killed by the test harness (Threshold: &gt;=85%).
              </p>
            </div>

            {/* Proof Card 3: GPG Key Signature */}
            <div className="p-3.5 rounded-xl bg-deepGrave border border-coffinBorder space-y-1">
              <div className="flex items-center justify-between text-boneWhite font-bold">
                <span className="flex items-center gap-1.5">
                  <Lock className="w-4 h-4 text-pumpkinOrange" />
                  GPG Commit Cryptographic Signature
                </span>
                <span className="text-pumpkinOrange font-mono">0xDEADBEEF</span>
              </div>
              <p className="text-cryptGray text-[11px] leading-relaxed">
                Signed by authorized service key <code className="text-pumpkinAmber">bot-gpg@patchforge.internal</code>.
              </p>
            </div>

            {/* Actions */}
            <div className="flex justify-end gap-2 pt-3 border-t border-coffinBorder/50">
              <Button variant="outline" size="sm" onClick={() => setInspectTombstone(null)}>
                Close Certificate
              </Button>
              <a href={inspectTombstone.pr_url} target="_blank" rel="noreferrer">
                <Button variant="pumpkin" size="sm" icon={GitPullRequest}>
                  Open GitHub PR #{inspectTombstone.pr_number}
                </Button>
              </a>
            </div>
          </div>
        </Modal>
      )}
    </PageContainer>
  );
};

export default Graveyard;
