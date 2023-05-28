from parser.objects.function import Function
from interpreter.scope import Scope

class Environment:
    function_scope: Scope = Scope()
    local_scope: Scope = Scope()

    def __init__(self) -> None:
        pass

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

    def add_variable(self, variable):
        self.local_scope.add_variable(variable)