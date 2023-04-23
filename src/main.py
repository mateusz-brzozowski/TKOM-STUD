from lexer.lexer import Lexer
from lexer.error_manager import ErrorManager
from lexer.token_manager import TokenType


def main() -> None:
    with open('kod1.txt', 'r') as file:
        lexer = Lexer(file, ErrorManager())
        while lexer.next_token().token_type != TokenType.EOF:
            print(lexer.token)
        print(lexer.token)
        lexer.error_manager.print_errors()


if __name__ == '__main__':
    main()
