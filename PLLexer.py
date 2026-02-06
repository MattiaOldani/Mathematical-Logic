# Generated from PL.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,8,43,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,3,1,3,1,4,1,4,1,
        5,1,5,1,6,4,6,33,8,6,11,6,12,6,34,1,7,4,7,38,8,7,11,7,12,7,39,1,
        7,1,7,0,0,8,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,1,0,2,1,0,97,122,
        3,0,9,10,13,13,32,32,44,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,
        1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,1,17,
        1,0,0,0,3,19,1,0,0,0,5,21,1,0,0,0,7,23,1,0,0,0,9,27,1,0,0,0,11,29,
        1,0,0,0,13,32,1,0,0,0,15,37,1,0,0,0,17,18,5,124,0,0,18,2,1,0,0,0,
        19,20,5,94,0,0,20,4,1,0,0,0,21,22,5,38,0,0,22,6,1,0,0,0,23,24,5,
        78,0,0,24,25,5,79,0,0,25,26,5,84,0,0,26,8,1,0,0,0,27,28,5,40,0,0,
        28,10,1,0,0,0,29,30,5,41,0,0,30,12,1,0,0,0,31,33,7,0,0,0,32,31,1,
        0,0,0,33,34,1,0,0,0,34,32,1,0,0,0,34,35,1,0,0,0,35,14,1,0,0,0,36,
        38,7,1,0,0,37,36,1,0,0,0,38,39,1,0,0,0,39,37,1,0,0,0,39,40,1,0,0,
        0,40,41,1,0,0,0,41,42,6,7,0,0,42,16,1,0,0,0,3,0,34,39,1,6,0,0
    ]

class PLLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    ATOM = 7
    WS = 8

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'|'", "'^'", "'&'", "'NOT'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>",
            "ATOM", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "ATOM", 
                  "WS" ]

    grammarFileName = "PL.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


