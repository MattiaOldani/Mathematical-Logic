= Implementazione

L'implementazione Python dei *BDD* ha visto la creazione di una interfaccia *BDD* e di una classe *Node* per la gestione di tutte le operazioni che sono implementabili.

I *Node* modellano i singoli nodi dei BDD, e contengono informazioni sull'atomica che etichetta il nodo, i due nodi figli, il valore di verità (solo se il nodo è foglia) e alcuni dati che permettono di calcolare gli assegnamenti delle foglie.

L'interfaccia *BDD* definisce una serie di operazioni che ogni BDD deve essere capace di eseguire, come la *Restrict*, *Exists*, *Forall*, e altre operazioni di controllo e stampa.

Non sono state inserite *Reduce* e *Apply* come operazioni perché sono stato implementati due BDD diversi, uno *Dummy* che usa la Reduce e uno *Steroid* che usa invece la Apply.

== DummyBDD

Un *DummyBDD* è un BDD che accetta come input una *espressione* e costruisce il BDD completo. Tramite il metodo *reduce* andiamo a ridurre il BDD creato con l'algoritmo di *Reduce* che abbiamo mostrato prima.

#let dummy_reduce = "
from alberelli.rbdd.bdd import DummyBDD

expression = 'p | (q & r)'
bdd = DummyBDD(expression)

bdd.print_to_dot('non_reduced')

bdd.reduce()
bdd.print_to_dot('reduced')
".trim()

#align(center)[
  #box(
    inset: 10pt,
    stroke: 1pt + black,
  )[
    #align(left)[
      #raw(dummy_reduce, align: left, lang: "python")
    ]
  ]
]

Ovviamente, questa soluzione è inefficiente visto che viene creato sempre l'albero completo.

Esponiamo comunque i metodi di *Restrict* (restrict), *Exists* (exists) e di *Forall* (forall), ma Exists e Forall non seguono l'implementazione canonica perché non si ha il metodo Apply.

#let dummy_quantifier = "
from alberelli.rbdd.bdd import DummyBDD

expression = 'p | (q & r)'
bdd = DummyBDD(expression)

bdd.reduce()
bdd.restrict('p', False)

bdd.print_to_dot('restrict')

print(bdd.exists('q'))
print(bdd.forall('q'))
".trim()

#align(center)[
  #box(
    inset: 10pt,
    stroke: 1pt + black,
  )[
    #align(left)[
      #raw(dummy_quantifier, align: left, lang: "python")
    ]
  ]
]

== SteroidBDD

Uno *SteroidBDD* è un BDD che rinuncia all'operazione di *Reduce* in favore della *Apply* per costruire un BDD senza passare dall'albero completo. Vedremo *due* diverse *implementazioni* di *SteroidBDD*, che però si basano sulla stessa *grammatica*.

=== Antlr4

L'idea che hanno gli *SteroidBDD* è quella di costruire il BDD di un'espressione trasformandola in un *Abstract Syntax Tree* (AST), per poi costruire i singoli BDD e infine unirli grazie alla *Apply*. È stata definita una grammatica grazie ad *Antlr4* che si presenta nel seguente modo.

#align(center)[
  #box(
    stroke: 1pt + black,
    inset: 10pt,
  )[
    #align(left)[
      #raw(read("../PL.g4"), align: left)
    ]
  ]
]

Con questa grammatica è stata implementata anche la *precedenza*.

=== Parsed

Una prima versione di SteroidBDD è il *ParsedSteroidBDD*, che accetta come input una *espressione* e costruisce il BDD già ridotto usando la *Apply*. Questo metodo è richiamato da un oggetto *Builder*, generato da *Antlr4*, che visita l'*AST* e mano a mano compone i singoli BDD delle espressioni.

Chiamare più volte il metodo Apply su un ParsedSteroidBDD non modifica il suo stato.

#let parsed_apply = "
from alberelli.arbdd.bdd import ParsedSteroidBDD

expression = 'p | (q & r)'
bdd = ParsedSteroidBDD(expression)

bdd.print_to_dot('reduced')
".trim()

#align(center)[
  #box(
    inset: 10pt,
    stroke: 1pt + black,
  )[
    #align(left)[
      #raw(parsed_apply, align: left, lang: "python")
    ]
  ]
]

In questo caso le operazioni di *Exists* e *Forall* sono canoniche perché abbiamo la *Apply*, oltre alla *Restrict*, cruciale per implementare i due quantificatori.

#let parsed_quantifier = "
from alberelli.arbdd.bdd import ParsedSteroidBDD

expression = 'p | (q & r)'
bdd = ParsedSteroidBDD(expression)

bdd.restrict('p', False)

bdd.print_to_dot('restrict')

print(bdd.exists('q'))
print(bdd.forall('q'))
".trim()

#align(center)[
  #box(
    inset: 10pt,
    stroke: 1pt + black,
  )[
    #align(left)[
      #raw(parsed_quantifier, align: left, lang: "python")
    ]
  ]
]

=== Interactive

Una seconda versione di SteroidBDD è l'*InteractiveSteroidBDD*, che non ha input perché permette di costruire il BDD in maniera *interattiva*, quindi definendo mano a mano le singole variabili e combinandole con le operazioni a nostra disposizione.

Qua, ovviamente, l'AST non va navigato con il *Builder*, non avendo subito una espressione, ma è l'utente che si deve responsabilizzare per effettuare una costruzione corretta della sua espressione.

In questo caso dobbiamo chiamare esplicitamente il metodo *Apply* per costruire il BDD dell'espressione finale.

#let interactive_apply = "
from alberelli.arbdd.bdd import InteractiveSteroidBDD

bdd = InteractiveSteroidBDD()

p = bdd.variable('p')
q = bdd.variable('q')
r = bdd.variable('r')

qANDr = bdd.apply('AND', q, r)
_ = bdd.apply('OR', p, qANDr)

bdd.print_in_dot('reduced')
".trim()

#align(center)[
  #box(
    inset: 10pt,
    stroke: 1pt + black,
  )[
    #align(left)[
      #raw(interactive_apply, align: left, lang: "python")
    ]
  ]
]

Anche in questo caso le operazioni di *Exists* e *Forall* sono canoniche perché abbiamo la *Apply* e la *Restrict* implementate.

#let interactive_quantifier = "
from alberelli.arbdd.bdd import InteractiveSteroidBDD

bdd = InteractiveSteroidBDD()

p = bdd.variable('p')
q = bdd.variable('q')
r = bdd.variable('r')

qANDr = bdd.apply('AND', q, r)
_ = bdd.apply('OR', p, qANDr)

bdd.restrict('p', False)

bdd.print_to_dot('restrict')

print(bdd.exists('q'))
print(bdd.forall('q'))
".trim()

#align(center)[
  #box(
    inset: 10pt,
    stroke: 1pt + black,
  )[
    #align(left)[
      #raw(interactive_quantifier, align: left, lang: "python")
    ]
  ]
]
