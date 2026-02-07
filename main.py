from __future__ import annotations
from alberelli.rbdd.bdd import DummyBDD

from antlr4 import CommonTokenStream, InputStream
from PLLexer import PLLexer
from PLParser import PLParser
from PLVisitor import PLVisitor

import re


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

    for expression in expressions:
        bdd = DummyBDD(expression)

        bdd.show()
        print("*" * 50)
        bdd.reduce()
        bdd.show()
        print("-" * 50)

    for expression in expressions:
        bdd = SteroidBDD(expression)

        bdd.show()
        print("-" * 50)


if __name__ == "__main__":
    main()
