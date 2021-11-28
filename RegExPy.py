from NFAToDFA import subsetConstruction
from RecursiveDescentParser import RecursiveDescentParser, Lexer
from ThompsonVisitor import ThompsonVisitor

class RegexCompiler:
    def __init__(self, regex) -> None:
        self.lexer = Lexer(regex)
        self.parser = RecursiveDescentParser(self.lexer)
        self.tree = self.parser.parseExpression()
        self.visitor = ThompsonVisitor()
        self.nfa = self.tree.accept(self.visitor)
        self.dfa = subsetConstruction(self.nfa, self.lexer.alphabet)
        self.dfa.minimize()
        self.dfa.printToFile()
        self.nfa.printNFA()

    def isMatch(self, string) -> bool:
        return self.dfa.accept(string)

    def matches(self, string):
        matchSet = set()

        for i,_ in enumerate(string):
            for j, _ in enumerate(string):
                if (self.isMatch(string[i:j+1])):
                    matchSet.add(string[i:j+1])
        return matchSet

