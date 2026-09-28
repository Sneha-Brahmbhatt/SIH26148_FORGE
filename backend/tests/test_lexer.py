from language.lexer import Lexer, TokenType

def test_lexer_basic():
    code = 'CASE "CASE-001"\nREQUIRE ANALYST "investigator@org.example"'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.CASE
    assert tokens[1].type == TokenType.STRING
    assert tokens[1].value == "CASE-001"
    assert tokens[3].type == TokenType.REQUIRE
    assert tokens[4].type == TokenType.ANALYST
