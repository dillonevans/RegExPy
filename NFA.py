
EPS = "epsilon"

class NFA: 
    def __init__(self, isAcceptState) -> None:
        self.isAcceptState = isAcceptState 
        self.set = set() 
        self.acceptState = None

    def addTransition(self, input: chr, state) -> None:
        self.set.add((input, state))

    def addEpislonTranstion(self,state) -> None:
        self.addTransition(EPS, state)        

def union(left, right):
    unionDfa = NFA(False)
    unionDfa.addEpislonTranstion(left)
    unionDfa.addEpislonTranstion(right)
    return unionDfa