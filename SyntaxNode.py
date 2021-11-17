from abc import ABC, abstractclassmethod
from enum import Enum
from NFA import EPS, NFA, State, concatenate

class SyntaxNode(ABC):
    abstractclassmethod
    def evaluate(self) -> NFA:
        pass
    def __str__(self) -> str:
        pass

class BinaryOperator(Enum):
    UNION = '|'
    CONCATENATION= '?'

class UnaryOperator(Enum):
    KLEENE_STAR = '*'

class BinaryOperatorNode(SyntaxNode):
    def __init__(self, left: SyntaxNode, operator: BinaryOperator, right: SyntaxNode) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f"{self.left}{self.right}{self.operator.value}"
        
class CharacterNode(SyntaxNode):
    def __init__(self, char: chr) -> None:
        self.char = char

    def __str__(self) -> str:
        return f"{self.char}"


class UnaryOperatorNode(SyntaxNode):
    def __init__(self, operator: UnaryOperator, operand: SyntaxNode) -> None:
        self.operator = operator
        self.operand = operand

    def __str__(self) -> str:
        return f"{self.operand}{self.operator.value}"


