"""
FORGE Pydantic v2 API Schemas
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class CaseCreate(BaseModel):
    case_id: Optional[str] = "CASE-001"
    title: str = "SIH26148 Digital Forensic Investigation"
    description: Optional[str] = "Standard computer and network forensic analysis case"
    analyst_id: str = "investigator@org.example"

class CaseResponse(BaseModel):
    case_id: str
    title: str
    description: Optional[str]
    status: str
    analyst_id: str
    created_at_utc: str
    closed_at_utc: Optional[str] = None

class ScriptCreate(BaseModel):
    script_id: Optional[str] = "SCR-000001"
    name: str = "Demo Full Analysis"
    description: Optional[str] = "Full computer and network forensic analysis workflow"
    source_code: str
    author_id: str = "investigator@org.example"

class ScriptValidateRequest(BaseModel):
    source_code: str
    policy_name: Optional[str] = "standard-read-only-v1"

class ScriptExecuteRequest(BaseModel):
    script_id: Optional[str] = "SCR-000001"
    source_code: str
    case_id: Optional[str] = "CASE-001"
    analyst_id: Optional[str] = "investigator@org.example"
    policy_name: Optional[str] = "standard-read-only-v1"

class ScriptValidationResponse(BaseModel):
    valid: bool
    lexer: Dict[str, Any]
    parser: Dict[str, Any]
    semantic: Dict[str, Any]
    policy: Dict[str, Any]
    script_sha256: str
    ready_for_execution: bool

class ExecutionResponse(BaseModel):
    execution_id: str
    case_id: str
    script_id: str
    script_version: str
    analyst_id: str
    status: str
    policy_decision: str
    policy_result: Dict[str, Any]
    started_at_utc: str
    completed_at_utc: Optional[str]
    duration_ms: int
    evidence_count: int = 0
    timeline_count: int = 0
    findings_count: int = 0
