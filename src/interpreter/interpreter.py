from interpreter.visitor import Visitor
from interpreter.environment import Environment
from parser.parser import Parser
from parser.objects.program import Program
from parser.objects.function import Function
from parser.objects.block import Block
from parser.objects.statement import (
    IfStatement,
    ReturnStatement
)
from parser.objects.expression import (
    CallExpression
)


class ReturnException(Exception):
    def __init__(self, return_value) -> None:
        self.return_value = return_value


class Interpreter(Visitor):
    praser: Parser
    environment: Environment

    def __init__(self, parser: Parser) -> None:
        self.parser = parser

    def interpret(self):
        tree = self.parser.parse_program()
        print(tree)
        self.environment = Environment()
        self.visit(tree)

    def visit_Program(self, program: Program):
        for object in program.objects:
            self.visit(object)

        if self.environment.has_function('main'):
            main_function = self.environment.get_function('main')
            main_call = CallExpression(main_function.position, main_function.name, [])
            self.visit_CallExpression(main_call)

    def visit_Function(self, function: Function):
        self.environment.add_function(function)

    def visit_IfStatement(self, if_statement: IfStatement) -> None:
        pass

    def visit_ReturnStatement(self, return_statement: ReturnStatement) -> None:
        return_value = self.visit(return_statement.expression)
        raise ReturnException(return_value)

    def visit_CallExpression(self, call_expression: CallExpression) -> None:
        function = self.environment.get_function(call_expression.identifier)

        arguments = []
        for argument in call_expression.expressions:
            arguments.append(self.visit(argument))

        self.visit(function.block)

    def visit_Block(self, block: Block) -> None:
        for statement in block.statements:
            self.visit(statement)