from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def children(self) -> tuple:
        pass

    @abstractmethod
    def is_leaf(self) -> bool:
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
