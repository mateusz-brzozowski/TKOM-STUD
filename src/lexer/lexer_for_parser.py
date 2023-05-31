from io import TextIOBase

from error.error_manager import ErrorManager
from lexer.lexer import Lexer
from lexer.token_manager import Token, TokenType


class LexerForParser(Lexer):
    def __init__(
        self,
        stream: TextIOBase,
        error_manager: ErrorManager,
        max_identifier_length: int,
        max_string_length: int,
        max_int: int,
    ) -> None:
        super().__init__(
            stream,
            error_manager,
            max_identifier_length,
            max_string_length,
            max_int,
        )

    def next_token(self) -> Token:
        """Returns next token except comments"""
        token = super().next_token()
        while token.token_type == TokenType.COMMENT:
            token = super().next_token()
        return token
