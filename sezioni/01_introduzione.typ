= Introduzione

Il problema di decidere la *soddisfacibilità* di una formula della *logica proposizionale* è centrale in numerose applicazioni dell'informatica, insieme ai problemi di *validità* ed *equivalenza logica*.

I *Binary Decision Diagrams* (*BDD*) costituiscono una delle *tecniche* più diffuse per il calcolo simbolico su formule proposizionali. Un *BDD* è una *struttura dati* che rappresenta la semantica di una formula mediante un grafo diretto aciclico. La formula non viene trattata come una semplice espressione sintattica, ma come una funzione booleana, rappresentata attraverso una struttura grafica che può essere progressivamente ridotta.

Attraverso un *algoritmo di riduzione* il grafo viene trasformato in una forma compatta con una proprietà fondamentale: formule logicamente equivalenti producono lo *stesso BDD ridotto*. Questa caratteristica fornisce una procedura decisionale per l'equivalenza logica: date due formule $A_1$ e $A_2$ è sufficiente costruire i rispettivi BDD e verificarne l'identità strutturale.
