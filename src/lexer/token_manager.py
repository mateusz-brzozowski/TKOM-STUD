from __future__ import annotations
from enum import Enum
from typing import Union

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from lexer.utility import Position


class TokenType(Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"

    ASSIGN = "="

    AND = "and"
    OR = "or"
    NOT = "not"

    EQUAL = "=="
    NOT_EQUAL = "!="
    GREATER = ">"
    LESS = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="

    COMMENT = "#"

    INTEGER = "int"
    DECIMAL = "dec"
    BOOL = "bool"

    BOOL_TRUE = "True"
    BOOL_FALSE = "False"

    STRING = "String"
    STRING_QUOTE = "\""

    SHAPE = "Shape"
    CIRCLE = "Circle"
    SQUARE = "Square"
    RECTANGLE = "Rectangle"
    TRIANGLE = "Triangle"
    RHOMB = "Rhomb"
    TRAPEZE = "Trapeze"
    POLYGON = "Polygon"
    CANVAS = "Canvas"

    SEMICOLON = ";"
    COLON = ":"
    COMMA = ","
    DOT = "."

    FUNCTION = "def"
    RETURN = "return"

    START_CURLY = "{"
    STOP_CURLY = "}"
    START_ROUND = "("
    STOP_ROUND = ")"
    START_SQUARE = "["
    STOP_SQUARE = "]"

    IF = "if"
    ELSE = "else"

    WHILE = "while"
    FOR = "for"

    UNDEFINED = "undefined"
    IDENTIFIER = "identifier"
    EOF = "eof"


class Token:
    token_type: TokenType
    value: Union[str, int, float, bool]
    position: Position

    def __init__(
        self,
        token_type: TokenType,
        value: Union[str, int, float, bool],
        position: Position
    ) -> None:
        self.token_type = token_type
        self.value = value
        self.position = position

    def __str__(self) -> str:
        return f"Token({self.token_type.name}, {self.value}, {self.position})"