from typing import final
from Parser import Parser, Lexer
from TreeToNFA import *
lexer = Lexer("abc | ab")
parser = Parser(lexer)

tree = parser.parseExpression(0)

nfa = convertTreeToNFA(tree, lexer.alphabet)

for key, value in nfa.transitionFunction.items():

    if value:
        print(f"({key[0]}, {key[1]}) = {value}")
