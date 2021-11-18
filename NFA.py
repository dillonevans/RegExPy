EPS = "epsilon"

class NFA:
    def __init__(self, alphabet, states, startState, acceptState) -> None:
        self.startState = startState
        self.acceptState = acceptState
        self.transitionTable = {}
        self.states = states
        self.alphabet = alphabet

        # The transition function of an NFA is Q x Σ --> P(Q)
        for state in states:
            for symbol in alphabet:
                self.transitionTable[(state, symbol)] = []

    def addTransition(self, fromState, input, toState) ->None:
        self.transitionTable[(fromState, input)].append(toState)
    



