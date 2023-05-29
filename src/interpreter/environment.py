from parser.objects.function import Function
from interpreter.scope import Scope

class Environment:
    def __init__(self) -> None:
        self.function_scope: Scope = Scope()
        self.local_scope: Scope = Scope()
        self.last_scope: Scope = Scope()

    def add_function(self, function: Function) -> None:
        self.function_scope.add_variable(function)

    def has_function(self, name: str) -> bool:
        return self.function_scope.has_variable(name)

    def get_function(self, name: str) -> Function:
        return self.function_scope.get_variable(name)

    def create_local_scope(self):
        self.local_scope = Scope(self.local_scope)

    def destroy_local_scope(self):
        self.local_scope = self.local_scope.parent_scope

    def create_function_local_scope(self, variables):
        self.last_scope = self.local_scope
        self.local_scope = Scope()
        for variable in variables:
            self.local_scope.add_variable(variable)

    def destroy_function_local_scope(self):
        self.local_scope = self.last_scope

    def add_variable(self, variable):
        self.local_scope.add_variable(variable)

    def has_variable(self, name: str) -> bool:
        return self.local_scope.has_variable(name)

    def get_variable(self, name: str):
        return self.local_scope.get_variable(name)

    def set_variable(self, name: str, value):
        self.local_scope.set_variable(name, value)

    def set_type(self, name: str, type):
        self.local_scope.set_type(name, type)

    def set_value(self, name: str, value):
        self.local_scope.set_value(name, value)