# PatchForge AI - Main Orchestrator Container Image
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    gnupg \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .
RUN pip install --no-cache-dir -e .

EXPOSE 8000

# Default entrypoint starts FastAPI dashboard backend
CMD ["uvicorn", "patchforge.api.server:app", "--host", "0.0.0.0", "--port", "8000"]

