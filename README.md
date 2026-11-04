# 🎃 PatchForge AI — Unified Autonomous Remediation & Formal Verification Engine

> Transitioning modern DevSecOps from passive alert generation to deterministic, formally verified remediation.

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

### 1. Installation
```bash
pip install -r requirements.txt
pip install -e .
```

### 2. Run Autonomous Remediation CLI
```bash
patchforge run \
  --sarif ./tests/fixtures/sarif/semgrep_cwe89_sqli.sarif.json \
  --repo-path ./ \
  --language python \
  --aws-region us-east-1
```

### 3. Launch the 🎃 Halloween Dashboard
```bash
# Terminal 1: Backend API Server
uvicorn patchforge.api.server:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: React Frontend UI
cd dashboard
npm install
npm run dev
# Open browser at: http://localhost:5173
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

