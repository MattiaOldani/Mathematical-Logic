from alberelli.bdd import BDD
from alberelli.node import Node

from functools import reduce
import re


class DummyBDD(BDD):
    def __init__(self, expression: str) -> None:
        self.nodes = dict()
        self.names = dict()
        self.lookup = dict()
        self.parents = dict()
        self.is_reduced = False

        self.expression = expression
        self._extract_atoms()

        atoms = self.atoms.copy()

        self._add_root(Node(atoms[0], None, None, None, dict()))  # type: ignore

        while atoms:
            atom = atoms.pop(0)

            nodes = self._get_nodes_by_atom_name(atom)
            for node in nodes:
                node_data = node.data

                for value in [True, False]:
                    data = node_data.copy()
                    data[atom] = value

                    if len(atoms) > 0:
                        to_add = Node(atoms[0], None, None, None, data)  # type: ignore
                    else:
                        truth = self._evaluate_expression(expression, data)
                        name = "TRUE" if truth else "FALSE"
                        to_add = Node(name, None, None, truth, data)  # type: ignore

                    self._add_node(to_add, node, value)

        assert len(self.nodes) == 2 ** (len(self.atoms) + 1) - 1
        assert len(self.names) in {len(self.atoms) + 1, len(self.atoms) + 2}
        assert len(self.parents) == 2 ** (len(self.atoms) + 1) - 2

    def show(self) -> None:
        print(f"Expression: {self.expression}")
        self._print_level(self.root, 0)

    def _print_level(self, node: Node, depth: int) -> None:
        print(f"{'  ' * depth}{node}")
        for children in node.children():
            if children is None:
                continue
            self._print_level(children, depth + 1)

    def reduce(self) -> None:
        if self.is_reduced:
            return

        self._remove_leaves()
        self.root = self._reduce(self.root)
        self._recreate_state()
        self.is_reduced = True

    def _add_node(self, node: Node, parent: Node, truth: bool) -> None:
        self.nodes[id(node)] = node
        self.names[node.name] = self.names.get(node.name, []) + [node]
        if truth:
            parent.T = node
        else:
            parent.F = node
        self.parents[id(node)] = self.parents.get(id(node), []) + [parent]

    def _delete_node(self, node: Node) -> None:
        del self.nodes[id(node)]

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

        if id(node) in self.parents:
            del self.parents[id(node)]

        del node

    def _extract_atoms(self) -> None:
        self.atoms = list(sorted(set(re.compile("[a-z]+").findall(self.expression))))

    def _grammar_2_python(self, expression: str) -> str:
        return (
            expression.replace("TRUE", "True")
            .replace("FALSE", "False")
            .replace("&", "and")
            .replace("|", "or")
            .replace("NOT", "not")
        )

    def _evaluate_expression(self, expression: str, truth_values: dict[str, bool]):
        items = sorted(truth_values.items(), key=lambda x: len(x[0]), reverse=True)
        for name, value in items:
            expression = expression.replace(name, str(value).upper())

        return eval(self._grammar_2_python(expression))

    def _add_root(self, root: Node) -> None:
        self.root = root
        self.nodes[id(root)] = root
        self.names[root.name] = self.names.get(root.name, []) + [root]

    def _get_nodes_by_atom_name(self, atom: str) -> list[Node]:
        return self.names.get(atom, []).copy()

    def _get_parents_by_node_ID(self, ID: int) -> list[Node]:
        return self.parents.get(ID, []).copy()

    def _remove_leaves(self) -> None:
        leaves = self._get_nodes_by_atom_name("TRUE")
        leaves += self._get_nodes_by_atom_name("FALSE")
        assert len(leaves) == 2 ** len(self.atoms)

        parents = set(
            reduce(
                lambda acc, nodes: acc + nodes,
                [self._get_parents_by_node_ID(id(leaf)) for leaf in leaves],
                [],
            )
        )
        assert len(parents) == len(leaves) // 2

        TRUE = Node("TRUE", None, None, True, dict())  # type: ignore
        FALSE = Node("FALSE", None, None, False, dict())  # type: ignore

        TRUE_ID = id(TRUE)
        FALSE_ID = id(FALSE)

        self.parents[TRUE_ID] = []
        self.parents[FALSE_ID] = []

        for node in parents:
            true_node, false_node = node.children()

            if true_node.name == "TRUE":
                node.T = TRUE
                self.parents[TRUE_ID] += [node]
            else:
                node.T = FALSE
                self.parents[FALSE_ID] += [node]

            if false_node.name == "TRUE":
                node.F = TRUE
                self.parents[TRUE_ID] += [node]
            else:
                node.F = FALSE
                self.parents[FALSE_ID] += [node]

        while leaves:
            node = leaves.pop()
            self._delete_node(node)

        self.nodes[TRUE_ID] = TRUE
        self.nodes[FALSE_ID] = FALSE

        self.names["TRUE"] = [TRUE]
        self.names["FALSE"] = [FALSE]

        self.lookup[(id(TRUE), None, None)] = TRUE
        self.lookup[(id(FALSE), None, None)] = FALSE

        assert len(self.nodes) == 2 ** (len(self.atoms)) + 1
        assert len(self.names) == len(self.atoms) + 2
        assert len(self.parents) == 2 ** (len(self.atoms))

    def _reduce(self, node: Node) -> Node:
        if node.is_leaf():
            return node

        TRUE = self._reduce(node.T)
        FALSE = self._reduce(node.F)

        if TRUE == FALSE:
            self._delete_node(node)
            return TRUE

        node.T = TRUE
        node.F = FALSE

        return self._node_lookup(node)

    def _node_lookup(self, node: Node) -> Node:
        key = (id(node), node.T, node.F)
        if key not in self.lookup:
            self.lookup[key] = node

        return self.lookup[key]

    def _recreate_state(self) -> None:
        self.nodes = dict()
        self.names = dict()
        self.lookup = dict()
        self.parents = dict()

        self._navigate_tree(self.root)

    def _navigate_tree(self, node: Node) -> None:
        self.nodes[id(node)] = node

        names = self.names.get(node.name, [])
        if node not in names:
            names += [node]
        self.names[node.name] = names

        if node.is_leaf():
            return

        TRUE, FALSE = node.children()

        TRUE_parents = self.parents.get(id(TRUE), [])
        if node not in TRUE_parents:
            TRUE_parents += [node]

        FALSE_parents = self.parents.get(id(FALSE), [])
        if node not in FALSE_parents:
            FALSE_parents += [node]

        self.parents[id(TRUE)] = TRUE_parents
        self.parents[id(FALSE)] = FALSE_parents

        self._navigate_tree(TRUE)
        self._navigate_tree(FALSE)
