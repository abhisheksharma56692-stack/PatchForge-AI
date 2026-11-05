import React, { useState } from 'react';
import { PageContainer } from '../components/layout/PageContainer';
import { CauldronGauge } from '../components/domain/CauldronGauge';
import { Tabs } from '../components/common/Tabs';
import { Badge } from '../components/common/Badge';
import { Card } from '../components/common/Card';
import {
  ShieldAlert,
  ShieldCheck,
  Cpu,
  HardDrive,
  Clock,
  WifiOff,
  UserCheck,
  Lock,
  Terminal,
} from 'lucide-react';

export const SandboxDungeon = () => {
  const [activeConsoleTab, setActiveConsoleTab] = useState('pytest');

  const consoleTabs = [
    { id: 'pytest', label: '1. Unit & Regression Tests (Must PASS)' },
    { id: 'exploit', label: '2. Dynamic Exploit PoC (Must BLOCK)' },
    { id: 'mutation', label: '3. AST Mutation Testing (Score >= 85%)' },
    { id: 'deltasast', label: '4. Delta-SAST Re-Scan (0 Findings)' },
  ];

  const consoleOutputs = {
    pytest: `============================= test session starts ==============================
platform linux -- Python 3.11.8, pytest-8.1.1, pluggy-1.4.0
rootdir: /workspace
collected 142 items

tests/unit/test_auth.py ..................................               [ 23%]
tests/unit/test_database.py ....................................         [ 49%]
tests/unit/test_api_views.py ........................................... [ 79%]
tests/integration/test_user_flow.py ..............................       [100%]

============================= 142 passed in 4.12s ==============================
[SANDBOX STATUS] Functional Invariance Verified: 0 regressions introduced.`,

    exploit: `🕷️ [RED TEAM EXPLOIT RUNNER] Launching dynamic reproduction test...
Target: backend/views/user.py
Payload: username = "admin' OR '1'='1"

[PHASE A: Pre-Patch Baseline]
> GET /api/user?username=admin' OR '1'='1
< HTTP 200 OK (SQL Injection successful: 42 records leaked)
STATUS: ❌ VULNERABILITY CONFIRMED

[PHASE B: Post-Patch Evaluation]
> Applying Patch: git apply candidate.patch
> GET /api/user?username=admin' OR '1'='1
< HTTP 404 Not Found (Treated as literal username string: 'admin\\' OR \\'1\\'=\\'1')
STATUS: ✅ ATTACK DEFENDED / EXPLOIT NEUTRALIZED`,

    mutation: `🧬 [MUTMUT AST MUTATION HARNESS] Injecting atomic AST mutants into patched nodes...
Target File: backend/views/user.py (Lines 39-48)
Total Injected Mutants: 14

Mutant #1 (Line 41): query string literal inversion ..... KILLED by test_auth.py
Mutant #2 (Line 42): parameter array list removal ....... KILLED by test_auth.py
Mutant #3 (Line 43): cursor.execute -> None ............. KILLED by test_api_views.py
Mutant #4 (Line 44): record fetchone -> return mock ..... KILLED by test_user_flow.py
Mutant #5 (Line 45): if not record inverted ............. KILLED by test_api_views.py
...
Mutant #14 (Line 48): 404 status code -> 200 ............ KILLED by test_api_views.py

Killed: 13 / 14 Mutants (1 equivalent mutant)
Mutation Score: 92.8% (Threshold >= 85.0% MET) ✅`,

    deltasast: `🔍 [DELTA-SAST SCANNER] Executing in-container static analyzer re-scan...
Engine: Semgrep CLI v1.68.0
Ruleset: p/security-audit, p/owasp-top-ten, p/cwe-top-25
Scanning /workspace...

Findings Summary:
- Original Finding (python.django.security.injection.sql.sql-injection): ELIMINATED (0 findings)
- New Introduced Findings: 0
Status: CLEAN ✅`,
  };

  return (
    <PageContainer
      title="🧪 The Sandbox Dungeon"
      subtitle="Hermetic, rootless, air-gapped micro-containers verifying untrusted AI patches under strict kernel cgroups"
      action={
        <div className="flex items-center gap-2">
          <Badge variant="neutralized" icon={WifiOff}>
            AIR-GAP: --network none
          </Badge>
          <Badge variant="purple" icon={UserCheck}>
            ROOTLESS: UID 1001
          </Badge>
        </div>
      }
    >
      {/* 4 Hardened Security Banners */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-deepGrave border border-ghostGreen/40 flex items-center gap-3">
          <div className="p-2 rounded-lg bg-ghostGreen/10 text-ghostGreen">
            <WifiOff className="w-5 h-5" />
          </div>
          <div className="font-mono text-xs">
            <div className="text-cryptGray uppercase text-[10px]">Network Isolation</div>
            <div className="text-ghostGreen font-bold mt-0.5">Air-Gapped (None)</div>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-deepGrave border border-coffinBorder flex items-center gap-3">
          <div className="p-2 rounded-lg bg-coffinPurple text-pumpkinOrange">
            <Lock className="w-5 h-5" />
          </div>
          <div className="font-mono text-xs">
            <div className="text-cryptGray uppercase text-[10px]">Privilege Escalation</div>
            <div className="text-boneWhite font-bold mt-0.5">no-new-privileges</div>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-deepGrave border border-coffinBorder flex items-center gap-3">
          <div className="p-2 rounded-lg bg-coffinPurple text-pumpkinOrange">
            <HardDrive className="w-5 h-5" />
          </div>
          <div className="font-mono text-xs">
            <div className="text-cryptGray uppercase text-[10px]">Root Filesystem</div>
            <div className="text-boneWhite font-bold mt-0.5">read_only + tmpfs</div>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-deepGrave border border-cauldronGold/40 flex items-center gap-3">
          <div className="p-2 rounded-lg bg-cauldronGold/10 text-cauldronGold">
            <Clock className="w-5 h-5" />
          </div>
          <div className="font-mono text-xs">
            <div className="text-cryptGray uppercase text-[10px]">Watchdog Timer</div>
            <div className="text-cauldronGold font-bold mt-0.5">60s Hard Limit</div>
          </div>
        </div>
      </div>

      {/* Cauldron Resource Telemetry Gauges */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <CauldronGauge
          value={85}
          label="CPU Core Allotment"
          metric="1.7 / 2.0 Cores"
          threshold={80}
          colorScheme="orange"
        />
        <CauldronGauge
          value={68}
          label="Memory (cgroup limit)"
          metric="1392 / 2048 MB"
          threshold={85}
          colorScheme="green"
        />
        <CauldronGauge
          value={92.8}
          label="Mutation Score"
          metric="92.8%"
          threshold={85}
          colorScheme="green"
        />
      </div>

      {/* Live In-Container Execution Stream */}
      <Card
        title="Ephemeral Container Verification Stream"
        subtitle="Dual-condition test gate execution output (pytest + reproduction exploit + mutmut + Semgrep)"
        icon={Terminal}
      >
        <Tabs
          tabs={consoleTabs}
          activeTab={activeConsoleTab}
          onChange={setActiveConsoleTab}
          className="mb-4"
        />

        <pre className="p-4 rounded-xl bg-black/90 border border-coffinBorder text-slimeLime font-mono text-xs overflow-x-auto max-h-[380px] leading-relaxed select-text">
          {consoleOutputs[activeConsoleTab]}
        </pre>
      </Card>
    </PageContainer>
  );
};

export default SandboxDungeon;
