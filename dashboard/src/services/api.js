/**
 * API service calling the FastAPI backend.
 */
const BASE_URL = '/api';

export async function fetchDashboardSummary() {
  try {
    const res = await fetch(`${BASE_URL}/dashboard`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn('Using fallback summary:', err);
    return {
      total_vulnerabilities: 12,
      open_skulls: 3,
      in_progress_bats: 2,
      remediated_ghosts: 7,
      mean_time_to_remediate_sec: 184.5,
      pipeline_health_percent: 98.5,
      active_runs: 1,
    };
  }
}

export async function fetchVulnerabilities() {
  try {
    const res = await fetch(`${BASE_URL}/vulns`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn('Using fallback vulns:', err);
    return [
      {
        finding_id: 'semgrep-cwe89-01',
        cwe_id: 'CWE-89',
        title: 'SQL Injection in user authentication',
        severity: 'HIGH',
        skull_rating: '4_skulls',
        file_path: 'backend/views/user.py',
        start_line: 28,
        scanner: 'semgrep',
        status: 'AWAKENING',
        exposure_age_hours: 0.5,
      },
      {
        finding_id: 'bandit-cwe22-02',
        cwe_id: 'CWE-22',
        title: 'Path Traversal in document download',
        severity: 'CRITICAL',
        skull_rating: '5_skulls',
        file_path: 'routes/download.py',
        start_line: 15,
        scanner: 'bandit',
        status: 'CONJURING',
        exposure_age_hours: 1.8,
      },
    ];
  }
}

export async function fetchRuns() {
  try {
    const res = await fetch(`${BASE_URL}/runs`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function fetchGraveyard() {
  try {
    const res = await fetch(`${BASE_URL}/runs/graveyard`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    return [
      {
        run_id: 'run-cwe89-42',
        cwe_id: 'CWE-89',
        status: 'TOMBSTONE_READY',
        duration: 12.4,
        pr_url: 'https://github.com/org/repo/pull/42',
        timestamp: Date.now() / 1000 - 3600,
        tombstone_inscription: '⚰️ R.I.P. CWE-89 (SQL Injection) — Neutralized by PatchForge AI',
      },
    ];
  }
}

