// Book template for the PDF edition.
// Pandoc fills the $variables$ from build/metadata.yaml.

#let horizontalrule = align(center)[#v(0.6em) * \* \* * #v(0.6em)]

#show terms: it => {
  it.children
    .map(child => [
      #strong[#child.term]
      #block(inset: (left: 1.5em, top: -0.4em))[#child.description]
      ])
    .join()
}

#set page(
  paper: "$if(papersize)$$papersize$$else$a4$endif$",
  margin: (
    left: $if(margin-left)$$margin-left$$else$2.5cm$endif$,
    right: $if(margin-right)$$margin-right$$else$2.5cm$endif$,
    top: $if(margin-top)$$margin-top$$else$2.5cm$endif$,
    bottom: $if(margin-bottom)$$margin-bottom$$else$2.5cm$endif$,
  ),
  numbering: "1",
  number-align: center,
)

#set text(
  font: "$if(mainfont)$$mainfont$$else$New Computer Modern$endif$",
  size: $if(fontsize)$$fontsize$$else$11pt$endif$,
  lang: "en",
)

#set par(justify: true, leading: 0.7em)

#set table(inset: 6pt, stroke: (x, y) => if y == 0 { (bottom: 0.7pt) } else { none })

#show figure.where(kind: image): set figure.caption(position: bottom)
#show figure.caption: it => [#emph[#it.body]]

// ── Chapter headings: every level-1 heading starts a fresh page ──
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(6em)
  set text(size: 20pt, weight: "bold")
  block(it.body)
  v(2.5em)
}

#show heading.where(level: 2): it => {
  v(1.4em)
  set text(size: 14pt, weight: "bold")
  block(it.body)
  v(0.6em)
}

// ── Title page ────────────────────────────────────────────────
#page(numbering: none)[
  #v(22%)
  #align(center)[
    #text(size: 40pt, weight: "bold")[$title$]
    $if(subtitle)$
    #v(1.2em)
    #text(size: 16pt, style: "italic")[$subtitle$]
    $endif$
    #v(4em)
    #text(size: 13pt)[by]
    #v(0.4em)
    #text(size: 18pt)[$for(author)$$author$$sep$, $endfor$]
    #v(1fr)
    $if(edition)$
    #text(size: 11pt)[$edition$]
    #v(0.8em)
    $endif$
    $if(publisher)$
    #text(size: 11pt)[$publisher$]
    #v(0.8em)
    $endif$
    $if(rights)$
    #text(size: 9pt)[$rights$]
    $endif$
    #v(8%)
  ]
]

// ── Table of contents, on its own page ────────────────────────
$if(toc)$
#page[
  #v(4em)
  #text(size: 20pt, weight: "bold")[Contents]
  #v(2em)
  #outline(title: none, depth: $if(toc-depth)$$toc-depth$$else$2$endif$)
]
$endif$

// ── The book ──────────────────────────────────────────────────
#counter(page).update(1)

$body$
