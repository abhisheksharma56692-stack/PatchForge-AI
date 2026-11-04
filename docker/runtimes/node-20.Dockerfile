# Ephemeral Micro-Sandbox for Node.js / TypeScript Projects
FROM node:20-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Pre-install test & mutation harnesses
RUN npm install -g mocha jest @stryker-mutator/core

# Rootless execution
RUN groupadd -g 1001 sandbox && useradd -u 1001 -g sandbox -m -s /bin/bash sandbox

WORKDIR /workspace
RUN chown -R sandbox:sandbox /workspace

USER 1001:1001

CMD ["/bin/bash"]

