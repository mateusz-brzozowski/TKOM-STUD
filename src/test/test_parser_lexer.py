import pytest
import io

from src.lexer.lexer import Lexer
from src.error.error_manager import ErrorManager
from src.parser.parser import Parser
from src.parser.objects.program import Program
from src.parser.objects.function import Function
from src.parser.objects.block import Block
from src.parser.objects.statement import CommentStatement
from src.utility.utility import Position


CorrectSourceCode = [
    ("def main(){}", Program([])),
]


@pytest.mark.parametrize("stream,expected", CorrectSourceCode)
def test_token_type(stream, expected):
    with io.StringIO("# sddaf") as stream:
        lexer = Lexer(stream, ErrorManager())
        parser = Parser(lexer, ErrorManager())
        output = parser._parse_comment()
        assert isinstance(output, CommentStatement)
