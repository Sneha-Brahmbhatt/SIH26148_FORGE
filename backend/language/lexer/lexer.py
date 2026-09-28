"""
FORGE DSL Lexer
Tokenizes FORGE forensic script source code into structured token streams.
Preserves precise line and column information for diagnostics.
"""

from enum import Enum, auto
from typing import List, Optional, Any
import re

class TokenType(Enum):
    # Keywords
    CASE = "CASE"
    REQUIRE = "REQUIRE"
    ANALYST = "ANALYST"
    POLICY = "POLICY"
    CAPABILITIES = "CAPABILITIES"
    
    # Forensic Commands
    HOST_INFO = "HOST_INFO"
    PROCESS_LIST = "PROCESS_LIST"
    SERVICE_LIST = "SERVICE_LIST"
    SYSTEM_CONFIG = "SYSTEM_CONFIG"
    USER_SESSIONS = "USER_SESSIONS"
    FILE_LIST = "FILE_LIST"
    FILE_METADATA = "FILE_METADATA"
    HASH_FILES = "HASH_FILES"
    EVENT_LOGS = "EVENT_LOGS"
    BROWSER_HISTORY = "BROWSER_HISTORY"
    REGISTRY_METADATA = "REGISTRY_METADATA"
    PCAP_LOAD = "PCAP_LOAD"
    NETWORK_CONNECTIONS = "NETWORK_CONNECTIONS"
    DNS_ACTIVITY = "DNS_ACTIVITY"
    PROTOCOL_STATS = "PROTOCOL_STATS"
    FLOW_SUMMARY = "FLOW_SUMMARY"
    BUILD_TIMELINE = "BUILD_TIMELINE"
    ANALYZE_FINDINGS = "ANALYZE_FINDINGS"
    EXPORT_EVIDENCE = "EXPORT_EVIDENCE"
    EXPORT_REPORT = "EXPORT_REPORT"

    # Prohibited Commands (for semantic/lexer recognition & early blocking testing)
    EXECUTE_PROCESS = "EXECUTE_PROCESS"
    WRITE_EVIDENCE = "WRITE_EVIDENCE"
    DISABLE_SECURITY_CONTROL = "DISABLE_SECURITY_CONTROL"

    # Literals & Identifiers
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"

    # Operators & Punctuation
    ASSIGN = "="
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    COMMA = ","

    # Trivia & Sentinel
    NEWLINE = "NEWLINE"
    EOF = "EOF"

KEYWORDS = {
    "CASE": TokenType.CASE,
    "REQUIRE": TokenType.REQUIRE,
    "ANALYST": TokenType.ANALYST,
    "POLICY": TokenType.POLICY,
    "CAPABILITIES": TokenType.CAPABILITIES,
    
    # Commands
    "HOST_INFO": TokenType.HOST_INFO,
    "PROCESS_LIST": TokenType.PROCESS_LIST,
    "SERVICE_LIST": TokenType.SERVICE_LIST,
    "SYSTEM_CONFIG": TokenType.SYSTEM_CONFIG,
    "USER_SESSIONS": TokenType.USER_SESSIONS,
    "FILE_LIST": TokenType.FILE_LIST,
    "FILE_METADATA": TokenType.FILE_METADATA,
    "HASH_FILES": TokenType.HASH_FILES,
    "EVENT_LOGS": TokenType.EVENT_LOGS,
    "BROWSER_HISTORY": TokenType.BROWSER_HISTORY,
    "REGISTRY_METADATA": TokenType.REGISTRY_METADATA,
    "PCAP_LOAD": TokenType.PCAP_LOAD,
    "NETWORK_CONNECTIONS": TokenType.NETWORK_CONNECTIONS,
    "DNS_ACTIVITY": TokenType.DNS_ACTIVITY,
    "PROTOCOL_STATS": TokenType.PROTOCOL_STATS,
    "FLOW_SUMMARY": TokenType.FLOW_SUMMARY,
    "BUILD_TIMELINE": TokenType.BUILD_TIMELINE,
    "ANALYZE_FINDINGS": TokenType.ANALYZE_FINDINGS,
    "EXPORT_EVIDENCE": TokenType.EXPORT_EVIDENCE,
    "EXPORT_REPORT": TokenType.EXPORT_REPORT,

    # Prohibited
    "EXECUTE_PROCESS": TokenType.EXECUTE_PROCESS,
    "WRITE_EVIDENCE": TokenType.WRITE_EVIDENCE,
    "DISABLE_SECURITY_CONTROL": TokenType.DISABLE_SECURITY_CONTROL,
}

class Token:
    def __init__(self, type_: TokenType, value: Any, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def to_dict(self):
        return {
            "type": self.type.value if isinstance(self.type, TokenType) else str(self.type),
            "value": self.value,
            "line": self.line,
            "column": self.column
        }

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, L{self.line}:C{self.column})"

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"LexerError at line {line}, column {column}: {message}")
        self.message = message
        self.line = line
        self.column = column

class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.length = len(source_code)

    def _peek(self, offset: int = 0) -> Optional[str]:
        pos = self.position + offset
        if pos < self.length:
            return self.source[pos]
        return None

    def _advance(self) -> Optional[str]:
        if self.position < self.length:
            ch = self.source[self.position]
            self.position += 1
            if ch == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return ch
        return None

    def tokenize(self) -> List[Token]:
        tokens = []
        while self.position < self.length:
            ch = self._peek()

            # Skip whitespace except newlines
            if ch in (' ', '\t', '\r'):
                self._advance()
                continue

            # Newlines
            if ch == '\n':
                line, col = self.line, self.column
                self._advance()
                tokens.append(Token(TokenType.NEWLINE, "\n", line, col))
                continue

            # Line & block comments
            if ch == '/' and self._peek(1) == '/':
                while self._peek() is not None and self._peek() != '\n':
                    self._advance()
                continue
            
            if ch == '/' and self._peek(1) == '*':
                start_line, start_col = self.line, self.column
                self._advance() # /
                self._advance() # *
                while self.position < self.length:
                    if self._peek() == '*' and self._peek(1) == '/':
                        self._advance() # *
                        self._advance() # /
                        break
                    self._advance()
                else:
                    raise LexerError("Unterminated block comment", start_line, start_col)
                continue

            # String literals
            if ch in ('"', "'"):
                quote_type = ch
                start_line, start_col = self.line, self.column
                self._advance()
                val_chars = []
                escaped = False
                while self.position < self.length:
                    curr = self._peek()
                    if escaped:
                        if curr == 'n': val_chars.append('\n')
                        elif curr == 't': val_chars.append('\t')
                        elif curr == '\\': val_chars.append('\\')
                        elif curr == quote_type: val_chars.append(quote_type)
                        else: val_chars.append(curr)
                        escaped = False
                        self._advance()
                    elif curr == '\\':
                        escaped = True
                        self._advance()
                    elif curr == quote_type:
                        self._advance()
                        break
                    elif curr == '\n':
                        raise LexerError("Unterminated string literal", start_line, start_col)
                    else:
                        val_chars.append(curr)
                        self._advance()
                else:
                    raise LexerError("Unterminated string literal", start_line, start_col)
                tokens.append(Token(TokenType.STRING, "".join(val_chars), start_line, start_col))
                continue

            # Numbers
            if ch.isdigit():
                start_line, start_col = self.line, self.column
                num_chars = []
                is_float = False
                while self._peek() is not None and (self._peek().isdigit() or (self._peek() == '.' and not is_float)):
                    c = self._advance()
                    if c == '.':
                        is_float = True
                    num_chars.append(c)
                num_str = "".join(num_chars)
                num_val = float(num_str) if is_float else int(num_str)
                tokens.append(Token(TokenType.NUMBER, num_val, start_line, start_col))
                continue

            # Identifiers and Keywords
            if ch.isalpha() or ch == '_':
                start_line, start_col = self.line, self.column
                ident_chars = []
                while self._peek() is not None and (self._peek().isalnum() or self._peek() == '_'):
                    ident_chars.append(self._advance())
                word = "".join(ident_chars)
                token_type = KEYWORDS.get(word, TokenType.IDENTIFIER)
                tokens.append(Token(token_type, word, start_line, start_col))
                continue

            # Single-character tokens
            start_line, start_col = self.line, self.column
            if ch == '=':
                self._advance()
                tokens.append(Token(TokenType.ASSIGN, "=", start_line, start_col))
            elif ch == '(':
                self._advance()
                tokens.append(Token(TokenType.LPAREN, "(", start_line, start_col))
            elif ch == ')':
                self._advance()
                tokens.append(Token(TokenType.RPAREN, ")", start_line, start_col))
            elif ch == '[':
                self._advance()
                tokens.append(Token(TokenType.LBRACKET, "[", start_line, start_col))
            elif ch == ']':
                self._advance()
                tokens.append(Token(TokenType.RBRACKET, "]", start_line, start_col))
            elif ch == ',':
                self._advance()
                tokens.append(Token(TokenType.COMMA, ",", start_line, start_col))
            else:
                raise LexerError(f"Unexpected character '{ch}'", start_line, start_col)

        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens
