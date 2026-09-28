"""
FORGE SQLAlchemy 2.0 Database Models
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, Float, Index, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class AnalystModel(Base):
    __tablename__ = "analysts"
    analyst_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, default="Analyst")
    created_at_utc = Column(String, default=lambda: datetime.now(timezone.utc).isoformat())

class CaseModel(Base):
    __tablename__ = "cases"
    case_id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="ACTIVE") # ACTIVE, CLOSED, ARCHIVED
    analyst_id = Column(String, ForeignKey("analysts.analyst_id"), nullable=False)
    created_at_utc = Column(String, default=lambda: datetime.now(timezone.utc).isoformat())
    closed_at_utc = Column(String, nullable=True)

class ScriptModel(Base):
    __tablename__ = "scripts"
    script_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    current_version = Column(String, default="1.0.0")
    author_id = Column(String, nullable=False)
    created_at_utc = Column(String, default=lambda: datetime.now(timezone.utc).isoformat())

class ScriptVersionModel(Base):
    __tablename__ = "script_versions"
    script_version_id = Column(String, primary_key=True, index=True)
    script_id = Column(String, ForeignKey("scripts.script_id"), nullable=False)
    version = Column(String, nullable=False)
    source_code = Column(Text, nullable=False)
    sha256 = Column(String, nullable=False)
    created_at_utc = Column(String, default=lambda: datetime.now(timezone.utc).isoformat())
    created_by = Column(String, nullable=False)

class ExecutionModel(Base):
    __tablename__ = "executions"
    execution_id = Column(String, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("cases.case_id"), index=True, nullable=False)
    script_version_id = Column(String, nullable=False)
    analyst_id = Column(String, nullable=False)
    policy_version = Column(String, default="standard-read-only-v1")
    runtime_version = Column(String, default="forge-0.1.0")
    status = Column(String, index=True, default="PENDING") # PENDING, APPROVED, BLOCKED, RUNNING, COMPLETED, FAILED
    policy_decision = Column(String, default="PENDING") # APPROVED, BLOCKED
    started_at_utc = Column(String, default=lambda: datetime.now(timezone.utc).isoformat())
    completed_at_utc = Column(String, nullable=True)
    duration_ms = Column(Integer, default=0)
    manifest_json = Column(Text, nullable=True)
    result_summary_json = Column(Text, nullable=True)

class EvidenceModel(Base):
    __tablename__ = "evidence"
    evidence_id = Column(String, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("cases.case_id"), index=True, nullable=False)
    execution_id = Column(String, ForeignKey("executions.execution_id"), index=True, nullable=False)
    script_id = Column(String, nullable=False)
    script_version = Column(String, nullable=False)
    source = Column(String, nullable=False)
    collector = Column(String, nullable=False)
    evidence_type = Column(String, nullable=False)
    collection_status = Column(String, default="SUCCESS")
    collected_at_utc = Column(String, default=lambda: datetime.now(timezone.utc).isoformat())
    sha256 = Column(String, index=True, nullable=False)
    hash_algorithm = Column(String, default="SHA-256")
    record_count = Column(Integer, default=1)
    synthetic = Column(Boolean, default=True)
    provenance_id = Column(String, nullable=False)
    raw_data_json = Column(Text, nullable=True)

class ProvenanceModel(Base):
    __tablename__ = "provenance_records"
    provenance_id = Column(String, primary_key=True, index=True)
    case_id = Column(String, nullable=False)
    execution_id = Column(String, nullable=False)
    analyst_id = Column(String, nullable=False)
    script_id = Column(String, nullable=False)
    script_version = Column(String, nullable=False)
    script_sha256 = Column(String, nullable=False)
    policy_version = Column(String, nullable=False)
    runtime_version = Column(String, nullable=False)
    dataset_version = Column(String, nullable=False)
    details_json = Column(Text, nullable=True)

class TimelineEventModel(Base):
    __tablename__ = "timeline_events"
    timeline_event_id = Column(String, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("cases.case_id"), index=True, nullable=False)
    execution_id = Column(String, ForeignKey("executions.execution_id"), index=True, nullable=False)
    timestamp_utc = Column(String, index=True, nullable=False)
    event_type = Column(String, index=True, nullable=False)
    source = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    evidence_id = Column(String, nullable=True)
    related_object = Column(String, nullable=True)
    severity = Column(String, default="INFO")
    synthetic = Column(Boolean, default=True)

class FindingModel(Base):
    __tablename__ = "findings"
    finding_id = Column(String, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("cases.case_id"), index=True, nullable=False)
    execution_id = Column(String, ForeignKey("executions.execution_id"), index=True, nullable=False)
    severity = Column(String, index=True, nullable=False) # HIGH, MEDIUM, LOW, INFO
    category = Column(String, nullable=False)
    timestamp_utc = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    observed_evidence = Column(Text, nullable=True)
    derived_analysis = Column(Text, nullable=True)
    analyst_interpretation_required = Column(Text, nullable=True)
    confidence = Column(String, nullable=False)
    analysis_type = Column(String, nullable=False)
    details_json = Column(Text, nullable=True)

class AuditLogModel(Base):
    __tablename__ = "audit_logs"
    audit_id = Column(String, primary_key=True, index=True)
    case_id = Column(String, index=True, nullable=False)
    execution_id = Column(String, index=True, nullable=False)
    actor = Column(String, nullable=False)
    action = Column(String, nullable=False)
    object_type = Column(String, nullable=False)
    object_id = Column(String, nullable=False)
    result = Column(String, nullable=False)
    timestamp_utc = Column(String, index=True, nullable=False)
    details_json = Column(Text, nullable=True)
    prev_audit_hash = Column(String, nullable=False)
    audit_hash = Column(String, nullable=False)

class ReportModel(Base):
    __tablename__ = "reports"
    report_id = Column(String, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("cases.case_id"), nullable=False)
    execution_id = Column(String, ForeignKey("executions.execution_id"), nullable=False)
    format_type = Column(String, nullable=False) # json, csv, html, pdf
    file_path = Column(String, nullable=False)
    sha256 = Column(String, nullable=False)
    created_at_utc = Column(String, default=lambda: datetime.now(timezone.utc).isoformat())

class ExportModel(Base):
    __tablename__ = "exports"
    export_id = Column(String, primary_key=True, index=True)
    case_id = Column(String, nullable=False)
    execution_id = Column(String, nullable=False)
    target_var = Column(String, nullable=False)
    output_path = Column(String, nullable=False)
    created_at_utc = Column(String, default=lambda: datetime.now(timezone.utc).isoformat())
