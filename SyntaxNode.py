from abc import ABC, abstractclassmethod
from enum import Enum
from Token import TokenType

from Visitor import Visitor

class SyntaxNode(ABC):
    abstractclassmethod
    def accept(self, visitor):
        pass
    def __str__(self) -> str:
        pass

class BinaryOperator(Enum):
    UNION = '|'
    CONCATENATION= '\u2022'

class UnaryOperator(Enum):
    KLEENE_STAR = '*',
    KLEENE_PLUS = '+',
    QUESTION = '?',
    UNBOUNDED_MAX_REPETITION = '{,n}'
    BOUNDED_MIN_BOUNDED_MAX_REPETITION = '{m,n?}'

class BinaryOperatorNode(SyntaxNode):
    def __init__(self, left: SyntaxNode, operator: BinaryOperator, right: SyntaxNode) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f"{self.left}{self.right}{self.operator.value}"

    def accept(self, visitor: Visitor):
        return visitor.visitBinaryOperatorNode(self)
        
class CharacterNode(SyntaxNode):
    def __init__(self, char: chr) -> None:
        self.char = char

    def __str__(self) -> str:
        return f"{self.char}"

    def accept(self, visitor: Visitor):
        return visitor.visitCharacterNode(self)     

class UnaryOperatorNode(SyntaxNode):
    def __init__(self, operator: UnaryOperator, operand: SyntaxNode) -> None:
        self.operator = operator
        self.operand = operand

    def __str__(self) -> str:
        return f"{self.operand}{self.operator.value}"

    def accept(self, visitor: Visitor):
        return visitor.visitUnaryOperatorNode(self)

class RepetitionQuantifierNode(UnaryOperatorNode):
    def __init__(self, min, max, operand: SyntaxNode) -> None:
        self.min = min
        self.max = max
        type = None
        if (not max):
            type = UnaryOperator.UNBOUNDED_MAX_REPETITION
        else:
            type = UnaryOperator.BOUNDED_MIN_BOUNDED_MAX_REPETITION
                
        super().__init__(type, operand)

    def __str__(self) -> str:
        return f"{self.operand}{self.operator.value}"

    def accept(self, visitor: Visitor):
        return visitor.visitRepetitionQuantifierNode(self)

class CharacterClassNode(SyntaxNode):
    def __init__(self, characters) -> None:
        self.characters = characters
    
    def __str__(self) -> str:
       return f"{self.operand}{self.operator.value}" 

    def accept(self, visitor: Visitor):
        return visitor.visitCharacterClassNode(self)

class RangeNode(SyntaxNode):
    def __init__(self, min, max) -> None:
        self.min = min
        self.max = max
        self.nodes = []
        for i in range(ord(max) - ord(min) + 1):
            self.nodes.append(CharacterNode(chr(ord(min) + i)))
        

    def __str__(self) -> str:
       return f"{self.nodes}"

    def accept(self, visitor: Visitor):
        return visitor.visitRangeNode(self)