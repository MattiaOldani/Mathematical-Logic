from __future__ import annotations
from alberelli.base.node import Node


class RNode(Node):
    def __init__(self, name: str, ID: str, data: dict) -> None:
        self.name = name
        self.ID = ID
        self.data = data
        self.T = None
        self.F = None

    def set_true(self, node: RNode) -> None:
        self.T = node

    def set_false(self, node: RNode) -> None:
        self.F = node

    # forse meglio in altro modo
    def children(self) -> tuple:
        if self.is_leaf():
            return ()

        return (self.T, self.F)

    def is_leaf(self) -> bool:
        return self.T is None and self.F is None

    def compare(self, other: RNode) -> bool:
        return self.name == other.name and self.T == other.T and self.F == other.F

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RNode):
            return False

        return self.ID == other.ID

    def __str__(self) -> str:
        return f"[Name:{self.name}][ID:{self.ID}]"

    def __hash__(self) -> int:
        return hash(self.ID)
