"""
FORGE DSL Semantic Validator
Performs static analysis on the AST to verify command validity, symbol definitions,
argument types, arities, and policy pre-checks before execution.
"""

from typing import List, Dict, Any, Set
from language.ast.nodes import (
    ProgramNode, CaseNode, RequireNode, CapabilityListNode,
    AssignmentNode, CallNode, StringLiteralNode, NumberLiteralNode,
    IdentifierNode, ArrayLiteralNode, ExportNode, ReportNode, ASTNode
)

ALLOWED_COMMANDS = {
    "HOST_INFO": {"arity": [0], "cap": "HOST_READ"},
    "PROCESS_LIST": {"arity": [0], "cap": "PROCESS_READ"},
    "SERVICE_LIST": {"arity": [0], "cap": "SERVICE_READ"},
    "SYSTEM_CONFIG": {"arity": [0], "cap": "SYSTEM_READ"},
    "USER_SESSIONS": {"arity": [0], "cap": "USER_READ"},
    "FILE_LIST": {"arity": [1], "cap": "FILE_READ"},
    "FILE_METADATA": {"arity": [1], "cap": "FILE_READ"},
    "HASH_FILES": {"arity": [2], "cap": "FILE_HASH"},
    "EVENT_LOGS": {"arity": [1], "cap": "EVENT_READ"},
    "BROWSER_HISTORY": {"arity": [0], "cap": "ARTIFACT_READ"},
    "REGISTRY_METADATA": {"arity": [1], "cap": "REGISTRY_READ"},
    "PCAP_LOAD": {"arity": [1], "cap": "PCAP_READ"},
    "NETWORK_CONNECTIONS": {"arity": [1], "cap": "NETWORK_READ"},
    "DNS_ACTIVITY": {"arity": [1], "cap": "NETWORK_READ"},
    "PROTOCOL_STATS": {"arity": [1], "cap": "NETWORK_READ"},
    "FLOW_SUMMARY": {"arity": [1], "cap": "NETWORK_READ"},
    "BUILD_TIMELINE": {"arity": [1], "cap": "TIMELINE_BUILD"},
    "ANALYZE_FINDINGS": {"arity": [2, 3, 4], "cap": "FINDING_GENERATE"},
    "EXPORT_EVIDENCE": {"arity": [2], "cap": "EXPORT_DATA"},
    "EXPORT_REPORT": {"arity": [3], "cap": "REPORT_GENERATE"},
}

PROHIBITED_COMMANDS = {
    "EXECUTE_PROCESS": "EXECUTE_PROCESS",
    "WRITE_EVIDENCE": "WRITE_EVIDENCE",
    "DISABLE_SECURITY_CONTROL": "DISABLE_SECURITY_CONTROL",
    "INJECT_CODE": "INJECT_CODE",
    "LOAD_DRIVER": "LOAD_DRIVER",
    "BYPASS_SECURITY_CONTROL": "BYPASS_SECURITY_CONTROL"
}

ALLOWED_CAPABILITIES = {
    "CASE_MANAGE", "IDENTITY_ASSERT", "POLICY_ASSERT", "CAPABILITY_ASSERT",
    "HOST_READ", "PROCESS_READ", "SERVICE_READ", "SYSTEM_READ", "USER_READ",
    "FILE_READ", "FILE_HASH", "EVENT_READ", "ARTIFACT_READ", "REGISTRY_READ",
    "PCAP_READ", "NETWORK_READ", "TIMELINE_BUILD", "FINDING_GENERATE",
    "EXPORT_DATA", "REPORT_GENERATE"
}

PROHIBITED_CAPABILITIES = {
    "WRITE_EVIDENCE", "EXECUTE_PROCESS", "LOAD_DRIVER", "INJECT_CODE",
    "RAW_DEVICE_WRITE", "NETWORK_EGRESS", "DISABLE_SECURITY_CONTROL",
    "BYPASS_SECURITY_CONTROL"
}

class SemanticValidator:
    def __init__(self):
        self.diagnostics: List[Dict[str, Any]] = []
        self.defined_variables: Set[str] = set()
        self.has_case_declaration = False
        self.has_capability_declaration = False
        self.declared_capabilities: Set[str] = set()

    def add_error(self, code: str, message: str, line: int, column: int):
        self.diagnostics.append({
            "level": "ERROR",
            "code": code,
            "message": message,
            "line": line,
            "column": column
        })

    def add_warning(self, code: str, message: str, line: int, column: int):
        self.diagnostics.append({
            "level": "WARNING",
            "code": code,
            "message": message,
            "line": line,
            "column": column
        })

    def validate(self, program: ProgramNode) -> List[Dict[str, Any]]:
        self.diagnostics.clear()
        self.defined_variables.clear()
        self.has_case_declaration = False
        self.has_capability_declaration = False
        self.declared_capabilities.clear()

        for stmt in program.statements:
            self._visit_statement(stmt)

        if not self.has_case_declaration:
            self.add_error("MISSING_CASE_DECLARATION", "Script must begin with a CASE declaration (e.g. CASE 'CASE-001')", 1, 1)

        if not self.has_capability_declaration:
            self.add_error("MISSING_CAPABILITY_DECLARATION", "Script must declare capabilities using REQUIRE CAPABILITIES [...]", 1, 1)

        return self.diagnostics

    def _visit_statement(self, stmt: ASTNode):
        if isinstance(stmt, CaseNode):
            self.has_case_declaration = True
            if not stmt.case_id or not stmt.case_id.strip():
                self.add_error("EMPTY_CASE_ID", "Case ID cannot be empty", stmt.line, stmt.column)

        elif isinstance(stmt, RequireNode):
            if stmt.requirement_type == "CAPABILITIES":
                self.has_capability_declaration = True
                if isinstance(stmt.value, CapabilityListNode):
                    for cap in stmt.value.capabilities:
                        if cap in PROHIBITED_CAPABILITIES:
                            self.add_error("PROHIBITED_CAPABILITY_REQUESTED", f"Requested capability '{cap}' is prohibited by safety policy", stmt.line, stmt.column)
                        elif cap not in ALLOWED_CAPABILITIES:
                            self.add_error("UNKNOWN_CAPABILITY", f"Unknown capability '{cap}'", stmt.line, stmt.column)
                        else:
                            self.declared_capabilities.add(cap)

        elif isinstance(stmt, AssignmentNode):
            # Visit expression first to ensure right-hand side symbols exist
            self._visit_expression(stmt.expr)
            if stmt.identifier in self.defined_variables:
                self.add_warning("DUPLICATE_VARIABLE_DECLARATION", f"Variable '{stmt.identifier}' is redefined", stmt.line, stmt.column)
            self.defined_variables.add(stmt.identifier)

        elif isinstance(stmt, CallNode):
            self._visit_call(stmt)

    def _visit_expression(self, expr: ASTNode):
        if isinstance(expr, IdentifierNode):
            if expr.name not in self.defined_variables:
                self.add_error("UNDEFINED_VARIABLE", f"Variable '{expr.name}' used before assignment", expr.line, expr.column)
        elif isinstance(expr, CallNode):
            self._visit_call(expr)
        elif isinstance(expr, ArrayLiteralNode):
            for elem in expr.elements:
                self._visit_expression(elem)

    def _visit_call(self, call: CallNode):
        cmd = call.command

        # Check prohibited command
        if cmd in PROHIBITED_COMMANDS:
            self.add_error("PROHIBITED_COMMAND_USED", f"Command '{cmd}' is prohibited and violates forensic execution policy", call.line, call.column)
            return

        # Check unknown command
        if cmd not in ALLOWED_COMMANDS:
            self.add_error("UNKNOWN_COMMAND", f"Unknown forensic command: '{cmd}'", call.line, call.column)
            return

        spec = ALLOWED_COMMANDS[cmd]
        arg_count = len(call.args)
        if arg_count not in spec["arity"]:
            allowed_str = " or ".join(str(a) for a in spec["arity"])
            self.add_error("INVALID_ARGUMENT_COUNT", f"Command '{cmd}' expects {allowed_str} arguments, but got {arg_count}", call.line, call.column)

        # Command specific checks
        for arg in call.args:
            self._visit_expression(arg)

        if cmd == "HASH_FILES":
            if len(call.args) >= 2 and isinstance(call.args[1], StringLiteralNode):
                algo = call.args[1].value.upper()
                if algo not in ("SHA256", "SHA-256", "MD5", "SHA512"):
                    self.add_error("INVALID_HASH_ALGORITHM", f"Unsupported hash algorithm '{algo}'. Supported: SHA256, SHA512, MD5", call.line, call.column)

        elif cmd == "EVENT_LOGS":
            if len(call.args) >= 1 and isinstance(call.args[0], StringLiteralNode):
                source = call.args[0].value
                if source not in ("System", "Security", "Application"):
                    self.add_error("INVALID_EVENT_SOURCE", f"Invalid event log source '{source}'. Expected System, Security, or Application", call.line, call.column)

        elif cmd == "EXPORT_REPORT":
            if len(call.args) >= 3 and isinstance(call.args[2], StringLiteralNode):
                fmt = call.args[2].value.lower()
                if fmt not in ("json", "csv", "html", "pdf"):
                    self.add_error("INVALID_REPORT_FORMAT", f"Invalid report format '{fmt}'. Supported: json, csv, html, pdf", call.line, call.column)
