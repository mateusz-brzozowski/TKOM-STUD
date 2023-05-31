from parser.objects.type import (Bool, Canvas, Circle, Dec, Int, Polygon,
                                 Rectangle, Rhomb, Shape, Square, String,
                                 Trapeze, Triangle, Type)

from lexer.token_manager import TokenType

MAX_INT: int = 2**31 - 1
MAX_FLOAT: int = 2**31 - 1
MAX_STRING_LENGTH: int = 200
MAX_IDENTIFIER_LENGTH: int = 200
NL_TYPES: list[str] = ["\n", "\r", "\r\n", "\n\r"]
EOF_CHARS: list[str] = ["", None]

SINGLE_TOKENS: dict[str, TokenType] = {
    "+": TokenType.ADD,
    "-": TokenType.SUBTRACT,
    "*": TokenType.MULTIPLY,
    "/": TokenType.DIVIDE,
    "(": TokenType.START_ROUND,
    ")": TokenType.STOP_ROUND,
    "[": TokenType.START_SQUARE,
    "]": TokenType.STOP_SQUARE,
    "{": TokenType.START_CURLY,
    "}": TokenType.STOP_CURLY,
    ";": TokenType.SEMICOLON,
    ":": TokenType.COLON,
    ",": TokenType.COMMA,
    ".": TokenType.DOT,
}

DOUBLE_TOKENS: dict[str, tuple[str, TokenType, TokenType]] = {
    ">": ("=", TokenType.GREATER, TokenType.GREATER_EQUAL),
    "<": ("=", TokenType.LESS, TokenType.LESS_EQUAL),
    "=": ("=", TokenType.ASSIGN, TokenType.EQUAL),
    "!": ("=", TokenType.NOT, TokenType.NOT_EQUAL),
}

KEYWORDS: dict[str, TokenType] = {
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

DECLARATION_TYPES: dict[TokenType, Type] = {
    TokenType.INTEGER: Int,
    TokenType.DECIMAL: Dec,
    TokenType.BOOL: Bool,
    TokenType.STRING: String,
    TokenType.SHAPE: Shape,
    TokenType.CIRCLE: Circle,
    TokenType.SQUARE: Square,
    TokenType.RECTANGLE: Rectangle,
    TokenType.TRIANGLE: Triangle,
    TokenType.RHOMB: Rhomb,
    TokenType.TRAPEZE: Trapeze,
    TokenType.POLYGON: Polygon,
    TokenType.CANVAS: Canvas,
}

RELATIVE_OPERATORS: list[TokenType] = [
    TokenType.GREATER,
    TokenType.LESS,
    TokenType.GREATER_EQUAL,
    TokenType.LESS_EQUAL,
    TokenType.EQUAL,
    TokenType.NOT_EQUAL,
]

SUM_OPERATORS: list[TokenType] = [
    TokenType.SUBTRACT,
    TokenType.ADD,
]

MULTIPLY_OPERATORS: list[TokenType] = [
    TokenType.MULTIPLY,
    TokenType.DIVIDE,
]

UNARY_OPERATORS: list[TokenType] = [
    TokenType.NOT,
    TokenType.SUBTRACT,
]

LITERAL_TYPES: dict[Type, type] = {
    Int: int,
    Dec: float,
    Bool: bool,
    String: str,
}

OBJECT_TYPES: dict[Type, type] = {
    "Shape": Shape,
    "Circle": Circle,
    "Square": Square,
    "Rectangle": Rectangle,
    "Triangle": Triangle,
    "Rhomb": Rhomb,
    "Trapeze": Trapeze,
    "Polygon": Polygon,
    "Canvas": Canvas,
}


class Position:
    line: int
    column: int

    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"{self.line}, {self.column}"
