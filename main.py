import re

from collections import defaultdict


class Node:
    def __init__(self, name: str, ID: str, data: dict):
        self.name = name
        self.ID = ID
        self.data = data
        self.T = None
        self.F = None

    def set_true(self, node_ID: str):
        self.T = node_ID

    def set_false(self, node_ID: str):
        self.F = node_ID

    def children(self) -> tuple:
        if self.is_leaf():
            return ()

        return (self.T, self.F)

    def is_leaf(self) -> bool:
        return self.T is None and self.F is None

    def __str__(self) -> str:
        return f"{self.name}[{self.ID}]"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False

        return self.ID == other.ID

    def __hash__(self) -> int:
        return hash((self.name, self.ID))


class BDD:
    def __init__(self, atoms: list[str]):
        self.atoms = atoms.copy()
        self.nodes = dict()
        self.names = defaultdict(lambda: [])
        self.parents = defaultdict(lambda: [])

    def add_root(self, root: Node) -> None:
        self.root = root
        self.nodes[root.ID] = root
        self.names[root.name] += [root]

    def add_node(self, node: Node, parent: Node, truth: bool) -> None:
        self.nodes[node.ID] = node
        self.names[node.name] += [node]
        if truth:
            parent.set_true(node.ID)
        else:
            parent.set_false(node.ID)
        self.parents[node.ID] += [parent]

    def get_nodes_by_atom_name(self, atom: str) -> list[Node]:
        return self.names[atom]

    def get_parent_by_ID(self, node_ID) -> Node:
        return self.parents[node_ID][0]

    def show(self) -> None:
        self.__print(self.root, 0)

    def __print(self, node: Node, depth: int) -> None:
        print(f"{'  ' * depth}{node}")
        for children in node.children():
            self.__print(self.nodes[children], depth + 1)

    def reduce(self) -> None:
        self.__remove_leaves()

        first, second = True, True
        while first or second:
            first = self.__first_layer()
            second = self.__second_layer()

    def __remove_leaves(self) -> None:
        leaves = self.get_nodes_by_atom_name("TRUE")
        leaves += self.get_nodes_by_atom_name("FALSE")
        assert len(leaves) == 2 ** len(self.atoms)

        parents = list(set([self.get_parent_by_ID(n.ID) for n in leaves]))
        assert len(parents) == len(leaves) // 2

        self.parents["TRUE"] = []
        self.parents["FALSE"] = []

        TRUE = Node("TRUE", "TRUE", dict())
        FALSE = Node("FALSE", "FALSE", dict())

        self.names["TRUE"] = [TRUE]
        self.names["FALSE"] = [FALSE]

        for node in parents:
            true_node_ID, false_node_ID = node.children()

            if self.nodes[true_node_ID].name == "TRUE":
                node.set_true("TRUE")
                self.parents["TRUE"] += [node]
            else:
                node.set_true("FALSE")
                self.parents["FALSE"] += [node]

            if self.nodes[false_node_ID].name == "TRUE":
                node.set_false("TRUE")
                self.parents["TRUE"] += [node]
            else:
                node.set_false("FALSE")
                self.parents["FALSE"] += [node]

        for node in leaves:
            del node

        self.nodes["TRUE"] = TRUE
        self.nodes["FALSE"] = FALSE

    def __first_layer(self) -> bool:
        return False

    def __second_layer(self) -> bool:
        return False


def evaluate_expression(expression: str, truth_values: dict[str, bool]) -> bool:
    items = sorted(truth_values.items(), key=lambda x: len(x[0]), reverse=True)
    for name, value in items:
        expression = expression.replace(name, str(value).upper())

    return eval(grammar_2_python(expression))


def grammar_2_python(expression: str) -> str:
    return (
        expression.replace("TRUE", "True")
        .replace("FALSE", "False")
        .replace("&", "and")
        .replace("|", "or")
        .replace("NOT", "not")
    )


def extract_atoms(expression: str) -> list[str]:
    return sorted(
        sorted(list(set(re.compile("[a-z]+").findall(expression)))),
        key=len,
        reverse=True,
    )


def main():
    expressions = open("expression.txt", "r").readlines()

    for expression in expressions:
        atoms = extract_atoms(expression)

        bdd = BDD(atoms)

        root = Node(atoms[0], "", dict())
        bdd.add_root(root)

        while atoms:
            atom = atoms.pop(0)

            nodes = bdd.get_nodes_by_atom_name(atom)
            for node in nodes:
                node_data = node.data

                data = node_data.copy()
                data[atom] = True
                data["added_atom"] = atom
                ID = (node.ID + " " + atom).strip()

                if len(atoms) > 0:
                    to_add = Node(atoms[0], ID, data)
                else:
                    to_add = Node(
                        "TRUE" if evaluate_expression(expression, data) else "FALSE",
                        ID,
                        data,
                    )

                bdd.add_node(to_add, node, True)

                data = node_data.copy()
                data[atom] = False
                data["added_atom"] = atom
                ID = (node.ID + " not(" + atom + ")").strip()

                if len(atoms) > 0:
                    to_add = Node(atoms[0], ID, data)
                else:
                    to_add = Node(
                        "TRUE" if evaluate_expression(expression, data) else "FALSE",
                        ID,
                        data,
                    )

                bdd.add_node(to_add, node, False)

        bdd.show()
        print("*" * 50)
        bdd.reduce()
        bdd.show()
        print("-" * 50)


if __name__ == "__main__":
    main()
