"""
FORGE DSL Parser
Recursive-descent parser that constructs an Abstract Syntax Tree (AST) from Lexer tokens.
"""

from typing import List, Optional, Tuple, Any
from language.lexer.lexer import Token, TokenType
from language.ast.nodes import (
    ProgramNode, CaseNode, RequireNode, CapabilityListNode,
    AssignmentNode, CallNode, StringLiteralNode, NumberLiteralNode,
    IdentifierNode, ArrayLiteralNode, ExportNode, ReportNode, ASTNode
)

class ParserError(Exception):
    def __init__(self, message: str, line: int = 1, column: int = 1):
        super().__init__(f"ParserError at L{line}:C{column}: {message}")
        self.message = message
        self.line = line
        self.column = column

class Parser:
    def __init__(self, tokens: List[Token]):
        # Filter out NEWLINE tokens for easier parsing, but keep position data
        self.tokens = [t for t in tokens if t.type != TokenType.NEWLINE]
        self.position = 0
        self.length = len(self.tokens)

    def _peek(self, offset: int = 0) -> Token:
        pos = self.position + offset
        if pos < self.length:
            return self.tokens[pos]
        # Return EOF token
        last = self.tokens[-1] if self.tokens else Token(TokenType.EOF, "", 1, 1)
        return Token(TokenType.EOF, "", last.line, last.column)

    def _match(self, *types: TokenType) -> bool:
        if self._peek().type in types:
            self.position += 1
            return True
        return False

    def _expect(self, type_: TokenType, error_msg: str) -> Token:
        token = self._peek()
        if token.type == type_:
            self.position += 1
            return token
        raise ParserError(f"{error_msg} (got '{token.value}')", token.line, token.column)

    def parse(self) -> ProgramNode:
        first_token = self._peek()
        program = ProgramNode(first_token.line, first_token.column)

        while self._peek().type != TokenType.EOF:
            stmt = self._parse_statement()
            if stmt:
                program.add_statement(stmt)

        return program

    def _parse_statement(self) -> ASTNode:
        token = self._peek()

        if token.type == TokenType.CASE:
            return self._parse_case()
        elif token.type == TokenType.REQUIRE:
            return self._parse_require()
        elif token.type == TokenType.EXPORT_EVIDENCE:
            return self._parse_export_evidence()
        elif token.type == TokenType.EXPORT_REPORT:
            return self._parse_export_report()
        elif token.type == TokenType.IDENTIFIER:
            # Check if this is an assignment or function call
            if self._peek(1).type == TokenType.ASSIGN:
                return self._parse_assignment()
            elif self._peek(1).type == TokenType.LPAREN:
                return self._parse_function_call_statement()
            else:
                raise ParserError(f"Unexpected identifier '{token.value}'", token.line, token.column)
        elif token.type in (
            TokenType.HOST_INFO, TokenType.PROCESS_LIST, TokenType.SERVICE_LIST,
            TokenType.SYSTEM_CONFIG, TokenType.USER_SESSIONS, TokenType.FILE_LIST,
            TokenType.FILE_METADATA, TokenType.HASH_FILES, TokenType.EVENT_LOGS,
            TokenType.BROWSER_HISTORY, TokenType.REGISTRY_METADATA, TokenType.PCAP_LOAD,
            TokenType.NETWORK_CONNECTIONS, TokenType.DNS_ACTIVITY, TokenType.PROTOCOL_STATS,
            TokenType.FLOW_SUMMARY, TokenType.BUILD_TIMELINE, TokenType.ANALYZE_FINDINGS,
            TokenType.EXECUTE_PROCESS, TokenType.WRITE_EVIDENCE, TokenType.DISABLE_SECURITY_CONTROL
        ):
            return self._parse_function_call_statement()
        else:
            raise ParserError(f"Unexpected token '{token.value}'", token.line, token.column)

    def _parse_case(self) -> CaseNode:
        token = self._expect(TokenType.CASE, "Expected 'CASE'")
        id_token = self._expect(TokenType.STRING, "Expected case ID string literal after 'CASE'")
        return CaseNode(id_token.value, token.line, token.column)

    def _parse_require(self) -> ASTNode:
        req_token = self._expect(TokenType.REQUIRE, "Expected 'REQUIRE'")
        next_token = self._peek()

        if next_token.type == TokenType.ANALYST:
            self.position += 1
            val_token = self._expect(TokenType.STRING, "Expected analyst ID string literal after 'REQUIRE ANALYST'")
            return RequireNode("ANALYST", val_token.value, req_token.line, req_token.column)

        elif next_token.type == TokenType.POLICY:
            self.position += 1
            val_token = self._expect(TokenType.STRING, "Expected policy name string literal after 'REQUIRE POLICY'")
            return RequireNode("POLICY", val_token.value, req_token.line, req_token.column)

        elif next_token.type == TokenType.CAPABILITIES:
            self.position += 1
            self._expect(TokenType.LBRACKET, "Expected '[' after 'REQUIRE CAPABILITIES'")
            caps = []
            while self._peek().type != TokenType.RBRACKET and self._peek().type != TokenType.EOF:
                cap_tok = self._peek()
                if cap_tok.type in (TokenType.IDENTIFIER, TokenType.STRING) or cap_tok.type.name in (
                    "WRITE_EVIDENCE", "EXECUTE_PROCESS", "DISABLE_SECURITY_CONTROL"
                ):
                    caps.append(str(cap_tok.value))
                    self.position += 1
                else:
                    # Generic keyword or identifier capability name
                    caps.append(str(cap_tok.value))
                    self.position += 1

                if self._peek().type == TokenType.COMMA:
                    self.position += 1
            self._expect(TokenType.RBRACKET, "Expected ']' at end of capability list")
            cap_node = CapabilityListNode(caps, req_token.line, req_token.column)
            return RequireNode("CAPABILITIES", cap_node, req_token.line, req_token.column)
        else:
            raise ParserError(f"Unknown REQUIRE keyword '{next_token.value}'", next_token.line, next_token.column)

    def _parse_assignment(self) -> AssignmentNode:
        var_token = self._expect(TokenType.IDENTIFIER, "Expected variable identifier")
        self._expect(TokenType.ASSIGN, "Expected '='")
        expr = self._parse_expression()
        return AssignmentNode(var_token.value, expr, var_token.line, var_token.column)

    def _parse_function_call_statement(self) -> ASTNode:
        expr = self._parse_expression()
        return expr

    def _parse_expression(self) -> ASTNode:
        token = self._peek()

        if token.type == TokenType.STRING:
            self.position += 1
            return StringLiteralNode(token.value, token.line, token.column)

        elif token.type == TokenType.NUMBER:
            self.position += 1
            return NumberLiteralNode(token.value, token.line, token.column)

        elif token.type == TokenType.LBRACKET:
            return self._parse_array_literal()

        elif token.type == TokenType.IDENTIFIER:
            # Check if function call
            if self._peek(1).type == TokenType.LPAREN:
                return self._parse_call()
            self.position += 1
            return IdentifierNode(token.value, token.line, token.column)

        elif token.type in (
            TokenType.HOST_INFO, TokenType.PROCESS_LIST, TokenType.SERVICE_LIST,
            TokenType.SYSTEM_CONFIG, TokenType.USER_SESSIONS, TokenType.FILE_LIST,
            TokenType.FILE_METADATA, TokenType.HASH_FILES, TokenType.EVENT_LOGS,
            TokenType.BROWSER_HISTORY, TokenType.REGISTRY_METADATA, TokenType.PCAP_LOAD,
            TokenType.NETWORK_CONNECTIONS, TokenType.DNS_ACTIVITY, TokenType.PROTOCOL_STATS,
            TokenType.FLOW_SUMMARY, TokenType.BUILD_TIMELINE, TokenType.ANALYZE_FINDINGS,
            TokenType.EXPORT_EVIDENCE, TokenType.EXPORT_REPORT,
            TokenType.EXECUTE_PROCESS, TokenType.WRITE_EVIDENCE, TokenType.DISABLE_SECURITY_CONTROL
        ):
            return self._parse_call()

        else:
            raise ParserError(f"Unexpected token in expression: '{token.value}'", token.line, token.column)

    def _parse_call(self) -> CallNode:
        cmd_token = self._peek()
        self.position += 1
        self._expect(TokenType.LPAREN, f"Expected '(' after command {cmd_token.value}")

        args = []
        if self._peek().type != TokenType.RPAREN:
            while True:
                args.append(self._parse_expression())
                if self._peek().type == TokenType.COMMA:
                    self.position += 1
                else:
                    break

        self._expect(TokenType.RPAREN, f"Expected ')' after arguments for {cmd_token.value}")
        return CallNode(cmd_token.value, args, cmd_token.line, cmd_token.column)

    def _parse_array_literal(self) -> ArrayLiteralNode:
        token = self._expect(TokenType.LBRACKET, "Expected '['")
        elements = []
        if self._peek().type != TokenType.RBRACKET:
            while True:
                elements.append(self._parse_expression())
                if self._peek().type == TokenType.COMMA:
                    self.position += 1
                else:
                    break
        self._expect(TokenType.RBRACKET, "Expected ']'")
        return ArrayLiteralNode(elements, token.line, token.column)

    def _parse_export_evidence(self) -> CallNode:
        token = self._expect(TokenType.EXPORT_EVIDENCE, "Expected 'EXPORT_EVIDENCE'")
        self._expect(TokenType.LPAREN, "Expected '(' after EXPORT_EVIDENCE")
        target_var = self._parse_expression()
        self._expect(TokenType.COMMA, "Expected ',' after target variable in EXPORT_EVIDENCE")
        path_expr = self._parse_expression()
        self._expect(TokenType.RPAREN, "Expected ')' at end of EXPORT_EVIDENCE")
        return CallNode("EXPORT_EVIDENCE", [target_var, path_expr], token.line, token.column)

    def _parse_export_report(self) -> CallNode:
        token = self._expect(TokenType.EXPORT_REPORT, "Expected 'EXPORT_REPORT'")
        self._expect(TokenType.LPAREN, "Expected '(' after EXPORT_REPORT")
        target_var = self._parse_expression()
        self._expect(TokenType.COMMA, "Expected ',' after target variable in EXPORT_REPORT")
        path_expr = self._parse_expression()
        self._expect(TokenType.COMMA, "Expected ',' after path in EXPORT_REPORT")
        format_expr = self._parse_expression()
        self._expect(TokenType.RPAREN, "Expected ')' at end of EXPORT_REPORT")
        return CallNode("EXPORT_REPORT", [target_var, path_expr, format_expr], token.line, token.column)
