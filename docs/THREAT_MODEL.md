# PatchForge AI: Threat Model (STRIDE Methodology)

## 1. Overview
Executing untrusted, AI-generated code that modifies security-sensitive applications requires a defense-in-depth security model. This document formalizes the threat model using the STRIDE framework.

---

## 2. STRIDE Threat Matrix

| STRIDE Category | Threat Scenario | Impact | PatchForge Mitigation |
| :--- | :--- | :--- | :--- |
| **Spoofing** | Attacker spoofs an automated PR to inject malicious backdoors into master branch. | Critical | All generated Git commits are cryptographically signed using a dedicated **GPG key**. PRs originate strictly from an authorized service account. |
| **Tampering** | AI modifies existing unit test files, deletes assertions, or weakens `.semgrep.yml` rules to "force" tests to pass. | High | **Agent Gamma (Anti-Tamper Auditor):** Validates unified diffs; modifications to test directories, assertion deletions, or scanner configs are rejected outright. |
| **Repudiation** | Developers unable to verify why or how a specific patch was synthesized. | Medium | Every PR attaches a complete cryptographic **Verification Bill of Materials (V-BOM)**: raw SARIF input, Z3 formal proofs, and execution logs. |
| **Information Disclosure** | Vulnerable code, proprietary IP, or container secrets leaked to third parties via LLM calls or outbound traffic. | High | 1. Tree-sitter slicing minimizes transmitted context by 85%.<br>2. Containers execute with `--network none` (zero sockets permitted). |
| **Denial of Service** | Patch introduces infinite loops, memory leaks, or fork-bombs during compilation or sandbox testing. | Medium | Micro-sandbox applies hard Linux kernel cgroup constraints: 2.0 CPU cores, 2048MB memory, PID limit 100, and a 60-second hardware wall-clock timeout. |
| **Elevation of Privilege**| Candidate patch attempts container escape via kernel vulnerabilities or mounts host directories. | Critical | Container runtime runs strictly in rootless mode with `--cap-drop ALL`, `no-new-privileges:true`, and a read-only root filesystem. |

