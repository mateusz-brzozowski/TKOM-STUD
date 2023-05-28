class Scope:
    variables = {}

    def __init__(self, parent_scope=None) -> None:
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