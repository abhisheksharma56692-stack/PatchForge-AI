# Ephemeral Micro-Sandbox for Go Projects
FROM golang:1.22-alpine

RUN apk add --no-cache git bash

# Non-root user setup
RUN addgroup -g 1001 sandbox && adduser -u 1001 -G sandbox -s /bin/bash -D sandbox

WORKDIR /workspace
RUN chown -R sandbox:sandbox /workspace

USER 1001:1001

CMD ["/bin/bash"]

