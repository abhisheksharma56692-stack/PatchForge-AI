"""Snyk SARIF scanner adapter."""
import re
from typing import Dict, Any, List
from patchforge.models.vulnerability import VulnerabilityReport


class SnykAdapter:
    """Extracts and normalizes Snyk-specific SARIF findings."""

    def normalize(self, sarif: Dict[str, Any]) -> List[VulnerabilityReport]:
        reports: List[VulnerabilityReport] = []
        runs = sarif.get("runs", [])

        for run in runs:
            rules_dict = {}
            driver = run.get("tool", {}).get("driver", {})
            for r in driver.get("rules", []):
                rules_dict[r.get("id")] = r

            for idx, res in enumerate(run.get("results", [])):
                rule_id = res.get("ruleId", f"snyk-rule-{idx}")
                rule_meta = rules_dict.get(rule_id, {})
                properties = rule_meta.get("properties", {}) or res.get("properties", {})

                # Extract CWE
                cwe_id = "CWE-UNKNOWN"
                cwe_list = properties.get("cwe", [])
                if isinstance(cwe_list, list) and cwe_list:
                    cwe_match = re.search(r"CWE-\d+", str(cwe_list[0]), re.IGNORECASE)
                    if cwe_match:
                        cwe_id = cwe_match.group(0).upper()
                elif isinstance(cwe_list, str):
                    cwe_match = re.search(r"CWE-\d+", cwe_list, re.IGNORECASE)
                    if cwe_match:
                        cwe_id = cwe_match.group(0).upper()

                if cwe_id == "CWE-UNKNOWN":
                    # Check tags or relationships
                    for tag in properties.get("tags", []):
                        cwe_match = re.search(r"CWE-\d+", str(tag), re.IGNORECASE)
                        if cwe_match:
                            cwe_id = cwe_match.group(0).upper()
                            break

                # Severity & Skull Rating
                level = res.get("level", "warning").lower()
                cvss_score = properties.get("cvssV3_baseScore")
                if cvss_score and float(cvss_score) >= 9.0:
                    severity = "CRITICAL"
                    skull_score = "5_skulls"
                elif level == "error" or (cvss_score and float(cvss_score) >= 7.0):
                    severity = "HIGH"
                    skull_score = "4_skulls"
                elif level == "warning" or (cvss_score and float(cvss_score) >= 4.0):
                    severity = "MEDIUM"
                    skull_score = "3_skulls"
                else:
                    severity = "LOW"
                    skull_score = "2_skulls"

                # Location
                locs = res.get("locations", [])
                file_path = "unknown"
                start_line = 1
                end_line = 1
                start_col = 1
                end_col = 1
                sink_symbol = ""

                if locs:
                    phys = locs[0].get("physicalLocation", {})
                    art = phys.get("artifactLocation", {})
                    file_path = art.get("uri", "unknown")
                    reg = phys.get("region", {})
                    start_line = reg.get("startLine", 1)
                    end_line = reg.get("endLine", start_line)
                    start_col = reg.get("startColumn", 1)
                    end_col = reg.get("endColumn", 1)
                    snippet = reg.get("snippet", {}).get("text", "")
                    if snippet:
                        sink_symbol = snippet.strip()

                message = res.get("message", {}).get("text", rule_id)
                short_desc = rule_meta.get("shortDescription", {}).get("text", rule_id)

                reports.append(
                    VulnerabilityReport(
                        finding_id=f"snyk-{rule_id}-{idx}",
                        cwe_id=cwe_id,
                        title=short_desc or rule_id,
                        description=message,
                        severity=severity,
                        skull_score=skull_score,
                        file_path=file_path,
                        start_line=start_line,
                        end_line=end_line,
                        start_col=start_col,
                        end_col=end_col,
                        sink_symbol=sink_symbol,
                        scanner="snyk",
                        raw_sarif_location=locs[0] if locs else None,
                        status="AWAKENING",
                    )
                )

        return reports

