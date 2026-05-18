= Binary Decision Diagram

Un *Binary Decision Diagram* (BDD), come una tabella di verità, rappresenta i valori di una formula proposizionale sotto tutte le possibili interpretazioni. Possiamo rappresentare un BDD con un *grafo*, in cui ogni *nodo* è etichettato con una *atomica* e gli *archi* rappresentano l'assegnazione di valori veri o falsi a quella atomica: ad esempio, un arco solido per il valore vero e un arco tratteggiato per il valore falso.

#align(center)[
  #image("assets/esempio.png")
]

Ogni cammino dall'origine a una foglia corrisponde a un'*interpretazione* completa della formula, e la foglia stessa è etichettata con il valore della formula sotto quell'interpretazione. Notiamo inoltre che nessun atomo compare più di una volta lungo un ramo dall'origine alla foglia, così che venga fatto un solo assegnamento.

A ciascun ramo $b$ è associata un'*interpretazione* $I_b$. Se il ramo segue l'arco vero di un nodo etichettato $p$, allora $I_b (p) = T$; se invece prende l'arco falso, allora $I_b (p) = F$. La foglia finale indica il valore $v_(I_b)(A)$ della formula $A$ sotto quell'interpretazione.

La definizione di BDD però non impone un ordine degli atomi lungo i rami. Tuttavia, gli algoritmi sui BDD richiedono che gli ordini lungo i diversi rami non siano in conflitto.

Un *Ordered Binary Decision Diagram* (*OBDD*) è un BDD in cui l'insieme degli ordini di apparizione degli atomi lungo i rami è compatibile.

Questa piccola estensione ci permetterà dopo di confrontare BDD per diverse formule.
