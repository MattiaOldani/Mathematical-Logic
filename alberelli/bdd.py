from abc import ABC, abstractmethod
from alberelli.node import Node


class BDD(ABC):
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
