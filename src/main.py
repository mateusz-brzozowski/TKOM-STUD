from lexer.lexer import Lexer
from parser.parser import Parser
from error.error_manager import ErrorManager
from lexer.token_manager import TokenType
from visitor.visitor import Visitor

def main() -> None:
    with open('kod1.txt', 'r') as file:
        lexer = Lexer(file, ErrorManager())
        parser = Parser(lexer, ErrorManager())
        visitor = Visitor()
        program = parser.parse_program()
        print(program)
        # lexer.error_manager.print_errors()
        # parser.error_manager.print_errors()
        # while lexer.next_token().token_type != TokenType.EOF:
        #     print(lexer.token)
        # print(lexer.token)
        # lexer.error_manager.print_errors()


if __name__ == '__main__':
    main()
