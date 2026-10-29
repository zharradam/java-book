# Generate the typographic covers: images/cover.jpg (book, 1600x2560) and
# images/cover-square.jpg (audiobook, 2400x2400 as audiobook stores ask).
#
# Deliberately carries no photograph: the previous cover used an image
# from the National Library of New Zealand for which no reproduction
# permission is held. Replace this with a photographic cover only when a
# licensed image and its credit line are recorded in PERMISSIONS.md.
from PIL import Image, ImageDraw, ImageFont

CREAM = (247, 242, 230)
INK = (38, 34, 29)
RULE = (124, 108, 84)
FAINT = (150, 134, 108)

def f(name, size):
    return ImageFont.truetype(f'C:/Windows/Fonts/{name}', size)

reg, bold, ital = 'georgia.ttf', 'georgiab.ttf', 'georgiai.ttf'

def cover(W, H, s, y, path):
    """Draw the cover at W x H; s scales sizes, y holds each line's top edge."""
    img = Image.new('RGB', (W, H), CREAM)
    d = ImageDraw.Draw(img)
    S = lambda n: round(n * s)

    def center(text, fnt, top, fill=INK, spacing=0):
        if spacing:
            total = sum(d.textlength(c, font=fnt) + spacing for c in text) - spacing
            x = (W - total) / 2
            for c in text:
                d.text((x, top), c, font=fnt, fill=fill)
                x += d.textlength(c, font=fnt) + spacing
        else:
            d.text(((W - d.textlength(text, font=fnt)) / 2, top), text, font=fnt, fill=fill)

    def rule(top, half_width, width=3, colour=RULE):
        d.line([(W/2 - half_width, top), (W/2 + half_width, top)], fill=colour, width=width)

    # Outer frame: double rule, the classic period-history look
    M = S(110)
    d.rectangle([M, M, W - M, H - M], outline=RULE, width=S(4))
    d.rectangle([M + S(18), M + S(18), W - M - S(18), H - M - S(18)], outline=RULE, width=S(2))

    # Title block
    center('JAVA', f(bold, S(250)), y['title'], spacing=S(18))
    rule(y['rule1'], S(300), S(3))
    center('The Sailing Ship', f(ital, S(82)), y['ship'])
    center('1813–1940', f(ital, S(82)), y['dates'])
    rule(y['rule2'], S(300), S(3))

    # Descriptive subtitle — the book's own framing
    center('The voyage of the East Indiaman', f(reg, S(54)), y['sub1'], fill=RULE)
    center('to South Australia, 1839–1840', f(reg, S(54)), y['sub2'], fill=RULE)

    # Author
    center('STEPHEN MICHAEL BARNETT', f(reg, S(66)), y['author'], spacing=S(6))

    # Imprint
    center('TEN BRAT PRESS', f(reg, S(44)), y['imprint'], fill=FAINT, spacing=S(8))

    img.save(path, quality=92)
    print('wrote', path, img.size)

cover(1600, 2560, 1, dict(title=430, rule1=790, ship=860, dates=985, rule2=1140,
                          sub1=1290, sub2=1380, author=1900, imprint=2260),
      'images/cover.jpg')

# Same design tightened vertically to fit a square
cover(2400, 2400, 1.5, dict(title=375, rule1=840, ship=915, dates=1100, rule2=1335,
                            sub1=1440, sub2=1575, author=1830, imprint=2040),
      'images/cover-square.jpg')
