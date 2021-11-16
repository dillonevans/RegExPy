
EPS = "epsilon"

class DFA: 
    def __init__(self) -> None:
        self.isAcceptState = False 
        self.set = set() 

    def addTransition(self, input: chr, state) -> None:
        self.set.add((input, state))

def union(left, right):
    unionDfa = DFA()
    unionDfa.addTransition(EPS, left)
    unionDfa.addTransition(EPS, right)
    return unionDfa