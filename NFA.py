EPS = '\u03b5'

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

    def printNFA(self):
        f = open("NFA.dot", "w",  encoding="utf-8")
        f.write("digraph G {\n")
  
        for state in self.states:
            if state is not self.acceptState:
                f.write(f"\t{state}[label = \"{state}\" shape = circle]\n")
            else:
                f.write(f"\t{state}[label = \"{state}\" shape = doublecircle]\n")
  
        for (state, input), stateList in self.transitionTable.items():
            for s in stateList:
                f.write(f"\t{state} -> {s}[label = \"{input}\"]\n")

        f.write("}")
        f.close()

    



