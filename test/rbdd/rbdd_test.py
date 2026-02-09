from alberelli.rbdd.bdd import DummyBDD

import pytest


CREATION = [
    ("p | (q & r)", 15, 5, 14, 8),
    ("p ^ q ^ r", 15, 5, 14, 8),
    ("(p ^ q) ^ (p ^ r)", 15, 5, 14, 8),
    ("p | NOT(p)", 3, 2, 2, 2),
    ("p & NOT(p)", 3, 2, 2, 2),
]


@pytest.mark.parametrize("expression,nodes,names,parents,leaves", CREATION)
def test_dummy_creation(expression, nodes, names, parents, leaves):
    bdd = DummyBDD(expression)
    bdd_leaves = bdd._get_nodes_by_atom_name("TRUE")
    bdd_leaves += bdd._get_nodes_by_atom_name("FALSE")

    # Relation between parameters
    assert len(bdd.nodes) == 2 ** (len(bdd.atoms) + 1) - 1
    assert len(bdd.names) in {len(bdd.atoms) + 1, len(bdd.atoms) + 2}
    assert len(bdd.parents) == 2 ** (len(bdd.atoms) + 1) - 2
    assert len(bdd_leaves) == 2 ** len(bdd.atoms)

    # Specific values
    assert len(bdd.nodes) == nodes
    assert len(bdd.names) == names
    assert len(bdd.parents) == parents
    assert len(bdd_leaves) == leaves


LEAVES = [
    ("p | (q & r)", 9, 5, 8),
    ("p ^ q ^ r", 9, 5, 8),
    ("(p ^ q) ^ (p ^ r)", 9, 5, 8),
    ("p | NOT(p)", 2, 2, 1),
    ("p & NOT(p)", 2, 2, 1),
]


@pytest.mark.parametrize("expression,nodes,names,parents", LEAVES)
def test_remove_leaves(expression, nodes, names, parents):
    bdd = DummyBDD(expression)
    bdd._remove_leaves()

    # Relation between parameters
    assert len(bdd.nodes) in {2 ** (len(bdd.atoms)), 2 ** (len(bdd.atoms)) + 1}
    assert len(bdd.names) in {len(bdd.atoms) + 1, len(bdd.atoms) + 2}
    assert len(bdd.parents) in {2 ** (len(bdd.atoms)) - 1, 2 ** (len(bdd.atoms))}

    # Specific values
    assert len(bdd.nodes) == nodes
    assert len(bdd.names) == names
    assert len(bdd.parents) == parents


REDUCE = [
    ("p | (q & r)", 5, 5, 4),
    ("p ^ q ^ r", 7, 5, 6),
    ("(p ^ q) ^ (p ^ r)", 5, 4, 4),
    ("p | NOT(p)", 1, 1, 0),
    ("p & NOT(p)", 1, 1, 0),
]


@pytest.mark.parametrize("expression,nodes,names,parents", REDUCE)
def test_reduce(expression, nodes, names, parents):
    bdd = DummyBDD(expression)
    bdd.reduce()

    assert len(bdd.nodes) == nodes
    assert len(bdd.names) == names
    assert len(bdd.parents) == parents


RESTRICT = [
    ("p | (q & r)", "p", True, 1, 1, 0),
    ("p | (q & r)", "p", False, 4, 4, 3),
    ("p ^ q ^ r", "p", True, 5, 4, 4),
    ("p ^ q ^ r", "p", False, 5, 4, 4),
    ("(p ^ q) ^ (p ^ r)", "p", True, 5, 4, 4),
    ("(p ^ q) ^ (p ^ r)", "p", False, 5, 4, 4),
    ("(p ^ q) ^ (p ^ r)", "q", True, 3, 3, 2),
    ("(p ^ q) ^ (p ^ r)", "q", False, 3, 3, 2),
]


@pytest.mark.parametrize("expression,atom,value,nodes,names,parents", RESTRICT)
def test_restrict(expression, atom, value, nodes, names, parents):
    bdd = DummyBDD(expression)
    bdd.reduce()
    bdd.restrict(atom, value)
    bdd.reduce()

    assert len(bdd.nodes) == nodes
    assert len(bdd.names) == names
    assert len(bdd.parents) == parents


EX_FA = [
    ("p | (q & r)", "p", True, False),
    ("p ^ q ^ r", "p", True, False),
    ("(p ^ q) ^ (p ^ r)", "q", True, False),
    ("p | NOT(p)", "p", True, True),
    ("p & NOT(p)", "p", False, False),
]


@pytest.mark.parametrize("expression,atom,exists,forall", EX_FA)
def test_exists_forall(expression, atom, exists, forall):
    bdd = DummyBDD(expression)
    bdd.reduce()

    assert bdd.exists(atom) == exists
    assert bdd.forall(atom) == forall
