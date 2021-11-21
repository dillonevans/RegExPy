from Lexer import Lexer
from SyntaxNode import BinaryOperator, BinaryOperatorNode, CharacterNode, SyntaxNode, UnaryOperator, UnaryOperatorNode
from Token import Token, TokenType

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.tokens = list()
        self.position = 0
        while (lexer.hasReachedEOF() == False):
            self.tokens.append(lexer.lex())

    def peek(self, offset) -> Token:
        index = self.position + offset
        return self.tokens[index]

    def getCurrentToken(self) -> Token:
        return self.peek(0)

    def getNextToken(self) -> Token:
        current = self.getCurrentToken()
        self.position += 1
        return current

    @staticmethod
    def getBinaryOperatorPrecedence(syntax: TokenType) -> int:
        if (syntax == TokenType.CONCATENATION_TOKEN):
            return 2 
        elif (syntax == TokenType.UNION_TOKEN):
            return 1
        else:
            return 0

    def isBinaryOperator(syntaxType: TokenType) -> bool:
        return syntaxType in [TokenType.CONCATENATION_TOKEN, TokenType.UNION_TOKEN]
   
    def getBinaryOperatorFromToken(syntax: TokenType) -> BinaryOperator:
        if (syntax == TokenType.CONCATENATION_TOKEN):
            return BinaryOperator.CONCATENATION
        else:
            return BinaryOperator.UNION

    def parsePrimary(self) -> SyntaxNode:
        currentToken = self.getCurrentToken()
        syntaxType = currentToken.type

        if (syntaxType == TokenType.CHARACTER):
            self.match(TokenType.CHARACTER)
            return CharacterNode(currentToken.text)

        elif (syntaxType == TokenType.LEFT_PARENTHESIS_TOKEN):
            self.match(TokenType.LEFT_PARENTHESIS_TOKEN)
            tree = self.parseExpression(0)
            self.match(TokenType.RIGHT_PARENTHESIS_TOKEN)
            return tree

    def parsePostfix(self) -> SyntaxNode:
            node = self.parsePrimary()
            tokenType = self.getCurrentToken().type 
            while(tokenType in [TokenType.KLEENE_CLOSURE_TOKEN, TokenType.KLEENE_PLUS_TOKEN, TokenType.QUESTION_TOKEN]):
                if (tokenType == TokenType.KLEENE_CLOSURE_TOKEN):
                    node = UnaryOperatorNode(UnaryOperator.KLEENE_STAR, node)
                elif (tokenType == TokenType.QUESTION_TOKEN):
                    node = UnaryOperatorNode(UnaryOperator.QUESTION, node)
                else:
                    node = UnaryOperatorNode(UnaryOperator.KLEENE_PLUS, node)
                self.match(tokenType)
                tokenType = self.getCurrentToken().type 
            return node

    def parseExpression(self, minPrecedence: int) -> SyntaxNode:
        left = self.parsePostfix()
        lookAhead = self.getCurrentToken().type
        while (Parser.isBinaryOperator(lookAhead) and Parser.getBinaryOperatorPrecedence(lookAhead) > minPrecedence):
            self.getNextToken()
            right = self.parseExpression(Parser.getBinaryOperatorPrecedence(lookAhead))
            left = BinaryOperatorNode(left, Parser.getBinaryOperatorFromToken(lookAhead), right)
            lookAhead = self.getCurrentToken().type

            if (lookAhead == TokenType.RIGHT_PARENTHESIS_TOKEN):
                return left
                
        return left

    def match(self, expected) -> Token:
        current = self.getCurrentToken()
        if (current.type == expected):
            return self.getNextToken()
        else:
            raise SyntaxError()