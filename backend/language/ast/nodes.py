"""
FORGE AST Nodes
Defines AST data structures representing valid FORGE DSL constructs.
"""

from typing import List, Any, Dict, Optional

class ASTNode:
    def __init__(self, node_type: str, line: int = 1, column: int = 1, source_text: str = ""):
        self.node_type = node_type
        self.line = line
        self.column = column
        self.source_text = source_text
        self.children: List['ASTNode'] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_type": self.node_type,
            "line": self.line,
            "column": self.column,
            "source_text": self.source_text,
            "children": [child.to_dict() for child in self.children]
        }

class ProgramNode(ASTNode):
    def __init__(self, line: int = 1, column: int = 1):
        super().__init__("ProgramNode", line, column, "Program")
        self.statements: List[ASTNode] = []

    def add_statement(self, stmt: ASTNode):
        self.statements.append(stmt)
        self.children.append(stmt)

    def to_dict(self) -> Dict[str, Any]:
        res = super().to_dict()
        res["statements"] = [stmt.to_dict() for stmt in self.statements]
        return res

class CaseNode(ASTNode):
    def __init__(self, case_id: str, line: int = 1, column: int = 1):
        super().__init__("CaseNode", line, column, f'CASE "{case_id}"')
        self.case_id = case_id

    def to_dict(self) -> Dict[str, Any]:
        res = super().to_dict()
        res["case_id"] = self.case_id
        return res

class RequireNode(ASTNode):
    def __init__(self, requirement_type: str, value: Any, line: int = 1, column: int = 1):
        super().__init__("RequireNode", line, column, f'REQUIRE {requirement_type} {value}')
        self.requirement_type = requirement_type  # ANALYST, POLICY, CAPABILITIES
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        res = super().to_dict()
        res["requirement_type"] = self.requirement_type
        res["value"] = self.value if not isinstance(self.value, ASTNode) else self.value.to_dict()
        return res

class CapabilityListNode(ASTNode):
    def __init__(self, capabilities: List[str], line: int = 1, column: int = 1):
        super().__init__("CapabilityListNode", line, column, f'REQUIRE CAPABILITIES {capabilities}')
        self.capabilities = capabilities

    def to_dict(self) -> Dict[str, Any]:
        res = super().to_dict()
        res["capabilities"] = self.capabilities
        return res

class AssignmentNode(ASTNode):
    def __init__(self, identifier: str, expr: ASTNode, line: int = 1, column: int = 1):
        super().__init__("AssignmentNode", line, column, f'{identifier} = ...')
        self.identifier = identifier
        self.expr = expr
        self.children.append(expr)

    def to_dict(self) -> Dict[str, Any]:
        res = super().to_dict()
        res["identifier"] = self.identifier
        res["expr"] = self.expr.to_dict()
        return res

class CallNode(ASTNode):
    def __init__(self, command: str, args: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__("CallNode", line, column, f'{command}(...)')
        self.command = command
        self.args = args
        for arg in args:
            self.children.append(arg)

    def to_dict(self) -> Dict[str, Any]:
        res = super().to_dict()
        res["command"] = self.command
        res["args"] = [arg.to_dict() for arg in self.args]
        return res

class StringLiteralNode(ASTNode):
    def __init__(self, value: str, line: int = 1, column: int = 1):
        super().__init__("StringLiteralNode", line, column, f'"{value}"')
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        res = super().to_dict()
        res["value"] = self.value
        return res

class NumberLiteralNode(ASTNode):
    def __init__(self, value: float, line: int = 1, column: int = 1):
        super().__init__("NumberLiteralNode", line, column, str(value))
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        res = super().to_dict()
        res["value"] = self.value
        return res

class IdentifierNode(ASTNode):
    def __init__(self, name: str, line: int = 1, column: int = 1):
        super().__init__("IdentifierNode", line, column, name)
        self.name = name

    def to_dict(self) -> Dict[str, Any]:
        res = super().to_dict()
        res["name"] = self.name
        return res

class ArrayLiteralNode(ASTNode):
    def __init__(self, elements: List[ASTNode], line: int = 1, column: int = 1):
        super().__init__("ArrayLiteralNode", line, column, f'[{len(elements)} elements]')
        self.elements = elements
        for elem in elements:
            self.children.append(elem)

    def to_dict(self) -> Dict[str, Any]:
        res = super().to_dict()
        res["elements"] = [elem.to_dict() for elem in self.elements]
        return res

class ExportNode(ASTNode):
    def __init__(self, target_var: str, output_path: str, line: int = 1, column: int = 1):
        super().__init__("ExportNode", line, column, f'EXPORT_EVIDENCE({target_var}, "{output_path}")')
        self.target_var = target_var
        self.output_path = output_path

    def to_dict(self) -> Dict[str, Any]:
        res = super().to_dict()
        res["target_var"] = self.target_var
        res["output_path"] = self.output_path
        return res

class ReportNode(ASTNode):
    def __init__(self, target_var: str, output_path: str, format_type: str, line: int = 1, column: int = 1):
        super().__init__("ReportNode", line, column, f'EXPORT_REPORT({target_var}, "{output_path}", "{format_type}")')
        self.target_var = target_var
        self.output_path = output_path
        self.format_type = format_type

    def to_dict(self) -> Dict[str, Any]:
        res = super().to_dict()
        res["target_var"] = self.target_var
        res["output_path"] = self.output_path
        res["format_type"] = self.format_type
        return res
