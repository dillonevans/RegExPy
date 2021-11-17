from Visitor import Visitor
from NFA import State, NFA, concatenate, kleeneStarClosure, union
from SyntaxNode import *

class ConvertToNFAVisitor(Visitor):
    
    def __init__(self, alphabet) -> None:
        self.alphabet = alphabet

    def visitCharacterNode(self, node) -> NFA:
        startState, acceptState = State(), State()
        baseNFA = NFA(self.alphabet, [startState, acceptState], startState, acceptState,)
        baseNFA.addTransition(startState, node.char, acceptState)
        return baseNFA

    def visitBinaryOperatorNode(self, node) -> NFA:
        left = node.left.accept(self)
        right = node.right.accept(self)

        if (node.operator == BinaryOperator.CONCATENATION):
            return concatenate(left, right)
        elif (node.operator == BinaryOperator.UNION):
            return union(left, right)

    def visitUnaryOperatorNode(self, node) -> NFA:
        if (node.operator == UnaryOperator.KLEENE_STAR):
            return kleeneStarClosure(node.operand.accept(self))
