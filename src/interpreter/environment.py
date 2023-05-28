from parser.objects.function import Function
from interpreter.scope import Scope

class Environment:
    global_scope: Scope = Scope()

    def __init__(self) -> None:
        pass

    def add_function(self, function: Function) -> None:
        self.global_scope.add_variable(function)

    def has_function(self, name: str) -> bool:
        return self.global_scope.has_variable(name)

    def get_function(self, name: str) -> Function:
        return self.global_scope.get_variable(name)