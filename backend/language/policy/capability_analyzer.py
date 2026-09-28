"""
FORGE Capability Analyzer
Analyzes script AST to extract required, invoked, granted, and prohibited capabilities.
"""

from typing import Dict, Any, List, Set
from language.ast.nodes import (
    ProgramNode, CaseNode, RequireNode, CapabilityListNode,
    AssignmentNode, CallNode, StringLiteralNode, ArrayLiteralNode, ASTNode
)
from language.semantic.validator import ALLOWED_COMMANDS, PROHIBITED_COMMANDS, PROHIBITED_CAPABILITIES

COMMAND_CAPABILITY_MAP = {cmd: info["cap"] for cmd, info in ALLOWED_COMMANDS.items()}

class CapabilityAnalyzer:
    def __init__(self):
        self.declared_capabilities: List[str] = []
        self.invoked_capabilities: Set[str] = set()
        self.denied_capabilities: List[str] = []
        self.command_checks: List[Dict[str, Any]] = []

    def analyze(self, program: ProgramNode) -> Dict[str, Any]:
        self.declared_capabilities.clear()
        self.invoked_capabilities.clear()
        self.denied_capabilities.clear()
        self.command_checks.clear()

        # Step 1: Collect declared capabilities
        for stmt in program.statements:
            if isinstance(stmt, RequireNode) and stmt.requirement_type == "CAPABILITIES":
                if isinstance(stmt.value, CapabilityListNode):
                    for cap in stmt.value.capabilities:
                        self.declared_capabilities.append(cap)
                        if cap in PROHIBITED_CAPABILITIES:
                            if cap not in self.denied_capabilities:
                                self.denied_capabilities.append(cap)

        # Step 2: Inspect commands invoked in program
        for stmt in program.statements:
            self._inspect_node(stmt)

        # Step 3: Check if all invoked command capabilities are granted by declared capabilities
        declared_set = set(self.declared_capabilities)
        missing_capabilities = list(self.invoked_capabilities - declared_set)

        # Determine decision
        if self.denied_capabilities or missing_capabilities:
            policy_decision = "BLOCKED"
        else:
            policy_decision = "APPROVED"

        return {
            "required_capabilities": self.declared_capabilities,
            "invoked_capabilities": sorted(list(self.invoked_capabilities)),
            "missing_capabilities": missing_capabilities,
            "denied_capabilities": self.denied_capabilities,
            "command_checks": self.command_checks,
            "policy_decision": policy_decision
        }

    def _inspect_node(self, node: ASTNode):
        if isinstance(node, CallNode):
            cmd = node.command
            if cmd in PROHIBITED_COMMANDS:
                cap = PROHIBITED_COMMANDS[cmd]
                if cap not in self.denied_capabilities:
                    self.denied_capabilities.append(cap)
                self.command_checks.append({
                    "command": cmd,
                    "required_capability": cap,
                    "status": "DENIED",
                    "reason": f"Prohibited operation '{cmd}' violates safety policy",
                    "line": node.line
                })
            elif cmd in COMMAND_CAPABILITY_MAP:
                cap = COMMAND_CAPABILITY_MAP[cmd]
                self.invoked_capabilities.add(cap)
                is_granted = cap in self.declared_capabilities
                status = "GRANTED" if is_granted else "MISSING"
                reason = "Capability declared and allowed" if is_granted else f"Capability '{cap}' not declared in REQUIRE CAPABILITIES"
                self.command_checks.append({
                    "command": cmd,
                    "required_capability": cap,
                    "status": status,
                    "reason": reason,
                    "line": node.line
                })
            for arg in node.args:
                self._inspect_node(arg)

        elif isinstance(node, AssignmentNode):
            self._inspect_node(node.expr)

        elif isinstance(node, ArrayLiteralNode):
            for elem in node.elements:
                self._inspect_node(elem)
