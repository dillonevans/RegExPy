from copy import deepcopy 

EPS = "epsilon"

class State:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return hex(id(self))

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

    def addTransition(self, fromState, input, toState: State) ->None:
        self.transitionTable[(fromState, input)].append(toState)
    

def concatenate(left: NFA, right: NFA) -> NFA:
    merged = NFA(left.alphabet, left.states + right.states, left.startState, right.acceptState)

    for d in (left.transitionTable, right.transitionTable):
        for key, value in d.items():
            for state in value:
                merged.addTransition(key[0], key[1], state)

    merged.addTransition(left.acceptState, EPS, right.startState)
    return merged

def union(left: NFA, right: NFA) -> NFA:

    startState, acceptState = State(), State()
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
    
def kleeneStarClosure(nfa: NFA):
    closureStartState, closureAcceptState = State(), State()
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

def kleenePlusClosure(nfa: NFA):
    return concatenate(nfa, kleeneStarClosure(deepcopy(nfa)))
    


