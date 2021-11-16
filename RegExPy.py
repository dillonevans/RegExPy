from Parser import Parser, Lexer
from SyntaxNode import *
lexer = Lexer("a(a|b)b")
parser = Parser(lexer)

tree = parser.parseExpression(0)
tree.printTree()
print()
