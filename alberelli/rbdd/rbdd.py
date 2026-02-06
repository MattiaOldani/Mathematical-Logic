from alberelli.base.bdd import BDD
from alberelli.rbdd.rnode import RNode

from functools import reduce

import re


class RBDD(BDD):
    def __init__(self, expression: str) -> None:
        self.nodes = dict()
        self.names = dict()
        self.parents = dict()

        self.expression = expression
        self._extract_atoms()

        atoms = self.atoms.copy()

        self._add_root(RNode(atoms[0], "", dict()))

        while atoms:
            atom = atoms.pop(0)

            nodes = self._get_nodes_by_atom_name(atom)
            for node in nodes:
                node_data = node.data

                data = node_data.copy()
                data[atom] = True
                ID = (node.ID + " " + atom).strip()

                if len(atoms) > 0:
                    to_add = RNode(atoms[0], ID, data)
                else:
                    to_add = RNode(
                        "TRUE"
                        if self._evaluate_expression(expression, data)
                        else "FALSE",
                        ID,
                        data,
                    )

                self.add_node(to_add, node, True)

                data = node_data.copy()
                data[atom] = False
                ID = (node.ID + " not(" + atom + ")").strip()

                if len(atoms) > 0:
                    to_add = RNode(atoms[0], ID, data)
                else:
                    to_add = RNode(
                        "TRUE"
                        if self._evaluate_expression(expression, data)
                        else "FALSE",
                        ID,
                        data,
                    )

                self.add_node(to_add, node, False)

        assert len(self.nodes) == 2 ** (len(self.atoms) + 1) - 1
        assert len(self.names) in {len(self.atoms) + 1, len(self.atoms) + 2}
        assert len(self.parents) == 2 ** (len(self.atoms) + 1) - 2

    def add_node(self, node: RNode, parent: RNode, truth: bool) -> None:
        self.nodes[node.ID] = node
        self.names[node.name] = self.names.get(node.name, []) + [node]
        if truth:
            parent.set_true(node)
        else:
            parent.set_false(node)
        self.parents[node.ID] = self.parents.get(node.ID, []) + [parent]

    def delete_node(self, node: RNode) -> None:
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

    def reduce(self) -> None:
        self._remove_leaves()
        self.root = self._reduce(self.root)
        self._recreate_state()

    def show(self) -> None:
        print(f"Expression: {self.expression}")
        self._print_level(self.root, 0)

    def _print_level(self, node: RNode, depth: int) -> None:
        print(f"{'  ' * depth}{node}")
        for children in node.children():
            self._print_level(children, depth + 1)

    def _extract_atoms(self) -> None:
        self.atoms = list(
            sorted(
                sorted(list(set(re.compile("[a-z]+").findall(self.expression)))),
                key=len,
                reverse=True,
            )
        )

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

    def _add_root(self, root: RNode) -> None:
        self.root = root
        self.nodes[root.ID] = root
        self.names[root.name] = self.names.get(root.name, []) + [root]

    def _get_nodes_by_atom_name(self, atom: str) -> list[RNode]:
        return self.names.get(atom, []).copy()

    def _get_parents_by_node_ID(self, node_ID: str) -> list[RNode]:
        return self.parents.get(node_ID, []).copy()

    def _remove_leaves(self) -> None:
        leaves = self._get_nodes_by_atom_name("TRUE")
        leaves += self._get_nodes_by_atom_name("FALSE")
        assert len(leaves) == 2 ** len(self.atoms)

        parents = set(
            reduce(
                lambda acc, nodes: acc + nodes,
                [self._get_parents_by_node_ID(leaf.ID) for leaf in leaves],
                [],
            )
        )
        assert len(parents) == len(leaves) // 2

        TRUE = RNode("TRUE", "TRUE", dict())
        FALSE = RNode("FALSE", "FALSE", dict())

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

    def _reduce(self, node: RNode) -> RNode:
        if node.is_leaf():
            return node

        TRUE = self._reduce(node.T)  # type: ignore
        FALSE = self._reduce(node.F)  # type: ignore

        if TRUE == FALSE:
            self.delete_node(node)
            return TRUE

        node.set_true(TRUE)
        node.set_false(FALSE)

        return self._node_lookup(node)

    def _node_lookup(self, other: RNode) -> RNode:
        for node in self.nodes.values():
            if other.compare(node):
                return node

        return other

    def _recreate_state(self) -> None:
        self.nodes = dict()
        self.names = dict()
        self.parents = dict()

        self._navigate_tree(self.root)

    def _navigate_tree(self, node: RNode) -> None:
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

        self._navigate_tree(TRUE)
        self._navigate_tree(FALSE)
