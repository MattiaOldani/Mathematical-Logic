from alberelli.arbdd.bdd import SteroidBDD
from alberelli.node import Node

from antlr4 import CommonTokenStream, InputStream
from alberelli.builder.PLLexer import PLLexer
from alberelli.builder.PLParser import PLParser
from alberelli.builder.PLVisitor import PLVisitor


class Builder(PLVisitor):
    def __init__(self, BDD: SteroidBDD) -> None:
        self.BDD = BDD

        lexer = PLLexer(InputStream(self.BDD.expression))
        stream = CommonTokenStream(lexer)
        parser = PLParser(stream)
        self.tree = parser.start()

    def visitAtom(self, ctx) -> Node:
        if ctx.ATOM():
            return self.BDD.variable(ctx.ATOM().getText())
        return self.visit(ctx.expr())

    def visitNotExpr(self, ctx) -> Node:
        if ctx.getChildCount() == 4:
            node = self.visit(ctx.expr())
            return self.BDD.apply("XOR", node, self.BDD.TRUE)
        return self.visit(ctx.atom())

    def visitAndExpr(self, ctx) -> Node:
        node = self.visit(ctx.notExpr(0))
        for i in range(1, len(ctx.notExpr())):
            node = self.BDD.apply("AND", node, self.visit(ctx.notExpr(i)))
        return node

    def visitXorExpr(self, ctx) -> Node:
        node = self.visit(ctx.andExpr(0))
        for i in range(1, len(ctx.andExpr())):
            node = self.BDD.apply("XOR", node, self.visit(ctx.andExpr(i)))
        return node

    def visitOrExpr(self, ctx) -> Node:
        node = self.visit(ctx.xorExpr(0))
        for i in range(1, len(ctx.xorExpr())):
            node = self.BDD.apply("OR", node, self.visit(ctx.xorExpr(i)))
        return node

    def visitStart(self, ctx) -> Node:
        return self.visit(ctx.expr())
