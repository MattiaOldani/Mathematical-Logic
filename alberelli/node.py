from __future__ import annotations


class Node:
    def __init__(self, name: str, T: Node, F: Node, value: bool, data: dict) -> None:
        self.name = name
        self.T = T
        self.F = F
        self.value = value
        self.data = data

    def children(self) -> tuple:
        return (self.T, self.F)

    def is_leaf(self) -> bool:
        return self.T is None and self.F is None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False

        return self.name == other.name and self.T == other.T and self.F == other.F

    def __str__(self) -> str:
        return f"[Name:{self.name}][Value:{self.value}]"

    def __hash__(self) -> int:
        return id(self)
