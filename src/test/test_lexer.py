import io

import pytest

from error.error_lexer import (CommentOverflowError, DecimalOverflowError,
                               IntegerOverflowError, InvalidNewLineSymbolError,
                               LexerError, StringOverflowError,
                               TooLongIdentifierError,
                               UnexpectedCharacterError,
                               UnexpectedNewLineSymbolError,
                               UnterminatedStringError)
from src.error.error_manager import ErrorManager
from src.lexer.lexer import Lexer
from src.lexer.token_manager import TokenType

TestCorrectTokensData: list[tuple[str, TokenType]] = [
    ("1", TokenType.INTEGER_VALUE.name),
    ("1.1", TokenType.DECIMAL_VALUE.name),
    ("0", TokenType.INTEGER_VALUE.name),
    ("0.0", TokenType.DECIMAL_VALUE.name),
    ("0.00001", TokenType.DECIMAL_VALUE.name),
    ("True", TokenType.BOOL_TRUE.name),
    ("False", TokenType.BOOL_FALSE.name),
    ('"String"', TokenType.STRING_VALUE.name),
    ('"Str\ni\rn\tg"', TokenType.STRING_VALUE.name),
    ('"S😂😊tr\ni\rn\tg"', TokenType.STRING_VALUE.name),
    ("Shape", TokenType.SHAPE.name),
    ("+", TokenType.ADD.name),
    ("-", TokenType.SUBTRACT.name),
    ("*", TokenType.MULTIPLY.name),
    ("and", TokenType.AND.name),
    ("or", TokenType.OR.name),
    ("not", TokenType.NOT.name),
    ("==", TokenType.EQUAL.name),
    ("!=", TokenType.NOT_EQUAL.name),
    (">", TokenType.GREATER.name),
    (">=", TokenType.GREATER_EQUAL.name),
    ("#asd", TokenType.COMMENT.name),
    ("main", TokenType.IDENTIFIER.name),
    ("int", TokenType.INTEGER.name),
    (r'"St\"r\ni\rn\tg"', TokenType.STRING_VALUE.name),
    (r'"\""', TokenType.STRING_VALUE.name),
    (r'"\\\""', TokenType.STRING_VALUE.name),
    (r'"\t\t😎😋😚"', TokenType.STRING_VALUE.name),
]


@pytest.mark.parametrize("stream,expected", TestCorrectTokensData)
def test_token_type(stream, expected):
    with io.StringIO(stream) as stream:
        lexer = Lexer(stream, ErrorManager())
        lexer.next_token()
        assert lexer.token.token_type.name is expected


TestMultiTokensData: list[tuple[str, list[TokenType]]] = [
    (
        """1.0
    2.0
    312
    """,
        [
            TokenType.DECIMAL_VALUE.name,
            TokenType.DECIMAL_VALUE.name,
            TokenType.INTEGER_VALUE.name,
        ],
    ),
    (
        """"String"
    123
    123.123
    True
    """,
        [
            TokenType.STRING_VALUE.name,
            TokenType.INTEGER_VALUE.name,
            TokenType.DECIMAL_VALUE.name,
            TokenType.BOOL_TRUE.name,
        ],
    ),
    (
        """ #asdasd
        int x = 1;
        True or False;
        """,
        [
            TokenType.COMMENT.name,
            TokenType.INTEGER.name,
            TokenType.IDENTIFIER.name,
            TokenType.ASSIGN.name,
            TokenType.INTEGER_VALUE.name,
            TokenType.SEMICOLON.name,
            TokenType.BOOL_TRUE.name,
            TokenType.OR.name,
            TokenType.BOOL_FALSE.name,
            TokenType.SEMICOLON.name,
        ],
    ),
    (
        """if(True){
            while(i < 10){
            }
        }
        """,
        [
            TokenType.IF.name,
            TokenType.START_ROUND.name,
            TokenType.BOOL_TRUE.name,
            TokenType.STOP_ROUND.name,
            TokenType.START_CURLY.name,
            TokenType.WHILE.name,
            TokenType.START_ROUND.name,
            TokenType.IDENTIFIER.name,
            TokenType.LESS.name,
            TokenType.INTEGER_VALUE.name,
            TokenType.STOP_ROUND.name,
            TokenType.START_CURLY.name,
            TokenType.STOP_CURLY.name,
            TokenType.STOP_CURLY.name,
        ],
    ),
    (
        """def main(){
            Circle c = c or c and c;
        }
        """,
        [
            TokenType.FUNCTION.name,
            TokenType.IDENTIFIER.name,
            TokenType.START_ROUND.name,
            TokenType.STOP_ROUND.name,
            TokenType.START_CURLY.name,
            TokenType.CIRCLE.name,
            TokenType.IDENTIFIER.name,
            TokenType.ASSIGN.name,
            TokenType.IDENTIFIER.name,
            TokenType.OR.name,
            TokenType.IDENTIFIER.name,
            TokenType.AND.name,
            TokenType.IDENTIFIER.name,
            TokenType.SEMICOLON.name,
            TokenType.STOP_CURLY.name,
        ],
    ),
]


@pytest.mark.parametrize("stream,expected", TestMultiTokensData)
def test_mulit_tokens_type(stream, expected):
    with io.StringIO(stream) as stream:
        lexer = Lexer(stream, ErrorManager())
        tokens = []
        token = lexer.next_token().token_type.name
        while token != TokenType.EOF.name:
            tokens.append(token)
            token = lexer.next_token().token_type.name
        assert tokens == expected


TestUndefinedTokensData: list[str] = [
    "131231323231231231",
    "123.123123123123123",
    '"asd',
    "@=",
    "#1231233123123213122311321112312331231232131223113211",
    '"1231233123123213122311321112312331231232131223113211"',
    "bardzo_dluga_zmiennaaaaaaaaaaaaa",
]


@pytest.mark.parametrize("stream", TestUndefinedTokensData)
def test_Undefined_token(stream):
    with io.StringIO(stream) as stream:
        lexer = Lexer(stream, ErrorManager(), 20, 20, 200)
        lexer.error_manager.errors = []
        lexer.next_token()
        assert lexer.token.token_type.name is TokenType.UNDEFINED.name


TestErrorsData: list[tuple[str, LexerError]] = [
    ('"asd', UnterminatedStringError),
    (
        "1231233123123213122311321112312331231232131223113211",
        IntegerOverflowError,
    ),
    ("123.123123123123123", DecimalOverflowError),
    ("@=", UnexpectedCharacterError),
    (
        "#1231233123123213122311321112312331231232131223113211",
        CommentOverflowError,
    ),
    (
        '"1231233123123213122311321112312331231232131223113211"',
        StringOverflowError,
    ),
    ('"123123', UnterminatedStringError),
    ("bardzo_dluga_zmiennaaaaaaaaaaaaa", TooLongIdentifierError),
    ("123%123", UnexpectedCharacterError),
    ("1.13%123", UnexpectedCharacterError),
    ("123\n" "123\r", InvalidNewLineSymbolError),
    ("123\n\n", UnexpectedNewLineSymbolError),
]


@pytest.mark.parametrize("stream,expected", TestErrorsData)
def test_error_types(stream, expected):
    with io.StringIO(stream) as stream:
        lexer = Lexer(stream, ErrorManager(), 20, 20, 300)
        lexer.error_manager.errors = []
        while lexer.next_token().token_type.name != TokenType.EOF.name:
            pass
        assert type(lexer.error_manager.errors[0]) == expected
