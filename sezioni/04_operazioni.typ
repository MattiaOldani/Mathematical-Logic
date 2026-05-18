= Operazioni sui BDD

Possiamo modificare la struttura di un albero tramite una serie di *riduzioni*, che trasformano l'albero fino alla sua versione *ridotta*.

== Reduce e Reduced BDD

L'operazione di riduzione prende in input un *BDD* e crea appunto un *BDD ridotto*.

#let var = "var"

Vengono effettuate due operazioni:
+ *rimozione delle foglie duplicate*: il BDD ha $2^n$ foglie, etichettate con *T* e *F*; se il BDD ha più di due foglie distinte, allora rimuoviamo le $2^n$ foglie aggiungendo invece $2$ sole foglie, etichettate con *T* ed *F*, e colleghiamo i nodi che han perso le foglie a queste due facendo l'ultimo assegnamento della variabile del nodo;
+ *riduzione ricorsiva*: visitiamo in profondità l'albero partendo dalla radice, e ogni volta che non siamo in nodo $n$ che non è una foglia (caso base della ricorsione) effettuiamo la riduzione sui due sotto-alberi del nodo, che indichiamo con i due nodi radice $r_1$ ed $r_2$. Otteniamo poi due casi:
  - se $r_1 = r_2$ allora ritorniamo $r_1$ perché l'assegnamento di $n$ dà lo stesso valore $r_1$;
  - se dopo la generazione della tupla $T = (var(n), r_1, r_2)$ ci accorgiamo che la stessa tupla già stata osservata in una esecuzione precedente (tramite *memoizzazione*), ritorniamo il nodo che l'aveva generata la prima volta.

Il secondo punto della riduzione ricorsiva "rompe" la struttura ad albero, permettendo ad alcuni nodi di avere più padri, ma questo ci permette di non tenere *sotto-alberi simili* e di potare tutti i rami che non servono.

Il BDD che otteniamo dalla *riduzione* è *logicamente equivalente* al BDD di partenza.

Per effettuare poi il confronto tra BDD ridotti ci serve un *ordinamento*: con questa proprietà noi siamo in grado di confrontare tranquillamente due BDD perché li rendiamo *canonici* secondo l'ordinamento dato.

== Apply

Creare un BDD partendo da un *albero completo* è poco conveniente, perché la dimensione iniziale sarebbe simile a quella della tabella di verità -- anzi, è anche di più in termini di numero di nodi. La forza dei BDD risiede nella possibilità di *effettuare operazioni* direttamente su *BDD ridotti*. Infatti, possiamo ottenere un BDD ridotto per l'espressione $A_1 "op" A_2$ conoscendo i BDD ridotti per $A_1$ e $A_2$.

Sfruttiamo ancora un'*operazione ricorsiva*:
+ se i due alberi sono entrambi foglie etichettate con $a_1$ e $a_2$ allora ritorniamo il nodo etichettato da $a_1 "op" a_2$;
+ se i due alberi sono etichettati dalla stessa variabile $p$ ritorniamo un nuovo albero con:
  - $p$ come radice;
  - come sotto-albero SX questa operazione ricorsivamente applicata ai due sotto-alberi SX;
  - idem per il sotto-albero DX;
+ se i due alberi sono etichettati da due variabili $p_1$ e $p_2$ tali che $p_1 < p_2$ nell'ordinamento definito, allora ritorniamo un albero con:
  - $p_1$ come radice;
  - come sotto-albero SX questa operazione ricorsivamente applicata al sotto-albero SX di $A_1$ e sull'intero albero di $A_2$;
  - idem per il sotto-albero DX;
+ se invece $p_2 < p_1$ stessa cosa ma con $A_1$ e $A_2$ invertite.

Questa tecnica ci permette di costruire il *BDD ridotto* senza passare dal *BDD completo*.

== Restrict

L'operazione di *restrizione* prende una formula $A$, una atomica $p$ e un valore di verità $w in {T,F}$ e restituisce la formula ottenuta sostituendo $p$ con $w$, effettuando quindi una *valutazione parziale* di $A$. Come notazione usiamo $A_(|p=w)$.

L'algoritmo di *Restrict* è ancora *ricorsivo* su un BDD dato in input assieme all'atomica $p$ e al valore di verità $w$:
+ se l'albero è una foglia T oppure F essa viene ritornata;
+ se la radice è $p$ ritornare il BDD che ha come radice il nodo che si raggiunge da $p$ sull'arco definito da $w$;
+ se la radice non è $p$ ritornare il nodo etichettato da $p$ e che ha come nodi figli i nodi ottenuti dalla Restrict ricorsiva sui due figli.

Il BDD risultante da Restrict potrebbe non essere ridotto, quindi normalmente si applica subito una operazione di *Reduce*.

== Quantificatori esistenziali e universali

Grazie alla *Restrict* ora possiamo definire i due *quantificatori* principali:
+ *esistenziale* $exists p(A)$ che vale *T* se $A$ è vera per qualche assegnamento parziale di $p$;
+ *universale* $forall p(A)$ che vale *T* se $A$ è vera su tutti gli assegnamenti parziali di $p$.

Con i BDD possiamo eseguire due operazioni di *Restrict* per calcolare questi due quantificatori. In particolare:
+ applicando due Restrict, entrambe su $p$ ma una con *T* e una con *F*, e poi applicando una Apply con *OR* otteniamo l'*esistenziale*;
+ applicando due Restrict, entrambe su $p$ ma una con *T* e una con *F*, e poi applicando una Apply con *AND* otteniamo l'*universale*.

Queste operazioni consentono di manipolare formule complesse in maniera efficiente utilizzando *BDD ridotti*, garantendo al contempo una *canonicità* utile per i confronti.
