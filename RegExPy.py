from Parser import Parser, Lexer
from SyntaxNode import printTree
lexer = Lexer("ab|ba")
parser = Parser(lexer)

tree = parser.parseExpression(0)
printTree(tree)
