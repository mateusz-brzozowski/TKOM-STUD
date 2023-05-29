from interpreter.variable import Variable

class Scope:
    variables: dict[Variable]

    def __init__(self, parent_scope=None) -> None:
        self.variables = {}
        self.parent_scope = parent_scope

    def add_variable(self, variable):
        if not self._find_variable(variable):
            self.variables[variable.get_name()] = variable

    def _find_variable(self, variable) -> bool:
        return variable in self.variables

    def has_variable(self, name) -> bool:
        if self._find_variable(name):
            return True
        elif self.parent_scope:
            return self.parent_scope.has_variable(name)
        else:
            return False

    def get_variable(self, name):
        if self._find_variable(name):
            return self.variables[name]
        elif self.parent_scope:
            return self.parent_scope.get_variable(name)
        else:
            return None

    def set_variable(self, name, value):
        if self._find_variable(name):
            self.variables[name].set_value(value)
        elif self.parent_scope:
            self.parent_scope.set_variable(name, value)
        else:
            raise Exception(f"Variable {name} not found")

    def set_type(self, name, type):
        if self._find_variable(name):
            self.variables[name].set_type(type)
        elif self.parent_scope:
            self.parent_scope.set_type(name, type)
        else:
            raise Exception(f"Variable {name} not found")

    def set_value(self, name, value):
        if self._find_variable(name):
            self.variables[name].set_value(value)
        elif self.parent_scope:
            self.parent_scope.set_value(name, value)
        else:
            raise Exception(f"Variable {name} not found")