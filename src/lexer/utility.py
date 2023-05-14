from typing import Dict, List, Tuple

from lexer.token_manager import TokenType

MAX_INT: int = 2 ** 31 - 1
MAX_FLOAT: int = 2 ** 31 - 1
MAX_STRING_LENGTH: int = 20
MAX_IDENTIFIER_LENGTH: int = 20
EOF_TYPES: List[str] = ['\n', '\r']
EOF_CHARS: List[str] = ['', None]

SIMPLE_TOKENS: Dict[str, TokenType] = {
    '+': TokenType.ADD,
    '-': TokenType.SUBTRACT,
    '*': TokenType.MULTIPLY,
    '/': TokenType.DIVIDE,
    '(': TokenType.START_ROUND,
    ')': TokenType.STOP_ROUND,
    '[': TokenType.START_SQUARE,
    ']': TokenType.STOP_SQUARE,
    '{': TokenType.START_CURLY,
    '}': TokenType.STOP_CURLY,
    ';': TokenType.SEMICOLON,
    ':': TokenType.COLON,
    ',': TokenType.COMMA,
    '.': TokenType.DOT,
}

COMPLEX_TOKENS: Dict[str, Tuple[str, TokenType, TokenType]] = {
    ">": ("=", TokenType.GREATER, TokenType.GREATER_EQUAL),
    "<": ("=", TokenType.LESS, TokenType.LESS_EQUAL),
    "=": ("=", TokenType.ASSIGN, TokenType.EQUAL),
    "!": ("=", TokenType.NOT, TokenType.NOT_EQUAL),
}

KEYWORDS: Dict[str, TokenType] = {
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
    "int": TokenType.INTEGER,
    "dec": TokenType.DECIMAL,
    "bool": TokenType.BOOL,
    "True": TokenType.BOOL_TRUE,
    "False": TokenType.BOOL_FALSE,
    "String": TokenType.STRING,
    "Shape": TokenType.SHAPE,
    "Circle": TokenType.CIRCLE,
    "Square": TokenType.SQUARE,
    "Rectangle": TokenType.RECTANGLE,
    "Triangle": TokenType.TRIANGLE,
    "Rhomb": TokenType.RHOMB,
    "Trapeze": TokenType.TRAPEZE,
    "Polygon": TokenType.POLYGON,
    "Canvas": TokenType.CANVAS,
    "def": TokenType.FUNCTION,
    "return": TokenType.RETURN,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
}


class Position:
    line: int
    column: int

    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"({self.line}, {self.column})"
