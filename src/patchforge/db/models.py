"""SQLAlchemy relational entity models for PatchForge AI."""
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from patchforge.db.base import Base, TimestampMixin


class VulnerabilityModel(Base, TimestampMixin):
    """Stores static application security scanner findings."""
    __tablename__ = "vulnerabilities"

    id = Column(String(64), primary_key=True, index=True)
    cwe_id = Column(String(32), nullable=False, index=True)
    cve_id = Column(String(32), nullable=True)
    title = Column(String(256), nullable=False)
    scanner_name = Column(String(64), nullable=False)
    rule_id = Column(String(256), nullable=False)
    file_path = Column(String(512), nullable=False, index=True)
    start_line = Column(Integer, nullable=False)
    end_line = Column(Integer, nullable=False)
    start_col = Column(Integer, default=0)
    end_col = Column(Integer, default=0)
    sink_symbol = Column(Text, nullable=False)
    severity = Column(String(16), nullable=False, default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    skull_count = Column(Integer, nullable=False, default=4)        # 1 to 5 skulls for Halloween UI
    status = Column(String(32), nullable=False, default="OPEN", index=True)  # OPEN, IN_PROGRESS, RESOLVED, MUTED
    slice_line_count = Column(Integer, default=25)
    raw_sarif_hash = Column(String(64), nullable=True)

    # Relationships
    runs = relationship("RemediationRunModel", back_populates="vulnerability", cascade="all, delete-orphan")


class RemediationRunModel(Base, TimestampMixin):
    """Tracks discrete executions of the multi-agent closed loop pipeline."""
    __tablename__ = "remediation_runs"

    id = Column(String(64), primary_key=True, index=True)
    vulnerability_id = Column(String(64), ForeignKey("vulnerabilities.id", ondelete="CASCADE"), nullable=False)
    repo_path = Column(String(512), nullable=False)
    target_branch = Column(String(128), default="main")
    remediation_branch = Column(String(128), nullable=True)
    iteration_count = Column(Integer, default=1)
    max_iterations = Column(Integer, default=5)
    status = Column(String(32), nullable=False, default="INITIALIZING", index=True)
    baseline_tests_passed = Column(Boolean, default=False)
    reproduction_defended = Column(Boolean, default=False)
    mutation_score = Column(Float, default=0.0)
    delta_sast_clean = Column(Boolean, default=False)
    duration_seconds = Column(Float, default=0.0)
    pr_url = Column(String(512), nullable=True)
    pr_number = Column(Integer, nullable=True)
    commit_sha = Column(String(64), nullable=True)
    s3_artifact_prefix = Column(String(512), nullable=True)
    tombstone_inscription = Column(Text, nullable=True)
    error_summary = Column(Text, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    vulnerability = relationship("VulnerabilityModel", back_populates="runs")
    patches = relationship("CandidatePatchModel", back_populates="run", cascade="all, delete-orphan")
    test_results = relationship("TestResultModel", back_populates="run", cascade="all, delete-orphan")
    audit_events = relationship("AuditEventModel", back_populates="run", cascade="all, delete-orphan")


class CandidatePatchModel(Base, TimestampMixin):
    """Stores unified diff candidates synthesized per iteration."""
    __tablename__ = "candidate_patches"

    id = Column(String(64), primary_key=True, index=True)
    run_id = Column(String(64), ForeignKey("remediation_runs.id", ondelete="CASCADE"), nullable=False)
    iteration = Column(Integer, nullable=False)
    diff_content = Column(Text, nullable=False)
    ast_slice_range = Column(String(64), nullable=True)
    audit_approved = Column(Boolean, default=False)
    audit_violations = Column(JSON, default=list)
    z3_proof_status = Column(String(64), default="UNCONDITIONALLY_SAFE")

    # Relationships
    run = relationship("RemediationRunModel", back_populates="patches")


class TestResultModel(Base, TimestampMixin):
    """Execution telemetry captured inside the hermetic container sandbox."""
    __tablename__ = "test_results"

    id = Column(String(64), primary_key=True, index=True)
    run_id = Column(String(64), ForeignKey("remediation_runs.id", ondelete="CASCADE"), nullable=False)
    iteration = Column(Integer, nullable=False)
    test_type = Column(String(32), nullable=False)  # BASELINE_UNIT, REPRODUCTION_POC, MUTATION, DELTA_SAST
    passed = Column(Boolean, nullable=False)
    exit_code = Column(Integer, nullable=False)
    tests_passed_count = Column(Integer, default=0)
    tests_failed_count = Column(Integer, default=0)
    stdout_snippet = Column(Text, nullable=True)
    stderr_snippet = Column(Text, nullable=True)
    duration_seconds = Column(Float, default=0.0)

    # Relationships
    run = relationship("RemediationRunModel", back_populates="test_results")


class AuditEventModel(Base, TimestampMixin):
    """Audit ledger entries tracking every agent state transition."""
    __tablename__ = "audit_events"

    id = Column(String(64), primary_key=True, index=True)
    run_id = Column(String(64), ForeignKey("remediation_runs.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(64), nullable=False)
    stage = Column(String(32), nullable=False)
    payload = Column(JSON, default=dict)

    # Relationships
    run = relationship("RemediationRunModel", back_populates="audit_events")

