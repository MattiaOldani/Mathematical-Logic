# Generated from PL.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,8,59,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,6,
        1,0,1,0,1,0,1,1,1,1,1,2,1,2,1,2,5,2,23,8,2,10,2,12,2,26,9,2,1,3,
        1,3,1,3,5,3,31,8,3,10,3,12,3,34,9,3,1,4,1,4,1,4,5,4,39,8,4,10,4,
        12,4,42,9,4,1,5,1,5,1,5,1,5,1,5,1,5,3,5,50,8,5,1,6,1,6,1,6,1,6,1,
        6,3,6,57,8,6,1,6,0,0,7,0,2,4,6,8,10,12,0,0,56,0,14,1,0,0,0,2,17,
        1,0,0,0,4,19,1,0,0,0,6,27,1,0,0,0,8,35,1,0,0,0,10,49,1,0,0,0,12,
        56,1,0,0,0,14,15,3,2,1,0,15,16,5,0,0,1,16,1,1,0,0,0,17,18,3,4,2,
        0,18,3,1,0,0,0,19,24,3,6,3,0,20,21,5,1,0,0,21,23,3,6,3,0,22,20,1,
        0,0,0,23,26,1,0,0,0,24,22,1,0,0,0,24,25,1,0,0,0,25,5,1,0,0,0,26,
        24,1,0,0,0,27,32,3,8,4,0,28,29,5,2,0,0,29,31,3,8,4,0,30,28,1,0,0,
        0,31,34,1,0,0,0,32,30,1,0,0,0,32,33,1,0,0,0,33,7,1,0,0,0,34,32,1,
        0,0,0,35,40,3,10,5,0,36,37,5,3,0,0,37,39,3,10,5,0,38,36,1,0,0,0,
        39,42,1,0,0,0,40,38,1,0,0,0,40,41,1,0,0,0,41,9,1,0,0,0,42,40,1,0,
        0,0,43,44,5,4,0,0,44,45,5,5,0,0,45,46,3,2,1,0,46,47,5,6,0,0,47,50,
        1,0,0,0,48,50,3,12,6,0,49,43,1,0,0,0,49,48,1,0,0,0,50,11,1,0,0,0,
        51,57,5,7,0,0,52,53,5,5,0,0,53,54,3,2,1,0,54,55,5,6,0,0,55,57,1,
        0,0,0,56,51,1,0,0,0,56,52,1,0,0,0,57,13,1,0,0,0,5,24,32,40,49,56
    ]

class PLParser ( Parser ):

    grammarFileName = "PL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'|'", "'^'", "'&'", "'NOT'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "ATOM", "WS" ]

    RULE_start = 0
    RULE_expr = 1
    RULE_orExpr = 2
    RULE_xorExpr = 3
    RULE_andExpr = 4
    RULE_notExpr = 5
    RULE_atom = 6

    ruleNames =  [ "start", "expr", "orExpr", "xorExpr", "andExpr", "notExpr", 
                   "atom" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    ATOM=7
    WS=8

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(PLParser.ExprContext,0)


        def EOF(self):
            return self.getToken(PLParser.EOF, 0)

        def getRuleIndex(self):
            return PLParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStart" ):
                return visitor.visitStart(self)
            else:
                return visitor.visitChildren(self)




    def start(self):

        localctx = PLParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self.expr()
            self.state = 15
            self.match(PLParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def orExpr(self):
            return self.getTypedRuleContext(PLParser.OrExprContext,0)


        def getRuleIndex(self):
            return PLParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = PLParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self.orExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def xorExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PLParser.XorExprContext)
            else:
                return self.getTypedRuleContext(PLParser.XorExprContext,i)


        def getRuleIndex(self):
            return PLParser.RULE_orExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrExpr" ):
                listener.enterOrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrExpr" ):
                listener.exitOrExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrExpr" ):
                return visitor.visitOrExpr(self)
            else:
                return visitor.visitChildren(self)




    def orExpr(self):

        localctx = PLParser.OrExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_orExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19
            self.xorExpr()
            self.state = 24
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 20
                self.match(PLParser.T__0)
                self.state = 21
                self.xorExpr()
                self.state = 26
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class XorExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def andExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PLParser.AndExprContext)
            else:
                return self.getTypedRuleContext(PLParser.AndExprContext,i)


        def getRuleIndex(self):
            return PLParser.RULE_xorExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterXorExpr" ):
                listener.enterXorExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitXorExpr" ):
                listener.exitXorExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitXorExpr" ):
                return visitor.visitXorExpr(self)
            else:
                return visitor.visitChildren(self)




    def xorExpr(self):

        localctx = PLParser.XorExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_xorExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self.andExpr()
            self.state = 32
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==2:
                self.state = 28
                self.match(PLParser.T__1)
                self.state = 29
                self.andExpr()
                self.state = 34
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AndExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def notExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PLParser.NotExprContext)
            else:
                return self.getTypedRuleContext(PLParser.NotExprContext,i)


        def getRuleIndex(self):
            return PLParser.RULE_andExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndExpr" ):
                listener.enterAndExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndExpr" ):
                listener.exitAndExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndExpr" ):
                return visitor.visitAndExpr(self)
            else:
                return visitor.visitChildren(self)




    def andExpr(self):

        localctx = PLParser.AndExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_andExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.notExpr()
            self.state = 40
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==3:
                self.state = 36
                self.match(PLParser.T__2)
                self.state = 37
                self.notExpr()
                self.state = 42
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NotExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(PLParser.ExprContext,0)


        def atom(self):
            return self.getTypedRuleContext(PLParser.AtomContext,0)


        def getRuleIndex(self):
            return PLParser.RULE_notExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNotExpr" ):
                listener.enterNotExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNotExpr" ):
                listener.exitNotExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNotExpr" ):
                return visitor.visitNotExpr(self)
            else:
                return visitor.visitChildren(self)




    def notExpr(self):

        localctx = PLParser.NotExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_notExpr)
        try:
            self.state = 49
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 43
                self.match(PLParser.T__3)
                self.state = 44
                self.match(PLParser.T__4)
                self.state = 45
                self.expr()
                self.state = 46
                self.match(PLParser.T__5)
                pass
            elif token in [5, 7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 48
                self.atom()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ATOM(self):
            return self.getToken(PLParser.ATOM, 0)

        def expr(self):
            return self.getTypedRuleContext(PLParser.ExprContext,0)


        def getRuleIndex(self):
            return PLParser.RULE_atom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom" ):
                listener.enterAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom" ):
                listener.exitAtom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtom" ):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)




    def atom(self):

        localctx = PLParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_atom)
        try:
            self.state = 56
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7]:
                self.enterOuterAlt(localctx, 1)
                self.state = 51
                self.match(PLParser.ATOM)
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 2)
                self.state = 52
                self.match(PLParser.T__4)
                self.state = 53
                self.expr()
                self.state = 54
                self.match(PLParser.T__5)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





