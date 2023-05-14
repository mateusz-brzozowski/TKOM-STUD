import pytest
import io

from src.lexer.lexer import Lexer
from src.lexer.token_manager import TokenType
from src.error.error_manager import ErrorManager, ErrorTypes

TestCorrectTokensData = [
    ("1", TokenType.INTEGER.name),
    ("1.1", TokenType.DECIMAL.name),
    ("0", TokenType.INTEGER.name),
    ("0.0", TokenType.DECIMAL.name),
    ("0.00001", TokenType.DECIMAL.name),
    ("True", TokenType.BOOL_TRUE.name),
    ("False", TokenType.BOOL_FALSE.name),
    ("\"String\"", TokenType.STRING.name),
    ("\"Str\ni\rn\tg\"", TokenType.STRING.name),
    ('\"S😂😊tr\ni\rn\tg\"', TokenType.STRING.name),
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
    ("main", TokenType.IDENTIFIER.name)
]


@pytest.mark.parametrize("stream,expected", TestCorrectTokensData)
def test_token_type(stream, expected):
    with io.StringIO(stream) as stream:
        lexer = Lexer(stream, ErrorManager())
        lexer.next_token()
        assert lexer.token.token_type.name is expected


TestUndefinedTokensData = [
    "131231323231231231",
    "123.123123123123123",
    "\"asd",
    "@=",
    "#1231233123123213122311321112312331231232131223113211",
    "\"1231233123123213122311321112312331231232131223113211\"",
    "bardzo_dluga_zmiennaaaaaaaaaaaaa",
]


@pytest.mark.parametrize("stream", TestUndefinedTokensData)
def test_Undefined_token(stream):
    with io.StringIO(stream) as stream:
        lexer = Lexer(stream, ErrorManager())
        lexer.next_token()
        assert lexer.token.token_type.name is TokenType.UNDEFINED.name


TestErrorsData = [
    ("\"asd", ErrorTypes.UNTERMINATED_STRING.name),
    ("1231233123123213122311321112312331231232131223113211",
     ErrorTypes.INTEGER_OVERFLOW.name),
    ("123.123123123123123", ErrorTypes.DECIMAL_OVERFLOW.name),
    ("@=", ErrorTypes.UNEXPECTED_CHARACTER.name),
    ("#1231233123123213122311321112312331231232131223113211",
     ErrorTypes.COMMENT_OVERFLOW.name),
    ("\"1231233123123213122311321112312331231232131223113211\"",
     ErrorTypes.STRING_OVERFLOW.name),
    ("\"123123", ErrorTypes.UNTERMINATED_STRING.name),
    ("bardzo_dluga_zmiennaaaaaaaaaaaaa", ErrorTypes.IDENTIFIER_OVERFLOW.name),
    ("123%123", ErrorTypes.UNEXPECTED_CHARACTER.name),
    ("1.13%123", ErrorTypes.UNEXPECTED_CHARACTER.name),
]


@pytest.mark.parametrize("stream,expected", TestErrorsData)
def test_error_types(stream, expected):
    with io.StringIO(stream) as stream:
        lexer = Lexer(stream, ErrorManager())
        while lexer.next_token().token_type.name != TokenType.UNDEFINED.name:
            pass
        assert lexer.error_manager.errors[0][0].name == expected
