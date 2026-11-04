# Ephemeral Micro-Sandbox for Python Projects
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Pre-install test & mutation harnesses
RUN pip install --no-cache-dir pytest pytest-mock mutmut semgrep

# Enforce non-root user (rootless container runtime)
RUN groupadd -g 1001 sandbox && useradd -u 1001 -g sandbox -m -s /bin/bash sandbox

WORKDIR /workspace
RUN chown -R sandbox:sandbox /workspace

USER 1001:1001

CMD ["/bin/bash"]

