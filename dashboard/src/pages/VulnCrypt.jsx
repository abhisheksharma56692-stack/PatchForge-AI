import React, { useState } from 'react';
import { PageContainer } from '../components/layout/PageContainer';
import { SkullRating } from '../components/domain/SkullRating';
import { Badge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import { Modal } from '../components/common/Modal';
import { useVulnerabilities } from '../context/VulnerabilityContext';
import { useAudio } from '../context/AudioContext';
import {
  Search,
  Filter,
  Eye,
  Wrench,
  FileCode,
  ShieldAlert,
  Terminal,
} from 'lucide-react';

export const VulnCrypt = ({ onNavigateToWorkbench }) => {
  const {
    vulnerabilities,
    allVulnerabilities,
    filterSeverity,
    setFilterSeverity,
    searchQuery,
    setSearchQuery,
    scannerFilter,
    setScannerFilter,
  } = useVulnerabilities();

  const [inspectVuln, setInspectVuln] = useState(null);
  const { playClick } = useAudio();

  const scanners = ['ALL', 'Semgrep', 'Bandit', 'Snyk', 'CodeQL'];

  const handleInspect = (vuln) => {
    playClick();
    setInspectVuln(vuln);
  };

  const handleRemediate = (vuln) => {
    playClick();
    onNavigateToWorkbench?.(vuln);
  };

  return (
    <PageContainer
      title="💀 The Vulnerability Crypt"
      subtitle="Vault of detected security flaws, abstract syntax tree slices, and tainted execution paths"
      action={
        <div className="flex items-center gap-2">
          <Badge variant="critical">
            {vulnerabilities.filter((v) => v.skulls === 5).length} Catastrophic (5 Skulls)
          </Badge>
          <Badge variant="purple">{allVulnerabilities.length} Total Findings</Badge>
        </div>
      }
    >
      {/* Search & Filter Toolbar */}
      <div className="p-4 rounded-xl border border-coffinBorder bg-coffinDark/90 backdrop-blur-md flex flex-wrap items-center justify-between gap-4">
        {/* Search Input */}
        <div className="relative flex-1 min-w-[260px]">
          <Search className="w-4 h-4 text-cryptGray absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by CWE, file path, or keyword..."
            className="w-full bg-[#160c22] border border-coffinBorder rounded-lg pl-9 pr-4 py-2 text-xs font-mono text-boneWhite placeholder:text-cryptGray/50 focus:outline-none focus:border-pumpkinOrange transition-colors"
          />
        </div>

        {/* Skull Severity Filter Selector */}
        <div className="flex items-center gap-3">
          <span className="text-xs font-mono text-cryptGray flex items-center gap-1">
            <Filter className="w-3.5 h-3.5" /> Filter Skulls:
          </span>
          <div className="flex items-center gap-1 bg-[#140b1c] p-1 rounded-lg border border-coffinBorder">
            <button
              onClick={() => setFilterSeverity(0)}
              className={`px-2 py-0.5 rounded text-[11px] font-mono transition-colors ${
                filterSeverity === 0
                  ? 'bg-pumpkinOrange text-midnightBlack font-bold'
                  : 'text-cryptGray hover:text-boneWhite'
              }`}
            >
              All
            </button>
            {[5, 4, 3, 2].map((rating) => (
              <button
                key={rating}
                onClick={() => setFilterSeverity(rating)}
                className={`px-2 py-0.5 rounded text-[11px] font-mono transition-colors flex items-center gap-1 ${
                  filterSeverity === rating
                    ? 'bg-bloodRed text-boneWhite font-bold shadow-blood'
                    : 'text-cryptGray hover:text-boneWhite'
                }`}
              >
                <span>{rating}</span>
                <span>💀</span>
              </button>
            ))}
          </div>
        </div>

        {/* Scanner Source Tag Buttons */}
        <div className="flex items-center gap-1">
          {scanners.map((sc) => (
            <button
              key={sc}
              onClick={() => setScannerFilter(sc)}
              className={`px-2.5 py-1 rounded text-xs font-mono transition-colors ${
                scannerFilter === sc
                  ? 'bg-coffinPurple text-pumpkinOrange border border-pumpkinOrange/60 font-semibold'
                  : 'bg-deepGrave text-cryptGray border border-coffinBorder/60 hover:text-boneWhite'
              }`}
            >
              {sc}
            </button>
          ))}
        </div>
      </div>

      {/* Vulnerabilities Table */}
      <div className="rounded-xl border border-coffinBorder bg-coffinDark/95 backdrop-blur-md overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead className="bg-[#150a20] border-b border-coffinBorder/60 text-cryptGray uppercase text-[11px] tracking-wider select-none">
              <tr>
                <th className="py-3 px-4">Severity</th>
                <th className="py-3 px-4">Finding & CWE</th>
                <th className="py-3 px-4">Tainted Sink Expression</th>
                <th className="py-3 px-4">File Location</th>
                <th className="py-3 px-4">Scanner</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-coffinBorder/40">
              {vulnerabilities.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-cryptGray italic">
                    🕸️ Zero matching curses found in this vault.
                  </td>
                </tr>
              ) : (
                vulnerabilities.map((v) => (
                  <tr
                    key={v.id}
                    className="hover:bg-coffinPurple/30 transition-colors group cursor-pointer"
                  >
                    <td className="py-3 px-4 whitespace-nowrap">
                      <SkullRating count={v.skulls} size="sm" />
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-pumpkinAmber">{v.cwe_id}</span>
                        <span className="text-boneWhite truncate max-w-xs">{v.title}</span>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <code className="px-2 py-0.5 rounded bg-black/60 text-ghostGreen border border-coffinBorder/50 font-mono text-[11px] truncate block max-w-xs">
                        {v.sink_symbol}
                      </code>
                    </td>
                    <td className="py-3 px-4 text-cryptGray truncate max-w-xs">
                      {v.file_path}:{v.line_number}
                    </td>
                    <td className="py-3 px-4 text-cryptGray whitespace-nowrap">
                      <Badge variant="purple" size="sm">
                        {v.scanner}
                      </Badge>
                    </td>
                    <td className="py-3 px-4 text-right whitespace-nowrap">
                      <div className="flex items-center justify-end gap-1.5">
                        <Button
                          variant="ghost-outline"
                          size="sm"
                          icon={Eye}
                          onClick={() => handleInspect(v)}
                        >
                          Slice
                        </Button>
                        <Button
                          variant="pumpkin"
                          size="sm"
                          icon={Wrench}
                          onClick={() => handleRemediate(v)}
                        >
                          Forge Fix
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* AST Inspection Modal */}
      {inspectVuln && (
        <Modal
          isOpen={!!inspectVuln}
          onClose={() => setInspectVuln(null)}
          title={`🔬 AST Slicing Context: ${inspectVuln.cwe_id}`}
          subtitle={`${inspectVuln.file_path} (Line ${inspectVuln.line_number})`}
        >
          <div className="space-y-4 font-mono text-xs">
            <div className="p-3 rounded-lg bg-deepGrave border border-coffinBorder">
              <div className="text-[10px] text-cryptGray uppercase">Tainted Execution Sink:</div>
              <div className="text-red-400 font-bold mt-1">{inspectVuln.sink_symbol}</div>
            </div>

            <div>
              <div className="flex items-center justify-between pb-1 text-cryptGray text-[11px]">
                <span>Tree-sitter Backward Taint Slice ({inspectVuln.slice_line_count} statements isolated):</span>
                <span className="text-ghostGreen">82% Context Reduction</span>
              </div>
              <pre className="p-4 rounded-xl bg-black/80 border border-coffinBorder text-ghostGreen overflow-x-auto max-h-60 leading-relaxed">
{`# Sliced from ${inspectVuln.file_path}
def handle_request(request):
    username = request.GET.get('user', '')  # Source: Tainted Input
    cursor = db.connection.cursor()
    # Taint propagates through query concatenation:
    query = f"SELECT * FROM accounts WHERE user = '{username}'"
    cursor.execute(query)  # Sink: Arbitrary code / SQL injection`}
              </pre>
            </div>

            <div className="flex justify-end gap-2 pt-2 border-t border-coffinBorder/50">
              <Button variant="outline" size="sm" onClick={() => setInspectVuln(null)}>
                Close
              </Button>
              <Button
                variant="pumpkin"
                size="sm"
                icon={Wrench}
                onClick={() => {
                  const target = inspectVuln;
                  setInspectVuln(null);
                  handleRemediate(target);
                }}
              >
                Launch Workbench Pipeline
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </PageContainer>
  );
};

export default VulnCrypt;
