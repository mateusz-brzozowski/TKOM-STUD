from parser.objects.block import Block
from parser.objects.expression import (AndExpression, BooleanExpression,
                                       CallExpression, CastExpression,
                                       DecimalExpression, Expression,
                                       IdentifierExpression, IntegerExpression,
                                       LiteralExpression, MulExpression,
                                       NegatedExpression, OrExpression,
                                       RelativeExpression, StringExpression,
                                       SumExpression)
from parser.objects.function import Function
from parser.objects.program import Program
from parser.objects.statement import (AssignmentStatement,
                                      DeclarationStatement, IfStatement,
                                      IterateStatement, ReturnStatement,
                                      Statement, WhileStatement)
from parser.objects.type import Type

from error.error_manager import ErrorManager
from error.error_parser import (ExistArgumentError, ExistFunctionError,
                                MissingArgumentError, MissingExpressionError,
                                MissingIdentifierError, UnexpectedTokenError)
from lexer.lexer import Lexer
from lexer.token_manager import TokenType
from utility.utility import (DECLARATION_TYPES, MULTIPLY_OPERATORS,
                             RELATIVE_OPERATORS, SUM_OPERATORS,
                             UNARY_OPERATORS)


class Parser:
    lexer: Lexer
    error_manager: ErrorManager

    def __init__(self, lexer: Lexer, error_manger: ErrorManager) -> None:
        self.lexer = lexer
        self.error_manager = error_manger
        self.lexer.next_token()

    def _check_and_consume_token(self, expected_token: TokenType) -> bool:
        """Check if current token is expected token and consume it."""
        if self.lexer.token.token_type != expected_token:
            self.error_manager.add_error(
                UnexpectedTokenError(
                    self.lexer.token.position,
                    self.lexer.token.token_type,
                    expected_token,
                )
            )
            return False
        self.lexer.next_token()
        return True

    # program = {fun_declaration};
    def parse_program(self) -> Program:
        """Parse program."""
        functions: list[Function] = []

        while function := self._parse_fun_declaration():
            if function.name in [function.name for function in functions]:
                self.error_manager.add_error(
                    ExistFunctionError(
                        self.lexer.token.position, function.name
                    )
                )
            else:
                functions.append(function)

        return Program(functions)

    # fun_declaration = "def", [type], identifier,
    #                   '(', [argument_list], ')', block;
    def _parse_fun_declaration(self) -> Function:
        """Parse function declaration."""
        if self.lexer.token.token_type != TokenType.FUNCTION:
            return None
        self.lexer.next_token()

        declaration_type = self._parse_type()
        if declaration_type is not None:
            self.lexer.next_token()

        if self.lexer.token.token_type != TokenType.IDENTIFIER:
            self.error_manager.add_error(
                MissingIdentifierError(
                    self.lexer.token.position, self.lexer.token.value
                )
            )
        name = self.lexer.token.value

        self.lexer.next_token()

        self._check_and_consume_token(TokenType.START_ROUND)

        argument_list = self._parse_argument_list()

        self._check_and_consume_token(TokenType.STOP_ROUND)

        block = self._parse_block()

        return Function(
            self.lexer.token.position,
            name,
            block,
            argument_list,
            declaration_type,
        )

    def _parse_type(self) -> Type:
        """Parse possible declaration type."""
        if self.lexer.token.token_type in DECLARATION_TYPES:
            return DECLARATION_TYPES[self.lexer.token.token_type]
        return None

    # argument_list = argument_dec, {',', argument_dec};
    def _parse_argument_list(self) -> list[tuple[Type, str]]:
        """Parse argument declaration list."""
        argument_list = []
        argument_dec = self._parse_argument_dec()

        if argument_dec is None:
            return argument_list

        argument_list.append(argument_dec)

        while self.lexer.token.token_type == TokenType.COMMA:
            self.lexer.next_token()
            argument_dec = self._parse_argument_dec()
            if argument_dec is None:
                argument_dec = [0, 0]
                self.error_manager.add_error(
                    MissingArgumentError(
                        self.lexer.token.position, self.lexer.token.value
                    )
                )
            elif argument_dec in argument_list:
                self.error_manager.add_error(
                    ExistArgumentError(
                        self.lexer.token.position, self.lexer.token.value
                    )
                )
            else:
                argument_list.append(argument_dec)
        return argument_list

    # argument_dec = type, identifier;
    def _parse_argument_dec(self) -> tuple[Type, str]:
        """Parse argument declaration."""
        declaration_type = self._parse_type()
        if declaration_type is None:
            return None

        self.lexer.next_token()
        if self.lexer.token.token_type != TokenType.IDENTIFIER:
            self.error_manager.add_error(
                MissingIdentifierError(
                    self.lexer.token.position, self.lexer.token.value
                )
            )
            return None
        identifier = self.lexer.token.value
        self.lexer.next_token()
        return (declaration_type, identifier)

    # block = '{',  {statement}, '}';
    def _parse_block(self) -> Block:
        """Parse block."""
        self._check_and_consume_token(TokenType.START_CURLY)

        statements = []
        while statement := self._parse_statement():
            statements.append(statement)

        self._check_and_consume_token(TokenType.STOP_CURLY)

        return Block(statements)

    # statement = if_statement | while_statement | iterate_statement |
    #             return_statement | declaration | assignment | expression;
    def _parse_statement(self) -> Statement:
        """Parse statement."""
        return (
            self._parse_if_statement()
            or self._parse_while_statement()
            or self._parse_iterate_statement()
            or self._parse_return_statement()
            or self._parse_declaration_statement()
            or self._parse_assignment_or_exp()
        )

    # if_statement = "if", "(", logical_expression, ")",
    #                block, ["else", block] ;
    def _parse_if_statement(self) -> IfStatement:
        """Parse if statement."""
        if self.lexer.token.token_type != TokenType.IF:
            return None

        self.lexer.next_token()
        self._check_and_consume_token(TokenType.START_ROUND)

        condition = self._parse_logical_expression()

        if condition is None:
            self.error_manager.add_error(
                MissingExpressionError(
                    self.lexer.token.position, self.lexer.token.value
                )
            )

        self._check_and_consume_token(TokenType.STOP_ROUND)

        block = self._parse_block()

        else_block = None
        if self.lexer.token.token_type == TokenType.ELSE:
            self.lexer.next_token()
            else_block = self._parse_block()

        return IfStatement(
            self.lexer.token.position, condition, block, else_block
        )

    # while_statement = "while", '(', logical_expression, ')', block;
    def _parse_while_statement(self) -> WhileStatement:
        """Parse while statement."""
        if self.lexer.token.token_type != TokenType.WHILE:
            return None

        self.lexer.next_token()
        self._check_and_consume_token(TokenType.START_ROUND)

        condition = self._parse_logical_expression()

        if condition is None:
            self.error_manager.add_error(
                MissingExpressionError(
                    self.lexer.token.position, self.lexer.token.value
                )
            )

        self._check_and_consume_token(TokenType.STOP_ROUND)

        block = self._parse_block()

        return WhileStatement(self.lexer.token.position, condition, block)

    # iterate_statement = "for", '(', argument_dec, ':', expression, ')',
    #                     block;
    def _parse_iterate_statement(self) -> IterateStatement:
        """Parse iterate statement."""
        if self.lexer.token.token_type != TokenType.FOR:
            return None

        self.lexer.next_token()
        self._check_and_consume_token(TokenType.START_ROUND)

        argument_dec = self._parse_argument_dec()

        if argument_dec is None:
            argument_dec = [0, 0]
            self.error_manager.add_error(
                MissingArgumentError(
                    self.lexer.token.position, self.lexer.token.value
                )
            )

        self._check_and_consume_token(TokenType.COLON)

        expression = self._parse_logical_expression()

        if expression is None:
            self.error_manager.add_error(
                MissingExpressionError(
                    self.lexer.token.position, self.lexer.token.value
                )
            )

        self._check_and_consume_token(TokenType.STOP_ROUND)

        block = self._parse_block()

        return IterateStatement(
            self.lexer.token.position, argument_dec, expression, block
        )

    # return_statement = "return", expression, ';';
    def _parse_return_statement(self) -> ReturnStatement:
        """Parse return statement."""
        if self.lexer.token.token_type != TokenType.RETURN:
            return None

        self.lexer.next_token()
        expression = self._parse_logical_expression()
        if expression is None:
            self.error_manager.add_error(
                MissingExpressionError(
                    self.lexer.token.position, self.lexer.token.value
                )
            )

        self._check_and_consume_token(TokenType.SEMICOLON)

        return ReturnStatement(self.lexer.token.position, expression)

    # declaration = argument_dec, ['=', expression], ';';
    def _parse_declaration_statement(self) -> DeclarationStatement:
        """Parse declaration statement."""
        argument_dec = self._parse_argument_dec()
        if argument_dec is None:
            return None

        if self.lexer.token.token_type == TokenType.ASSIGN:
            self.lexer.next_token()
            expression = self._parse_logical_expression()
        else:
            expression = None

        self._check_and_consume_token(TokenType.SEMICOLON)

        return DeclarationStatement(
            self.lexer.token.position, argument_dec, expression
        )

    # assignment_or_exp = identifier, ['=', expression], ';';
    def _parse_assignment_or_exp(self) -> Expression:
        """Parse assignment expression or single expression."""
        id_or_exp = self._parse_logical_expression()

        assignment = False
        if self.lexer.token.token_type == TokenType.ASSIGN:
            assignment = True
            self.lexer.next_token()
            expression = self._parse_logical_expression()

        if id_or_exp is not None:
            self._check_and_consume_token(TokenType.SEMICOLON)

        if assignment:
            return AssignmentStatement(
                self.lexer.token.position, id_or_exp, expression
            )
        else:
            return id_or_exp

    # expression_list = expression, {',', expression};
    def _parse_expression_list(self) -> list[Expression]:
        """ "Parse expression list."""
        expression_list = []
        expression = self._parse_logical_expression()

        if expression is None:
            return expression_list

        expression_list.append(expression)

        while self.lexer.token.token_type == TokenType.COMMA:
            self.lexer.next_token()
            expression = self._parse_logical_expression()
            if expression is None:
                self.error_manager.add_error(
                    MissingExpressionError(
                        self.lexer.token.position, self.lexer.token.value
                    )
                )
            else:
                expression_list.append(expression)
        return expression_list

    # expression = expression_call
    def _parse_expression(self) -> Expression:
        """Parse expression."""
        return self._parse_expression_call()

    # expression_call = simple_expression,
    #                   [".", identifier, '(', [expression_list], ')']
    def _parse_expression_call(self) -> Expression:
        """Parse single expression or expression call."""
        root_expression = self._parse_simple_expression()

        if self.lexer.token.token_type != TokenType.DOT:
            return root_expression

        self.lexer.next_token()
        if self.lexer.token.token_type != TokenType.IDENTIFIER:
            self.error_manager.add_error(
                MissingIdentifierError(
                    self.lexer.token.position, self.lexer.token.value
                )
            )
            return None
        called_expression = self._parse_expression_call()

        return CallExpression(
            self.lexer.token.position, root_expression, called_expression, []
        )

    def _parse_simple_expression(self) -> Expression:
        """"""
        return self._parse_id_or_fun_call() or self._parse_cast_or_expression()

    # id_or_fun_call = identifier | type, ['(', [expression_list], ')'];
    def _parse_id_or_fun_call(self) -> Expression:
        """Parse identifier or function call."""
        is_type = False
        if self.lexer.token.token_type == TokenType.IDENTIFIER:
            identifier = self.lexer.token.value
        elif self.lexer.token.token_type in DECLARATION_TYPES:
            is_type = True
            identifier = self.lexer.token.value
            expression = self._parse_literal()
            if expression is not None:
                return expression
        else:
            return None

        self.lexer.next_token()

        expression_list = []
        if self.lexer.token.token_type == TokenType.START_ROUND:
            self.lexer.next_token()
            expression_list = self._parse_expression_list()
            self._check_and_consume_token(TokenType.STOP_ROUND)
            return CallExpression(
                self.lexer.token.position, None, identifier, expression_list
            )
        if is_type:
            return None
        return IdentifierExpression(self.lexer.token.position, identifier)

    # cast_or_expression = '(', ("int" | "dec") | expression, ')';
    def _parse_cast_or_expression(self) -> Expression:
        """Parse cast expression or expression."""
        if self.lexer.token.token_type != TokenType.START_ROUND:
            return None

        self.lexer.next_token()
        if self.lexer.token.token_type in [
            TokenType.INTEGER,
            TokenType.DECIMAL,
        ]:
            cast_type = DECLARATION_TYPES[self.lexer.token.token_type]
            self.lexer.next_token()
            self._check_and_consume_token(TokenType.STOP_ROUND)
            expression = self._parse_logical_expression()
            return CastExpression(
                self.lexer.token.position, cast_type, expression
            )

        expression = self._parse_logical_expression()
        self._check_and_consume_token(TokenType.STOP_ROUND)
        return expression

    # logical_expression  = or_expression
    def _parse_logical_expression(self) -> Expression:
        """Parse logical expression."""
        return self._parse_or_expression()

    # or_expression = and_expression, {or_operator, and_expression};
    def _parse_or_expression(self) -> Expression:
        """ "Parse or expression."""
        left = self._parse_and_expression()
        if left is None:
            return None

        while self.lexer.token.token_type == TokenType.OR:
            operator = self.lexer.token.value
            self.lexer.next_token()
            right = self._parse_and_expression()
            if right is None:
                self.error_manager.add_error(
                    MissingExpressionError(
                        self.lexer.token.position, self.lexer.token.value
                    )
                )
                return None
            left = OrExpression(
                self.lexer.token.position, left, operator, right
            )
        return left

    # and_expression = relative_expression,
    #                  {and_operator, relative_expression};
    def _parse_and_expression(self) -> Expression:
        """Parse and expression."""
        left = self._parse_relative_expression()
        if left is None:
            return None

        while self.lexer.token.token_type == TokenType.AND:
            operator = self.lexer.token.value
            self.lexer.next_token()
            right = self._parse_relative_expression()
            if right is None:
                self.error_manager.add_error(
                    MissingExpressionError(
                        self.lexer.token.position, self.lexer.token.value
                    )
                )
                return None
            left = AndExpression(
                self.lexer.token.position, left, operator, right
            )
        return left

    # relative_expression = sum_expression,
    #                       {relative_operator, sum_expression};
    def _parse_relative_expression(self) -> Expression:
        """Parse relative expression."""
        left = self._parse_sum_expression()
        if left is None:
            return None

        while self.lexer.token.token_type in RELATIVE_OPERATORS:
            operator = self.lexer.token.value
            self.lexer.next_token()
            right = self._parse_sum_expression()
            if right is None:
                self.error_manager.add_error(
                    MissingExpressionError(
                        self.lexer.token.position, self.lexer.token.value
                    )
                )
                return None
            left = RelativeExpression(
                self.lexer.token.position, left, operator, right
            )
        return left

    # sum_expression = mul_expression, {sum_operator, mul_expression};
    def _parse_sum_expression(self) -> Expression:
        """Parse sum expression."""
        left = self._parse_mul_expression()
        if left is None:
            return None

        while self.lexer.token.token_type in SUM_OPERATORS:
            operator = self.lexer.token.value
            self.lexer.next_token()
            right = self._parse_mul_expression()
            if right is None:
                self.error_manager.add_error(
                    MissingExpressionError(
                        self.lexer.token.position, self.lexer.token.value
                    )
                )
                return None
            left = SumExpression(
                self.lexer.token.position, left, operator, right
            )
        return left

    # mul_expression = factor, {multiply_operator, factor};
    def _parse_mul_expression(self) -> Expression:
        """Parse multiply expression."""
        left = self._parse_negated()
        if left is None:
            return None

        while self.lexer.token.token_type in MULTIPLY_OPERATORS:
            operator = self.lexer.token.value
            self.lexer.next_token()
            right = self._parse_negated()
            if right is None:
                self.error_manager.add_error(
                    MissingExpressionError(
                        self.lexer.token.position, self.lexer.token.value
                    )
                )
                return None
            left = MulExpression(
                self.lexer.token.position, left, operator, right
            )
        return left

    # factor = ["-" | "not"], {literal_expression | expression}
    def _parse_negated(self) -> Expression:
        """Parse negated expression."""
        negated = False
        if self.lexer.token.token_type in UNARY_OPERATORS:
            negated = True
            operator = self.lexer.token.value
            self.lexer.next_token()

        expression = self._parse_factor()
        if negated and expression is None:
            self.error_manager.add_error(
                MissingExpressionError(
                    self.lexer.token.position, self.lexer.token.value
                )
            )
            return None

        if negated:
            return NegatedExpression(
                self.lexer.token.position, operator, expression
            )
        return expression

    def _parse_factor(self) -> Expression:
        """Parse literal expression or expression."""
        literal_expression = self._parse_literal()
        if literal_expression is not None:
            return literal_expression

        expression = self._parse_expression()
        if expression is not None:
            return expression

        return None

    # literal_expression = integer_value | decimal_value |
    #                      string_value | bool_value
    def _parse_literal(self) -> LiteralExpression:
        """Parse literal expression."""
        if self.lexer.token.token_type == TokenType.INTEGER_VALUE:
            position = self.lexer.position
            value = self.lexer.token.value
            self.lexer.next_token()
            return IntegerExpression(position, value)
        if self.lexer.token.token_type == TokenType.DECIMAL_VALUE:
            position = self.lexer.position
            value = self.lexer.token.value
            self.lexer.next_token()
            return DecimalExpression(position, value)
        elif self.lexer.token.token_type == TokenType.STRING_VALUE:
            position = self.lexer.position
            value = self.lexer.token.value
            self.lexer.next_token()
            return StringExpression(position, value)
        elif self.lexer.token.token_type in [
            TokenType.BOOL_TRUE,
            TokenType.BOOL_FALSE,
        ]:
            position = self.lexer.position
            value = self.lexer.token.value
            self.lexer.next_token()
            return BooleanExpression(position, value)
        return None
