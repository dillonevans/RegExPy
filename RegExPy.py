from NFAToDFA import subsetConstruction
from Parser import Parser, Lexer
from ThompsonVisitor import ThompsonVisitor
from NFA import EPS

def isMatch(string, regex) -> bool:
    lexer = Lexer(regex)
    parser = Parser(lexer)
    tree = parser.parseExpression(0)
    visitor = ThompsonVisitor([*lexer.alphabet, EPS])

    nfa = tree.accept(visitor)
    dfa = subsetConstruction(nfa, lexer.alphabet)
    return dfa.accept(string)


