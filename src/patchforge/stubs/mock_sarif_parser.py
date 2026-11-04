"""Mock SARIF parser stub for independent Member 2 development."""
from typing import List, Dict, Any
from patchforge.models.vulnerability import VulnerabilityReport, VulnerabilityLocation


def parse_sarif_file(file_path: str) -> List[VulnerabilityReport]:
    """Returns a realistic mock vulnerability finding matching Member 1 models."""
    return [
        VulnerabilityReport(
            finding_id="mock-semgrep-cwe89-0",
            cwe_id="CWE-89",
            title="SQL Injection in user lookup",
            description="Direct string concatenation in SQL execute() sink",
            severity="HIGH",
            skull_score="4_skulls",
            file_path="app.py",
            start_line=28,
            end_line=28,
            start_col=9,
            end_col=45,
            sink_symbol="cursor.execute(query)",
            scanner="semgrep",
            status="AWAKENING",
            tombstone_inscription="⚰️ R.I.P. CWE-89 (SQL Injection) — Neutralized by PatchForge",
        )
    ]

