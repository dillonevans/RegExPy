from NFA import EPS
from Token import Token, TokenType

CONCAT_OPERATOR = '\u2022'

# Handle implicit Concatenations
def formatText(text):
    current, prev = '', ''
    formatted = ""

    for char in text:
        if (char.isspace() == False):
            current  = char
            if (current.isalpha() or current == '('):
                if (prev.isalpha() or prev in ['*', ')', '+', '?']):
                    formatted =  f"{formatted}{CONCAT_OPERATOR}{current}"
                else:
                    formatted += current
            else:
                formatted += current
            prev = current
    print(formatted)
    return formatted

class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.position = 0
        self.text = formatText(text)
        self.alphabet = []

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

        current = self.getCurrentChar()
        self.advance()
        if current.isalpha():
            if current not in self.alphabet:
                self.alphabet.append(current)
            return Token(current, TokenType.CHARACTER)

        else:
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
            elif current == '\0':
                return Token(current, -1)
        
    def advance(self):
        self.position += 1

    def skipWhiteSpace(self):
        while self.getCurrentChar() == ' ':
            self.advance()
            
    def hasReachedEOF(self):
        return self.position > len(self.text)