from NFA import NFA, union
from SyntaxNode import *

def convertTreeToNFA(tree: SyntaxNode, alphabet) -> NFA:
    if (isinstance(tree, BinaryOperatorNode)):
        left = convertTreeToNFA(tree.left, alphabet)
        right = convertTreeToNFA(tree.right, alphabet)
        if (tree.operator == BinaryOperator.CONCATENATION):
            return concatenate(left, right)
        elif (tree.operator == BinaryOperator.UNION):
            return union(left, right)
            
    elif (isinstance(tree, CharacterNode)):
        baseNFA = NFA(alphabet)
        startState, acceptState = State(False), State(True)
        baseNFA.addTransition(startState, tree.char, acceptState)
        return baseNFA