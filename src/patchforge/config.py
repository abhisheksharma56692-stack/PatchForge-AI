"""Configuration management for PatchForge AI using Pydantic Settings."""
from typing import Optional
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PatchForgeSettings(BaseSettings):
    """Global configuration settings for PatchForge AI."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General & Pipeline
    environment: str = "development"
    log_level: str = "INFO"
    max_iterations: int = 5
    use_stubs: bool = False

    # Database Persistence Layer
    database_url: str = "sqlite:///./patchforge.db"

    # AWS Cloud Services
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[SecretStr] = None
    aws_secret_access_key: Optional[SecretStr] = None
    s3_artifact_bucket: str = "patchforge-artifacts"
    sqs_queue_url: Optional[str] = None
    dynamodb_table_name: str = "PatchForgeAuditTrail"
    ecr_repository_uri: Optional[str] = None

    # Bedrock LLM Config
    bedrock_model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    # Hermetic Sandbox Constraints
    docker_host: Optional[str] = None
    sandbox_base_image_python: str = "patchforge-runner-py311:latest"
    sandbox_base_image_node: str = "patchforge-runner-node20:latest"
    sandbox_base_image_go: str = "patchforge-runner-go122:latest"
    sandbox_network_mode: str = "none"  # Strictly air-gapped
    sandbox_memory_limit: str = "2048m"
    sandbox_cpu_limit: float = 2.0
    sandbox_timeout_sec: int = 60
    mutation_score_threshold: float = 85.0

    # VCS Delivery & Signing
    github_token: Optional[SecretStr] = None
    gitlab_token: Optional[SecretStr] = None
    gpg_key_id: Optional[str] = None
    git_committer_name: str = "PatchForge AI Bot"
    git_committer_email: str = "bot@patchforge.ai"

    # API & Dashboard Backend
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    dashboard_cors_origins: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"


settings = PatchForgeSettings()
