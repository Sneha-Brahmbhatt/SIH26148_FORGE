"""
FORGE FastAPI REST API Endpoints v1
"""

import hashlib
import json
import os
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import (
    AnalystModel, CaseModel, ScriptModel, ScriptVersionModel,
    ExecutionModel, EvidenceModel, ProvenanceModel, TimelineEventModel,
    FindingModel, AuditLogModel, ReportModel, ExportModel
)
from app.schemas.schemas import (
    CaseCreate, CaseResponse, ScriptCreate, ScriptValidateRequest,
    ScriptExecuteRequest, ScriptValidationResponse
)

from language.lexer import Lexer
from language.parser import Parser
from language.semantic import SemanticValidator
from language.policy import PolicyEngine
from language.runtime import Interpreter
from forensics.computer import collect_host_info, collect_processes, collect_services, list_files, collect_event_logs
from forensics.network import NetworkAnalyzer

router = APIRouter(prefix="/api/v1")

# Pre-defined Demo Scripts
DEMO_FULL_ANALYSIS_SCRIPT = """CASE "CASE-001"

REQUIRE ANALYST "investigator@org.example"
REQUIRE POLICY "standard-read-only-v1"
REQUIRE CAPABILITIES [
    HOST_READ,
    PROCESS_READ,
    SERVICE_READ,
    SYSTEM_READ,
    FILE_READ,
    FILE_HASH,
    EVENT_READ,
    NETWORK_READ,
    PCAP_READ,
    TIMELINE_BUILD,
    FINDING_GENERATE,
    EXPORT_DATA,
    REPORT_GENERATE
]

host_info = HOST_INFO()
processes = PROCESS_LIST()
services = SERVICE_LIST()
system = SYSTEM_CONFIG()

files = FILE_LIST("./datasets/computer/files")
file_metadata = FILE_METADATA(files)
file_hashes = HASH_FILES(files, "SHA256")

events_system = EVENT_LOGS("System")
events_security = EVENT_LOGS("Security")

pcap = PCAP_LOAD("./datasets/network/sample.pcap")
connections = NETWORK_CONNECTIONS(pcap)
dns = DNS_ACTIVITY(pcap)
protocol_stats = PROTOCOL_STATS(pcap)
flow_summary = FLOW_SUMMARY(pcap)

timeline = BUILD_TIMELINE([
    host_info,
    processes,
    services,
    file_metadata,
    events_system,
    events_security,
    connections,
    dns
])

findings = ANALYZE_FINDINGS(timeline, file_hashes, dns)

EXPORT_EVIDENCE(file_hashes, "./exports/file_hashes.json")
EXPORT_REPORT(findings, "./reports/CASE-001-report", "json")
EXPORT_REPORT(findings, "./reports/CASE-001-report", "csv")
EXPORT_REPORT(findings, "./reports/CASE-001-report", "html")
"""

DEMO_POLICY_BLOCKED_SCRIPT = """CASE "CASE-BAD"

REQUIRE ANALYST "unauthorized@org.example"
REQUIRE POLICY "standard-read-only-v1"
REQUIRE CAPABILITIES [
    WRITE_EVIDENCE,
    EXECUTE_PROCESS,
    DISABLE_SECURITY_CONTROL
]

EXECUTE_PROCESS("cmd.exe")
WRITE_EVIDENCE("./evidence/disk.E01", "modified")
"""

@router.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "FORGE — Forensic Object Runtime & Governed Execution",
        "version": "0.1.0",
        "policy_mode": "CAPABILITY_GOVERNED_SANDBOX",
        "safety_statement": "FORGE is intended only for authorized digital-forensic investigations and controlled security environments. It does not bypass, disable, evade, or interfere with endpoint security controls."
    }

# Cases Endpoints
@router.post("/cases", response_model=CaseResponse)
def create_case(req: CaseCreate, db: Session = Depends(get_db)):
    # Check if case exists
    existing = db.query(CaseModel).filter(CaseModel.case_id == req.case_id).first()
    if existing:
        return existing

    # Ensure analyst exists
    analyst = db.query(AnalystModel).filter(AnalystModel.analyst_id == req.analyst_id).first()
    if not analyst:
        analyst = AnalystModel(analyst_id=req.analyst_id, name="Lead Investigator", email=req.analyst_id, role="Analyst")
        db.add(analyst)
        db.commit()

    case_obj = CaseModel(
        case_id=req.case_id,
        title=req.title,
        description=req.description,
        analyst_id=req.analyst_id,
        status="ACTIVE"
    )
    db.add(case_obj)
    db.commit()
    db.refresh(case_obj)
    return case_obj

@router.get("/cases")
def list_cases(db: Session = Depends(get_db)):
    cases = db.query(CaseModel).all()
    if not cases:
        # Seed default CASE-001
        default_case = CaseModel(
            case_id="CASE-001",
            title="SIH26148 Digital Forensic Incident Response",
            description="Controlled computer and network forensic investigation against endpoint and PCAP datasets.",
            analyst_id="investigator@org.example",
            status="ACTIVE"
        )
        db.add(default_case)
        db.commit()
        cases = [default_case]
    return cases

@router.get("/cases/{case_id}")
def get_case(case_id: str, db: Session = Depends(get_db)):
    case_obj = db.query(CaseModel).filter(CaseModel.case_id == case_id).first()
    if not case_obj:
        raise HTTPException(status_code=404, detail="Case not found")
    return case_obj

# Script Validation & Execution Endpoints
@router.post("/scripts/validate", response_model=ScriptValidationResponse)
def validate_script(req: ScriptValidateRequest):
    source = req.source_code
    sha256_hash = hashlib.sha256(source.encode("utf-8")).hexdigest()

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        token_dicts = [t.to_dict() for t in tokens]
    except Exception as ex:
        return {
            "valid": False,
            "lexer": {"token_count": 0, "tokens": [], "error": str(ex)},
            "parser": {"ast": {}, "errors": [str(ex)]},
            "semantic": {"errors": [str(ex)], "warnings": []},
            "policy": {"decision": "BLOCKED", "violations": [str(ex)]},
            "script_sha256": sha256_hash,
            "ready_for_execution": False
        }

    try:
        parser = Parser(tokens)
        ast = parser.parse()
        ast_dict = ast.to_dict()
    except Exception as ex:
        return {
            "valid": False,
            "lexer": {"token_count": len(tokens), "tokens": token_dicts[:20]},
            "parser": {"ast": {}, "errors": [str(ex)]},
            "semantic": {"errors": [str(ex)], "warnings": []},
            "policy": {"decision": "BLOCKED", "violations": [str(ex)]},
            "script_sha256": sha256_hash,
            "ready_for_execution": False
        }

    # Semantic Validation
    validator = SemanticValidator()
    semantics_diagnostics = validator.validate(ast)
    sem_errors = [d for d in semantics_diagnostics if d["level"] == "ERROR"]

    # Policy Check
    policy_engine = PolicyEngine(req.policy_name or "standard-read-only-v1")
    policy_res = policy_engine.evaluate(ast)

    is_valid = len(sem_errors) == 0 and policy_res["decision"] == "APPROVED"

    return {
        "valid": is_valid,
        "lexer": {"token_count": len(tokens), "tokens": token_dicts[:30]},
        "parser": {"ast": ast_dict, "errors": []},
        "semantic": {"errors": sem_errors, "warnings": [d for d in semantics_diagnostics if d["level"] == "WARNING"]},
        "policy": policy_res,
        "script_sha256": sha256_hash,
        "ready_for_execution": is_valid
    }

@router.post("/scripts/execute")
def execute_script(req: ScriptExecuteRequest, db: Session = Depends(get_db)):
    source = req.source_code
    case_id = req.case_id or "CASE-001"
    analyst_id = req.analyst_id or "investigator@org.example"

    # Lex & Parse
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    # Run in Interpreter
    interpreter = Interpreter(req.policy_name or "standard-read-only-v1")
    res = interpreter.execute(
        program=ast,
        script_id=req.script_id or "SCR-000001",
        script_version="1.0.0",
        script_source=source,
        case_id=case_id,
        analyst_id=analyst_id
    )

    # Save execution record to DB
    exec_record = ExecutionModel(
        execution_id=res["execution_id"],
        case_id=case_id,
        script_version_id=req.script_id or "SCR-000001",
        analyst_id=analyst_id,
        policy_version=req.policy_name or "standard-read-only-v1",
        status=res["status"],
        policy_decision=res["policy_decision"],
        started_at_utc=res["started_at_utc"],
        completed_at_utc=res["completed_at_utc"],
        duration_ms=res["duration_ms"],
        manifest_json=json.dumps(res, sort_keys=True)
    )
    db.add(exec_record)

    # Save evidence records to DB
    for ev in res.get("evidence", []):
        db_ev = EvidenceModel(
            evidence_id=ev["evidence_id"],
            case_id=case_id,
            execution_id=res["execution_id"],
            script_id=req.script_id or "SCR-000001",
            script_version="1.0.0",
            source=ev["source"],
            collector=ev["collector"],
            evidence_type=ev["evidence_type"],
            collection_status=ev.get("collection_status", "SUCCESS"),
            collected_at_utc=ev.get("collected_at_utc"),
            sha256=ev["sha256"],
            hash_algorithm=ev.get("hash_algorithm", "SHA-256"),
            record_count=ev.get("record_count", 1),
            synthetic=ev.get("synthetic", True),
            provenance_id=ev["provenance_id"]
        )
        db.add(db_ev)

    # Save timeline events to DB
    for tl in res.get("timeline", []):
        db_tl = TimelineEventModel(
            timeline_event_id=tl["timeline_event_id"],
            case_id=case_id,
            execution_id=res["execution_id"],
            timestamp_utc=tl["timestamp_utc"],
            event_type=tl["event_type"],
            source=tl["source"],
            title=tl["title"],
            description=tl["description"],
            evidence_id=tl.get("evidence_id"),
            related_object=tl.get("related_object"),
            severity=tl.get("severity", "INFO"),
            synthetic=tl.get("synthetic", True)
        )
        db.add(db_tl)

    # Save findings to DB
    for fnd in res.get("findings", []):
        db_fnd = FindingModel(
            finding_id=fnd["finding_id"],
            case_id=case_id,
            execution_id=res["execution_id"],
            severity=fnd["severity"],
            category=fnd["category"],
            timestamp_utc=fnd["timestamp_utc"],
            title=fnd["title"],
            description=fnd["description"],
            observed_evidence=fnd.get("observed_evidence"),
            derived_analysis=fnd.get("derived_analysis"),
            analyst_interpretation_required=fnd.get("analyst_interpretation_required"),
            confidence=fnd.get("confidence", "HIGH"),
            analysis_type=fnd.get("analysis_type", "AUTOMATED")
        )
        db.add(db_fnd)

    # Save audit logs to DB
    for aud in res.get("audit_logs", []):
        db_aud = AuditLogModel(
            audit_id=aud["audit_id"],
            case_id=case_id,
            execution_id=res["execution_id"],
            actor=aud["actor"],
            action=aud["action"],
            object_type=aud["object_type"],
            object_id=aud["object_id"],
            result=aud["result"],
            timestamp_utc=aud["timestamp_utc"],
            details_json=aud.get("details_json"),
            prev_audit_hash=aud["prev_audit_hash"],
            audit_hash=aud["audit_hash"]
        )
        db.add(db_aud)

    db.commit()
    return res

# SIH Demo Endpoint
@router.post("/demo/run")
def run_sih_demo(db: Session = Depends(get_db)):
    req = ScriptExecuteRequest(
        script_id="SCR-DEMO-FULL",
        source_code=DEMO_FULL_ANALYSIS_SCRIPT,
        case_id="CASE-001",
        analyst_id="investigator@org.example"
    )
    return execute_script(req, db)

# Executions List & Details
@router.get("/executions")
def list_executions(db: Session = Depends(get_db)):
    execs = db.query(ExecutionModel).order_by(ExecutionModel.started_at_utc.desc()).all()
    results = []
    for e in execs:
        manifest = json.loads(e.manifest_json) if e.manifest_json else {}
        results.append({
            "execution_id": e.execution_id,
            "case_id": e.case_id,
            "script_version_id": e.script_version_id,
            "analyst_id": e.analyst_id,
            "status": e.status,
            "policy_decision": e.policy_decision,
            "started_at_utc": e.started_at_utc,
            "completed_at_utc": e.completed_at_utc,
            "duration_ms": e.duration_ms,
            "evidence_count": len(manifest.get("evidence", [])),
            "timeline_count": len(manifest.get("timeline", [])),
            "findings_count": len(manifest.get("findings", []))
        })
    return results

@router.get("/executions/{execution_id}")
def get_execution(execution_id: str, db: Session = Depends(get_db)):
    e = db.query(ExecutionModel).filter(ExecutionModel.execution_id == execution_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Execution not found")
    return json.loads(e.manifest_json) if e.manifest_json else {}

@router.get("/executions/{execution_id}/ast")
def get_execution_ast(execution_id: str, db: Session = Depends(get_db)):
    lexer = Lexer(DEMO_FULL_ANALYSIS_SCRIPT)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    return ast.to_dict()

@router.get("/executions/{execution_id}/tokens")
def get_execution_tokens(execution_id: str):
    lexer = Lexer(DEMO_FULL_ANALYSIS_SCRIPT)
    tokens = lexer.tokenize()
    return [t.to_dict() for t in tokens]

@router.get("/executions/{execution_id}/policy")
def get_execution_policy(execution_id: str):
    lexer = Lexer(DEMO_FULL_ANALYSIS_SCRIPT)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    engine = PolicyEngine()
    return engine.evaluate(ast)

@router.get("/evidence")
def list_evidence(db: Session = Depends(get_db)):
    evs = db.query(EvidenceModel).all()
    return evs

@router.get("/evidence/{evidence_id}")
def get_evidence(evidence_id: str, db: Session = Depends(get_db)):
    ev = db.query(EvidenceModel).filter(EvidenceModel.evidence_id == evidence_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return ev

# Forensic Subsystem Data Queries
@router.get("/hosts")
def get_hosts():
    return [collect_host_info()]

@router.get("/processes")
def get_processes():
    return collect_processes()

@router.get("/services")
def get_services():
    return collect_services()

@router.get("/files")
def get_files():
    files = list_files("./datasets/computer/files")
    return [{"path": f, "filename": os.path.basename(f)} for f in files]

@router.get("/events")
def get_events(source: str = "System"):
    return collect_event_logs(source)

@router.get("/network/flows")
def get_network_flows():
    analyzer = NetworkAnalyzer()
    return analyzer.get_flow_summary()

@router.get("/network/dns")
def get_network_dns():
    analyzer = NetworkAnalyzer()
    return analyzer.get_dns_activity()

@router.get("/network/protocols")
def get_network_protocols():
    analyzer = NetworkAnalyzer()
    return analyzer.get_protocol_stats()

@router.get("/timeline")
def get_timeline(db: Session = Depends(get_db)):
    tls = db.query(TimelineEventModel).order_by(TimelineEventModel.timestamp_utc.asc()).all()
    return tls

@router.get("/findings")
def get_findings(db: Session = Depends(get_db)):
    fnds = db.query(FindingModel).all()
    return fnds

@router.get("/audit")
def get_audit_logs(db: Session = Depends(get_db)):
    logs = db.query(AuditLogModel).order_by(AuditLogModel.timestamp_utc.asc()).all()
    return logs

@router.get("/chain-of-custody/{case_id}")
def get_chain_of_custody(case_id: str, db: Session = Depends(get_db)):
    logs = db.query(AuditLogModel).filter(AuditLogModel.case_id == case_id).all()
    evidence = db.query(EvidenceModel).filter(EvidenceModel.case_id == case_id).all()
    return {
        "case_id": case_id,
        "audit_events_count": len(logs),
        "evidence_items_count": len(evidence),
        "chain_events": logs,
        "evidence_items": evidence
    }

@router.get("/reports")
def list_reports():
    reports_dir = "./reports"
    files = []
    if os.path.exists(reports_dir):
        for f in os.listdir(reports_dir):
            full_p = os.path.join(reports_dir, f).replace("\\", "/")
            stat = os.stat(full_p)
            files.append({
                "report_id": f"RPT-{hashlib.md5(f.encode('utf-8')).hexdigest()[:6]}",
                "filename": f,
                "path": full_p,
                "size_bytes": stat.st_size,
                "sha256": hashlib.sha256(open(full_p, "rb").read()).hexdigest(),
                "created_at_utc": "2026-09-25T14:25:00Z"
            })
    return files

@router.get("/reports/{filename}/download")
def download_report(filename: str):
    full_path = os.path.join("./reports", os.path.basename(filename))
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="Report file not found")
    return FileResponse(path=full_path, filename=filename)

@router.get("/language/reference")
def get_language_reference():
    return {
        "dsl_name": "FORGE Forensic DSL",
        "version": "1.0.0",
        "safety_model": "CAPABILITY_GOVERNED_ALLOWLIST",
        "commands": [
            {"command": 'CASE "ID"', "capability": "CASE_MANAGE", "purpose": "Binds execution to a specific forensic case", "syntax": 'CASE "CASE-001"'},
            {"command": 'REQUIRE ANALYST "email"', "capability": "IDENTITY_ASSERT", "purpose": "Asserts analyst identity for provenance", "syntax": 'REQUIRE ANALYST "investigator@org.example"'},
            {"command": 'REQUIRE POLICY "name"', "capability": "POLICY_ASSERT", "purpose": "Asserts execution policy version", "syntax": 'REQUIRE POLICY "standard-read-only-v1"'},
            {"command": 'REQUIRE CAPABILITIES [...]', "capability": "CAPABILITY_ASSERT", "purpose": "Declares explicit capabilities required by script", "syntax": "REQUIRE CAPABILITIES [HOST_READ, FILE_READ, FILE_HASH]"},
            {"command": "HOST_INFO()", "capability": "HOST_READ", "purpose": "Collects target host and OS metadata", "syntax": "host_info = HOST_INFO()"},
            {"command": "PROCESS_LIST()", "capability": "PROCESS_READ", "purpose": "Collects process inventory and command lines", "syntax": "processes = PROCESS_LIST()"},
            {"command": "SERVICE_LIST()", "capability": "SERVICE_READ", "purpose": "Collects system service inventory", "syntax": "services = SERVICE_LIST()"},
            {"command": "FILE_LIST(path)", "capability": "FILE_READ", "purpose": "Lists files within approved dataset directory", "syntax": 'files = FILE_LIST("./datasets/computer/files")'},
            {"command": "FILE_METADATA(files)", "capability": "FILE_READ", "purpose": "Extracts file size, timestamps, and extensions", "syntax": "metadata = FILE_METADATA(files)"},
            {"command": 'HASH_FILES(files, "SHA256")', "capability": "FILE_HASH", "purpose": "Calculates SHA-256 hashes for baseline integrity", "syntax": 'hashes = HASH_FILES(files, "SHA256")'},
            {"command": 'EVENT_LOGS(source)', "capability": "EVENT_READ", "purpose": "Parses event logs (System, Security, Application)", "syntax": 'events = EVENT_LOGS("System")'},
            {"command": "BROWSER_HISTORY()", "capability": "ARTIFACT_READ", "purpose": "Parses browser history artifacts", "syntax": "history = BROWSER_HISTORY()"},
            {"command": "REGISTRY_METADATA(keys)", "capability": "REGISTRY_READ", "purpose": "Parses registry keys and persistence artifacts", "syntax": "registry = REGISTRY_METADATA()"},
            {"command": "PCAP_LOAD(path)", "capability": "PCAP_READ", "purpose": "Loads PCAP capture or network dataset", "syntax": 'pcap = PCAP_LOAD("./datasets/network/sample.pcap")'},
            {"command": "NETWORK_CONNECTIONS(pcap)", "capability": "NETWORK_READ", "purpose": "Summarizes active network connections and flows", "syntax": "conns = NETWORK_CONNECTIONS(pcap)"},
            {"command": "DNS_ACTIVITY(pcap)", "capability": "NETWORK_READ", "purpose": "Parses DNS queries, responses, and NXDOMAIN ratios", "syntax": "dns = DNS_ACTIVITY(pcap)"},
            {"command": "PROTOCOL_STATS(pcap)", "capability": "NETWORK_READ", "purpose": "Calculates network protocol distribution", "syntax": "stats = PROTOCOL_STATS(pcap)"},
            {"command": "FLOW_SUMMARY(pcap)", "capability": "NETWORK_READ", "purpose": "Aggregates talkers and flow summaries by IP", "syntax": "flows = FLOW_SUMMARY(pcap)"},
            {"command": "BUILD_TIMELINE(sources)", "capability": "TIMELINE_BUILD", "purpose": "Merges computer & network events into unified timeline", "syntax": "timeline = BUILD_TIMELINE([host_info, processes, dns])"},
            {"command": "ANALYZE_FINDINGS(timeline, hashes, dns)", "capability": "FINDING_GENERATE", "purpose": "Generates evidence-backed forensic findings", "syntax": "findings = ANALYZE_FINDINGS(timeline, file_hashes, dns)"},
            {"command": 'EXPORT_EVIDENCE(object, path)', "capability": "EXPORT_DATA", "purpose": "Exports evidence object to JSON/CSV", "syntax": 'EXPORT_EVIDENCE(file_hashes, "./exports/hashes.json")'},
            {"command": 'EXPORT_REPORT(object, path, format)', "capability": "REPORT_GENERATE", "purpose": "Generates reproducible JSON/CSV/HTML report", "syntax": 'EXPORT_REPORT(findings, "./reports/CASE-001", "html")'}
        ],
        "prohibited_capabilities": [
            "WRITE_EVIDENCE", "EXECUTE_PROCESS", "LOAD_DRIVER", "INJECT_CODE",
            "RAW_DEVICE_WRITE", "NETWORK_EGRESS", "DISABLE_SECURITY_CONTROL",
            "BYPASS_SECURITY_CONTROL"
        ]
    }
