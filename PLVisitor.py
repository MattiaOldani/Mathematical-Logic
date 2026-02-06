# Generated from PL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PLParser import PLParser
else:
    from PLParser import PLParser

# This class defines a complete generic visitor for a parse tree produced by PLParser.

class PLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PLParser#start.
    def visitStart(self, ctx:PLParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLParser#expr.
    def visitExpr(self, ctx:PLParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLParser#orExpr.
    def visitOrExpr(self, ctx:PLParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLParser#xorExpr.
    def visitXorExpr(self, ctx:PLParser.XorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLParser#andExpr.
    def visitAndExpr(self, ctx:PLParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLParser#notExpr.
    def visitNotExpr(self, ctx:PLParser.NotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLParser#atom.
    def visitAtom(self, ctx:PLParser.AtomContext):
        return self.visitChildren(ctx)



del PLParser