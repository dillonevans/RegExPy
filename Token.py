from enum import Enum

class TokenType(Enum):
    CHARACTER = 1
    UNION_TOKEN = 2
    KLEENE_CLOSURE_TOKEN = 3
    CONCATENATION_TOKEN = 4
    LEFT_PARENTHESIS_TOKEN = 5
    RIGHT_PARENTHESIS_TOKEN = 6


class Token:
    def __init__(self, text: str, type: TokenType ) -> None:
        self.text = text
        self.type = type