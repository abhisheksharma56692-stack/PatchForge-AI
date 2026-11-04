# PatchForge AI: Enterprise Deployment Guide

## 1. Deployment Modalities

PatchForge AI is designed for four deployment configurations across enterprise environments, all backed by **AWS cloud services**:

### 1.1 Mode A: Native GitHub Actions / GitLab CI Runner
Integrates directly into target repository pipelines.
- Triggered on PR creation or nightly scheduled SAST scans.
- Ingests CI-generated SARIF artifacts and uploads to **Amazon S3**.
- Pulls hardened sandbox images from **Amazon ECR**.
- Autonomously generates remediation branches and Pull Requests.

```yaml
# Sample GitHub Action Workflow Step
- name: Run PatchForge AI Remediation
  uses: docker://123456789012.dkr.ecr.us-east-1.amazonaws.com/patchforge:latest
  with:
    sarif: ./reports/semgrep.sarif
    aws-region: us-east-1
    auto-pr: true
```

---

### 1.2 Mode B: Centralized AWS Kubernetes DevSecOps Daemon (Amazon EKS)
Deployed as a scalable microservice on **Amazon EKS**:
- Listens to organization-wide webhook events from GitHub Enterprise / GitLab via **Amazon SQS** event queue.
- LLM inference routed through **AWS Bedrock** (Claude 3.5 Sonnet) — zero self-hosted GPU infrastructure.
- Multi-tenant sandboxing using rootless Podman or gVisor (`runsc`).
- Audit trail telemetry stored in **Amazon DynamoDB**.

---

### 1.3 Mode C: Security Engineer CLI (`patchforge-cli`)
Interactive, local developer experience:
```bash
export AWS_PROFILE=patchforge-dev
patchforge run \
  --sarif ./reports/semgrep.sarif \
  --repo-path ./ \
  --language python \
  --max-iterations 5 \
  --auto-pr \
  --aws-region us-east-1
```

---

### 1.4 Mode D: 🎃 Halloween Operations Dashboard
Served via FastAPI backend (`src/patchforge/api/server.py`) and React frontend (`dashboard/`):
```bash
# Start backend
uvicorn patchforge.api.server:app --host 0.0.0.0 --port 8000

# Start frontend
cd dashboard && npm run dev
```
Accessible at `http://localhost:5173`.

