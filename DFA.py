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
  
        for (state, input), transitionState in self.transitionFunction.items():
            f.write(f"\t{state} -> {transitionState}[label = \"{input}\"]\n")

        f.write("}")
        f.close()

    def minimize(self):
        index = 0
        transitionTablePrime, nameMap = {}, {}
        statesPrime, acceptStatesPrime = [], []
        equivalenceClass = self.generateEquivalenceClasses()

        # Assign a unique identifier to each equivalence class
        for (state,_) in self.transitionFunction:
            statePrime = equivalenceClass[state]
            if (statePrime not in nameMap):
                nameMap[statePrime] = f"q_{index}"
                statesPrime.append(nameMap[statePrime])
                index += 1

        acceptStatesPrime = []
        transitionTablePrime = {}

        # Construct the new transition table using the equivalence classes
        # of the original states as well as the new set of 
        # accept states 
        for (p,input), q in self.transitionFunction.items():
            pPrime = equivalenceClass[p]
            qPrime = equivalenceClass[q]
            if (set(self.acceptStates).intersection(pPrime)):
                if (nameMap[pPrime] not in acceptStatesPrime):
                    acceptStatesPrime.append(nameMap[pPrime])
            transitionTablePrime[nameMap[pPrime],input] = nameMap[qPrime]

        # Set M to M'
        self.acceptStates = acceptStatesPrime
        self.states = statesPrime
        self.transitionFunction = transitionTablePrime
        self.startState = nameMap[equivalenceClass[self.startState]]

    def generateEquivalenceClasses(self):
        distinguishable = {}

        # Find distinguishable pairs
        for (p, _) in self.transitionFunction:
            for (q, _) in self.transitionFunction:
                isDistinguishable = (p in self.acceptStates and q not in self.acceptStates) or (p not in self.acceptStates and q in self.acceptStates)
                distinguishable[p,q] = isDistinguishable

        # Keep marking until there are no more distinguishable states
        foundDistinguishablePair = True
        while (foundDistinguishablePair):
            foundDistinguishablePair = False
            for (p,q) in distinguishable:
                for input in self.alphabet:
                    moveP = self.transitionFunction[p,input]
                    moveQ = self.transitionFunction[q,input]
                    if (not distinguishable[p,q] and distinguishable[moveP, moveQ]):
                        distinguishable[p,q] = True
                        foundDistinguishablePair = True

        equivalenceClass = {}

        # Generate the equivalence classes based on whether or not the pair of
        # states are distinguishable. This is an application 
        # of the Myhill-Nerode Theorem
        for (p,q), distinguishable in distinguishable.items():
            if (not distinguishable):
                if (p not in equivalenceClass):
                    equivalenceClass[p] = frozenset(q)
                else:
                    equivalenceClass[p] = equivalenceClass[p].union(frozenset(q))
        return equivalenceClass