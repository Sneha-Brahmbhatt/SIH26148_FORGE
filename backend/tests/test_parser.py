from language.lexer import Lexer
from language.parser import Parser

def test_parser_ast():
    code = 'CASE "CASE-101"\nREQUIRE CAPABILITIES [HOST_READ, FILE_READ]\nfiles = FILE_LIST("./datasets/computer/files")'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    assert ast.node_type == "ProgramNode"
    assert len(ast.statements) == 3
