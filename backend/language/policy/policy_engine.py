"""
FORGE Policy Engine
Enforces execution policy 'standard-read-only-v1', capability checks, and path boundaries.
"""

from typing import Dict, Any, List
import os
import re
from language.ast.nodes import ProgramNode, CallNode, StringLiteralNode, ASTNode
from language.policy.capability_analyzer import CapabilityAnalyzer

APPROVED_DATASET_DIRS = ["datasets", "./datasets", "datasets/computer", "datasets/network"]
APPROVED_EXPORT_DIRS = ["exports", "./exports", "reports", "./reports"]

class PolicyEngine:
    def __init__(self, policy_name: str = "standard-read-only-v1"):
        self.policy_name = policy_name
        self.capability_analyzer = CapabilityAnalyzer()

    def evaluate(self, program: ProgramNode) -> Dict[str, Any]:
        cap_analysis = self.capability_analyzer.analyze(program)
        path_violations = self._validate_paths(program)

        violations = []
        if cap_analysis["denied_capabilities"]:
            for cap in cap_analysis["denied_capabilities"]:
                violations.append(f"Prohibited capability requested or required: {cap}")

        if cap_analysis["missing_capabilities"]:
            for cap in cap_analysis["missing_capabilities"]:
                violations.append(f"Command requires capability '{cap}' which was not declared in script REQUIRE CAPABILITIES")

        if path_violations:
            violations.extend(path_violations)

        decision = "APPROVED" if (not violations and cap_analysis["policy_decision"] == "APPROVED") else "BLOCKED"

        return {
            "policy_name": self.policy_name,
            "decision": decision,
            "required_capabilities": cap_analysis["required_capabilities"],
            "invoked_capabilities": cap_analysis["invoked_capabilities"],
            "missing_capabilities": cap_analysis["missing_capabilities"],
            "denied_capabilities": cap_analysis["denied_capabilities"],
            "command_checks": cap_analysis["command_checks"],
            "path_violations": path_violations,
            "violations": violations,
            "safety_statement": (
                "FORGE is intended only for authorized digital-forensic investigations "
                "and controlled security environments. It does not bypass, disable, evade, "
                "or interfere with endpoint security controls."
            )
        }

    def _validate_paths(self, node: ASTNode) -> List[str]:
        violations = []
        if isinstance(node, CallNode):
            cmd = node.command
            if cmd in ("FILE_LIST", "FILE_METADATA", "PCAP_LOAD"):
                if len(node.args) >= 1 and isinstance(node.args[0], StringLiteralNode):
                    path_str = node.args[0].value
                    if not self._is_safe_dataset_path(path_str):
                        violations.append(f"Access denied to dataset path '{path_str}'. Path must be within approved dataset directory.")

            elif cmd in ("EXPORT_EVIDENCE", "EXPORT_REPORT"):
                if len(node.args) >= 2 and isinstance(node.args[1], StringLiteralNode):
                    path_str = node.args[1].value
                    if not self._is_safe_export_path(path_str):
                        violations.append(f"Access denied to output path '{path_str}'. Path must be within approved exports/ or reports/ directory.")

            for arg in node.args:
                violations.extend(self._validate_paths(arg))

        elif isinstance(node, ProgramNode):
            for stmt in node.statements:
                violations.extend(self._validate_paths(stmt))

        return violations

    def _is_safe_dataset_path(self, path_str: str) -> bool:
        normalized = path_str.replace("\\", "/")
        if ".." in normalized.split("/"):
            return False
        return any(normalized.startswith(prefix) for prefix in ["./datasets", "datasets", "/datasets"]) or "datasets/" in normalized

    def _is_safe_export_path(self, path_str: str) -> bool:
        normalized = path_str.replace("\\", "/")
        if ".." in normalized.split("/"):
            return False
        return any(normalized.startswith(prefix) for prefix in [
            "./exports", "exports", "./reports", "reports"
        ]) or "exports/" in normalized or "reports/" in normalized
