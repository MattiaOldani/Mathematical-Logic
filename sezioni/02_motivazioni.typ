= Motivazioni

Supponiamo di voler decidere se due formule $A_1$ e $A_2$ della logica proposizionale siano *logicamente equivalenti*. Un approccio naturale consiste nel costruire e confrontare le *tabelle di verità* delle due formule. Chiaramente, questo approccio è molto *inefficiente*, perché per ogni formula con $n$ variabili sono necessarie $2^n$ righe.

Qui entrano in gioco i *BDD*. Il loro uso permette di *ridurre* le tabelle di verità, rimuovendo la *ridondanza* e fornendo una procedura di decisione efficiente per l'equivalenza logica e la soddisfacibilità delle formule.
