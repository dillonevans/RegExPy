from copy import deepcopy 

EPS = "epsilon"

class State:
    def __init__(self, isAcceptState) -> None:
        self.isAcceptState = isAcceptState

    def __str__(self) -> str:
        return hex(id(self))

class NFA:
    def __init__(self, alphabet) -> None:
        self.startState = None
        self.acceptState = None
        self.transitionFunction = {}
        self.states = []
        self.alphabet = alphabet

    def addTransition(self, fromState, input, toState: State) ->None:

        if not self.transitionFunction: 
            self.startState = fromState

        if fromState not in self.states:
            self.states.append(fromState)

            for symbol in self.alphabet:
                self.transitionFunction[(fromState, symbol)] = []

        if toState not in self.states:
            self.states.append(toState)
            
            for symbol in self.alphabet:
                self.transitionFunction[(toState, symbol)] = []

        self.transitionFunction[(fromState, input)].append(toState)

        if (toState.isAcceptState): 
            self.acceptState = toState


def concatenate(left: NFA, right: NFA) -> NFA:
    merged = NFA(left.alphabet)
    leftAcceptState = left.acceptState
    rightStartState = right.startState
    leftAcceptState.isAcceptState = False

    merged.startState = left.startState
    merged.acceptState = right.acceptState

    merged.transitionFunction =  {**left.transitionFunction, **right.transitionFunction}
    merged.states = left.states + right.states
    merged.addTransition(leftAcceptState, EPS, rightStartState)
    return merged

def union(left: NFA, right: NFA) -> NFA:
    unionNFA = NFA(left.alphabet)
    startState, acceptState = State(False), State(True)

    leftStartState, rightStartState = left.startState, right.startState
    leftAcceptState, rightAcceptState = left.acceptState, right.acceptState

    leftAcceptState.isAcceptState = False
    rightAcceptState.isAcceptState = False

    unionNFA.transitionFunction = {**left.transitionFunction, **right.transitionFunction}
    unionNFA.states = left.states + right.states

    unionNFA.startState = startState
    unionNFA.acceptState = acceptState

    unionNFA.addTransition(startState, EPS, leftStartState)
    unionNFA.addTransition(startState, EPS, rightStartState)
    unionNFA.addTransition(leftAcceptState, EPS, acceptState)
    unionNFA.addTransition(rightAcceptState, EPS, acceptState)

    return unionNFA
    
def kleeneStarClosure(nfa: NFA):
    closureNFA = NFA(nfa.alphabet)
    
    closureStartState = State(False)
    closureAcceptState = State(True)
    closureNFA.startState = closureStartState
    closureNFA.acceptState = closureAcceptState
    closureNFA.states = nfa.states

    closureNFA.transitionFunction = {**nfa.transitionFunction}
    originalStartState, originalAcceptState = nfa.startState, nfa.acceptState

    closureNFA.addTransition(closureStartState, EPS, originalStartState)
    closureNFA.addTransition(closureStartState, EPS, closureAcceptState)
    closureNFA.addTransition(originalAcceptState, EPS, originalStartState)
    closureNFA.addTransition(originalAcceptState, EPS,closureAcceptState)
    return closureNFA

def kleenePlusClosure(nfa: NFA):

    return concatenate(nfa, kleeneStarClosure(deepcopy(nfa)))
    


