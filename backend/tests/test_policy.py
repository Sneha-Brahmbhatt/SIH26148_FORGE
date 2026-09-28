from language.lexer import Lexer
from language.parser import Parser
from language.policy import PolicyEngine

def test_policy_approval():
    code = 'CASE "CASE-001"\nREQUIRE CAPABILITIES [HOST_READ]\nhost_info = HOST_INFO()'
    tokens = Lexer(code).tokenize()
    ast = Parser(tokens).parse()
    res = PolicyEngine().evaluate(ast)
    assert res["decision"] == "APPROVED"

def test_policy_denial():
    code = 'CASE "CASE-BAD"\nREQUIRE CAPABILITIES [EXECUTE_PROCESS]\nEXECUTE_PROCESS("cmd.exe")'
    tokens = Lexer(code).tokenize()
    ast = Parser(tokens).parse()
    res = PolicyEngine().evaluate(ast)
    assert res["decision"] == "BLOCKED"
    assert "EXECUTE_PROCESS" in res["denied_capabilities"]
