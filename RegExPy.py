from NFAToDFA import subsetConstruction
from Parser import Parser, Lexer
from ThompsonVisitor import ThompsonVisitor

def isMatch(string, regex) -> bool:
    lexer = Lexer(regex)
    parser = Parser(lexer)
    tree = parser.parseExpression(0)
    visitor = ThompsonVisitor()

    nfa = tree.accept(visitor)
    print(nfa.transitionTable)
    dfa = subsetConstruction(nfa, lexer.alphabet)
    print(dfa.transitionFunction)
    return dfa.accept(string)
