from enum import Enum

class TokenType(Enum):
    CHARACTER = 1
    UNION_TOKEN = 2
    KLEENE_CLOSURE_TOKEN = 3,
    KLEENE_PLUS_TOKEN = 4,
    CONCATENATION_TOKEN = 5,
    QUESTION_TOKEN = 6,
    LEFT_PARENTHESIS_TOKEN = 7,
    RIGHT_PARENTHESIS_TOKEN = 8


class Token:
    def __init__(self, text: str, type: TokenType ) -> None:
        self.text = text
        self.type = type