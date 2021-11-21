from NFAToDFA import subsetConstruction
from Parser import Parser, Lexer
from ConvertToNFAVisitor import ConvertToNFAVisitor
from NFA import EPS

def isMatch(string, regex) -> bool:
    lexer = Lexer(regex)
    parser = Parser(lexer)
    tree = parser.parseExpression(0)
    visitor = ConvertToNFAVisitor([*lexer.alphabet, EPS])

    nfa = tree.accept(visitor)
    dfa = subsetConstruction(nfa, lexer.alphabet)
    return dfa.accept(string)


