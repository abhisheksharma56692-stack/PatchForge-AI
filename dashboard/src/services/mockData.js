// High-fidelity fallback fixtures for standalone testing of PatchForge AI Dashboard

export const mockDashboardSummary = {
  total_vulnerabilities: 18,
  open_skulls: 4,
  in_progress_bats: 2,
  remediated_ghosts: 12,
  mean_time_to_remediate_sec: 142.5,
  pipeline_health_percent: 99.4,
  aws_bedrock_tokens_used: 124890,
  sandbox_containers_spawned: 36,
};

export const mockVulnerabilities = [
  {
    id: 'vuln-001',
    cwe_id: 'CWE-89',
    cve_id: 'CVE-2026-3819',
    title: 'SQL Injection in User Authentication Endpoint',
    severity: 'CRITICAL',
    skulls: 5,
    file_path: 'backend/views/user.py',
    line_number: 42,
    sink_symbol: 'cursor.execute(f"SELECT * FROM users WHERE username = \'{user}\'")',
    scanner: 'Semgrep v1.68',
    detected_at: '2026-11-04T14:20:00Z',
    status: 'IN_REMEDIATION',
    slice_line_count: 28,
  },
  {
    id: 'vuln-002',
    cwe_id: 'CWE-22',
    cve_id: 'CVE-2026-4012',
    title: 'Improper Limitation of a Pathname to a Restricted Directory',
    severity: 'HIGH',
    skulls: 4,
    file_path: 'backend/handlers/file_storage.py',
    line_number: 89,
    sink_symbol: 'open(os.path.join(BASE_DIR, filename), "rb")',
    scanner: 'Bandit v1.7.5',
    detected_at: '2026-11-04T15:10:00Z',
    status: 'TRIAGED',
    slice_line_count: 32,
  },
  {
    id: 'vuln-003',
    cwe_id: 'CWE-79',
    cve_id: 'CVE-2026-2911',
    title: 'Cross-Site Scripting (XSS) via Unsanitized Template Output',
    severity: 'MEDIUM',
    skulls: 3,
    file_path: 'frontend/templates/profile.html',
    line_number: 115,
    sink_symbol: 'innerHTML = user_bio_raw',
    scanner: 'Snyk Code',
    detected_at: '2026-11-04T16:05:00Z',
    status: 'QUEUED',
    slice_line_count: 18,
  },
  {
    id: 'vuln-004',
    cwe_id: 'CWE-787',
    cve_id: 'CVE-2026-5510',
    title: 'Out-of-bounds Write in String Buffer Tokenizer',
    severity: 'CRITICAL',
    skulls: 5,
    file_path: 'native/tokenizer.c',
    line_number: 164,
    sink_symbol: 'strcpy(buffer + offset, input)',
    scanner: 'CodeQL',
    detected_at: '2026-11-04T16:30:00Z',
    status: 'QUEUED',
    slice_line_count: 42,
  },
];

export const mockGraveyardTombstones = [
  {
    id: 'grave-001',
    cwe_id: 'CWE-89',
    title: 'SQL Injection in Account Search Query',
    file_path: 'backend/routes/accounts.py',
    resolved_at: '2026-11-04T12:00:00Z',
    mttr_seconds: 135,
    pr_url: 'https://github.com/patchforge-org/demo-repo/pull/104',
    pr_number: 104,
    mutation_score: 93.8,
    remediated_by: 'Agent Beta + Z3 Solver',
  },
  {
    id: 'grave-002',
    cwe_id: 'CWE-22',
    title: 'Path Traversal via User File Download Route',
    file_path: 'backend/services/storage_service.py',
    resolved_at: '2026-11-03T18:45:00Z',
    mttr_seconds: 158,
    pr_url: 'https://github.com/patchforge-org/demo-repo/pull/103',
    pr_number: 103,
    mutation_score: 91.2,
    remediated_by: 'Agent Beta + Z3 Solver',
  },
  {
    id: 'grave-003',
    cwe_id: 'CWE-79',
    title: 'Stored XSS in Comment Field',
    file_path: 'web/controllers/comments.js',
    resolved_at: '2026-11-03T11:20:00Z',
    mttr_seconds: 112,
    pr_url: 'https://github.com/patchforge-org/demo-repo/pull/102',
    pr_number: 102,
    mutation_score: 96.0,
    remediated_by: 'Agent Beta',
  },
  {
    id: 'grave-004',
    cwe_id: 'CWE-502',
    title: 'Deserialization of Untrusted Data via Python Pickle',
    file_path: 'workers/task_queue.py',
    resolved_at: '2026-11-02T19:10:00Z',
    mttr_seconds: 174,
    pr_url: 'https://github.com/patchforge-org/demo-repo/pull/101',
    pr_number: 101,
    mutation_score: 89.5,
    remediated_by: 'Agent Beta + Z3 Solver',
  },
];

export const mockSampleDiff = `--- a/backend/views/user.py
+++ b/backend/views/user.py
@@ -39,7 +39,8 @@
 def get_user_profile(request, username):
     cursor = connection.cursor()
-    query = f"SELECT id, username, email FROM users WHERE username = '{username}'"
-    cursor.execute(query)
+    query = "SELECT id, username, email FROM users WHERE username = %s"
+    cursor.execute(query, [username])
     record = cursor.fetchone()
     if not record:
         return JsonResponse({"error": "User not found"}, status=404)`;

export const mockLiveTerminalLogs = [
  '🕷️ [SARIF INGEST] Ingested 1 report (Rule: python.django.security.injection.sql)',
  '🔬 [AST SLICER] Parsed Concrete Syntax Tree via Tree-sitter (Python 3.11)',
  '📐 [PDG BUILDER] Generated Program Dependence Graph (Nodes: 48, Edges: 72)',
  '✂️ [BACKWARD SLICE] Extracted minimal taint slice: 28 statements isolated (84.2% reduction)',
  '🔮 [Z3 SMT PROVER] Formulating First-Order Logic boundary safety theorem...',
  '✅ [Z3 SMT PROVER] Theorem PROVED: SATISFIABLE_INVARIANT (Parametric query constraint enforced)',
  '🤖 [AGENT ALPHA] Synthesized deterministic dynamic reproduction test (test_cwe89_poc.py)',
  '📦 [SANDBOX] Mounting unpatched codebase inside rootless micro-container (--network none)...',
  '❌ [SANDBOX EVAL] Reproduction exploit TRIGGERED: Target confirmed vulnerable',
  '🤖 [AGENT BETA] Synthesizing minimal unified diff patch under Z3 invariants...',
  '🛡️ [AGENT GAMMA] Anti-Tamper Audit: Diff verified clean (Zero test deletions, Zero config tampering)',
  '📦 [SANDBOX] Mounting candidate patch: git apply candidate.patch',
  '🧪 [SANDBOX RUNNER] Executing baseline test suite: 142/142 tests PASSED (0 regressions)',
  '🛡️ [SANDBOX RUNNER] Re-executing reproduction exploit: ATTACK BLOCKED / NEUTRALIZED ✅',
  '🧬 [MUTATION ENGINE] Running mutmut on patched lines: 14 mutants generated',
  '💥 [MUTATION ENGINE] 13/14 mutants killed -> Mutation Score: 92.8% (Target >= 85%)',
  '🔍 [DELTA-SAST] Executing Semgrep re-scan inside sandbox: 0 findings matching CWE-89',
  '🔏 [VCS DISPATCH] Created branch patchforge/remediate-cwe-89-9a4f with GPG-signed commit',
  '🚀 [PULL REQUEST] Published GitHub PR #104: Verified Remediation ready for review',
];

