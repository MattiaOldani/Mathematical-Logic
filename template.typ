#let project(title: "", body) = {
  set document(title: title)

  set text(font: "New Computer Modern", lang: "it")

  set par(justify: true)

  set page(numbering: "1")

  set heading(numbering: "1.")

  set list(indent: 1.2em)
  set enum(indent: 1.2em)

  align(center)[
    #block(text(1.5em, [Università degli Studi di Milano]))

    #block(text(1.5em, [Dipartimento di Informatica]))

    #block(text(1.5em, [Mathematical Logic -- 2025/2026]))

    #block(text(1.5em, [Oldani Mattia [53690A]]))

    #v(25pt)

    #block(text(2em, weight: 900, title))

    #v(50pt)

    #image("sezioni/assets/bdd.png", width: 65%)
  ]

  show outline.entry: it => {
    if it.element.func() == figure {
      let res
      if it.element.numbering != none {
        res = link(
          it.element.location(),
          it.indented(it.prefix(), [ --- ] + it.element.body + h(1fr) + it.page()),
        )
      } else {
        res = link(
          it.element.location(),
          it.indented(it.prefix(), it.element.body + h(1fr) + it.page()),
        )
      }

      v(2.3em, weak: true)
      strong(text(size: 16pt, res))
    } else {
      it
    }
  }

  show outline.entry.where(level: 1): it => {
    v(12pt, weak: true)
    strong(it)
  }

  show link: underline
  show ref: underline

  show figure: set block(breakable: true)

  pagebreak()

  outline(indent: 2em)

  pagebreak()

  body
}
