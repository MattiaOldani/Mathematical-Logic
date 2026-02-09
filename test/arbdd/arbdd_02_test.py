from alberelli.arbdd.bdd import InteractiveSteroidBDD


def test_expression_reduce_L1():
    bdd = InteractiveSteroidBDD()

    p = bdd.variable("p")
    q = bdd.variable("q")
    r = bdd.variable("r")

    qar = bdd.apply("AND", q, r)
    _ = bdd.apply("OR", p, qar)

    assert len(bdd.nodes) == 5
    assert len(bdd.parents) == 4

    another = bdd.copy()
    another.restrict("p", True)

    assert len(another.nodes) == 1
    assert len(another.parents) == 0

    another = bdd.copy()
    another.restrict("p", False)

    assert len(another.nodes) == 4
    assert len(another.parents) == 3

    assert bdd.exists("p", True)
    assert bdd.exists("p", False)
    assert not bdd.forall("p")


def test_expression_reduce_L2():
    bdd = InteractiveSteroidBDD()

    p = bdd.variable("p")
    q = bdd.variable("q")
    r = bdd.variable("r")

    pxq = bdd.apply("XOR", p, q)
    _ = bdd.apply("XOR", pxq, r)

    assert len(bdd.nodes) == 7
    assert len(bdd.parents) == 6

    another = bdd.copy()
    another.restrict("p", True)

    assert len(another.nodes) == 5
    assert len(another.parents) == 4

    another = bdd.copy()
    another.restrict("p", False)

    assert len(another.nodes) == 5
    assert len(another.parents) == 4

    assert bdd.exists("p", True)
    assert bdd.exists("p", False)
    assert not bdd.forall("p")


def test_expression_apply():
    bdd = InteractiveSteroidBDD()

    p = bdd.variable("p")
    q = bdd.variable("q")
    r = bdd.variable("r")

    pxq = bdd.apply("XOR", p, q)
    pxr = bdd.apply("XOR", p, r)
    _ = bdd.apply("XOR", pxq, pxr)

    assert len(bdd.nodes) == 5
    assert len(bdd.parents) == 4

    another = bdd.copy()
    another.restrict("p", True)

    assert len(another.nodes) == 5
    assert len(another.parents) == 4

    another = bdd.copy()
    another.restrict("p", False)

    assert len(another.nodes) == 5
    assert len(another.parents) == 4

    another = bdd.copy()
    another.restrict("q", True)

    assert len(another.nodes) == 3
    assert len(another.parents) == 2

    another = bdd.copy()
    another.restrict("q", False)

    assert len(another.nodes) == 3
    assert len(another.parents) == 2

    assert bdd.exists("p", True)
    assert bdd.exists("p", False)
    assert not bdd.forall("p")


def test_tauto():
    bdd = InteractiveSteroidBDD()

    p = bdd.variable("p")

    np = bdd.apply("NOT", p)
    _ = bdd.apply("OR", p, np)

    assert len(bdd.nodes) == 1
    assert len(bdd.parents) == 0

    assert bdd.exists("p", True)
    assert bdd.exists("p", False)
    assert bdd.forall("p")


def test_falsity():
    bdd = InteractiveSteroidBDD()

    p = bdd.variable("p")

    np = bdd.apply("NOT", p)
    _ = bdd.apply("AND", p, np)

    assert len(bdd.nodes) == 1
    assert len(bdd.parents) == 0

    assert not bdd.exists("p", True)
    assert not bdd.exists("p", False)
    assert not bdd.forall("p")
