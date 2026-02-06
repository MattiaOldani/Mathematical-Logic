from __future__ import annotations
from functools import reduce

from antlr4 import CommonTokenStream, InputStream
from PLLexer import PLLexer
from PLParser import PLParser
from PLVisitor import PLVisitor

import re


class Node:
    def __init__(self, name: str, ID: str, data: dict) -> None:
        self.name = name
        self.ID = ID
        self.data = data
        self.T = None
        self.F = None

    def set_true(self, node: Node) -> None:
        self.T = node

    def set_false(self, node: Node) -> None:
        self.F = node

    def children(self) -> tuple:
        if self.is_leaf():
            return ()

        return (self.T, self.F)

    def is_leaf(self) -> bool:
        return self.T is None and self.F is None

    def compare(self, other: Node) -> bool:
        return self.name == other.name and self.T == other.T and self.F == other.F

    def __str__(self) -> str:
        return f"[Name:{self.name}][ID:{self.ID}][Data:{self.data}]"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False

        return self.ID == other.ID

    def __hash__(self) -> int:
        return hash(self.ID)


class SteroidNode:
    def __init__(
        self, variable: str, T: SteroidNode, F: SteroidNode, value=None
    ) -> None:
        self.variable = variable
        self.T = T
        self.F = F
        self.value = value

    def is_leaf(self) -> bool:
        return self.variable is None

    def children(self) -> tuple:
        return (self.T, self.F)

    def __str__(self) -> str:
        return f"[Variable:{self.variable}][Value:{self.value}]"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SteroidNode):
            return False

        return (
            self.variable == other.variable
            and self.T == other.T
            and self.F == other.F
            and self.value == other.value
        )

    def __lt__(self, other: SteroidNode) -> bool:
        if self.variable is None:
            return False

        if other.variable is None:
            return True

        return self.variable < other.variable


class BDD:
    def __init__(self, expression: str):
        self.nodes = dict()
        self.names = dict()
        self.parents = dict()

        self.expression = expression
        self.__extract_atoms()

        atoms = self.atoms.copy()

        self.__add_root(Node(atoms[0], "", dict()))

        while atoms:
            atom = atoms.pop(0)

            nodes = self.__get_nodes_by_atom_name(atom)
            for node in nodes:
                node_data = node.data

                data = node_data.copy()
                data[atom] = True
                ID = (node.ID + " " + atom).strip()

                if len(atoms) > 0:
                    to_add = Node(atoms[0], ID, data)
                else:
                    to_add = Node(
                        "TRUE"
                        if self.__evaluate_expression(expression, data)
                        else "FALSE",
                        ID,
                        data,
                    )

                self.add_node(to_add, node, True)

                data = node_data.copy()
                data[atom] = False
                ID = (node.ID + " not(" + atom + ")").strip()

                if len(atoms) > 0:
                    to_add = Node(atoms[0], ID, data)
                else:
                    to_add = Node(
                        "TRUE"
                        if self.__evaluate_expression(expression, data)
                        else "FALSE",
                        ID,
                        data,
                    )

                self.add_node(to_add, node, False)

        assert len(self.nodes) == 2 ** (len(self.atoms) + 1) - 1
        assert len(self.names) in {len(self.atoms) + 1, len(self.atoms) + 2}
        assert len(self.parents) == 2 ** (len(self.atoms) + 1) - 2

    def __evaluate_expression(self, expression: str, truth_values: dict[str, bool]):
        items = sorted(truth_values.items(), key=lambda x: len(x[0]), reverse=True)
        for name, value in items:
            expression = expression.replace(name, str(value).upper())

        return eval(self.__grammar_2_python(expression))

    def __grammar_2_python(self, expression: str) -> str:
        return (
            expression.replace("TRUE", "True")
            .replace("FALSE", "False")
            .replace("&", "and")
            .replace("|", "or")
            .replace("NOT", "not")
        )

    def __extract_atoms(self) -> None:
        self.atoms = list(
            sorted(
                sorted(list(set(re.compile("[a-z]+").findall(self.expression)))),
                key=len,
                reverse=True,
            )
        )

    def __add_root(self, root: Node) -> None:
        self.root = root
        self.nodes[root.ID] = root
        self.names[root.name] = self.names.get(root.name, []) + [root]

    def add_node(self, node: Node, parent: Node, truth: bool) -> None:
        self.nodes[node.ID] = node
        self.names[node.name] = self.names.get(node.name, []) + [node]
        if truth:
            parent.set_true(node)
        else:
            parent.set_false(node)
        self.parents[node.ID] = self.parents.get(node.ID, []) + [parent]

    def delete_node(self, node: Node) -> None:
        del self.nodes[node.ID]

        self.names[node.name].remove(node)
        if len(self.names[node.name]) == 0:
            del self.names[node.name]

        to_remove_after = []
        for ID, parents in self.parents.items():
            if node in parents:
                parents.remove(node)
                if len(parents) == 0:
                    to_remove_after += [ID]

        assert len(to_remove_after) == 0

        if node.ID in self.parents:
            del self.parents[node.ID]

        del node

    def __get_nodes_by_atom_name(self, atom: str) -> list[Node]:
        return self.names.get(atom, []).copy()

    def __get_parents_by_node_ID(self, node_ID: str) -> list[Node]:
        return self.parents.get(node_ID, []).copy()

    def show(self) -> None:
        # print("NODI")
        # print(self.nodes, len(self.nodes))
        # print("NOMI")
        # print(self.names, len(self.names))
        # print("PARENTI")
        # print(self.parents, len(self.parents))
        # print()
        print(f"Expression: {self.expression}")
        self.__print(self.root, 0)

    def __print(self, node: Node, depth: int) -> None:
        print(f"{'  ' * depth}{node}")
        for children in node.children():
            self.__print(children, depth + 1)

    def reduce(self) -> None:
        self.__remove_leaves()
        self.root = self.__reduce(self.root)
        self.__recreate_state()

    def __remove_leaves(self) -> None:
        leaves = self.__get_nodes_by_atom_name("TRUE")
        leaves += self.__get_nodes_by_atom_name("FALSE")
        assert len(leaves) == 2 ** len(self.atoms)

        parents = set(
            reduce(
                lambda acc, nodes: acc + nodes,
                [self.__get_parents_by_node_ID(leaf.ID) for leaf in leaves],
                [],
            )
        )
        assert len(parents) == len(leaves) // 2

        TRUE = Node("TRUE", "TRUE", dict())
        FALSE = Node("FALSE", "FALSE", dict())

        self.parents["TRUE"] = []
        self.parents["FALSE"] = []

        for node in parents:
            true_node, false_node = node.children()

            if true_node.name == "TRUE":
                node.set_true(TRUE)
                self.parents["TRUE"] += [node]
            else:
                node.set_true(FALSE)
                self.parents["FALSE"] += [node]

            if false_node.name == "TRUE":
                node.set_false(TRUE)
                self.parents["TRUE"] += [node]
            else:
                node.set_false(FALSE)
                self.parents["FALSE"] += [node]

        while leaves:
            node = leaves.pop()
            self.delete_node(node)

        self.nodes["TRUE"] = TRUE
        self.nodes["FALSE"] = FALSE

        self.names["TRUE"] = [TRUE]
        self.names["FALSE"] = [FALSE]

        assert len(self.nodes) == 2 ** (len(self.atoms)) + 1
        assert len(self.names) == len(self.atoms) + 2
        assert len(self.parents) == 2 ** (len(self.atoms))

    def __reduce(self, node: Node) -> Node:
        if node.is_leaf():
            return node

        TRUE = self.__reduce(node.T)  # type: ignore
        FALSE = self.__reduce(node.F)  # type: ignore

        if TRUE == FALSE:
            self.delete_node(node)
            return TRUE

        node.set_true(TRUE)
        node.set_false(FALSE)

        return self.__node_lookup(node)

    def __node_lookup(self, other: Node) -> Node:
        for node in self.nodes.values():
            if other.compare(node):
                return node

        return other

    def __recreate_state(self) -> None:
        self.nodes = dict()
        self.names = dict()
        self.parents = dict()

        self.__navigate_tree_for_state(self.root)

    def __navigate_tree_for_state(self, node: Node) -> None:
        self.nodes[node.ID] = node

        names = self.names.get(node.name, [])
        if node not in names:
            names += [node]
        self.names[node.name] = names

        if node.is_leaf():
            return

        TRUE, FALSE = node.children()

        TRUE_parents = self.parents.get(TRUE.ID, [])
        if node not in TRUE_parents:
            TRUE_parents += [node]

        FALSE_parents = self.parents.get(FALSE.ID, [])
        if node not in FALSE_parents:
            FALSE_parents += [node]

        self.parents[TRUE.ID] = TRUE_parents
        self.parents[FALSE.ID] = FALSE_parents

        self.__navigate_tree_for_state(TRUE)
        self.__navigate_tree_for_state(FALSE)


class SteroidBDD:
    def __init__(self, expression: str) -> None:
        self.expression = expression
        self.__extract_atoms()

        TRUE = SteroidNode(None, None, None, True)  # type: ignore
        FALSE = SteroidNode(None, None, None, False)  # type: ignore

        self.TRUE = TRUE
        self.FALSE = FALSE

        self.unique = dict()
        self.computed = dict()

        builder = SteroidBDDBuilder(self)
        self.root = builder.visit(builder.context)

        self.__recreate_state()

    def apply(self, operation: str, n1: SteroidNode, n2: SteroidNode) -> SteroidNode:
        key = (operation, id(n1), id(n2))
        if key in self.computed:
            return self.computed[key]

        match [n1.is_leaf(), n2.is_leaf()]:
            case [True, True]:
                node = self.__exec_operation(operation, n1, n2)
                self.computed[key] = node
                return node
            case _:
                if n1.variable == n2.variable:
                    T = self.apply(operation, n1.T, n2.T)  # type: ignore
                    F = self.apply(operation, n1.F, n2.F)  # type: ignore
                    node = self.get_node(n1.variable, T, F)
                    self.computed[key] = node
                    return node

                first, second = sorted([n1, n2])
                T = self.apply(operation, first.T, second)  # type: ignore
                F = self.apply(operation, first.F, second)  # type: ignore
                node = self.get_node(first.variable, T, F)
                self.computed[key] = node
                return node

    def __exec_operation(
        self, operation: str, n1: SteroidNode, n2: SteroidNode
    ) -> SteroidNode:
        assert n1.is_leaf()
        assert n2.is_leaf()

        match operation:
            case "AND":
                node = self.TRUE if n1.value and n2.value else self.FALSE
            case "XOR":
                node = self.TRUE if n1.value ^ n2.value else self.FALSE  # type: ignore
            case "OR":
                node = self.TRUE if n1.value or n2.value else self.FALSE

        return node

    def variable(self, atom: str) -> SteroidNode:
        return self.get_node(atom, self.TRUE, self.FALSE)

    def get_node(self, atom: str, T: SteroidNode, F: SteroidNode) -> SteroidNode:
        if T == F:
            return T

        key = (atom, id(T), id(F))

        if key not in self.unique:
            node = SteroidNode(atom, T, F)
            self.unique[key] = node

        return self.unique[key]

    def __extract_atoms(self) -> None:
        self.atoms = list(
            sorted(
                sorted(list(set(re.compile("[a-z]+").findall(self.expression)))),
                key=len,
                reverse=True,
            )
        )

    def __recreate_state(self) -> None:
        self.nodes = dict()
        self.names = dict()
        self.parents = dict()

        self.TRUE.variable = "TRUE"
        self.FALSE.variable = "FALSE"

        self.__navigate_tree_for_state(self.root)

    def __navigate_tree_for_state(self, node: SteroidNode) -> None:
        self.nodes[id(node)] = node

        names = self.names.get(node.variable, [])
        if node not in names:
            names += [node]
        self.names[node.variable] = names

        if node.is_leaf():
            return

        T, F = node.children()

        if T is not None:
            TRUE_parents = self.parents.get(id(T), [])
            if node not in TRUE_parents:
                TRUE_parents += [node]

            self.parents[id(T)] = TRUE_parents
            self.__navigate_tree_for_state(T)

        if F is not None:
            FALSE_parents = self.parents.get(id(F), [])
            if node not in FALSE_parents:
                FALSE_parents += [node]

            self.parents[id(F)] = FALSE_parents

            self.__navigate_tree_for_state(F)

    def show(self) -> None:
        # print("NODI")
        # print(self.nodes, len(self.nodes))
        # print("NOMI")
        # print(self.names, len(self.names))
        # print("PARENTI")
        # print(self.parents, len(self.parents))
        # print()
        print(f"Expression: {self.expression}")
        if hasattr(self, "root"):
            self.__print(self.root, 0)  # type: ignore

    def __print(self, node: SteroidNode, depth: int) -> None:
        print(f"{'  ' * depth}{node}")
        for children in node.children():
            if children is None:
                continue
            self.__print(children, depth + 1)


class SteroidBDDBuilder(PLVisitor):
    def __init__(self, BDD: SteroidBDD) -> None:
        self.BDD = BDD

        self.lexer = PLLexer(InputStream(self.BDD.expression))
        self.stream = CommonTokenStream(self.lexer)
        self.parser = PLParser(self.stream)
        self.context = self.parser.start()

    def visitAtom(self, ctx):
        if ctx.ATOM():
            return self.BDD.variable(ctx.ATOM().getText())
        return self.visit(ctx.expr())

    def visitNotExpr(self, ctx):
        if ctx.getChildCount() == 4:
            child = self.visit(ctx.expr())
            return self.BDD.apply("XOR", child, self.BDD.TRUE)
        return self.visit(ctx.atom())

    def visitAndExpr(self, ctx):
        bdd = self.visit(ctx.notExpr(0))
        for i in range(1, len(ctx.notExpr())):
            bdd = self.BDD.apply("AND", bdd, self.visit(ctx.notExpr(i)))
        return bdd

    def visitXorExpr(self, ctx):
        bdd = self.visit(ctx.andExpr(0))
        for i in range(1, len(ctx.andExpr())):
            bdd = self.BDD.apply("XOR", bdd, self.visit(ctx.andExpr(i)))
        return bdd

    def visitOrExpr(self, ctx):
        bdd = self.visit(ctx.xorExpr(0))
        for i in range(1, len(ctx.xorExpr())):
            bdd = self.BDD.apply("OR", bdd, self.visit(ctx.xorExpr(i)))
        return bdd

    def visitStart(self, ctx):
        return self.visit(ctx.expr())


def main():
    expressions = [line.strip() for line in open("expression.txt", "r").readlines()]

    print("Normal BDD")
    for expression in expressions:
        bdd = BDD(expression)

        bdd.show()
        print("*" * 50)
        bdd.reduce()
        bdd.show()
        print("-" * 50)

    print()
    print("Steroid BDD")
    for expression in expressions:
        bdd = SteroidBDD(expression)

        bdd.show()
        print("-" * 50)


if __name__ == "__main__":
    main()
