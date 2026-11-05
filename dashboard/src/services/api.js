import {
  mockDashboardSummary,
  mockVulnerabilities,
  mockGraveyardTombstones,
  mockSampleDiff,
} from './mockData';

const API_BASE = '/api';

export const fetchDashboardSummary = async () => {
  try {
    const res = await fetch(`${API_BASE}/dashboard`);
    if (!res.ok) throw new Error('API fetch failed');
    return await res.json();
  } catch {
    // Graceful fallback to mock data for standalone dev
    return mockDashboardSummary;
  }
};

export const fetchVulnerabilities = async () => {
  try {
    const res = await fetch(`${API_BASE}/vulns`);
    if (!res.ok) throw new Error('API fetch failed');
    return await res.json();
  } catch {
    return mockVulnerabilities;
  }
};

export const fetchGraveyardTombstones = async () => {
  try {
    const res = await fetch(`${API_BASE}/runs`);
    if (!res.ok) throw new Error('API fetch failed');
    return await res.json();
  } catch {
    return mockGraveyardTombstones;
  }
};

export const triggerRemediationRun = async (payload) => {
  try {
    const res = await fetch(`${API_BASE}/runs/trigger`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return await res.json();
  } catch {
    return {
      status: 'INITIATED',
      run_id: `run-${Date.now()}`,
      message: 'Remediation pipeline dispatched (Mock Mode)',
    };
  }
};
