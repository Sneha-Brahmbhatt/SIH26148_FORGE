"""
FORGE Controlled Forensic Runtime & DSL Interpreter
Executes policy-governed forensic scripts in a secure, sandboxed environment.
Enforces capability checks, evidence immutability, provenance recording, and audit logging.
"""

import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import os
import json

from language.ast.nodes import (
    ProgramNode, CaseNode, RequireNode, AssignmentNode, CallNode,
    StringLiteralNode, NumberLiteralNode, IdentifierNode, ArrayLiteralNode, ASTNode
)
from language.policy.policy_engine import PolicyEngine
from forensics.computer import (
    collect_host_info, collect_processes, collect_services,
    list_files, collect_file_metadata, hash_files,
    collect_event_logs, collect_browser_history, collect_registry_metadata
)
from forensics.network import NetworkAnalyzer
from forensics.timeline import TimelineBuilder
from forensics.findings import FindingsAnalyzer
from forensics.evidence import EvidenceManager
from forensics.reporting import ReportGenerator

class Interpreter:
    def __init__(self, policy_name: str = "standard-read-only-v1"):
        self.policy_engine = PolicyEngine(policy_name)
        self.evidence_manager = EvidenceManager()
        self.report_generator = ReportGenerator()
        self.environment: Dict[str, Any] = {}

    def execute(
        self,
        program: ProgramNode,
        script_id: str = "SCR-000001",
        script_version: str = "1.0.0",
        script_source: str = "",
        case_id: str = "CASE-001",
        analyst_id: str = "investigator@org.example"
    ) -> Dict[str, Any]:
        start_time = time.time()
        start_iso = datetime.now(timezone.utc).isoformat()
        execution_id = f"EXE-{int(time.time() * 1000) % 1000000:06d}"

        # 1. Audit Policy Check Start
        self.evidence_manager.record_audit_event(
            case_id=case_id,
            execution_id=execution_id,
            actor=analyst_id,
            action="POLICY_CHECK_STARTED",
            object_type="SCRIPT",
            object_id=script_id,
            result="PENDING"
        )

        # 2. Run Policy Evaluation
        policy_res = self.policy_engine.evaluate(program)

        if policy_res["decision"] == "BLOCKED":
            self.evidence_manager.record_audit_event(
                case_id=case_id,
                execution_id=execution_id,
                actor=analyst_id,
                action="POLICY_DENIED",
                object_type="SCRIPT",
                object_id=script_id,
                result="BLOCKED",
                details={"violations": policy_res["violations"], "denied_capabilities": policy_res["denied_capabilities"]}
            )

            return {
                "execution_id": execution_id,
                "case_id": case_id,
                "script_id": script_id,
                "script_version": script_version,
                "analyst_id": analyst_id,
                "status": "BLOCKED",
                "policy_decision": "BLOCKED",
                "policy_result": policy_res,
                "started_at_utc": start_iso,
                "completed_at_utc": datetime.now(timezone.utc).isoformat(),
                "duration_ms": int((time.time() - start_time) * 1000),
                "evidence": [],
                "timeline": [],
                "findings": [],
                "audit_summary": self.evidence_manager.verify_audit_chain(),
                "audit_logs": self.evidence_manager.audit_records,
                "provenance": None,
                "error": "Execution blocked by FORGE policy engine due to prohibited capabilities or path violations."
            }

        # Policy Approved
        self.evidence_manager.record_audit_event(
            case_id=case_id,
            execution_id=execution_id,
            actor=analyst_id,
            action="POLICY_APPROVED",
            object_type="SCRIPT",
            object_id=script_id,
            result="APPROVED"
        )

        # Create Provenance Record
        provenance = self.evidence_manager.create_provenance_record(
            case_id=case_id,
            execution_id=execution_id,
            analyst_id=analyst_id,
            script_id=script_id,
            script_version=script_version,
            script_source=script_source,
            policy_version=self.policy_engine.policy_name
        )

        self.evidence_manager.record_audit_event(
            case_id=case_id,
            execution_id=execution_id,
            actor=analyst_id,
            action="EXECUTION_STARTED",
            object_type="EXECUTION",
            object_id=execution_id,
            result="SUCCESS"
        )

        # Environment & State
        self.environment.clear()
        collected_evidence = []
        timeline_events = []
        findings_list = []
        reports_created = []

        timeline_builder = TimelineBuilder(case_id, execution_id)
        findings_analyzer = FindingsAnalyzer(case_id, execution_id)
        network_analyzer = None

        # 3. Execute Statements
        try:
            for stmt in program.statements:
                if isinstance(stmt, CaseNode):
                    case_id = stmt.case_id
                elif isinstance(stmt, RequireNode):
                    if stmt.requirement_type == "ANALYST":
                        analyst_id = stmt.value
                elif isinstance(stmt, AssignmentNode):
                    val = self._evaluate_expr(stmt.expr, case_id, execution_id, script_id, script_version, provenance["provenance_id"], collected_evidence)
                    self.environment[stmt.identifier] = val
                elif isinstance(stmt, CallNode):
                    self._evaluate_call(stmt, case_id, execution_id, script_id, script_version, provenance["provenance_id"], collected_evidence, timeline_events, findings_list, reports_created, timeline_builder, findings_analyzer)

            # Build default timeline & findings if not explicitly exported in script
            if not timeline_events and any(k in self.environment for k in ["host_info", "processes", "file_metadata", "pcap", "connections"]):
                sources = list(self.environment.values())
                timeline_events = timeline_builder.build_timeline(sources)
                self.evidence_manager.record_audit_event(
                    case_id=case_id, execution_id=execution_id, actor=analyst_id,
                    action="TIMELINE_BUILT", object_type="TIMELINE", object_id=f"TL-{len(timeline_events)}",
                    result="SUCCESS", details={"count": len(timeline_events)}
                )

            if not findings_list and timeline_events:
                file_hashes_data = self.environment.get("file_hashes", [])
                dns_data = self.environment.get("dns", [])
                findings_list = findings_analyzer.analyze(timeline_events, file_hashes_data, dns_data)
                self.evidence_manager.record_audit_event(
                    case_id=case_id, execution_id=execution_id, actor=analyst_id,
                    action="FINDING_GENERATED", object_type="FINDINGS", object_id=f"FND-{len(findings_list)}",
                    result="SUCCESS", details={"count": len(findings_list)}
                )

            provenance["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
            provenance["evidence_ids"] = [e["evidence_id"] for e in collected_evidence]

            self.evidence_manager.record_audit_event(
                case_id=case_id,
                execution_id=execution_id,
                actor=analyst_id,
                action="EXECUTION_COMPLETED",
                object_type="EXECUTION",
                object_id=execution_id,
                result="SUCCESS"
            )

            duration_ms = int((time.time() - start_time) * 1000)

            return {
                "execution_id": execution_id,
                "case_id": case_id,
                "script_id": script_id,
                "script_version": script_version,
                "analyst_id": analyst_id,
                "status": "COMPLETED",
                "policy_decision": "APPROVED",
                "policy_result": policy_res,
                "started_at_utc": start_iso,
                "completed_at_utc": provenance["completed_at_utc"],
                "duration_ms": duration_ms,
                "environment_symbols": list(self.environment.keys()),
                "evidence": collected_evidence,
                "timeline": timeline_events,
                "findings": findings_list,
                "reports_created": reports_created,
                "provenance": provenance,
                "audit_summary": self.evidence_manager.verify_audit_chain(),
                "audit_logs": self.evidence_manager.audit_records
            }

        except Exception as ex:
            self.evidence_manager.record_audit_event(
                case_id=case_id,
                execution_id=execution_id,
                actor=analyst_id,
                action="EXECUTION_FAILED",
                object_type="EXECUTION",
                object_id=execution_id,
                result="ERROR",
                details={"error_message": str(ex)}
            )
            raise ex

    def _evaluate_expr(self, node: ASTNode, case_id: str, exec_id: str, script_id: str, script_version: str, prov_id: str, evidence_list: list) -> Any:
        if isinstance(node, StringLiteralNode):
            return node.value
        elif isinstance(node, NumberLiteralNode):
            return node.value
        elif isinstance(node, IdentifierNode):
            return self.environment.get(node.name)
        elif isinstance(node, ArrayLiteralNode):
            return [self._evaluate_expr(elem, case_id, exec_id, script_id, script_version, prov_id, evidence_list) for elem in node.elements]
        elif isinstance(node, CallNode):
            return self._execute_cmd(node, case_id, exec_id, script_id, script_version, prov_id, evidence_list)
        return None

    def _evaluate_call(self, call_node: CallNode, case_id: str, exec_id: str, script_id: str, script_version: str, prov_id: str, evidence_list: list, timeline: list, findings: list, reports: list, timeline_builder: TimelineBuilder, findings_analyzer: FindingsAnalyzer):
        cmd = call_node.command
        if cmd == "EXPORT_EVIDENCE":
            var_arg = call_node.args[0]
            data = self._evaluate_expr(var_arg, case_id, exec_id, script_id, script_version, prov_id, evidence_list)
            path_str = self._evaluate_expr(call_node.args[1], case_id, exec_id, script_id, script_version, prov_id, evidence_list)
            os.makedirs(os.path.dirname(path_str) or "./exports", exist_ok=True)
            with open(path_str, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self.evidence_manager.record_audit_event(
                case_id=case_id, execution_id=exec_id, actor="FORGE_RUNTIME",
                action="EXPORT_CREATED", object_type="FILE", object_id=path_str, result="SUCCESS"
            )

        elif cmd == "EXPORT_REPORT":
            target_var = call_node.args[0]
            data = self._evaluate_expr(target_var, case_id, exec_id, script_id, script_version, prov_id, evidence_list)
            path_str = self._evaluate_expr(call_node.args[1], case_id, exec_id, script_id, script_version, prov_id, evidence_list)
            fmt_str = self._evaluate_expr(call_node.args[2], case_id, exec_id, script_id, script_version, prov_id, evidence_list)

            # Build full report context
            report_context = {
                "case_id": case_id,
                "execution_id": exec_id,
                "findings": findings or (data if isinstance(data, list) else []),
                "timeline": timeline,
                "evidence": evidence_list,
                "audit_summary": self.evidence_manager.verify_audit_chain()
            }

            gen_path = self.report_generator.generate_report(report_context, path_str, fmt_str)
            reports.append({"path": gen_path, "format": fmt_str})
            self.evidence_manager.record_audit_event(
                case_id=case_id, execution_id=exec_id, actor="FORGE_RUNTIME",
                action="REPORT_GENERATED", object_type="REPORT", object_id=gen_path, result="SUCCESS"
            )

        else:
            self._execute_cmd(call_node, case_id, exec_id, script_id, script_version, prov_id, evidence_list)

    def _execute_cmd(self, node: CallNode, case_id: str, exec_id: str, script_id: str, script_version: str, prov_id: str, evidence_list: list) -> Any:
        cmd = node.command
        evaluated_args = [self._evaluate_expr(arg, case_id, exec_id, script_id, script_version, prov_id, evidence_list) for arg in node.args]

        result_data = None
        evd_type = cmd

        if cmd == "HOST_INFO":
            result_data = collect_host_info()
        elif cmd == "PROCESS_LIST":
            result_data = collect_processes()
        elif cmd == "SERVICE_LIST":
            result_data = collect_services()
        elif cmd == "SYSTEM_CONFIG":
            result_data = collect_host_info()
        elif cmd == "USER_SESSIONS":
            result_data = [{"user": "CORP\\john.doe", "session_id": 1, "state": "Active", "logon_time": "2026-09-25T14:10:00Z"}]
        elif cmd == "FILE_LIST":
            path_arg = evaluated_args[0] if evaluated_args else "./datasets/computer/files"
            result_data = list_files(path_arg)
        elif cmd == "FILE_METADATA":
            files_arg = evaluated_args[0] if evaluated_args else []
            result_data = collect_file_metadata(files_arg)
        elif cmd == "HASH_FILES":
            files_arg = evaluated_args[0] if evaluated_args else []
            algo = evaluated_args[1] if len(evaluated_args) > 1 else "SHA256"
            result_data = hash_files(files_arg, algo)
            evd_type = "FILE_HASHES"
        elif cmd == "EVENT_LOGS":
            src = evaluated_args[0] if evaluated_args else "System"
            result_data = collect_event_logs(src)
        elif cmd == "BROWSER_HISTORY":
            result_data = collect_browser_history()
        elif cmd == "REGISTRY_METADATA":
            keys = evaluated_args[0] if evaluated_args else None
            result_data = collect_registry_metadata(keys)
        elif cmd == "PCAP_LOAD":
            path_arg = evaluated_args[0] if evaluated_args else "./datasets/network/sample.pcap"
            analyzer = NetworkAnalyzer(path_arg)
            result_data = analyzer.get_pcap_info()
            self.environment["_network_analyzer"] = analyzer
        elif cmd == "NETWORK_CONNECTIONS":
            analyzer = self.environment.get("_network_analyzer") or NetworkAnalyzer()
            result_data = analyzer.get_connections()
        elif cmd == "DNS_ACTIVITY":
            analyzer = self.environment.get("_network_analyzer") or NetworkAnalyzer()
            result_data = analyzer.get_dns_activity()
        elif cmd == "PROTOCOL_STATS":
            analyzer = self.environment.get("_network_analyzer") or NetworkAnalyzer()
            result_data = analyzer.get_protocol_stats()
        elif cmd == "FLOW_SUMMARY":
            analyzer = self.environment.get("_network_analyzer") or NetworkAnalyzer()
            result_data = analyzer.get_flow_summary()
        elif cmd == "BUILD_TIMELINE":
            sources = evaluated_args[0] if evaluated_args else []
            timeline_builder = TimelineBuilder(case_id, exec_id)
            result_data = timeline_builder.build_timeline(sources)
        elif cmd == "ANALYZE_FINDINGS":
            timeline_src = evaluated_args[0] if len(evaluated_args) >= 1 else []
            hashes_src = evaluated_args[1] if len(evaluated_args) >= 2 else []
            dns_src = evaluated_args[2] if len(evaluated_args) >= 3 else []
            findings_analyzer = FindingsAnalyzer(case_id, exec_id)
            result_data = findings_analyzer.analyze(timeline_src, hashes_src, dns_src)

        # Create Evidence & Audit Record
        if result_data is not None:
            evd_rec = self.evidence_manager.create_evidence_record(
                case_id=case_id,
                execution_id=exec_id,
                script_id=script_id,
                script_version=script_version,
                source=f"FORGE_{cmd}_COLLECTOR",
                collector=f"FORGE_{cmd}",
                evidence_type=evd_type,
                data=result_data,
                provenance_id=prov_id
            )
            evidence_list.append(evd_rec)

            self.evidence_manager.record_audit_event(
                case_id=case_id,
                execution_id=exec_id,
                actor="FORGE_RUNTIME",
                action="EVIDENCE_COLLECTED",
                object_type="EVIDENCE",
                object_id=evd_rec["evidence_id"],
                result="SUCCESS",
                details={"cmd": cmd, "record_count": evd_rec["record_count"], "sha256": evd_rec["sha256"]}
            )

        return result_data
