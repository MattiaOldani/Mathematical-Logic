from __future__ import annotations
from alberelli.arbdd.bdd import InteractiveSteroidBDD


def main():
    bdd = InteractiveSteroidBDD()

    p = bdd.variable("p")
    q = bdd.variable("q")
    r = bdd.variable("r")
    h = bdd.variable("h")

    pah = bdd.apply("AND", p, h)
    qar = bdd.apply("AND", q, r)
    _ = bdd.apply("OR", pah, qar)

    print("Ridotto")
    bdd.show()
    print("*" * 50)
    bdd.restrict("r", False)
    print("Ristretto ridotto")
    bdd.show()
    print("*" * 50)
    print("Exists con albero apply")
    copy = bdd.copy()
    print(copy.exists("r", False))
    print("*" * 50)
    print("Check per vedere se funziona la copy")
    bdd.show()
    print("*" * 50)
    bdd = InteractiveSteroidBDD()
    p = bdd.variable("p")
    q = bdd.variable("q")
    np = bdd.apply("NOT", p)
    pnp = bdd.apply("OR", p, np)
    _ = bdd.apply("OR", pnp, q)
    print("Albero con altra espressione con forall")
    bdd.show()
    print(bdd.forall("p"))


if __name__ == "__main__":
    main()
