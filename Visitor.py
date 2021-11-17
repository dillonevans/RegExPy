from abc import ABC, abstractmethod

class Visitor(ABC):

    abstractmethod
    def visitSyntaxNode(self, node):
        pass

    abstractmethod
    def visitCharacterNode(self, node):
        pass

    abstractmethod
    def visitBinaryOperatorNode(self, node):
        pass
    
    abstractmethod
    def visitUnaryOperatorNode(self, node):
        pass
