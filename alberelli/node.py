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

        return (
            self.name == other.name
            and self.T == other.T
            and self.F == other.F
            and self.value == other.value
        )

    def __str__(self) -> str:
        return f"[Name:{self.name}][Value:{self.value}]"

    def __hash__(self) -> int:
        return id(self)

    def __lt__(self, other: Node) -> bool:
        if self.name is None:
            return False

        if other.name is None:
            return True

        return self.name < other.name

    def copy(self) -> Node:
        T = self.T.copy() if self.T is not None else None
        F = self.F.copy() if self.F is not None else None
        data = self.data.copy() if self.data is not None else None
        return Node(self.name, T, F, self.value, data)  # type: ignore
