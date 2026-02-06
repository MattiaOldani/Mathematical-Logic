# Generated from PL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PLParser import PLParser
else:
    from PLParser import PLParser

# This class defines a complete listener for a parse tree produced by PLParser.
class PLListener(ParseTreeListener):

    # Enter a parse tree produced by PLParser#start.
    def enterStart(self, ctx:PLParser.StartContext):
        pass

    # Exit a parse tree produced by PLParser#start.
    def exitStart(self, ctx:PLParser.StartContext):
        pass


    # Enter a parse tree produced by PLParser#expr.
    def enterExpr(self, ctx:PLParser.ExprContext):
        pass

    # Exit a parse tree produced by PLParser#expr.
    def exitExpr(self, ctx:PLParser.ExprContext):
        pass


    # Enter a parse tree produced by PLParser#orExpr.
    def enterOrExpr(self, ctx:PLParser.OrExprContext):
        pass

    # Exit a parse tree produced by PLParser#orExpr.
    def exitOrExpr(self, ctx:PLParser.OrExprContext):
        pass


    # Enter a parse tree produced by PLParser#xorExpr.
    def enterXorExpr(self, ctx:PLParser.XorExprContext):
        pass

    # Exit a parse tree produced by PLParser#xorExpr.
    def exitXorExpr(self, ctx:PLParser.XorExprContext):
        pass


    # Enter a parse tree produced by PLParser#andExpr.
    def enterAndExpr(self, ctx:PLParser.AndExprContext):
        pass

    # Exit a parse tree produced by PLParser#andExpr.
    def exitAndExpr(self, ctx:PLParser.AndExprContext):
        pass


    # Enter a parse tree produced by PLParser#notExpr.
    def enterNotExpr(self, ctx:PLParser.NotExprContext):
        pass

    # Exit a parse tree produced by PLParser#notExpr.
    def exitNotExpr(self, ctx:PLParser.NotExprContext):
        pass


    # Enter a parse tree produced by PLParser#atom.
    def enterAtom(self, ctx:PLParser.AtomContext):
        pass

    # Exit a parse tree produced by PLParser#atom.
    def exitAtom(self, ctx:PLParser.AtomContext):
        pass



del PLParser