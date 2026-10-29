---
name: The Java
description: Java, The Sailing Ship 1813–1940, the free book, shown as a hardback whose endpapers are an Admiralty chart of the 1839–40 voyage.
colors:
  ink: "#1d3346"
  track: "#b23a26"
  gilt: "#9a5b22"
  sea: "#dfe9ec"
  sea-2: "#d3e1e6"
  endpaper: "#e9f0f2"
  land: "#efe6cf"
  paper: "#f6f1e4"
  ink-2: "#3f5a6e"
  rule: "#8aa3b1"
  cloth: "#22384c"
  photo-tint: "#b9cdd6"
typography:
  display:
    fontFamily: "IM Fell English SC, serif"
    fontSize: "clamp(3.6rem, 7.5vw, 6rem)"
    fontWeight: 400
    lineHeight: 0.95
    letterSpacing: "0.12em"
  byline:
    fontFamily: "IM Fell English SC, serif"
    fontSize: "1.45rem"
    fontWeight: 400
    letterSpacing: "0.1em"
  headline:
    fontFamily: "IM Fell English SC, serif"
    fontSize: "clamp(2rem, 4vw, 2.6rem)"
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: "0.06em"
  title:
    fontFamily: "IM Fell English SC, serif"
    fontSize: "1.25rem"
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: "0.06em"
  subtitle:
    fontFamily: "IM Fell English, Georgia, serif"
    fontSize: "clamp(1.15rem, 1.8vw, 1.4rem)"
    fontWeight: 400
  body:
    fontFamily: "IM Fell English, Georgia, serif"
    fontSize: "1.15rem"
    fontWeight: 400
    lineHeight: 1.6
  caption:
    fontFamily: "IM Fell English, Georgia, serif"
    fontSize: "0.95rem"
    fontWeight: 400
  label:
    fontFamily: "Barlow Semi Condensed, system-ui, sans-serif"
    fontSize: "1.1rem"
    fontWeight: 700
    lineHeight: 1.15
  label-strong:
    fontFamily: "Barlow Semi Condensed, system-ui, sans-serif"
    fontSize: "1.35rem"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "0.02em"
  label-small:
    fontFamily: "Barlow Semi Condensed, system-ui, sans-serif"
    fontSize: "0.85rem"
    fontWeight: 500
rounded:
  none: "0"
  board: "4px"
spacing:
  tile-gap: "0.6rem"
  block: "1.4rem"
  section: "clamp(3rem, 7vw, 5rem)"
  hero-gap: "clamp(2rem, 4vw, 4rem)"
components:
  button-read:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.sea}"
    typography: "{typography.label-strong}"
    rounded: "{rounded.none}"
    padding: "1.15rem 1.4rem"
  button-read-hover:
    backgroundColor: "{colors.track}"
    textColor: "{colors.sea}"
  download-tile:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.8rem 0.7rem"
  download-tile-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.sea}"
  finder-input:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: "0.85rem 1rem"
  finder-button:
    backgroundColor: "{colors.track}"
    textColor: "#ffffff"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 1.2rem"
  photo-credit:
    backgroundColor: "{colors.ink}"
    textColor: "#f2f5f6"
    typography: "{typography.label-small}"
    padding: "0.2rem 0.5rem"
---

# Design System: The Java

## Overview

**Creative North Star: "The Chart in the Endpapers"**

The site is a printed object laid on an Admiralty chart. The book itself is the hero: a 3D hardback of the real cover that opens to a chart endpaper on the left and a diary page on the right. Everything around it is chart material: a pale blue-grey sea, engraved navy ink, red track ink for the ship's course, parchment land, a double neat-line border and a fine graticule. Lettering is engraver's type (IM Fell); controls are a plain condensed sans (Barlow Semi Condensed) so that what you can press never reads as period ornament.

Two materials sit on top of the chart and belong to the system. First, gilt: the title and byline are cast copper-gold, the same treatment and gradient stops the cover generator (build/make_cover.py) uses, so the page lettering and the cover lettering are one metal. It is static; it does not track the cursor. Second, the ship herself: a full-bleed photograph of the *Java* at Gibraltar (courtesy of Peter Staveley, R.N.) lies under the chart at the edges, grayscale and multiplied with a sea-grey tint, and is frosted back to chart paper toward the centre, where the graticule takes over. The photograph is atmosphere at the margins; the reading surface in the middle is always chart.

Density is low and type is large, for an older audience: body at 1.15rem/1.6, headings in spaced small capitals, one dominant action. Corners are square, borders are ruled lines, and depth belongs to physical objects (the book, the turning leaf), never to interface panels.

**Key Characteristics:**
- Admiralty-chart palette: sea, navy ink, red track, parchment land.
- IM Fell for lettering, Barlow Semi Condensed for every control.
- Copper-gold gilt lettering for the book's title and author only.
- Full-bleed grayscale ship photograph at the edges, frosted to chart in the centre, always credited.
- Square corners, ruled and double-ruled lines, graticule.
- Real 3D only for the book object; flat everywhere else.

## Colors

A cool chart palette (sea and navy) with one red ink for the voyage and one warm metal for the book's name.

### Primary
- **Engraved Navy Ink** (ink): body text, rules, the neat line, the dominant "Read online" button fill, download-tile borders. The voice of the chart.

### Secondary
- **Track Red** (track): the ship's route and stations on the chart, link underlines, focus outlines, text selection, the hover state of the primary button, and the surname-search button. It marks the voyage and the point of action; it is never a large fill at rest except on the one search button.

### Tertiary
- **Copper Gilt** (gilt): the base colour of the cast-metal lettering. It never appears flat on its own; it is the fallback colour under the gilt gradient (stops #7a4318, #c98a45, #f7e2a6, #d7a04f, #8f5220, #e9bd70, #f9e7b4, #9a5b22 at 0/18/30/42/58/74/82/100%, carried in the sidecar).

### Neutral
- **Chart Sea** (sea): page background; text colour on navy fills.
- **Deep Chart Sea** (sea-2): the sea inside the endpaper chart frame.
- **Endpaper** (endpaper): the inside of the front board.
- **Parchment Land** (land): land masses on the chart.
- **Page Paper** (paper): diary page, page block, form field, translucent download-tile ground (60% opacity).
- **Faded Ink** (ink-2): secondary text, captions, the inner double neat line, chart coastline stroke.
- **Graticule Grey** (rule): graticule lines, the running-head rule, endpaper outline.
- **Bookcloth Navy** (cloth): the back board of the book.
- **Sea-grey Tint** (photo-tint): multiplied over the grayscale photograph so it sits in the chart's colour.

### Named Rules
**The One Track Rule.** Red is the ship's ink. Use it for the route, for focus and hover, and for underlines; never for decoration or for a second competing call to action.

**The Gilt Is the Book's Name Rule.** Copper-gold appears only on the book's title and author (on the page and on the cover). Not on section headings, buttons or numbers.

## Typography

**Display Font:** IM Fell English SC (serif fallback)
**Body Font:** IM Fell English (Georgia fallback), with italic
**Label/Control Font:** Barlow Semi Condensed 500/600/700 (system-ui fallback)

**Character:** Engraver's chart lettering against a clean, condensed working sans: the Fell types say "printed in 1840", Barlow says "you can press this".

### Hierarchy
- **Display** (400, clamp(3.6rem, 7.5vw, 6rem), 0.95, 0.12em tracking): the title "Java" only, gilt.
- **Byline** (400, 1.45rem, 0.1em tracking): the author's name under the title, gilt.
- **Headline** (400, clamp(2rem, 4vw, 2.6rem), 1.1, 0.06em): section headings below the hero, navy.
- **Title** (400, 1.25rem, 1.2, 0.06em): diary-page date; the endpaper legend date (1.15rem, track red).
- **Subtitle** (italic, clamp(1.15rem, 1.8vw, 1.4rem)): "The Sailing Ship 1813–1940", faded ink.
- **Body** (400, 1.15rem, 1.6): running text, max about 38rem in two-column rows.
- **Caption** (italic, 0.95rem): figure captions, place names, running heads, meta.
- **Label** (Barlow 700, 1.1rem / 1.35rem strong; 500 at 0.85–0.95rem for sub-lines): every button, tile and control.

### Named Rules
**The Small Capitals Rule.** Headings are IM Fell English SC, weight 400, letter-spaced 0.06–0.12em. Never bold, never all-caps via text-transform.

**The Controls Are Sans Rule.** Anything interactive (buttons, tiles, page-turn, close, credits) is set in Barlow Semi Condensed; links inside prose stay in Fell with a red underline.

## Layout

The first viewport is a framed chart sheet: `min-height: 100svh`, a two-column grid (book stage on the left, the offer column of minmax(20rem, 30rem) on the right), centred, with a gap of the hero-gap step. Above 1100px the columns sit side by side; at 1100px and below they stack and centre (offer max 34rem); at 760px and below the book shrinks to min(40svh, 340px) tall, download tiles become full-width rows with the detail right-aligned, and the lede moves below the actions.

Below the hero, content sits in a 64rem column with section padding of clamp(3rem, 7vw, 5rem). Rows are two-column grids (1fr auto for the ancestor finder; 1.1fr/0.9fr for text and figure) that collapse to one column at 760px.

The book's proportions come from one variable: height `min(74vh, 620px)`, width height × 0.625 (the cover's 1600×2560 ratio).

### The photograph and the frost
Four stacked full-bleed layers inside the hero: (1) the photograph, grayscale(1) contrast(1.05), positioned center 45%, cover; (2) a flat sea-grey tint layer with `mix-blend-mode: multiply`; (3) a frost layer with backdrop blur(8px) saturate(.7), a 120px graticule in rule grey at 45% and sea at 93%, masked by a radial ellipse (52% × 56% at 52% 50%) so the centre is solid chart and the edges show the ship; (4) the neat-line frame. On narrow screens the frost mask becomes a top-to-bottom fade (35% at the top to solid at 22%). The credit sits bottom-right on a navy chip on desktop and drops into the flow below the actions on mobile.

## Elevation & Depth

Interface surfaces are flat. Depth belongs to physical objects only: the hardback (perspective 2200px, a cursor-eased tilt, a two-layer soft shadow under the back board), the page-block edges, the gutter shading on pages, and the leaf turning over. The gilt lettering has its own stacked bevel (see Shadow Vocabulary) because it imitates cast metal.

### Shadow Vocabulary
- **Book cast shadow** (`box-shadow: 0 40px 80px rgba(16,30,42,.45), 0 12px 24px rgba(16,30,42,.35)`): under the back board only.
- **Gutter** (`box-shadow: inset 18px 0 24px -18px rgba(0,0,0,.25)`): the inner edge of a page; mirrored on the endpaper.
- **Gilt bevel** (`filter: drop-shadow(0 1px 0 #6e3d15) drop-shadow(0 1px 0 #5c3211) drop-shadow(0 1px 0 #4b280d) drop-shadow(0 6px 10px rgba(29,51,70,.35))`): title; the byline uses the lighter `drop-shadow(0 1px 0 #5c3211) drop-shadow(0 2px 4px rgba(29,51,70,.25))`.

### Named Rules
**The Objects Have Weight Rule.** Only the book, its pages and the gilt cast a shadow. Buttons, tiles, fields and sections never do.

## Shapes

Square. Buttons, tiles, fields, figures and the credit chip have no radius. The only curve is the book's fore-edge (4px on the boards). Borders are ruled lines: 1px navy for the outer neat line and figures, a 3px double rule in faded ink inset 5px inside it, 3px double rules above and below the ancestor band, 1.5px navy around tiles and fields.

## Components

### Buttons
- **Shape:** square (0).
- **Primary ("Read the book online"):** a full-width navy slab, sea-coloured label in Barlow 700 1.35rem with a 500 sub-line at 80% opacity, a right arrow drawn as inline SVG, padding 1.15rem 1.4rem. Exactly one per view.
- **Hover / Focus:** fill turns track red (0.2s). Focus everywhere is a 3px track-red outline offset 3px.
- **Download tiles:** three equal tiles beneath the primary, 1.5px navy border on translucent paper, label 700 1.1rem with a 500 0.85rem faded-ink detail line; hover inverts to navy fill with sea text.
- **Search button:** track red fill, white Barlow 700 label, butted against the field.
- **Text actions ("Open the book", "Close the book", "Earlier/Later"):** no box; Barlow 600, navy, red underline offset 0.25em or red on hover; inline SVG line icons at 14–18px.

### Inputs / Fields
- **Style:** paper fill, 1.5px navy border, square, Fell body type at 1.15rem, padding 0.85rem 1rem.
- **Focus:** the global red outline.

### The Book (signature)
A CSS 3D hardback: the real cover image on the front board with a soft sheen, a navy cloth back board and spine, ruled page edges. It eases toward the cursor (mouse only; off under reduced motion). Clicking opens the board to a chart endpaper (titled in spaced small capitals, the track drawn as it progresses, a legend with the date in red) and a diary page with a running head, date in small capitals, place in italic, the verbatim quotation and its diarist, and Earlier/Later controls. Page turns animate a leaf over 0.9s; arrow keys and Escape work while open.

### Chart (signature)
SVG: parchment land with faded-ink coastline, graticule at 0.5 stroke in rule grey, a dashed red ghost of the whole route at 55% opacity, the travelled route as a 6px round-capped red line, stations as sea-filled red rings that fill red when passed. Place names in Fell italic with a sea-coloured halo stroke.

### Gilt Lettering (signature)
A metal gradient (the eight copper-gold stops) at 260% width, positioned 38%, clipped to the glyphs, over the gilt bevel. Static. Used on the hero title and byline, and rendered identically by the cover generator.

## Do's and Don'ts

### Do:
- **Do** keep one navy primary button per view, with downloads as equal-weight outlined tiles beneath it.
- **Do** set every heading in IM Fell English SC at weight 400 with 0.06–0.12em tracking.
- **Do** set every control in Barlow Semi Condensed.
- **Do** use track red only for the route, focus, hover and link underlines.
- **Do** frame chart surfaces with the double neat line (1px ink outside, 3px double faded ink 5px inside).
- **Do** treat any full-bleed photograph as the hero photograph is treated: grayscale, multiplied with the sea-grey tint, frosted to chart toward the reading area, and credited on the surface with the PERMISSIONS.md credit line.
- **Do** match the cover generator's gilt stops whenever the title or author appears in gilt.
- **Do** honour reduced motion: no tilt, no leaf animation, instant cover.

### Don't:
- **Don't** apply gilt to anything but the book's title and author, or make it react to the cursor.
- **Don't** show a photograph in full colour or unframed under text; the centre of any reading surface stays chart paper.
- **Don't** round corners or put shadows on buttons, tiles, fields or sections.
- **Don't** use a bold or text-transformed uppercase heading in place of the Fell small capitals.
