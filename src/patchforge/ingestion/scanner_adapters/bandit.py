"""Bandit SARIF scanner adapter."""
import re
from typing import Dict, Any, List
from patchforge.models.vulnerability import VulnerabilityReport


class BanditAdapter:
    """Extracts and normalizes Bandit-specific SARIF findings."""

    # Common Bandit test ID to CWE mapping
    BANDIT_CWE_MAP = {
        "B608": "CWE-89",  # Hardcoded SQL expression
        "B108": "CWE-377", # Insecure temporary file
        "B301": "CWE-502", # Pickle deserialization
        "B201": "CWE-78",  # Flask app run with debug=True / command injection
        "B303": "CWE-327", # Insecure MD5/SHA1 hash
        "B602": "CWE-78",  # Shell injection subprocess
        "B605": "CWE-78",  # Start process with shell
        "B311": "CWE-330", # Pseudo-random generator
    }

    def normalize(self, sarif: Dict[str, Any]) -> List[VulnerabilityReport]:
        reports: List[VulnerabilityReport] = []
        runs = sarif.get("runs", [])

        for run in runs:
            rules_dict = {}
            driver = run.get("tool", {}).get("driver", {})
            for r in driver.get("rules", []):
                rules_dict[r.get("id")] = r

            for idx, res in enumerate(run.get("results", [])):
                rule_id = res.get("ruleId", f"bandit-rule-{idx}")
                rule_meta = rules_dict.get(rule_id, {})
                properties = rule_meta.get("properties", {}) or res.get("properties", {})

                # Extract CWE - check explicit properties first, then fallback to map
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
                    for bandit_id, mapped_cwe in self.BANDIT_CWE_MAP.items():
                        if bandit_id in rule_id.upper():
                            cwe_id = mapped_cwe
                            break

                # If still unknown, check message text
                if cwe_id == "CWE-UNKNOWN":
                    msg = res.get("message", {}).get("text", "")
                    cwe_match = re.search(r"CWE-\d+", msg, re.IGNORECASE)
                    if cwe_match:
                        cwe_id = cwe_match.group(0).upper()

                # Severity & Skull Rating
                level = res.get("level", "warning").lower()
                bandit_severity = properties.get("issue_severity", "").upper()
                if bandit_severity == "HIGH" or level == "error":
                    severity = "HIGH"
                    skull_score = "4_skulls"
                elif bandit_severity == "MEDIUM" or level == "warning":
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
                        finding_id=f"bandit-{rule_id}-{idx}",
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
                        scanner="bandit",
                        raw_sarif_location=locs[0] if locs else None,
                        status="AWAKENING",
                    )
                )

        return reports
