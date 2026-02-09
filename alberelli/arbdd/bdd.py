from __future__ import annotations

from alberelli.bdd import BDD
from alberelli.node import Node

import re


class ParsedSteroidBDD(BDD):
    def __init__(self, expression: str) -> None:
        from alberelli.builder.builder import Builder

        self.expression = expression
        self._extract_atoms()

        TRUE = Node(None, None, None, True, None)  # type: ignore
        FALSE = Node(None, None, None, False, None)  # type: ignore

        self.TRUE = TRUE
        self.FALSE = FALSE

        self.unique = dict()
        self.computed = dict()
        self.is_reduced = False

        builder = Builder(self)
        self.root = builder.create_tree()
        self.is_reduced = True

        self._recreate_state()

    def apply(self, operation: str, n1: Node, n2: Node) -> Node:
        if self.is_reduced:
            return self.root

        key = (operation, id(n1), id(n2))
        if key in self.computed:
            return self.computed[key]

        if n1.is_leaf() and n2.is_leaf():
            node = self._exec_operation(operation, n1, n2)
            self.computed[key] = node
            return node

        if n1.name == n2.name:
            T = self.apply(operation, n1.T, n2.T)
            F = self.apply(operation, n1.F, n2.F)
            node = self._node_lookup(n1.name, T, F)
            self.computed[key] = node
            return node

        first, second = sorted([n1, n2])
        T = self.apply(operation, first.T, second)
        F = self.apply(operation, first.F, second)
        node = self._node_lookup(first.name, T, F)
        self.computed[key] = node
        return node

    def restrict(self, atom: str, value: bool) -> None:
        self.root = self._restrict(self.root, atom, value)
        self._recreate_state()

    def _restrict(self, node: Node, atom: str, value: bool) -> Node:
        if node.is_leaf():
            return node

        if node.name == atom:
            return node.T if value else node.F

        T = self._restrict(node.T, atom, value)
        F = self._restrict(node.F, atom, value)

        return self._node_lookup(node.name, T, F)

    def exists(self, atom: str, value: bool) -> bool:
        root = self.copy()
        root.is_reduced = False

        T = self.copy()
        F = self.copy()

        T.restrict(atom, value)
        F.restrict(atom, not value)

        T.TRUE.name = None  # type: ignore
        T.FALSE.name = None  # type: ignore
        F.TRUE.name = None  # type: ignore
        F.FALSE.name = None  # type: ignore

        root.apply("OR", T.root, F.root)

        return root._has_true_leaf()

    def _has_true_leaf(self) -> bool:
        return id(self.TRUE) in self.nodes

    def forall(self, atom: str) -> bool:
        root = self.copy()
        root.is_reduced = False

        T = self.copy()
        F = self.copy()

        T.restrict(atom, True)
        F.restrict(atom, False)

        T.TRUE.name = None  # type: ignore
        T.FALSE.name = None  # type: ignore
        F.TRUE.name = None  # type: ignore
        F.FALSE.name = None  # type: ignore

        root.apply("AND", T.root, F.root)

        return root._has_no_false_leaf()

    def _has_no_false_leaf(self) -> bool:
        return id(self.FALSE) not in self.nodes

    def variable(self, atom: str) -> Node:
        return self._node_lookup(atom, self.TRUE, self.FALSE)

    def _exec_operation(self, operation: str, n1: Node, n2: Node) -> Node:
        assert n1.is_leaf()
        assert n2.is_leaf()

        match operation:
            case "AND":
                node = self.TRUE if n1.value and n2.value else self.FALSE
            case "XOR":
                node = self.TRUE if n1.value ^ n2.value else self.FALSE
            case "OR":
                node = self.TRUE if n1.value or n2.value else self.FALSE

        return node

    def show(self) -> None:
        print(f"Expression: {self.expression}")
        self._print_level(self.root, 0)

    def _print_level(self, node: Node, depth: int) -> None:
        print(f"{'  ' * depth}{node}")
        for children in node.children():
            if children is None:
                continue
            self._print_level(children, depth + 1)

    def _extract_atoms(self) -> None:
        self.atoms = list(sorted(set(re.compile("[a-z]+").findall(self.expression))))

    def _node_lookup(self, atom: str, T: Node, F: Node) -> Node:
        if T == F:
            return T

        key = (atom, id(T), id(F))

        if key not in self.unique:
            node = Node(atom, T, F, None, None)  # type: ignore
            self.unique[key] = node

        return self.unique[key]

    def _recreate_state(self) -> None:
        self.nodes = dict()
        self.parents = dict()

        self.TRUE.name = "TRUE"
        self.FALSE.name = "FALSE"

        self._navigate_tree(self.root)

    def _navigate_tree(self, node: Node) -> None:
        self.nodes[id(node)] = node

        if node.is_leaf():
            return

        T, F = node.children()

        if T is not None:
            TRUE_parents = self.parents.get(id(T), [])
            if node not in TRUE_parents:
                TRUE_parents += [node]

            self.parents[id(T)] = TRUE_parents
            self._navigate_tree(T)

        if F is not None:
            FALSE_parents = self.parents.get(id(F), [])
            if node not in FALSE_parents:
                FALSE_parents += [node]

            self.parents[id(F)] = FALSE_parents

            self._navigate_tree(F)

    def copy(self) -> ParsedSteroidBDD:
        bdd = ParsedSteroidBDD(self.expression)
        bdd.root = self.root.copy()

        bdd.TRUE = Node(None, None, None, True, None)  # type: ignore
        bdd.FALSE = Node(None, None, None, False, None)  # type: ignore

        bdd.atoms = self.atoms.copy()
        bdd.root = bdd._search_TF(bdd.root)
        bdd._recreate_state()

        return bdd

    def _search_TF(self, node: Node) -> Node:
        if node.name == "TRUE":
            return self.TRUE

        if node.name == "FALSE":
            return self.FALSE

        node.T = self._search_TF(node.T)
        node.F = self._search_TF(node.F)
        return node


class InteractiveSteroidBDD(BDD):
    def __init__(self) -> None:
        self.root = None

        TRUE = Node(None, None, None, True, None)  # type: ignore
        FALSE = Node(None, None, None, False, None)  # type: ignore

        self.TRUE = TRUE
        self.FALSE = FALSE

        self.unique = dict()
        self.computed = dict()

    def apply(self, operation: str, n1: Node, n2: Node = None) -> Node:  # type: ignore
        if n2 is None:
            n2 = self.TRUE

        self.TRUE.name = None  # type: ignore
        self.FALSE.name = None  # type: ignore
        self.root = self._apply(operation, n1, n2)
        self._recreate_state()
        return self.root

    def _apply(self, operation: str, n1: Node, n2: Node) -> Node:
        key = (operation, id(n1), id(n2))
        if key in self.computed:
            return self.computed[key]

        if n1.is_leaf() and n2.is_leaf():
            node = self._exec_operation(operation, n1, n2)
            self.computed[key] = node
            return node

        if n1.name == n2.name:
            T = self.apply(operation, n1.T, n2.T)
            F = self.apply(operation, n1.F, n2.F)
            node = self._node_lookup(n1.name, T, F)
            self.computed[key] = node
            return node

        first, second = sorted([n1, n2])
        T = self.apply(operation, first.T, second)
        F = self.apply(operation, first.F, second)
        node = self._node_lookup(first.name, T, F)
        self.computed[key] = node
        return node

    def _exec_operation(self, operation: str, n1: Node, n2: Node) -> Node:
        assert n1.is_leaf()
        assert n2.is_leaf()

        match operation:
            case "AND":
                node = self.TRUE if n1.value and n2.value else self.FALSE
            case "XOR":
                node = self.TRUE if n1.value ^ n2.value else self.FALSE
            case "OR":
                node = self.TRUE if n1.value or n2.value else self.FALSE
            case "NOT":
                node = self.TRUE if not n1.value else self.FALSE

        return node

    def restrict(self, atom: str, value: bool) -> None:
        self.root = self._restrict(self.root, atom, value)  # type: ignore

    def _restrict(self, node: Node, atom: str, value: bool) -> Node:
        if node.is_leaf():
            return node

        if node.name == atom:
            return node.T if value else node.F

        T = self._restrict(node.T, atom, value)
        F = self._restrict(node.F, atom, value)

        return self._node_lookup(node.name, T, F)

    def exists(self, atom: str, value: bool) -> bool:
        root = self.copy()
        T = self.copy()
        F = self.copy()

        T.restrict(atom, value)
        F.restrict(atom, not value)

        root.apply("OR", T.root, F.root)  # type: ignore

        return root._has_true_leaf()

    def _has_true_leaf(self) -> bool:
        return id(self.TRUE) in self.nodes

    def forall(self, atom: str) -> bool:
        root = self.copy()
        T = self.copy()
        F = self.copy()

        T.restrict(atom, True)
        F.restrict(atom, False)

        root.apply("AND", T.root, F.root)  # type: ignore

        return root._has_no_false_leaf()

    def _has_no_false_leaf(self) -> bool:
        return id(self.FALSE) not in self.nodes

    def variable(self, atom: str) -> Node:
        return self._node_lookup(atom, self.TRUE, self.FALSE)

    def _node_lookup(self, atom: str, T: Node, F: Node) -> Node:
        if T == F:
            return T

        key = (atom, id(T), id(F))

        if key not in self.unique:
            node = Node(atom, T, F, None, None)  # type: ignore
            self.unique[key] = node

        return self.unique[key]

    def _extract_atoms(self) -> None:
        pass

    def _recreate_state(self) -> None:
        self.nodes = dict()
        self.parents = dict()

        self.TRUE.name = "TRUE"
        self.FALSE.name = "FALSE"

        self._navigate_tree(self.root)  # type: ignore

    def _navigate_tree(self, node: Node) -> None:
        self.nodes[id(node)] = node

        if node.is_leaf():
            return

        T, F = node.children()

        if T is not None:
            TRUE_parents = self.parents.get(id(T), [])
            if node not in TRUE_parents:
                TRUE_parents += [node]

            self.parents[id(T)] = TRUE_parents
            self._navigate_tree(T)

        if F is not None:
            FALSE_parents = self.parents.get(id(F), [])
            if node not in FALSE_parents:
                FALSE_parents += [node]

            self.parents[id(F)] = FALSE_parents

            self._navigate_tree(F)

    def show(self) -> None:
        if self.root is None:
            print("Albero senza nodi")
            return

        self._print_level(self.root, 0)

    def _print_level(self, node: Node, depth: int) -> None:
        print(f"{'  ' * depth}{node}")
        for children in node.children():
            if children is None:
                continue
            self._print_level(children, depth + 1)

    def copy(self) -> InteractiveSteroidBDD:
        bdd = InteractiveSteroidBDD()
        if self.root is not None:
            bdd.root = self.root.copy()
        bdd._recreate_state()

        return bdd
