from Visitor import Visitor
from NFA import EPS, NFA
from SyntaxNode import *

class ThompsonVisitor(Visitor):
    """Performs Thompson's Construction on the Parse Tree"""
    
    def __init__(self) -> None:
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
        elif (node.operator == UnaryOperator.QUESTION):
            return self.question(node.operand.accept(self))
        else:
            return self.kleenePlus(node.operand.accept(self))
    
    def union(self, left, right) -> NFA:
        startState, acceptState = self.stateNum, self.stateNum + 1
        self.stateNum += 2
        states = [*left.states, *right.states, startState, acceptState]
        unionNFA = NFA(states, startState, acceptState)

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
        states = [*left.states, *[state for state in right.states if state != right.startState]]
        merged = NFA(states, left.startState, right.acceptState)

        print(right.acceptState)
        for d in (left.transitionTable, right.transitionTable):
            for key, value in d.items():
                for state in value:
                    if (state == right.startState):
                        merged.addTransition(key[0], key[1], left.acceptState)
                    elif (key[0] == right.startState):
                        merged.addTransition(left.acceptState, key[1], state)
                    else:
                        merged.addTransition(key[0], key[1], state)

        return merged

    def kleeneStarClosure(self, nfa: NFA) -> NFA:
        closureStartState, closureAcceptState = self.stateNum, self.stateNum + 1
        self.stateNum += 2
        states = [*nfa.states, closureStartState, closureAcceptState]
        closureNFA = NFA(states, closureStartState, closureAcceptState)

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
        baseNFA = NFA([startState, acceptState], startState, acceptState,)
        baseNFA.addTransition(startState, node.char, acceptState)
        return baseNFA

    def empty(self) -> NFA:
        startState, acceptState = self.stateNum, self.stateNum + 1
        self.stateNum += 2
        baseNFA = NFA([startState, acceptState], startState, acceptState,)
        baseNFA.addTransition(startState, EPS, acceptState)
        return baseNFA
    
    def question(self, node) -> NFA:
        return self.union(self.empty(), node)