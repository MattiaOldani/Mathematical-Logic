from __future__ import annotations
from alberelli.rbdd.bdd import DummyBDD
from alberelli.arbdd.bdd import ParsedSteroidBDD, InteractiveSteroidBDD


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
        bdd = ParsedSteroidBDD(expression)

        bdd.show()
        print("-" * 50)

    bdd = InteractiveSteroidBDD()
    a = bdd.variable("a")
    b = bdd.variable("b")
    c = bdd.variable("c")

    bxc = bdd.apply("XOR", b, c)
    na = bdd.apply("NOT", a)
    expression = bdd.apply("AND", na, bxc)

    bdd.show()


if __name__ == "__main__":
    main()
