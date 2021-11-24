from NFAToDFA import subsetConstruction
from Parser import Parser, Lexer
from ThompsonVisitor import ThompsonVisitor

class RegexCompiler:
    def __init__(self, regex) -> None:
        self.lexer = Lexer(regex)
        self.parser = Parser(self.lexer)
        self.tree = self.parser.parseExpression(0)
        self.visitor = ThompsonVisitor()
        self.nfa = self.tree.accept(self.visitor)
        self.dfa = subsetConstruction(self.nfa, self.lexer.alphabet)
        self.dfa.minimize()
        
    def isMatch(self, string) -> bool:
        return self.dfa.accept(string)
