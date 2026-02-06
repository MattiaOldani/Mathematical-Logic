grammar PL;

start: expr EOF;

expr: orExpr;

orExpr: xorExpr ('|' xorExpr)*;
xorExpr: andExpr ('^' andExpr)*;
andExpr: notExpr ('&' notExpr)*;
notExpr: 'NOT' '(' expr ')' | atom;
atom: ATOM | '(' expr ')';

ATOM: [a-z]+;
WS: [ \t\r\n]+ -> skip;