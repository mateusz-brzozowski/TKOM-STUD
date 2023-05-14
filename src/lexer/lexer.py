from io import TextIOBase
from typing import Union

from lexer.token_manager import Token, TokenType
from error.error_manager import ErrorManager, ErrorTypes
from utility.utility import (
    Position,
    EOF_CHARS,
    MAX_INT,
    MAX_IDENTIFIER_LENGTH,
    MAX_STRING_LENGTH,
    EOF_TYPES,
    SIMPLE_TOKENS,
    COMPLEX_TOKENS,
    KEYWORDS,
)


class Lexer:
    stream: TextIOBase
    error_manager: ErrorManager
    character: str
    position: Position = Position(1, 0)
    token_position: Position = Position(1, 0)
    token: Token
    new_line_char: str = None

    def __init__(
        self, stream: TextIOBase, error_manager: ErrorManager
    ) -> None:
        self.stream = stream
        self.error_manager = error_manager
        self.character = self.stream.read(1)
        self.token = Token(TokenType.UNDEFINED, "", self.token_position)

    def _check_eof(self) -> bool:
        if self.character not in EOF_TYPES:
            return False
        eof_char = self.character
        if self._next_char() in EOF_TYPES:
            eof_char += self.character
            self._next_char()
        if not self.new_line_char:
            self.new_line_char = eof_char
        elif self.new_line_char != eof_char:
            self._raise_error(ErrorTypes.UNEXPECTED_EOF, eof_char)
            return True
        self.position.line += 1
        self.position.column = 0
        return True

    def _is_white(self) -> bool:
        if self.character in EOF_CHARS or not self.character.isspace():
            return False
        while self.character not in EOF_CHARS and self.character.isspace():
            if self._check_eof():
                continue
            self._next_char()
        return True

    def _raise_error(
        self, error_type: ErrorTypes, value: Union[str, int, float, bool]
    ) -> None:
        self._next_char()
        self.token = Token(TokenType.UNDEFINED, value, self.token_position)
        self.error_manager.add_error(error_type, self.token)

    def _try_build_eof(self):
        if self.character:
            return False
        self.token = Token(TokenType.EOF, "", self.token_position)
        return True

    def _try_build_simple_tokens(self) -> bool:
        if self.character not in SIMPLE_TOKENS:
            return False

        self.token = Token(
            SIMPLE_TOKENS[self.character],
            self.character,
            self.token_position
            )
        self._next_char()
        return True

    def _try_build_complex_tokens(self) -> bool:
        if self.character not in COMPLEX_TOKENS:
            return False

        first_char = self.character
        self._next_char()
        if self.character == COMPLEX_TOKENS[first_char][0]:
            self.token = Token(
                COMPLEX_TOKENS[first_char][2],
                first_char + self.character,
                self.token_position
                )
            self._next_char()
        else:
            self.token = Token(
                COMPLEX_TOKENS[first_char][1],
                first_char,
                self.token_position
                )
        return True

    def _try_build_identifier_or__keyword_token(self) -> bool:
        if not self.character.isalpha() or self.character == "_":
            return False

        value = self.character
        while self._next_char().isalnum() or self.character == "_":
            if len(value) < MAX_IDENTIFIER_LENGTH:
                value += self.character
            else:
                self._raise_error(ErrorTypes.IDENTIFIER_OVERFLOW, value)
                return True

        if value in KEYWORDS:
            self.token = Token(KEYWORDS[value], value, self.token_position)
        else:
            self.token = Token(
                TokenType.IDENTIFIER,
                value,
                self.token_position
                )
        return True

    def _try_build_number_token(self) -> bool:
        if not self.character.isdecimal():
            return False

        value = ord(self.character) - ord('0')
        number_of_digits = 0

        while self._next_char().isdecimal():
            if (MAX_INT - ord(self.character) - ord('0')) / 10 - value > 0:
                value = value * 10 + (ord(self.character) - ord('0'))
                number_of_digits += 1
            else:
                self._raise_error(ErrorTypes.INTEGER_OVERFLOW, value)
                return True

        if self.character == '.':
            self._next_char()
            if not self.character.isdecimal():
                return False

            fraction = 0
            number_of_digits = 1
            fraction = ord(self.character) - ord('0')

            while self._next_char().isdecimal():
                if MAX_INT / 10 - fraction > 0:
                    fraction = fraction * 10 + (ord(self.character) - ord('0'))
                    number_of_digits += 1
                else:
                    self._raise_error(
                        ErrorTypes.DECIMAL_OVERFLOW,
                        value + fraction / 10 ** number_of_digits
                    )
                    return True
            self.token = Token(
                TokenType.DECIMAL,
                value + fraction / (10 ** number_of_digits),
                self.token_position
            )
            return True

        self.token = Token(TokenType.INTEGER, value, self.token_position)
        return True

    def _try_build_comment_token(self) -> bool:
        if self.character != '#':
            return False
        value = ""
        number_of_chars = 0
        new_line = self.new_line_char if self.new_line_char else EOF_TYPES
        while self._next_char() not in new_line and self.character:
            if number_of_chars == MAX_STRING_LENGTH:
                self._raise_error(ErrorTypes.COMMENT_OVERFLOW, value)
                return True
            value += self.character
            number_of_chars += 1
        self.token = Token(TokenType.COMMENT, value, self.token_position)
        return True

    def _try_build_string_token(self) -> bool:
        if self.character != '\"':
            return False
        value = ""
        number_of_chars = 0
        while self._next_char() != '\"':
            if self.character in EOF_CHARS:
                self._raise_error(ErrorTypes.UNTERMINATED_STRING, value)
                return True
            if number_of_chars == MAX_STRING_LENGTH:
                self._raise_error(ErrorTypes.STRING_OVERFLOW, value)
                return True
            value += self.character
            number_of_chars += 1

        self._next_char()
        self.token = Token(TokenType.STRING, value, self.token_position)
        return True

    def _next_char(self) -> str:
        self.character = self.stream.read(1)
        self.position.column += 1
        return self.character

    def next_token(self) -> Token:
        while self._is_white():
            pass

        self.token_position = self.position

        if (
            self._try_build_eof()
            or self._try_build_simple_tokens()
            or self._try_build_complex_tokens()
            or self._try_build_identifier_or__keyword_token()
            or self._try_build_number_token()
            or self._try_build_comment_token()
            or self._try_build_string_token()
        ):
            return self.token

        self._raise_error(ErrorTypes.UNEXPECTED_CHARACTER, self.character)
        return self.token
