from abc import ABC, abstractclassmethod
from enum import Enum
from NFA import NFA

class SyntaxNode(ABC):
    abstractclassmethod
    def evaluate(self) -> NFA:
        pass
    def printTree(self) -> None:
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

    def printTree(self) -> None:
        self.left.printTree()
        self.right.printTree()
        print(self.operator.value, end = '')
        
class CharacterNode(SyntaxNode):
    def __init__(self, char: chr) -> None:
        self.char = char

    def printTree(self) -> None:
        print(self.char, end = '')

class UnaryOperatorNode(SyntaxNode):
    def __init__(self, operator: UnaryOperator, operand: SyntaxNode) -> None:
        self.operator = operator
        self.operand = operand

    def printTree(self) -> None:
        self.operand.printTree()
        print(self.operator.value, end = '')

