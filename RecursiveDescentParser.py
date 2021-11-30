from Lexer import Lexer
from SyntaxNode import BinaryOperator, BinaryOperatorNode, CharacterClassNode, CharacterNode, RangeNode, RepetitionQuantifierNode, UnaryOperator, UnaryOperatorNode
from Token import Token, TokenType

class RecursiveDescentParser:
    def __init__(self, lexer: Lexer) -> None:
        self.tokens = []
        self.position = 0
        while (not lexer.hasReachedEOF()):
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

    def match(self, expected) -> Token:
        current = self.getCurrentToken()
        if (current.type == expected):
            return self.getNextToken()
        else:
            raise SyntaxError()

    def parsePostfix(self, tree):
        lookAhead = self.getCurrentToken().type
        min, max = 0, 0
        if (lookAhead == TokenType.KLEENE_CLOSURE_TOKEN):
            self.match(lookAhead)
            return UnaryOperatorNode(UnaryOperator.KLEENE_STAR, tree)
        elif (lookAhead == TokenType.KLEENE_PLUS_TOKEN):
            self.match(lookAhead)
            return UnaryOperatorNode(UnaryOperator.KLEENE_PLUS, tree)
        elif (lookAhead == TokenType.QUESTION_TOKEN):
            self.match(lookAhead)
            return UnaryOperatorNode(UnaryOperator.QUESTION, tree)
        elif (lookAhead == TokenType.LEFT_BRACE_TOKEN):
            self.match(TokenType.LEFT_BRACE_TOKEN)
            if (self.getCurrentToken().type == TokenType.NUMERIC_TOKEN):
                min = int(self.match(TokenType.NUMERIC_TOKEN).text)
                if (self.getCurrentToken().type != TokenType.COMMA_TOKEN):
                    self.match(TokenType.RIGHT_BRACE_TOKEN)
                    return RepetitionQuantifierNode(min, min, tree)
            
            self.match(TokenType.COMMA_TOKEN)

            if (self.getCurrentToken().type == TokenType.NUMERIC_TOKEN):
                max = int(self.match(TokenType.NUMERIC_TOKEN).text)
            else:
                max = None
            self.match(TokenType.RIGHT_BRACE_TOKEN)
            return RepetitionQuantifierNode(min,max, tree)

    def parseAtom(self):
        lookAhead = self.getCurrentToken().type

        if (lookAhead == TokenType.LEFT_PARENTHESIS_TOKEN):
            self.match(lookAhead)
            tree = self.parseExpression()
            self.match(TokenType.RIGHT_PARENTHESIS_TOKEN)
            return tree
        elif (lookAhead == TokenType.LEFT_BRACKET_TOKEN):
            self.match(lookAhead)
            tree = self.parseCharacterClass()
            self.match(TokenType.RIGHT_BRACKET_TOKEN)
            return tree
        char = self.match(TokenType.CHARACTER_TOKEN).text
        return CharacterNode(char)

    def parseFactor(self):
        atom = self.parseAtom()
        lookAhead = self.getCurrentToken().type

        if (lookAhead == TokenType.KLEENE_CLOSURE_TOKEN or
            lookAhead == TokenType.KLEENE_PLUS_TOKEN or
            lookAhead == TokenType.QUESTION_TOKEN or
            lookAhead == TokenType.LEFT_BRACE_TOKEN):
            return self.parsePostfix(atom)
        return atom

    def parseCharacterRange(self):
        beginChar = self.match(TokenType.CHARACTER_TOKEN).text
        lookAhead = self.getCurrentToken().type
        if (lookAhead == TokenType.RANGE_TOKEN):
            self.match(lookAhead)
            endChar = self.match(TokenType.CHARACTER_TOKEN).text
            return RangeNode(beginChar, endChar)
        return CharacterNode(beginChar)
        
    def parseCharacterClass(self):
        characters = []
        while (self.getCurrentToken().type is not TokenType.RIGHT_BRACKET_TOKEN):
            range = self.parseCharacterRange()
            characters.append(range)
        return CharacterClassNode(characters)

    def parseTerm(self):
        factor = self.parseFactor()
        lookAhead = self.getCurrentToken().type
        
        if (lookAhead == TokenType.CHARACTER_TOKEN or 
            lookAhead == TokenType.LEFT_PARENTHESIS_TOKEN or
            lookAhead == TokenType.LEFT_BRACKET_TOKEN):
            return BinaryOperatorNode(factor, BinaryOperator.CONCATENATION, self.parseTerm())
        elif (lookAhead == TokenType.EOF_TOKEN):
            return factor
        else:
            raise SyntaxError("Expected Term.")

    def parseExpression(self):
        term = self.parseTerm()
        lookAhead = self.getCurrentToken().text
        if (lookAhead == TokenType.UNION_TOKEN):
            self.match(lookAhead)
            return BinaryOperatorNode(term, BinaryOperator.UNION, self.parseExpression())
        return term