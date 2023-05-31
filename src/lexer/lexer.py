from io import TextIOBase
from typing import Union

from error.error_lexer import (CommentOverflowError, DecimalOverflowError,
                               IntegerOverflowError, LexerError,
                               StringOverflowError, TooLongIdentifierError,
                               UnexpectedCharacterError,
                               UnexpectedNewLineSymbolError,
                               UnterminatedStringError)
from error.error_manager import LexerErrorManager
from lexer.token_manager import Token, TokenType
from utility.utility import (COMPLEX_TOKENS, EOF_CHARS, KEYWORDS,
                             MAX_IDENTIFIER_LENGTH, MAX_INT, MAX_STRING_LENGTH,
                             NL_TYPES, SIMPLE_TOKENS, Position)


class Lexer:
    stream: TextIOBase
    error_manager: LexerErrorManager
    character: str
    position: Position
    token_position: Position
    token: Token
    new_line_char: str
    max_identifier_length: int
    max_string_length: int
    max_int: int

    def __init__(
        self,
        stream: TextIOBase,
        error_manager: LexerErrorManager,
        max_identifier_length: int = MAX_IDENTIFIER_LENGTH,
        max_string_length: int = MAX_STRING_LENGTH,
        max_int: int = MAX_INT,
    ) -> None:
        self.stream = stream
        self.error_manager = error_manager
        self.character = self.stream.read(1)
        self.position = Position(1, 0)
        self.token_position = Position(1, 0)
        self.new_line_char = None
        self.token = Token(TokenType.UNDEFINED, "", self.token_position)
        self.max_identifier_length = max_identifier_length
        self.max_string_length = max_string_length
        self.max_int = max_int

    def _check_new_line(self) -> bool:
        if self.new_line_char:
            if self.character == self.new_line_char:
                self.position.line += 1
                self.position.column = 0
                self._next_char()
                return True
            elif self.character.isspace():
                self._next_char()
                return True
            else:
                self._raise_error(UnexpectedNewLineSymbolError, self.character)
                return True
        else:
            return self._try_build_new_line()

    def _try_build_new_line(self) -> bool:
        if self.character not in NL_TYPES:
            return False
        new_line_char = self.character
        if self._next_char() in NL_TYPES:
            new_line_char += self.character
            self._next_char()
        if not self.new_line_char and new_line_char in NL_TYPES:
            self.new_line_char = new_line_char
        elif self.new_line_char != new_line_char:
            self._raise_error(
                UnexpectedNewLineSymbolError, new_line_char, self.new_line_char
            )
            return True
        self.position.line += 1
        self.position.column = 0
        return True

    def _is_white(self) -> bool:
        if self.character in EOF_CHARS or not self.character.isspace():
            return False
        while self.character not in EOF_CHARS and self.character.isspace():
            if self._check_new_line():
                continue
            self._next_char()
        return True

    def _raise_error(
        self,
        error: LexerError,
        value: Union[str, int, float, bool],
        expected: str = None,
    ) -> None:
        self._next_char()
        self.token = Token(TokenType.UNDEFINED, value, self.token_position)
        self.error_manager.add_error(error(self.position, value))

    def _try_build_eof(self) -> bool:
        if self.character:
            return False
        self.token = Token(TokenType.EOF, "", self.token_position)
        return True

    def _try_build_simple_tokens(self) -> bool:
        if self.character not in SIMPLE_TOKENS:
            return False

        self.token = Token(
            SIMPLE_TOKENS[self.character], self.character, self.token_position
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
                self.token_position,
            )
            self._next_char()
        else:
            self.token = Token(
                COMPLEX_TOKENS[first_char][1], first_char, self.token_position
            )
        return True

    def _try_build_identifier_or__keyword_token(self) -> bool:
        if not self.character.isalpha() or self.character == "_":
            return False

        value = self.character
        while self._next_char().isalnum() or self.character == "_":
            if len(value) < self.max_identifier_length:
                value += self.character
            else:
                self._raise_error(TooLongIdentifierError, value)
                return True

        if value in KEYWORDS:
            self.token = Token(KEYWORDS[value], value, self.token_position)
        else:
            self.token = Token(
                TokenType.IDENTIFIER, value, self.token_position
            )
        return True

    def _try_build_number_token(self) -> bool:
        if not self.character.isdecimal():
            return False

        value = ord(self.character) - ord("0")
        number_of_digits = 0

        while self._next_char().isdecimal():
            if (
                self.max_int - ord(self.character) - ord("0")
            ) / 10 - value > 0:
                value = value * 10 + (ord(self.character) - ord("0"))
                number_of_digits += 1
            else:
                self._raise_error(IntegerOverflowError, value)
                return True

        if self.character == ".":
            self._next_char()
            if not self.character.isdecimal():
                return False

            fraction = 0
            number_of_digits = 1
            fraction = ord(self.character) - ord("0")

            while self._next_char().isdecimal():
                if self.max_int / 10 - fraction > 0:
                    fraction = fraction * 10 + (ord(self.character) - ord("0"))
                    number_of_digits += 1
                else:
                    self._raise_error(
                        DecimalOverflowError,
                        value + fraction / 10**number_of_digits,
                    )
                    return True
            self.token = Token(
                TokenType.DECIMAL_VALUE,
                value + fraction / (10**number_of_digits),
                self.token_position,
            )
            return True

        self.token = Token(TokenType.INTEGER_VALUE, value, self.token_position)
        return True

    def _try_build_comment_token(self) -> bool:
        if self.character != "#":
            return False
        value = ""
        number_of_chars = 0
        new_line = self.new_line_char if self.new_line_char else NL_TYPES
        while self._next_char() not in new_line and self.character:
            if number_of_chars == self.max_string_length:
                self._raise_error(CommentOverflowError, value)
                return True
            value += self.character
            number_of_chars += 1
        self.token = Token(TokenType.COMMENT, value, self.token_position)
        return True

    def _try_build_string_token(self) -> bool:
        if self.character != '"':
            return False
        value = ""
        number_of_chars = 0
        while self._next_char() != '"':
            if self.character in EOF_CHARS:
                self._raise_error(UnterminatedStringError, value)
                return True
            if number_of_chars == self.max_string_length:
                self._raise_error(StringOverflowError, value)
                return True
            if self.character == "\\":
                self._next_char()
                if self.character == "\\":
                    value += "\\"
                else:
                    value += f"\\{self.character}"
            else:
                value += self.character
            number_of_chars += 1

        self._next_char()
        self.token = Token(TokenType.STRING_VALUE, value, self.token_position)
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

        self._raise_error(UnexpectedCharacterError, self.character)
        return self.token
