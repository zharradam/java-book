# Generate the typographic covers: images/cover.jpg (book, 1600x2560) and
# images/cover-square.jpg (audiobook, 2400x2400 as audiobook stores ask).
#
# Deliberately carries no photograph: the previous cover used an image
# from the National Library of New Zealand for which no reproduction
# permission is held. Replace this with a photographic cover only when a
# licensed image and its credit line are recorded in PERMISSIONS.md.
#
# Title and author are set in IM Fell English SC (build/fonts, SIL Open Font
# License) and cast in the same copper-gold as the title on theshipjava.uk.
from PIL import Image, ImageDraw, ImageFont, ImageFilter

CREAM = (247, 242, 230)
INK = (38, 34, 29)
RULE = (124, 108, 84)
FAINT = (150, 134, 108)
FELL = 'build/fonts/IMFellEnglishSC.ttf'

# Copper to gold, matching the .gilt gradient on the website
GILT = [(0, (122, 67, 24)), (.18, (201, 138, 69)), (.30, (247, 226, 166)), (.42, (215, 160, 79)), (.58, (143, 82, 32)),
        (.74, (233, 189, 112)), (.82, (249, 231, 180)), (1, (154, 91, 34))]

def f(name, size):
    return ImageFont.truetype(f'C:/Windows/Fonts/{name}', size)

reg, ital = 'georgia.ttf', 'georgiai.ttf'

def cover(W, H, s, y, path):
    """Draw the cover at W x H; s scales sizes, y holds each line's top edge."""
    img = Image.new('RGB', (W, H), CREAM)
    d = ImageDraw.Draw(img)
    S = lambda n: round(n * s)

    def center(text, fnt, top, fill=INK, spacing=0, draw=d):
        if spacing:
            total = sum(draw.textlength(c, font=fnt) + spacing for c in text) - spacing
            x = (W - total) / 2
            for c in text:
                draw.text((x, top), c, font=fnt, fill=fill)
                x += draw.textlength(c, font=fnt) + spacing
        else:
            draw.text(((W - draw.textlength(text, font=fnt)) / 2, top), text, font=fnt, fill=fill)

    def gilt(text, fnt, top, spacing, depth):
        """Copper-gold lettering: gradient through the glyphs, bronze extrusion, soft shadow."""
        mask = Image.new('L', (W, H), 0)
        center(text, fnt, top, fill=255, spacing=spacing, draw=ImageDraw.Draw(mask))
        x0, y0, x1, y1 = mask.getbbox()
        row = Image.new('RGB', (x1 - x0, 1))
        for x in range(x1 - x0):
            t = x / max(1, x1 - x0 - 1)
            for (a, ca), (b, cb) in zip(GILT, GILT[1:]):
                if a <= t <= b:
                    k = (t - a) / (b - a)
                    row.putpixel((x, 0), tuple(int(ca[i] + (cb[i] - ca[i]) * k) for i in range(3)))
                    break
        grad = Image.new('RGB', (W, H))
        grad.paste(row.resize((x1 - x0, y1 - y0)), (x0, y0))
        shadow = mask.filter(ImageFilter.GaussianBlur(S(18) * depth / 8)).point(lambda v: int(v * .35))
        img.paste((29, 51, 70), (0, S(22) * depth // 8), shadow)
        for dy, col in ((depth, (75, 40, 13)), (depth * 5 // 8, (92, 50, 17)), (depth * 3 // 8, (110, 61, 21))):
            img.paste(col, (0, dy), mask)
        img.paste(grad, (0, 0), mask)

    def rule(top, half_width, width=3, colour=RULE):
        d.line([(W/2 - half_width, top), (W/2 + half_width, top)], fill=colour, width=width)

    # Outer frame: double rule, the classic period-history look
    M = S(110)
    d.rectangle([M, M, W - M, H - M], outline=RULE, width=S(4))
    d.rectangle([M + S(18), M + S(18), W - M - S(18), H - M - S(18)], outline=RULE, width=S(2))

    # Title block
    gilt('Java', ImageFont.truetype(FELL, S(330)), y['title'], S(40), S(8))
    rule(y['rule1'], S(300), S(3))
    center('The Sailing Ship', f(ital, S(82)), y['ship'])
    center('1813–1940', f(ital, S(82)), y['dates'])
    rule(y['rule2'], S(300), S(3))

    # Descriptive subtitle — the book's own framing
    center('The voyage of the East Indiaman', f(reg, S(54)), y['sub1'], fill=RULE)
    center('to South Australia, 1839–1840', f(reg, S(54)), y['sub2'], fill=RULE)

    # Author
    gilt('Stephen Michael Barnett', ImageFont.truetype(FELL, S(96)), y['author'], S(6), S(4))

    # Imprint
    center('TEN BRAT PRESS', f(reg, S(44)), y['imprint'], fill=FAINT, spacing=S(8))

    img.save(path, quality=92)
    print('wrote', path, img.size)

cover(1600, 2560, 1, dict(title=330, rule1=790, ship=860, dates=985, rule2=1140,
                          sub1=1290, sub2=1380, author=1860, imprint=2260),
      'images/cover.jpg')

# Same design tightened vertically to fit a square
cover(2400, 2400, 1.5, dict(title=175, rule1=840, ship=915, dates=1100, rule2=1335,
                            sub1=1440, sub2=1575, author=1790, imprint=2040),
      'images/cover-square.jpg')
