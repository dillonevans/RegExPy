class DFA:
    def __init__(self, startState, states, acceptStates, transitionFunction, alphabet) -> None:
        self.startState = startState
        self.states = states
        self.acceptStates = acceptStates
        self.transitionFunction = transitionFunction
        self.alphabet = alphabet

    def accept(self, str) -> bool:
        currentState = self.startState
        for symbol in str:
            if (symbol not in self.alphabet):
                return False
            currentState = self.transitionFunction[currentState, symbol]
        
        return currentState in self.acceptStates