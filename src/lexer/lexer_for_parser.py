from io import TextIOBase
from lexer.lexer import Lexer
from error.error_manager import LexerErrorManager
from lexer.token_manager import Token, TokenType

class LexerForParser(Lexer):
    def __init__(self, stream: TextIOBase, error_manager: LexerErrorManager) -> None:
        super().__init__(stream, error_manager)


    def next_token(self) -> Token:
        token = super().next_token()
        while token.token_type == TokenType.COMMENT:
            token = super().next_token()
        return token