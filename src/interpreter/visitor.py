from __future__ import annotations

from parser.objects.node import Node


class Visitor:
    def visit(self, node: Node) -> Visitor:
        method = "_visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.invalid_visit)
        return visitor(node)

    def invalid_visit(self, node: Node) -> Exception:
        raise Exception(f"No visit_{node.__class__.__name__} method defined")
