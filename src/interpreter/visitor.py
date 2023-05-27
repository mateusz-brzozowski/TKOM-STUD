class Visitor:
    def accept(self, node):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node):
        raise Exception("No Visit_{} method".format(type(node).__name__))
