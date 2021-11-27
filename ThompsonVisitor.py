import enum
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

    def visitRepetitionQuantifierNode(self, node: RepetitionQuantifierNode) -> NFA:
        if (node.operator == UnaryOperator.BOUNDED_MIN_BOUNDED_MAX_REPETITION):
            return self.repetition(node)
        else:            
            nfa = node.operand.accept(self)
            for _ in range (node.min - 1):
                nfa = self.concatenate(nfa, node.operand.accept(self))
            return self.concatenate(nfa, self.kleeneStarClosure(node.operand.accept(self)))

    def repetition(self, node) -> NFA:
        nfaList = []

        for i in range(0, node.max - node.min + 1):
            nfa = node.operand.accept(self)
            for _ in range(0, node.min + i - 1):
                nfa = self.concatenate(nfa, node.operand.accept(self))
            nfaList.append(nfa)

        startState, acceptState = self.stateNum, self.stateNum + 1
        self.stateNum += 2

        states = [*[state for nfa in nfaList for state in nfa.states], startState, acceptState]
        unionNFA = NFA(states, startState, acceptState)

        for nfa in (nfaList):
            for (state, input), stateSet in nfa.transitionTable.items():
                unionNFA.transitionTable[state, input] = stateSet

            unionNFA.addTransition(startState, EPS, nfa.startState)
            unionNFA.addTransition(nfa.acceptState, EPS, acceptState)

        return unionNFA
    
    def union(self, left, right) -> NFA:
        startState, acceptState = self.stateNum, self.stateNum + 1
        self.stateNum += 2
        states = [*left.states, *right.states, startState, acceptState]
        unionNFA = NFA(states, startState, acceptState)

        for d in (left.transitionTable, right.transitionTable):
            for (state, input), stateSet in d.items():
                unionNFA.transitionTable[state, input] = stateSet

        unionNFA.addTransition(startState, EPS, left.startState)
        unionNFA.addTransition(startState, EPS, right.startState)
        unionNFA.addTransition(left.acceptState, EPS, acceptState)
        unionNFA.addTransition(right.acceptState, EPS, acceptState)
        return unionNFA

    def concatenate(self, left: NFA, right: NFA) -> NFA:

        concatenatedStates = [state for state in right.states if state != right.startState]
        states = [*left.states, *concatenatedStates]
        merged = NFA(states, left.startState, right.acceptState)

        # Merge the left and right transition functions
        for transitionTable in (left.transitionTable, right.transitionTable):
            for (currentState, input), value in transitionTable.items():
                for nextState in value:
                    # Replace transitions to the right NFA's start start
                    # with a transition to the accept state of the
                    # left NFA
                    if (nextState == right.startState):
                        merged.addTransition(currentState, input, left.acceptState)

                    # Consume the transitions from the start state of the right NFA
                    elif (currentState == right.startState):
                        merged.addTransition(left.acceptState,input, nextState)

                    # Add transitions as normal
                    else:
                        merged.addTransition(currentState, input, nextState)
        return merged

    def kleeneStarClosure(self, nfa: NFA) -> NFA:
        closureStartState, closureAcceptState = self.stateNum, self.stateNum + 1
        self.stateNum += 2
        states = [*nfa.states, closureStartState, closureAcceptState]
        closureNFA = NFA(states, closureStartState, closureAcceptState)

        for key, value in nfa.transitionTable.items():
            closureNFA.transitionTable[key] = value

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