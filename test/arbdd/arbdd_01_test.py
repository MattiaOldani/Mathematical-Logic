from alberelli.arbdd.bdd import ParsedSteroidBDD

import pytest


APPLY = [
    ("p | (q & r)", 5, 4),
    ("p ^ q ^ r", 7, 6),
    ("(p ^ q) ^ (p ^ r)", 5, 4),
    ("p | NOT(p)", 1, 0),
    ("p & NOT(p)", 1, 0),
]


@pytest.mark.parametrize("expression,nodes,parents", APPLY)
def test_steroid_creation_and_apply(expression, nodes, parents):
    bdd = ParsedSteroidBDD(expression)

    assert len(bdd.nodes) == nodes
    assert len(bdd.parents) == parents
    assert bdd.is_reduced


RESTRICT = [
    ("p | (q & r)", "p", True, 1, 0),
    ("p | (q & r)", "p", False, 4, 3),
    ("p ^ q ^ r", "p", True, 5, 4),
    ("p ^ q ^ r", "p", False, 5, 4),
    ("(p ^ q) ^ (p ^ r)", "p", True, 5, 4),
    ("(p ^ q) ^ (p ^ r)", "p", False, 5, 4),
    ("(p ^ q) ^ (p ^ r)", "q", True, 3, 2),
    ("(p ^ q) ^ (p ^ r)", "q", False, 3, 2),
]


@pytest.mark.parametrize("expression,atom,value,nodes,parents", RESTRICT)
def test_restrict(expression, atom, value, nodes, parents):
    bdd = ParsedSteroidBDD(expression)
    bdd.restrict(atom, value)

    assert len(bdd.nodes) == nodes
    assert len(bdd.parents) == parents
    assert bdd.is_reduced


EX_FA = [
    ("p | (q & r)", "p", True, True, False),
    ("p | (q & r)", "p", False, True, False),
    ("p ^ q ^ r", "p", True, True, False),
    ("p ^ q ^ r", "p", False, True, False),
    ("(p ^ q) ^ (p ^ r)", "q", True, True, False),
    ("(p ^ q) ^ (p ^ r)", "q", False, True, False),
    ("p | NOT(p)", "p", True, True, True),
    ("p | NOT(p)", "p", False, True, True),
    ("p & NOT(p)", "p", True, False, False),
    ("p & NOT(p)", "p", False, False, False),
]


@pytest.mark.parametrize("expression,atom,value,exists,forall", EX_FA)
def test_exists_forall(expression, atom, value, exists, forall):
    bdd = ParsedSteroidBDD(expression)

    assert bdd.exists(atom, value) == exists
    assert bdd.forall(atom) == forall
