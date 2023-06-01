from inspect import signature
from parser.objects.block import Block
from parser.objects.expression import (AndExpression, BooleanExpression,
                                       CallExpression, CastExpression,
                                       DecimalExpression, Expression,
                                       IdentifierExpression, IntegerExpression,
                                       LogicalExpression, MulExpression,
                                       NegatedExpression, OrExpression,
                                       RelativeExpression, StringExpression,
                                       SumExpression)
from parser.objects.function import Function
from parser.objects.program import Program
from parser.objects.statement import (AssignmentStatement,
                                      DeclarationStatement, IfStatement,
                                      IterateStatement, ReturnStatement,
                                      WhileStatement)
from parser.objects.type import Canvas, Dec, Int, Shape, Type
from parser.parser import Parser

from error.error_interpreter import (DivisionByZeroError,
                                     InvalidAssignmentTypeError,
                                     InvalidDeclarationTypeError,
                                     InvalidIterableTypeError,
                                     InvalidReturnTypeError,
                                     InvalidUnaryOperatorError,
                                     MaximumRecursionDepthError,
                                     MismatchedTypeError,
                                     MissingAssignmentValueError,
                                     MissingDeclarationValueError,
                                     MissingForConditionError,
                                     MissingFunctionDeclarationError,
                                     MissingIfConditionError,
                                     MissingMainFunctionError,
                                     MissingReturnTypeError,
                                     MissingReturnValueError,
                                     MissingVariableDeclarationError,
                                     MissingWhileConditionError,
                                     NumberOfArgumentError, RedeclarationError)
from interpreter.environment import Environment
from interpreter.variable import Variable
from interpreter.visitor import Visitor
from lexer.token_manager import TokenType
from utility.utility import (LITERAL_TYPES, MAX_REC_DEPTH, OBJECT_TYPES,
                             Position)


class Interpreter(Visitor):
    praser: Parser
    environment: Environment
    return_value: Type
    is_return: bool
    max_rec_depth: int

    def __init__(
        self, parser: Parser, max_rec_depth: int = MAX_REC_DEPTH
    ) -> None:
        self.parser = parser
        self.return_value = None
        self.is_return = False
        self.max_rec_depth = max_rec_depth

    def interpret(self):
        tree = self.parser.parse_program()
        self.environment = Environment()
        self.visit(tree)

    def _visit_Program(self, program: Program):
        for object in program.objects:
            self.visit(object)

        if self.environment.has_function("main"):
            main_function = self.environment.get_function("main")
            main_call = CallExpression(
                main_function.position, None, main_function.name, []
            )
            self._visit_CallExpression(main_call)
        else:
            raise MissingMainFunctionError(Position(0, 0))

    def _visit_Function(self, function: Function):
        self.environment.add_function(function)

    def _visit_IfStatement(self, if_statement: IfStatement) -> None:
        if self.is_return:
            return
        if if_statement.condition is None:
            raise MissingIfConditionError(if_statement.position)
        condition = self.visit(if_statement.condition)
        if condition:
            self.visit(if_statement.block)
        elif if_statement.else_block:
            self.visit(if_statement.else_block)

    def _visit_WhileStatement(self, while_statement: WhileStatement) -> None:
        if self.is_return:
            return
        if while_statement.condition is None:
            raise MissingWhileConditionError(while_statement.position)
        condition = self.visit(while_statement.condition)
        while condition:
            self.visit(while_statement.block)
            condition = self.visit(while_statement.condition)

    def _visit_IterateStatement(
        self, iterate_statement: IterateStatement
    ) -> None:
        if self.is_return:
            return
        if iterate_statement.expression is None:
            raise MissingForConditionError(iterate_statement.position)
        if iterate_statement.type != Shape:
            raise InvalidIterableTypeError(
                iterate_statement.position, iterate_statement.type, Shape
            )
        value = self._get_value(self.visit(iterate_statement.expression))
        if type(value) != Canvas:
            raise InvalidIterableTypeError(
                iterate_statement.position, type(value), Canvas
            )
        shapes = getattr(value, "shapes")
        self.environment.create_local_scope()
        self.environment.add_variable(
            Variable(
                iterate_statement.type, iterate_statement.identifier, None
            )
        )
        for shape in shapes:
            self.environment.set_value(iterate_statement.identifier, shape)
            self.visit(iterate_statement.block)
        self.environment.destroy_local_scope()

    def _visit_ReturnStatement(
        self, return_statement: ReturnStatement
    ) -> None:
        if return_statement.expression is None:
            raise MissingReturnValueError(return_statement.position)
        self.return_value = self.visit(return_statement.expression)
        self.is_return = True

    def _visit_DeclarationStatement(
        self, declaration_statement: DeclarationStatement
    ) -> None:
        if self.is_return:
            return
        if declaration_statement.expression is None:
            raise MissingDeclarationValueError(declaration_statement.position)

        value = self.visit(declaration_statement.expression)

        if isinstance(value, Variable):
            value = value.value

        declaration_type = declaration_statement.type
        if declaration_type in LITERAL_TYPES:
            declaration_type = LITERAL_TYPES[declaration_type]

        if value is None:
            raise InvalidDeclarationTypeError(
                declaration_statement.position, None, declaration_type
            )
        elif type(value) == tuple:
            raise MissingFunctionDeclarationError(
                declaration_statement.position, value[0]
            )
        elif declaration_type != type(value):
            raise InvalidDeclarationTypeError(
                declaration_statement.position, type(value), declaration_type
            )

        if self.environment.has_variable(declaration_statement.identifier):
            raise RedeclarationError(
                declaration_statement.position,
                declaration_statement.identifier,
            )

        self.environment.add_variable(
            Variable(declaration_type, declaration_statement.identifier, value)
        )

    def _visit_AssignmentStatement(
        self, assignment_statement: AssignmentStatement
    ) -> None:
        if self.is_return:
            return
        if assignment_statement.expression is None:
            raise MissingAssignmentValueError(assignment_statement.position)
        value = self._get_value(self.visit(assignment_statement.expression))
        name = assignment_statement.identifier.identifier

        if self.environment.has_variable(name):
            variable: Variable = self.environment.get_variable(name)
            if variable.type != type(value):
                raise InvalidAssignmentTypeError(
                    assignment_statement.position, type(value), variable.type
                )
            self.environment.set_value(name, value)
        else:
            raise MissingVariableDeclarationError(
                assignment_statement.position, name
            )

    def _visit_FunctionCall(self, function_call: CallExpression) -> None:
        name = function_call.called_expression
        function = self.environment.get_function(name)

        return_type = function.declaration_type
        if return_type in LITERAL_TYPES:
            return_type = LITERAL_TYPES[return_type]

        if len(function_call.arguments) != len(function.argument_list):
            raise NumberOfArgumentError(
                function_call.position,
                function.name,
                function_call.arguments,
                function.argument_list,
            )

        variables = []
        for argument, parameter in zip(
            function_call.arguments, function.argument_list
        ):
            value = self._get_value(self.visit(argument))
            variables.append(Variable(parameter[0], parameter[1], value))

        self.environment.create_function_local_scope(variables)

        if self.environment.get_recursion_depth() > self.max_rec_depth:
            raise MaximumRecursionDepthError(
                function_call.position, self.max_rec_depth, name
            )

        return_value = None
        self.visit(function.block)

        return_value = self._get_value(self.return_value)
        self.is_return = False
        if return_value is None and return_type is not None:
            raise MissingReturnTypeError(function_call.position, return_type)
        elif (
            type(return_value) != return_type
            and return_type is not None
            and return_value is not None
        ):
            raise InvalidReturnTypeError(
                function_call.position, type(return_value), return_type
            )

        self.environment.destroy_function_local_scope()
        return return_value

    def _visit_MethodCall(self, method_call: CallExpression) -> None:
        name = method_call.called_expression
        if name == "print":
            return self._execute_print(method_call.arguments)
        elif name in OBJECT_TYPES:
            return self._create_object(
                OBJECT_TYPES[name], method_call.arguments, method_call
            )
        return (method_call.called_expression, method_call.arguments)

    def _visit_VariableCall(self, variable_call: CallExpression) -> None:
        root = self._get_value(self.visit(variable_call.root_expression))
        name, arguments = self.visit(variable_call.called_expression)
        function = getattr(root, name, self._not_existing_function)
        if function == self._not_existing_function:
            raise MissingFunctionDeclarationError(variable_call.position, name)
        argument_values = [
            self._get_value(self.visit(argument)) for argument in arguments
        ]
        return function(*argument_values)

    def _not_existing_function(self, name) -> Exception:
        raise Exception(f"Function {name} not found")

    def _visit_CallExpression(self, call_expression: CallExpression) -> any:
        if self.is_return:
            return
        if call_expression.root_expression is None:
            name = call_expression.called_expression
            if self.environment.has_function(name):
                return self._visit_FunctionCall(call_expression)
            else:
                return self._visit_MethodCall(call_expression)
        else:
            return self._visit_VariableCall(call_expression)

    def _visit_IdentifierExpression(
        self, identifier_expression: IdentifierExpression
    ) -> Variable:
        if self.environment.has_variable(identifier_expression.identifier):
            variable: Variable = self.environment.get_variable(
                identifier_expression.identifier
            )
            return variable
        else:
            raise MissingVariableDeclarationError(
                identifier_expression.position,
                identifier_expression.identifier,
            )

    def _visit_CastExpression(self, cast_expression: CastExpression) -> any:
        variable = self._get_value(self.visit(cast_expression.expression))
        cast_type = cast_expression.cast_type
        new_value = self._get_cast_function(cast_type)(variable)
        return new_value

    def _visit_Block(self, block: Block) -> None:
        self.environment.create_local_scope()
        for statement in block.statements:
            self.visit(statement)
        self.environment.destroy_local_scope()

    def _visit_IntegerExpression(
        self, integer_expression: IntegerExpression
    ) -> int:
        return int(integer_expression.value)

    def _visit_DecimalExpression(
        self, decimal_expression: DecimalExpression
    ) -> float:
        return float(decimal_expression.value)

    def _visit_BooleanExpression(
        self, boolean_expression: BooleanExpression
    ) -> bool:
        return bool(boolean_expression.value)

    def _visit_StringExpression(
        self, string_expression: StringExpression
    ) -> str:
        return str(string_expression.value)

    def _visit_LogicalExpression(
        self, logical_expression: LogicalExpression
    ) -> bool:
        left = self._get_value(self.visit(logical_expression.left))
        right = self._get_value(self.visit(logical_expression.right))
        operator = logical_expression.operator
        if type(left) != type(right):
            raise MismatchedTypeError(
                logical_expression.position, type(left), type(right), operator
            )
        return self._get_operator_function(operator)(
            left, right, logical_expression
        )

    def _execute_print(self, expressions: list) -> None:
        output = ""
        for expression in expressions:
            output += str(self._get_value(self.visit(expression)))
        print(output)

    def _create_object(
        self, object_type: Type, arguments: list, expression: Expression
    ) -> any:
        argument_values = [
            self._get_value(self.visit(argument)) for argument in arguments
        ]
        if len(argument_values) != len(signature(object_type).parameters):
            raise NumberOfArgumentError(
                expression.position,
                object_type.__name__,
                argument_values,
                signature(object_type).parameters,
            )
        return object_type(*argument_values)

    def _get_operator_function(self, operator: str):
        operator_functions = {
            TokenType.OR.value: self._accept_or,
            TokenType.AND.value: self._accept_and,
            TokenType.EQUAL.value: self._accept_equal,
            TokenType.NOT_EQUAL.value: self._accept_not_equal,
            TokenType.GREATER.value: self._accept_greater,
            TokenType.LESS.value: self._accept_less,
            TokenType.GREATER_EQUAL.value: self._accept_greater_equal,
            TokenType.LESS_EQUAL.value: self._accept_less_equal,
            TokenType.ADD.value: self._accept_add,
            TokenType.SUBTRACT.value: self._accept_sub,
            TokenType.MULTIPLY.value: self._accept_mul,
            TokenType.DIVIDE.value: self._accept_div,
        }
        return operator_functions[operator]

    def _get_value(self, variable: any) -> any:
        if isinstance(variable, Variable):
            return variable.value
        else:
            return variable

    def _get_cast_function(self, cast_type: Type):
        cast_functions = {
            Int: self._accept_int,
            Dec: self._accept_dec,
        }
        return cast_functions[cast_type]

    def _visit_OrExpression(self, or_expression: OrExpression) -> bool:
        return self._visit_LogicalExpression(or_expression)

    def _visit_AndExpression(self, and_expression: AndExpression) -> bool:
        return self._visit_LogicalExpression(and_expression)

    def _visit_RelativeExpression(
        self, relative_expression: RelativeExpression
    ) -> bool:
        return self._visit_LogicalExpression(relative_expression)

    def _visit_SumExpression(self, sum_expression: SumExpression) -> any:
        return self._visit_LogicalExpression(sum_expression)

    def _visit_MulExpression(self, mul_expression: MulExpression) -> any:
        return self._visit_LogicalExpression(mul_expression)

    def _visit_NegatedExpression(
        self, negative_expression: NegatedExpression
    ) -> any:
        value = self._get_value(self.visit(negative_expression.expression))
        if negative_expression.operator == "not":
            if type(value) == bool:
                return not value
        elif negative_expression.operator == "-":
            if type(value) in [int, float]:
                return -value
        raise InvalidUnaryOperatorError(
            negative_expression.position, negative_expression.operator
        )

    def _accept_or(
        self, left: any, right: any, expression: Expression
    ) -> bool:
        return left or right

    def _accept_and(
        self, left: any, right: any, expression: Expression
    ) -> bool:
        return left and right

    def _accept_equal(
        self, left: any, right: any, expression: Expression
    ) -> bool:
        return left == right

    def _accept_not_equal(
        self, left: any, right: any, expression: Expression
    ) -> bool:
        return left != right

    def _accept_greater(
        self, left: any, right: any, expression: Expression
    ) -> bool:
        return left > right

    def _accept_less(
        self, left: any, right: any, expression: Expression
    ) -> bool:
        return left < right

    def _accept_greater_equal(
        self, left: any, right: any, expression: Expression
    ) -> bool:
        return left >= right

    def _accept_less_equal(
        self, left: any, right: any, expression: Expression
    ) -> bool:
        return left <= right

    def _accept_add(
        self, left: any, right: any, expression: Expression
    ) -> any:
        return left + right

    def _accept_sub(
        self, left: any, right: any, expression: Expression
    ) -> any:
        return left - right

    def _accept_mul(
        self, left: any, right: any, expression: Expression
    ) -> any:
        return left * right

    def _accept_div(
        self, left: any, right: any, expression: Expression
    ) -> any:
        if right == 0:
            raise DivisionByZeroError(expression.position)
        return left / right

    def _accept_int(self, value: float) -> int:
        return int(value)

    def _accept_dec(self, value: int) -> float:
        return float(value)
