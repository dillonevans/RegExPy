from Parser import Parser, Lexer
from ConvertToNFAVisitor import ConvertToNFAVisitor

lexer = Lexer("abc|def")
parser = Parser(lexer)

tree = parser.parseExpression(0)
print(tree)
visitor = ConvertToNFAVisitor(lexer.alphabet)

nfa = tree.accept(visitor)
for key, value in nfa.transitionTable.items():
    if value:
        print(f"({key[0]}, {key[1]}) = {value}")

print (nfa.acceptState)