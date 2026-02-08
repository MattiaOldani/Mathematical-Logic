from __future__ import annotations

from abc import ABC, abstractmethod
from alberelli.node import Node


class BDD(ABC):
    @abstractmethod
    def restrict(self, atom: str, value: bool) -> None:
        pass

    @abstractmethod
    def exists(self, atom: str, value: bool) -> bool:
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
