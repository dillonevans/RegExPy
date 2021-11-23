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

    def printToFile(self):
        f = open("DFA.dot", "w")
        f.write("digraph G {\n")
  
        for state in self.states:
            if (state not in self.acceptStates):
                f.write(f"\t{state}[label = \"{state}\" shape = circle]\n")
            else:
                f.write(f"\t{state}[label = \"{state}\" shape = doublecircle]\n")
  
        print(self.transitionFunction)
        for (state, input), transitionState in self.transitionFunction.items():
            f.write(f"\t{state} -> {transitionState}[label = \"{input}\"]\n")

        f.write("}")
        f.close()

