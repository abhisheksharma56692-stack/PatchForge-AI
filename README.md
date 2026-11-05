# 🎃 PatchForge AI — Unified Autonomous Remediation & Formal Verification Engine

> Transitioning modern DevSecOps from passive alert generation to deterministic, formally verified remediation.

---

## 📑 Core Documentation & Deliverables

* **🏆 [MVP Specification & Architecture Audit (MVP.md)](./MVP.md):** Complete Minimum Viable Product specification, 8-stage pipeline walk-through, benchmark matrix, and test verification report.
* **📊 [Downloadable Presentation Pitch Deck (.pptx)](./PatchForge_AI_Pitch_Deck.pptx):** 10-slide enterprise deck covering Idea, Problem, Solution, Architecture, Multi-Agent Duel, Hermetic Sandbox, AWS Integration, Halloween UI, and Implementation.
* **📐 [Comprehensive Architecture Blueprint (ARCHITECTURE.md)](./ARCHITECTURE.md):** C4 diagrams, STRIDE threat model, and technical specifications.
* **👥 [Team Division Task Sheets](./MEMBER_1_TASKS.md):** Independent breakdown for Member 1 (AI & Analysis - 45 files) and Member 2 (Infra & UI - 88 files).

---

## 🌟 Key Features

1. **Symbolic AST & PDG Slicing:** Uses Tree-sitter and NetworkX to generate Program Dependence Graphs (PDGs), reducing transmitted code by $80\text{--}90\%$ to eliminate context bloat and hallucination.
2. **SMT Solver Formal Invariants:** Translates code boundaries into First-Order Logic (FOL) verified by Microsoft Z3 to guarantee mathematical correctness.
3. **Adversarial Dual-Agent Orchestration:** Agent Alpha (Red Team) synthesizes PoC exploit tests, while Agent Beta (Blue Team) synthesizes minimal unified diffs overseen by Agent Gamma (Anti-Tamper Auditor).
4. **Hermetic Rootless Sandboxing:** Ephemeral micro-containers executed with `--network none`, `--read-only` rootfs, and strict cgroups quotas.
5. **Mutation Testing & Delta-SAST:** Enforces $\ge 85\%$ mutant kill score and asserts 0 residual static analysis warnings.
6. **AWS Cloud-Native Backend:** Integrated with **Amazon S3**, **AWS Bedrock** (Claude 3.5 Sonnet), **Amazon SQS**, **Amazon DynamoDB**, and **Amazon ECR**.
7. **🎃 Halloween Operations Dashboard:** Interactive real-time console with animated state machine visualizer, Vulnerability Crypt, and historical Graveyard.

---

## 🚀 Quick Start

### 1. One-Click Launchers (Recommended)
```powershell
# Option A: Launch Full Stack (Backend API + Database + Frontend UI)
.\start_all.bat

# Option B: Run Interactive Terminal MVP Remediation Demo
.\start_mvp_demo.bat
```

### 2. Manual Startup
```bash
# Terminal 1: Backend API & WebSocket Engine
.\start_backend.bat

# Terminal 2: Halloween React Operations Dashboard
.\start_frontend.bat
```
- **Operations Dashboard:** [http://localhost:5173](http://localhost:5173)
- **Backend API & Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3. Run Autonomous Remediation CLI
```bash
patchforge run \
  --sarif ./tests/fixtures/sarif/semgrep_cwe89_sqli.sarif.json \
  --repo-path ./ \
  --language python \
  --aws-region us-east-1
```

---

## 🧪 Running Tests

```bash
# Run Member 1 Unit Tests (SARIF, AST Slicing, Z3, Bedrock, Agents)
pytest tests/unit/ -v

# Run Member 2 Integration Tests (AWS Services, Sandbox, Dashboard, Delivery)
pytest tests/integration/ -v

# Run All Tests
pytest
```

