from NFA import EPS
from Token import Token, TokenType

CONCAT_OPERATOR = '\u2022'

class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.position = 0
        self.text = text
        self.alphabet = set()

    def getCurrentChar(self) -> chr:
        return self.peek(0)

    def peek(self, offset: int) -> chr:
        index = self.position + offset
        if index < len(self.text):
            return self.text[index]
        else: 
            return '\0'

    def lex(self) -> Token:
        self.skipWhiteSpace()
        start = self.position
        current = self.getCurrentChar()
        
        if current.isalpha():
            self.advance()
            self.alphabet.add(current)
            return Token(current, TokenType.CHARACTER_TOKEN)

        if (current.isdigit()):
            while (current.isdigit()):
                self.advance()
                current = self.getCurrentChar()
            lexeme = self.text[start:self.position]
            return Token(lexeme, TokenType.NUMERIC_TOKEN)
        else:
            self.advance()
            if current == '*':
                return Token(current, TokenType.KLEENE_CLOSURE_TOKEN)
            elif current == '+':
                return Token(current, TokenType.KLEENE_PLUS_TOKEN)
            elif current == CONCAT_OPERATOR:
                return Token(current, TokenType.CONCATENATION_TOKEN)
            elif current == '?':
                return Token(current, TokenType.QUESTION_TOKEN)
            elif current == '|':
                return Token(current, TokenType.UNION_TOKEN)
            elif current == '(':
                return Token(current, TokenType.LEFT_PARENTHESIS_TOKEN)
            elif current == ')':
                return Token(current, TokenType.RIGHT_PARENTHESIS_TOKEN)
            elif current == '{':
                return Token(current, TokenType.LEFT_BRACE_TOKEN)
            elif current == '}':
                return Token(current, TokenType.RIGHT_BRACE_TOKEN)
            elif current == ',':
                return Token(current, TokenType.COMMA_TOKEN)
            elif current == '[':
                return Token(current, TokenType.LEFT_BRACKET_TOKEN)
            elif current == ']':
                return Token(current, TokenType.RIGHT_BRACKET_TOKEN)
            elif current == '-':
                min = self.peek(-2)
                max = self.peek(0)
                for i in range(ord(min), ord(max) + 1):
                    self.alphabet.add(chr(i))
                return Token(current, TokenType.RANGE_TOKEN)
            elif current == '\0':
                return Token(current, TokenType.EOF_TOKEN)
        
    def advance(self):
        self.position += 1

    def skipWhiteSpace(self):
        while self.getCurrentChar() == ' ':
            self.advance()
            
    def hasReachedEOF(self):
        return self.position > len(self.text)