from os import name


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
        """Minimizes the DFA"""
        
        transitionTablePrime, nameMap = {}, {}
        statesPrime, acceptStatesPrime = [], []
        
        # Generate the equivalence class [p] for all p ∈ Q.
        # The code in this section is based on the algorithm 
        # described here: http://www.cs.cornell.edu/courses/cs2800/2013fa/Handouts/minimization.pdf
        equivalenceClass = self.generateEquivalenceClasses()

        # Generate a unique identifier for each equivalence class. 
        # This step is not necessary, but allows for easy to 
        # read state names in the minmized DFA
        nameMap = {equivalenceClass[state]: f"q_{i}" for (i, state) in enumerate(self.states)}

        # Generate the new set of states and accept states, as well as the
        # new transition function
        for state in self.states:

            # We define the new states set of states
            # Q' as {[p] | p ∈ Q }.
            statePrime = nameMap[equivalenceClass[state]]
            statesPrime.append(statePrime)
            
            # We define the new set of accept states 
            # F' as {[p] | p ∈ F }.
            if (state in self.acceptStates):
                acceptStatesPrime.append(statePrime)

            # We define the new transition function 
            # δ' as δ'([p], a) = [δ(p, a)]
            for a in self.alphabet:
                transitionTablePrime[statePrime, a] = nameMap[equivalenceClass[self.transitionFunction[state, a]]]

        # Set M to M'
        self.acceptStates = acceptStatesPrime
        self.states = statesPrime
        self.transitionFunction = transitionTablePrime
        self.startState = nameMap[equivalenceClass[self.startState]]

    def generateEquivalenceClasses(self):
        distinguishable = {}

        # Find distinguishable pairs
        for p in self.states:
            for q in self.states:

                # If p and q are the same state, then they are obviously not distinguishable
                if (p == q):
                    distinguishable[p,q] = False
                
                else:
                    # If p is an accept state and q is not, or vice versa, we can 
                    # automatically classify them as being distinguishable
                    # since only one is an accept state
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