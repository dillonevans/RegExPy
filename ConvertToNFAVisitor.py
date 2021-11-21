from Visitor import Visitor
from NFA import EPS, NFA
from SyntaxNode import *

class ConvertToNFAVisitor(Visitor):

    def __init__(self, alphabet) -> None:
        self.alphabet = alphabet
        self.stateNum = 0

    def visitCharacterNode(self, node) -> NFA:
        return self.basicSymbol(node)

    def visitBinaryOperatorNode(self, node) -> NFA:
        left = node.left.accept(self)
        right = node.right.accept(self)

        if (node.operator == BinaryOperator.CONCATENATION):
            return self.concatenate(left, right)
        elif (node.operator == BinaryOperator.UNION):
            return self.union(left, right)

    def visitUnaryOperatorNode(self, node) -> NFA:
        if (node.operator == UnaryOperator.KLEENE_STAR):
            return self.kleeneStarClosure(node.operand.accept(self))
        else:
            return self.kleenePlus(node.operand.accept(self))


    def union(self, left, right) -> NFA:
        startState, acceptState = self.stateNum, self.stateNum + 1
        self.stateNum += 2
        states = left.states + right.states + [startState, acceptState]
        unionNFA = NFA(left.alphabet, states, startState, acceptState)

        for d in (left.transitionTable, right.transitionTable):
            for key, value in d.items():
                for state in value:
                    unionNFA.addTransition(key[0], key[1], state)

        unionNFA.addTransition(startState, EPS, left.startState)
        unionNFA.addTransition(startState, EPS, right.startState)
        unionNFA.addTransition(left.acceptState, EPS, acceptState)
        unionNFA.addTransition(right.acceptState, EPS, acceptState)
        return unionNFA

    def concatenate(self, left: NFA, right: NFA) -> NFA:
        merged = NFA(left.alphabet, left.states + right.states, left.startState, right.acceptState)

        for d in (left.transitionTable, right.transitionTable):
            for key, value in d.items():
                for state in value:
                    merged.addTransition(key[0], key[1], state)

        merged.addTransition(left.acceptState, EPS, right.startState)
        return merged

    def kleeneStarClosure(self, nfa: NFA) -> NFA:
        closureStartState, closureAcceptState = self.stateNum, self.stateNum + 1
        self.stateNum += 2
        states = [closureStartState, closureAcceptState]
        closureNFA = NFA(nfa.alphabet, states + nfa.states, closureStartState, closureAcceptState)

        for key, value in nfa.transitionTable.items():
            for state in value:
                closureNFA.addTransition(key[0], key[1], state)

        closureNFA.addTransition(closureStartState, EPS, nfa.startState)
        closureNFA.addTransition(closureStartState, EPS, closureAcceptState)
        closureNFA.addTransition(nfa.acceptState, EPS, nfa.startState)
        closureNFA.addTransition(nfa.acceptState, EPS,closureAcceptState)
        return closureNFA

    def kleenePlus(self, nfa: NFA):
        return self.concatenate(nfa, self.kleeneStarClosure(nfa))

    def basicSymbol(self, node) -> NFA:
        startState, acceptState = self.stateNum, self.stateNum + 1
        self.stateNum += 2
        baseNFA = NFA(self.alphabet, [startState, acceptState], startState, acceptState,)
        baseNFA.addTransition(startState, node.char, acceptState)
        return baseNFA