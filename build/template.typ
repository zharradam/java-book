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

// The rule under a header row comes from the header itself (Pandoc emits
// table.hline() only when a table has one), so headerless lists get none.
#set table(inset: 6pt, stroke: none)
#set table.hline(stroke: 0.7pt)
// tables sit at the left margin (images stay centred)
#show figure.where(kind: table): set align(left)
#show table: set text(size: 9pt, hyphenate: false)
#show table: set par(justify: false)
// long tables must flow across pages rather than overflow the figure
#show figure.where(kind: table): set block(breakable: true)

#show figure.where(kind: image): set figure.caption(position: bottom)
// Captions: smaller than the body and set apart, so they cannot be read on
// into the paragraph that follows.
#show figure.caption: it => text(size: 9pt)[#emph[#it.body]]
#set figure(gap: 0.9em)
#show figure.where(kind: image): set block(above: 1.8em, below: 2em)
// Pictures may sit at the top or bottom of a page so that a picture too tall
// for the space left does not leave the rest of the page empty.
#show figure.where(kind: image): set figure(placement: auto)
#set place(clearance: 2em)
// Quoted extracts (diaries, letters, newspapers) are set in from both margins.
#show quote.where(block: true): it => pad(left: 2.2em, right: 2.2em, it.body)

// ── Chapter headings: every level-1 heading starts a fresh page ──
// The heading takes the top of the page itself, so that a picture placed
// early in a chapter cannot float up above that chapter's title.
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  place(top, float: true, clearance: 0pt, block(width: 100%, {
    v(6em)
    set text(size: 20pt, weight: "bold")
    block(it.body)
    v(2.5em)
  }))
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
