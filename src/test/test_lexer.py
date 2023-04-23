import pytest
import io

from src.lexer.lexer import Lexer
from src.lexer.token_manager import TokenType
from src.lexer.error_manager import ErrorManager

TestData = [
    ("1", TokenType.INTEGER),
]


@pytest.mark.parametrize("stream,expected", TestData)
def test_token_type(stream, expected):
    with io.StringIO(stream) as stream:
        lexer = Lexer(stream, ErrorManager())
        assert TokenType.INTEGER == expected
