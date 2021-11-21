from NFA import EPS, NFA
from DFA import DFA

def nullClosure(states: list, transitionTable):
    stack = []
    closure = set()

    for state in states:
        stack.append(state)
        closure.add(state)

    while stack:
        t = stack.pop()        

        for state in transitionTable[t, EPS]:
            u = state
            if (u not in closure):
                closure.add(u)
                stack.append(u)

    return closure

def move(stateSet, symbol, transitionTable):
    moveSet = set()
    for state in stateSet:
        for s in transitionTable[(state, symbol)]:
            moveSet.add(s)
    return moveSet    

def subsetConstruction(nfa: NFA, alphabet) -> DFA:
    dfaStartState = frozenset(nullClosure([nfa.startState], nfa.transitionTable))
    dfaStates = [dfaStartState]
    unmarkedStates = [dfaStartState]
    dfaTransitionTable = dict()
    dfaAcceptStates = list()
 
    while (unmarkedStates):
        stateSet = unmarkedStates.pop()

        for symbol in alphabet:
            newStateSet = (nullClosure(move(stateSet, symbol, nfa.transitionTable), nfa.transitionTable))
            if (newStateSet not in dfaStates):
                dfaStates.append(frozenset(newStateSet))
                unmarkedStates.append(newStateSet)
            dfaTransitionTable[frozenset(stateSet),symbol] = frozenset(newStateSet)

    for stateSet in dfaStates:
        if (nfa.acceptState in stateSet):
            dfaAcceptStates.append(stateSet)

    return DFA(dfaStartState, dfaStates, dfaAcceptStates, dfaTransitionTable, alphabet)
   