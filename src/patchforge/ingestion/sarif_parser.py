"""SARIF v2.1.0 JSON schema parser, validator, and normalizer."""
import json
import os
import re
from typing import List, Dict, Any, Optional

from patchforge.models.vulnerability import (
    VulnerabilityReport,
    VulnerabilityLocation,
    SARIFFinding,
)
from patchforge.ingestion.scanner_adapters.semgrep import SemgrepAdapter
from patchforge.ingestion.scanner_adapters.snyk import SnykAdapter
from patchforge.ingestion.scanner_adapters.bandit import BanditAdapter


def validate_sarif_schema(raw: Dict[str, Any]) -> bool:
    """Validates that a dictionary conforms to the basic SARIF v2.1.0 structural schema."""
    if not isinstance(raw, dict):
        return False
    
    # Must have runs array
    if "runs" not in raw or not isinstance(raw["runs"], list):
        return False
    
    # Version should ideally be 2.1.0 or schema present
    version = raw.get("version", "")
    schema = raw.get("$schema", "")
    if version != "2.1.0" and "sarif" not in schema.lower():
        # If neither version 2.1.0 nor sarif schema header is present, invalid
        return False
        
    return True


def normalize_location(location: Dict[str, Any]) -> VulnerabilityLocation:
    """Extracts a normalized VulnerabilityLocation from a SARIF physicalLocation object."""
    phys = location.get("physicalLocation", {})
    art = phys.get("artifactLocation", {})
    file_path = art.get("uri", "unknown")
    region = phys.get("region", {})
    start_line = region.get("startLine", 1)
    end_line = region.get("endLine", start_line)
    start_col = region.get("startColumn", 1)
    end_col = region.get("endColumn", 1)
    snippet = region.get("snippet", {}).get("text", "")

    return VulnerabilityLocation(
        file_path=file_path,
        start_line=start_line,
        end_line=end_line,
        start_col=start_col,
        end_col=end_col,
        sink_symbol=snippet.strip() if snippet else "",
        skull_rating="3_skulls",
    )


def extract_findings(sarif: Dict[str, Any]) -> List[SARIFFinding]:
    """Extracts raw SARIFFinding objects across all runs."""
    findings: List[SARIFFinding] = []
    runs = sarif.get("runs", [])

    for run in runs:
        driver = run.get("tool", {}).get("driver", {})
        scanner_name = driver.get("name", "generic").lower()
        rules_dict = {r.get("id"): r for r in driver.get("rules", [])}

        for idx, res in enumerate(run.get("results", [])):
            rule_id = res.get("ruleId", f"rule-{idx}")
            rule_meta = rules_dict.get(rule_id, {})
            message = res.get("message", {}).get("text", "")
            severity = res.get("level", "warning").upper()

            # Extract CWE
            props = rule_meta.get("properties", {})
            cwe_id = "CWE-UNKNOWN"
            cwe_list = props.get("cwe", [])
            if isinstance(cwe_list, list) and cwe_list:
                cwe_match = re.search(r"CWE-\d+", str(cwe_list[0]), re.IGNORECASE)
                if cwe_match:
                    cwe_id = cwe_match.group(0).upper()
            elif isinstance(cwe_list, str):
                cwe_match = re.search(r"CWE-\d+", cwe_list, re.IGNORECASE)
                if cwe_match:
                    cwe_id = cwe_match.group(0).upper()

            locs = res.get("locations", [])
            loc = normalize_location(locs[0]) if locs else VulnerabilityLocation(
                file_path="unknown", start_line=1, end_line=1
            )

            findings.append(
                SARIFFinding(
                    rule_id=rule_id,
                    cwe_id=cwe_id,
                    message=message,
                    severity=severity,
                    location=loc,
                    scanner_source=scanner_name,
                )
            )

    return findings


def parse_sarif_file(file_path: str) -> List[VulnerabilityReport]:
    """Parses a SARIF file from disk, validates schema, and normalizes into VulnerabilityReports."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"SARIF file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            raw_data = json.load(f)
        except json.JSONDecodeError as err:
            raise ValueError(f"Invalid JSON in SARIF file {file_path}: {err}") from err

    if not validate_sarif_schema(raw_data):
        raise ValueError(f"File {file_path} does not match valid SARIF v2.1.0 schema")

    # Detect scanner
    runs = raw_data.get("runs", [])
    if not runs:
        return []

    first_run = runs[0]
    driver_name = first_run.get("tool", {}).get("driver", {}).get("name", "").lower()

    if "semgrep" in driver_name:
        adapter = SemgrepAdapter()
        return adapter.normalize(raw_data)
    elif "snyk" in driver_name:
        adapter = SnykAdapter()
        return adapter.normalize(raw_data)
    elif "bandit" in driver_name:
        adapter = BanditAdapter()
        return adapter.normalize(raw_data)
    else:
        # Fallback to Semgrep adapter or generic conversion
        adapter = SemgrepAdapter()
        reports = adapter.normalize(raw_data)
        if not reports:
            # Map findings directly
            findings = extract_findings(raw_data)
            for f in findings:
                reports.append(
                    VulnerabilityReport(
                        finding_id=f"generic-{f.rule_id}",
                        cwe_id=f.cwe_id,
                        title=f.rule_id,
                        description=f.message,
                        severity=f.severity,
                        skull_score="3_skulls",
                        file_path=f.location.file_path,
                        start_line=f.location.start_line,
                        end_line=f.location.end_line,
                        start_col=f.location.start_col,
                        end_col=f.location.end_col,
                        sink_symbol=f.location.sink_symbol,
                        scanner=f.scanner_source,
                        status="AWAKENING",
                    )
                )
        return reports

