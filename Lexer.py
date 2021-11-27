from NFA import EPS
from Token import Token, TokenType

CONCAT_OPERATOR = '\u2022'

# Handle implicit Concatenations
def formatText(text):
    current, prev = '', ''
    formatted = ""
    isInBraces = False

    for char in text:
        if (not char.isspace()):
            current  = char
            if (current.isalpha() or current == '(' or current.isdigit()):
                if (prev.isalpha() or prev.isdigit() or prev in ['*', ')', '+', '?', '}', ',']):
                    if (not isInBraces):
                        formatted =  f"{formatted}{CONCAT_OPERATOR}"
                    
            formatted += current
            prev = current

            if (prev == '{'):
                isInBraces = True
            elif (prev == '}'):
                isInBraces = False
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
        start = self.position
        current = self.getCurrentChar()
        
        if current.isalpha():
            self.advance()
            if current not in self.alphabet:
                self.alphabet.append(current)
            return Token(current, TokenType.CHARACTER)

        if (current.isdigit()):
            while (current.isdigit()):
                self.advance()
                current = self.getCurrentChar()
            lexeme = self.text[start:self.position]
            return Token(lexeme, TokenType.NUMERIC)
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
            elif current == '\0':
                return Token(current, -1)
        
    def advance(self):
        self.position += 1

    def skipWhiteSpace(self):
        while self.getCurrentChar() == ' ':
            self.advance()
            
    def hasReachedEOF(self):
        return self.position > len(self.text)