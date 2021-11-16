from Lexer import Lexer
from SyntaxNode import BinaryOperator, BinaryOperatorNode, CharacterNode, UnaryOperator, UnaryOperatorNode
from Token import Token, TokenType

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.tokens = list()
        self.position = 0
        while (lexer.hasReachedEOF() == False):
            self.tokens.append(lexer.lex())

    def peek(self, offset):
        index = self.position + offset
        return self.tokens[index]

    def getCurrentToken(self) -> Token:
        return self.peek(0)

    def getNextToken(self):
        current = self.getCurrentToken()
        self.position += 1
        return current

    @staticmethod
    def getBinaryOperatorPrecedence(syntax: TokenType) -> int:
        if (syntax == TokenType.CONCATENATION_TOKEN):
            return 2 
        if (syntax == TokenType.UNION_TOKEN):
            return 1
        return 0

    def isBinaryOperator(syntaxType: TokenType) -> bool:
        return syntaxType == TokenType.CONCATENATION_TOKEN or syntaxType == TokenType.UNION_TOKEN
   
    def getBinaryOperatorFromToken(syntax: TokenType) -> BinaryOperator:
        if (syntax == TokenType.CONCATENATION_TOKEN):
            return BinaryOperator.CONCATENATION
        else:
            return BinaryOperator.UNION

    def parsePrimary(self):
        currentToken = self.getCurrentToken()
        syntaxType = currentToken.type
        if (syntaxType == TokenType.CHARACTER):
            self.match(TokenType.CHARACTER)
            return CharacterNode(currentToken.text)

    def parsePostfix(self):
            node = self.parsePrimary()
            while(self.getCurrentToken().type == TokenType.KLEENE_CLOSURE_TOKEN):
                node = UnaryOperatorNode(UnaryOperator.KLEENE_STAR, node)
                self.match(TokenType.KLEENE_CLOSURE_TOKEN)
            return node

    def parseExpression(self, minPrecedence: int):
        left = self.parsePostfix()
        lookAhead = self.getCurrentToken().type
        while (Parser.isBinaryOperator(lookAhead) and Parser.getBinaryOperatorPrecedence(lookAhead) > minPrecedence):
            self.getNextToken()
            right = self.parseExpression(Parser.getBinaryOperatorPrecedence(lookAhead))
            left = BinaryOperatorNode(left, Parser.getBinaryOperatorFromToken(lookAhead), right)
            lookAhead = self.getCurrentToken().type

        return left


    def match(self, expected):
    
        current = self.getCurrentToken()
        if (current.type == expected):
            return self.getNextToken()
        else:
            raise SyntaxError()