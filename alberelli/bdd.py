from __future__ import annotations

from abc import ABC, abstractmethod
from alberelli.node import Node

import graphviz


class BDD(ABC):
    @abstractmethod
    def restrict(self, atom: str, value: bool) -> None:
        pass

    @abstractmethod
    def exists(self, atom: str) -> bool:
        pass

    @abstractmethod
    def forall(self, atom: str) -> bool:
        pass

    @abstractmethod
    def show(self) -> None:
        pass

    @abstractmethod
    def _print_level(self, node: Node, depth: int) -> None:
        pass

    @abstractmethod
    def _extract_atoms(self) -> None:
        pass

    @abstractmethod
    def _recreate_state(self) -> None:
        pass

    @abstractmethod
    def _navigate_tree(self, node: Node) -> None:
        pass

    @abstractmethod
    def copy(self) -> BDD:
        pass

    @abstractmethod
    def print_in_dot(self, title: str) -> None:
        pass

    @abstractmethod
    def _navigate_for_print(
        self, node: Node, graph: graphviz.Digraph, visited: set[Node]
    ) -> None:
        pass
