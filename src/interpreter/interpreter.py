from interpreter.visitor import Visitor
from interpreter.environment import Environment
from interpreter.variable import Variable
from parser.parser import Parser
from parser.objects.program import Program
from parser.objects.function import Function
from parser.objects.block import Block
from parser.objects.type import Type, Int, Dec
from parser.objects.statement import (
    IfStatement,
    WhileStatement,
    IterateStatement,
    ReturnStatement,
    DeclarationStatement,
    AssignmentStatement,
)
from parser.objects.expression import (
    IntegerExpression,
    DecimalExpression,
    BooleanExpression,
    StringExpression,
    LogicalExpression,
    OrExpression,
    AndExpression,
    RelativeExpression,
    SumExpression,
    MulExpression,
    NegatedExpression,
    CallExpression,
    IdentifierExpression,
    CastExpression
)
from utility.utility import LITERAL_TYPES


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
            main_call = CallExpression(main_function.position, None, main_function.name, [])
            self.visit_CallExpression(main_call)

    def visit_Function(self, function: Function):
        self.environment.add_function(function)

    def visit_IfStatement(self, if_statement: IfStatement) -> None:
        condition = self.visit(if_statement.condition)
        if condition:
            self.visit(if_statement.block)
        elif if_statement.else_block:
            self.visit(if_statement.else_block)

    def visit_WhileStatement(self, while_statement: WhileStatement) -> None:
        condition = self.visit(while_statement.condition)
        while condition:
            self.visit(while_statement.block)
            condition = self.visit(while_statement.condition)

    def visit_IterateStatement(self, iterate_statement: IterateStatement) -> None:
        pass

    def visit_ReturnStatement(self, return_statement: ReturnStatement) -> None:
        return_value = self.visit(return_statement.expression)
        raise ReturnException(return_value)

    def visit_DeclarationStatement(self, declaration_statement: DeclarationStatement) -> None:
        value = self.visit(declaration_statement.expression)

        if isinstance(value, Variable):
            value = value.value

        declaration_type = declaration_statement.type
        if declaration_type in LITERAL_TYPES:
            declaration_type = LITERAL_TYPES[declaration_type]

        if declaration_type != type(value):
            raise Exception(f"Error [{declaration_statement.position}] in declaration Expected {declaration_type} but got {type(value)}")

        self.environment.add_variable(Variable(declaration_type, declaration_statement.identifier, value))


    def visit_AssignmentStatement(self, assignment_statement: AssignmentStatement) -> None:
        new_variable: Variable = self.visit(assignment_statement.expression)
        name = assignment_statement.identifier.identifier

        if self.environment.has_variable(name):
            variable: Variable = self.environment.get_variable(name)
            if variable.type != new_variable.type:
                raise Exception(f"Error [{assignment_statement.position}] in assignment Expected {variable.type} but got {new_variable.type}")
            self.environment.set_variable(name, new_variable.value)


    def visit_CallExpression(self, call_expression: CallExpression) -> None:
        function = self.environment.get_function(call_expression.called_expression)
        return_type = type(function.declaration_type)
        if return_type in LITERAL_TYPES:
            return_type = LITERAL_TYPES[return_type]

        arguments = []
        for argument in call_expression.arguments:
            arguments.append(self.visit(argument))

        try:
            self.visit(function.block)
        except ReturnException as return_exception:
            return_value = self._get_value(return_exception.return_value)
            print(return_value)
            if type(return_value) != return_type:
                raise Exception(f"Error [{call_expression.position}] in call Expected {return_type} but got {type(return_value)}")

    def visit_IdentifierExpression(self, identifier_expression: IdentifierExpression) -> Variable:
        if self.environment.has_variable(identifier_expression.identifier):
            variable: Variable = self.environment.get_variable(identifier_expression.identifier)
            return variable
        else:
            raise Exception(f"Variable {identifier_expression.identifier} not found")

    def visit_CastExpression(self, cast_expression: CastExpression) -> None:
        variable = self._get_value(self.visit(cast_expression.expression))
        cast_type = cast_expression.cast_type
        new_value = self._get_cast_function(cast_type)(variable)
        return new_value

    def visit_Block(self, block: Block) -> None:
        self.environment.create_local_scope()
        for statement in block.statements:
            self.visit(statement)
        self.environment.destroy_local_scope()

    def visit_IntegerExpression(self, integer_expression: IntegerExpression) -> int:
        return int(integer_expression.value)

    def visit_DecimalExpression(self, decimal_expression: DecimalExpression) -> float:
        return float(decimal_expression.value)

    def visit_BooleanExpression(self, boolean_expression: BooleanExpression) -> bool:
        return bool(boolean_expression.value)

    def visit_StringExpression(self, string_expression: StringExpression) -> str:
        return str(string_expression.value)

    def visit_LogicalExpression(self, logical_expression: LogicalExpression) -> bool:
        left = self._get_value(self.visit(logical_expression.left))
        right = self._get_value(self.visit(logical_expression.right))
        operator = logical_expression.operator
        return self._get_operator_function(operator)(left, right)

    def _get_operator_function(self, operator: str):
        operator_functions = {
            'or': self.accept_or,
            'and': self.accept_and,
            '==': self.accept_equal,
            '!=': self.accept_not_equal,
            '>': self.accept_greater,
            '<': self.accept_less,
            '>=': self.accept_greater_equal,
            '<=': self.accept_less_equal,
            '+': self.accept_add,
            '-': self.accept_sub,
            '*': self.accept_mul,
            '/': self.accept_div,
        }
        return operator_functions[operator]


    def _get_value(self, variable: any) -> any:
        if isinstance(variable, Variable):
            return variable.value
        else:
            return variable

    def _get_cast_function(self, cast_type: Type):
        cast_functions = {
            Int: self.accept_int,
            Dec: self.accept_dec,
        }
        return cast_functions[cast_type]

    def visit_OrExpression(self, or_expression: OrExpression) -> bool:
        return self.visit_LogicalExpression(or_expression)

    def visit_AndExpression(self, and_expression: AndExpression) -> bool:
        return self.visit_LogicalExpression(and_expression)

    def visit_RelativeExpression(self, relative_expression: RelativeExpression) -> bool:
        return self.visit_LogicalExpression(relative_expression)

    def visit_SumExpression(self, sum_expression: SumExpression) -> any:
        return self.visit_LogicalExpression(sum_expression)

    def visit_MulExpression(self, mul_expression: MulExpression) -> any:
        return self.visit_LogicalExpression(mul_expression)

    def visit_NegatedExpression(self, negative_expression: NegatedExpression) -> any:
        value = self.visit(negative_expression.expression)
        if negative_expression.operator == "not":
            return not value
        elif negative_expression.operator == "-":
            return -value
        else:
            raise Exception(f"Unknown operator {negative_expression.operator}")

    def accept_or(self, left: any, right: any) -> bool:
        if type(left) != bool or type(right) != bool:
            raise Exception(f"Expected bool but got {type(left)} and {type(right)}")
        return left or right

    def accept_and(self, left: any, right: any) -> bool:
        if type(left) != bool or type(right) != bool:
            raise Exception(f"Expected bool but got {type(left)} and {type(right)}")
        return left and right

    def accept_equal(self, left: any, right: any) -> bool:
        return left == right

    def accept_not_equal(self, left: any, right: any) -> bool:
        return left != right

    def accept_greater(self, left: any, right: any) -> bool:
        return left > right

    def accept_less(self, left: any, right: any) -> bool:
        return left < right

    def accept_greater_equal(self, left: any, right: any) -> bool:
        return left >= right

    def accept_less_equal(self, left: any, right: any) -> bool:
        return left <= right

    def accept_add(self, left: any, right: any) -> any:
        return left + right

    def accept_sub(self, left: any, right: any) -> any:
        return left - right

    def accept_mul(self, left: any, right: any) -> any:
        return left * right

    def accept_div(self, left: any, right: any) -> any:
        return left / right

    def accept_int(self, value: any) -> int:
        return int(value)

    def accept_dec(self, value: any) -> float:
        return float(value)