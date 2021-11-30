from enum import Enum

class TokenType(Enum):
    CHARACTER_TOKEN = 1
    NUMERIC_TOKEN = 2
    UNION_TOKEN = 3
    KLEENE_CLOSURE_TOKEN = 4
    KLEENE_PLUS_TOKEN = 5
    CONCATENATION_TOKEN = 6
    QUESTION_TOKEN = 7
    LEFT_PARENTHESIS_TOKEN = 8
    RIGHT_PARENTHESIS_TOKEN = 9
    LEFT_BRACE_TOKEN = 10
    RIGHT_BRACE_TOKEN = 11
    COMMA_TOKEN = 12,
    LEFT_BRACKET_TOKEN = 13,
    RIGHT_BRACKET_TOKEN = 14,
    RANGE_TOKEN = 15,
    EOF_TOKEN = 16

class Token:
    def __init__(self, text: str, type: TokenType ) -> None:
        self.text = text
        self.type = type