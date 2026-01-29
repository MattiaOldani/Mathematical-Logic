#let project(title: "", body) = {
  set document(title: title)

  set text(font: "New Computer Modern Math", lang: "en")

  set par(justify: true)

  set page(numbering: "1")

  set heading(numbering: "1.")

  set list(indent: 1.2em)
  set enum(indent: 1.2em)

  align(center)[
    #block(text(1.5em, [Università degli Studi di Milano]))

    #block(text(1.5em, [Dipartimento di Informatica]))

    #block(text(1.5em, [Mathematical Logic -- 2025/2026]))

    #v(12pt)

    #block(text(1.5em, [Oldani Mattia [53690A]]))

    #block(text(2em, title))

    #v(30pt)
  ]

  show link: underline
  show ref: underline

  show figure: set block(breakable: true)

  body
}
