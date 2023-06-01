from parser.objects.function import Function

from interpreter.scope import Scope
from interpreter.variable import Variable


class Environment:
    function_scope: Scope
    local_scope: Scope
    last_scope: Scope
    recursion_depth: int

    def __init__(self) -> None:
        self.function_scope: Scope = Scope()
        self.local_scope: Scope = Scope()
        self.last_scope: Scope = Scope()
        self.recursion_depth: int = 0

    def add_function(self, function: Function) -> None:
        self.function_scope.add_variable(function)

    def has_function(self, name: str) -> bool:
        return self.function_scope.has_variable(name)

    def get_function(self, name: str) -> Variable:
        return self.function_scope.get_variable(name)

    def create_local_scope(self) -> None:
        self.local_scope = Scope(self.local_scope)

    def destroy_local_scope(self) -> None:
        self.local_scope = self.local_scope.parent_scope

    def create_function_local_scope(self, variables: list[Variable]) -> None:
        self.last_scope = self.local_scope
        self.local_scope = Scope()
        for variable in variables:
            self.local_scope.add_variable(variable)
        self.recursion_depth += 1

    def destroy_function_local_scope(self) -> None:
        self.local_scope = self.last_scope
        self.recursion_depth -= 1

    def get_recursion_depth(self) -> int:
        return self.recursion_depth

    def add_variable(self, variable: Variable) -> None:
        self.local_scope.add_variable(variable)

    def has_variable(self, name: str) -> bool:
        return self.local_scope.has_variable(name)

    def get_variable(self, name: str) -> Variable:
        return self.local_scope.get_variable(name)

    def set_type(self, name: str, type) -> None:
        self.local_scope.set_type(name, type)

    def set_value(self, name: str, value: any) -> None:
        self.local_scope.set_value(name, value)
