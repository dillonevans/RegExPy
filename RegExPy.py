from typing import final
from Parser import Parser, Lexer
from SyntaxNode import *
from NFA import *
lexer = Lexer("ab")
parser = Parser(lexer)

tree = parser.parseExpression(0)

