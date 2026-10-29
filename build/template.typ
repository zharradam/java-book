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

// ── Cover, full page (same image as the EPUB cover) ───────────
#page(margin: 0pt, numbering: none, fill: rgb("#f7f2e6"))[
  #align(center + horizon)[#image("/images/cover.jpg", height: 100%)]
]

// ── Copyright page: the cover is the title page, so this carries only the imprint ──
#page(numbering: none)[
  #v(1fr)
  #set text(size: 10pt)
  #set par(spacing: 0.7em)
  *$title$*$if(subtitle)$: $subtitle$$endif$ \
  by $for(author)$$author$$sep$, $endfor$

  $if(edition)$
  $edition$ \
  $endif$
  $if(publisher)$
  Published by $publisher$ \
  $endif$
  $if(rights)$
  #text(size: 9pt)[$rights$]
  $endif$
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
