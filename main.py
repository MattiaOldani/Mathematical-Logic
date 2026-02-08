from __future__ import annotations
from alberelli.rbdd.bdd import DummyBDD
from alberelli.arbdd.bdd import ParsedSteroidBDD, InteractiveSteroidBDD


def main():
    expressions = [line.strip() for line in open("expression.txt", "r").readlines()]

    for expression in expressions:
        bdd = DummyBDD(expression)

        print("Non ridotto")
        bdd.show()
        print("*" * 50)
        bdd.reduce()
        print("Ridotto")
        bdd.show()
        print("*" * 50)
        bdd.restrict("r", False)
        print("Ristretto ma non ridotto")
        bdd.show()
        print("*" * 50)
        bdd.reduce()
        print("Ristretto ridotto")
        bdd.show()
        print("-" * 50)

    for expression in expressions:
        bdd = ParsedSteroidBDD(expression)

        print("Ridotto")
        bdd.show()
        print("*" * 50)
        bdd.restrict("r", False)
        print("Ristretto ridotto")
        bdd.show()
        print("-" * 50)

    bdd = InteractiveSteroidBDD()

    # a = bdd.variable("a")
    # b = bdd.variable("b")
    # c = bdd.variable("c")

    # bxc = bdd.apply("XOR", b, c)
    # na = bdd.apply("NOT", a)
    # expression = bdd.apply("AND", na, bxc)

    p = bdd.variable("p")
    q = bdd.variable("q")
    r = bdd.variable("r")
    h = bdd.variable("h")

    pah = bdd.apply("AND", p, h)
    qar = bdd.apply("AND", q, r)
    expression = bdd.apply("OR", pah, qar)

    print("Ridotto")
    bdd.show()
    print("*" * 50)
    bdd.restrict("r", False)
    print("Ristretto ridotto")
    bdd.show()


if __name__ == "__main__":
    main()
