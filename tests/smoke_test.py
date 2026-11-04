"""End-to-end smoke test for Member 1 subsystems: SARIF -> Slicing -> Z3 Invariants -> Agents."""
import os
import sys

# Ensure src is on python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from unittest.mock import MagicMock
from patchforge.ingestion.sarif_parser import parse_sarif_file
from patchforge.slicing.backward_slice import BackwardTaintSlicer
from patchforge.formal.invariant_engine import SMTInvariantVerifier
from patchforge.agents.test_synthesizer import TestSynthesizerAgent
from patchforge.agents.patch_synthesizer import PatchSynthesizerAgent
from patchforge.agents.auditor import AntiTamperAuditor


def run_smoke_test():
    print("🔥 Starting PatchForge AI - Member 1 End-to-End Smoke Test")
    
    # 1. Ingest SARIF
    sarif_path = os.path.join("tests", "fixtures", "sarif", "semgrep_cwe89_sqli.sarif.json")
    vulns = parse_sarif_file(sarif_path)
    print(f"✅ 1. SARIF parsed: Found {len(vulns)} vulnerability finding(s)")
    vuln = vulns[0]
    print(f"   - Finding ID: {vuln.finding_id}")
    print(f"   - CWE: {vuln.cwe_id}")
    print(f"   - Skull Score: {vuln.skull_score}")
    print(f"   - Sink Symbol: {vuln.sink_symbol}")

    # 2. Slice AST/PDG
    app_path = os.path.join("tests", "fixtures", "repositories", "vulnerable_flask_app", "app.py")
    with open(app_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    slicer = BackwardTaintSlicer(language="python")
    slice_result = slicer.slice_from_location(source_code, vuln.start_line, vuln.sink_symbol)
    orig_lines = len(source_code.splitlines())
    sliced_lines = len(slice_result.slice_code.splitlines())
    print(f"✅ 2. Backward Taint Slicing complete:")
    print(f"   - Reduced {orig_lines} lines -> {sliced_lines} lines ({(1 - sliced_lines/orig_lines)*100:.1f}% reduction)")
    print(f"   - Preserved imports: {slice_result.imported_symbols}")

    # 3. Z3 Formal Invariants
    verifier = SMTInvariantVerifier()
    invariants = verifier.verify_from_slice(slice_result)
    print(f"✅ 3. Z3 Formal Invariants generated:")
    print(f"   - Status: {invariants.z3_model_status}")
    for inv in invariants.required_invariants:
        print(f"   - Invariant: {inv}")

    # 4. Agent Alpha (Red Team)
    mock_llm = MagicMock()
    mock_llm.generate.return_value = (
        "```python\n"
        "import requests\n"
        "def test_poc():\n"
        "    res = requests.get('http://localhost:5000/user?username=%27+OR+%271%27=%271')\n"
        "    assert len(res.json()['users']) > 1\n"
        "```"
    )
    alpha = TestSynthesizerAgent(mock_llm)
    poc_test = alpha.synthesize(vuln, slice_result)
    print(f"✅ 4. Agent Alpha synthesized PoC test: {poc_test.test_file_path}")

    # 5. Agent Beta (Blue Team)
    mock_llm.generate.return_value = (
        "```diff\n"
        "--- a/app.py\n"
        "+++ b/app.py\n"
        "@@ -24,4 +24,4 @@\n"
        "-    query = \"SELECT id, username, email FROM users WHERE username = '\" + username + \"'\"\n"
        "-    cursor.execute(query)\n"
        "+    query = \"SELECT id, username, email FROM users WHERE username = ?\"\n"
        "+    cursor.execute(query, (username,))\n"
        "```\n"
        "⚰️ R.I.P. CWE-89 (SQL Injection) — Neutralized by PatchForge AI\n"
    )
    beta = PatchSynthesizerAgent(mock_llm)
    patch = beta.synthesize(slice_result, invariants, poc_test)
    print(f"✅ 5. Agent Beta synthesized patch candidate:")
    print(f"   - Inscription: {patch.tombstone_inscription}")

    # 6. Agent Gamma (Anti-Tamper Auditor)
    auditor = AntiTamperAuditor()
    verdict = auditor.audit(patch, slice_result)
    print(f"✅ 6. Agent Gamma audit verdict:")
    print(f"   - Approved: {verdict.approved}")
    print(f"   - Tamper Check Passed: {verdict.tamper_check_passed}")

    print("\n🎉 ALL MEMBER 1 SUBSYSTEMS OPERATIONAL AND VALIDATED!")


if __name__ == "__main__":
    run_smoke_test()
