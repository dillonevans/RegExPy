from abc import ABC, abstractclassmethod
from enum import Enum
from DFA import DFA

class SyntaxNode(ABC):
    abstractclassmethod
    def evaluate() -> DFA:
        pass

class BinaryOperator(Enum):
    UNION = '|',
    CONCATENATION= '?'

class UnaryOperator(Enum):
    KLEENE_STAR = '*'

class BinaryOperatorNode(SyntaxNode):
    def __init__(self, left: SyntaxNode, operator: BinaryOperator, right: SyntaxNode) -> None:
        self.left = left
        self.operator = operator
        self.right = right

class CharacterNode(SyntaxNode):
    def __init__(self, char: chr) -> None:
        self.char = char

class UnaryOperatorNode(SyntaxNode):
    def __init__(self, operator: UnaryOperator, operand: SyntaxNode) -> None:
        self.operator = operator
        self.operand = operand

def printTree(root):
    if (isinstance(root, BinaryOperatorNode)):
        printTree(root.left)
        printTree(root.right)
        print(root.operator.value, end='')
    
    elif (isinstance(root, UnaryOperatorNode)):
        printTree(root.operand)
        print(root.operator.value, end='')
    
    else:
        print(root.char, end='')

