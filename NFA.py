EPS = "epsilon"

class NFA:
    def __init__(self, states, startState, acceptState) -> None:
        self.startState = startState
        self.acceptState = acceptState
        self.transitionTable = {}
        self.states = states

    def addTransition(self, fromState, input, toState) -> None:
        stateSet = frozenset([toState])
        if ((fromState, input) not in self.transitionTable):
            self.transitionTable[fromState, input] = stateSet
        else:
            self.transitionTable[fromState, input] = self.transitionTable[fromState, input].union(stateSet)
    



