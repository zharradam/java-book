# Generate the typographic cover (images/cover.jpg).
#
# Deliberately carries no photograph: the previous cover used an image
# from the National Library of New Zealand for which no reproduction
# permission is held. Replace this with a photographic cover only when a
# licensed image and its credit line are recorded in PERMISSIONS.md.
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 2560
CREAM = (247, 242, 230)
INK = (38, 34, 29)
RULE = (124, 108, 84)
FAINT = (150, 134, 108)

img = Image.new('RGB', (W, H), CREAM)
d = ImageDraw.Draw(img)

def f(name, size):
    return ImageFont.truetype(f'C:/Windows/Fonts/{name}', size)

reg, bold, ital = 'georgia.ttf', 'georgiab.ttf', 'georgiai.ttf'

def center(text, fnt, y, fill=INK, spacing=0):
    if spacing:
        total = sum(d.textlength(c, font=fnt) + spacing for c in text) - spacing
        x = (W - total) / 2
        for c in text:
            d.text((x, y), c, font=fnt, fill=fill)
            x += d.textlength(c, font=fnt) + spacing
    else:
        d.text(((W - d.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)

def rule(y, half_width, width=3, colour=RULE):
    d.line([(W/2 - half_width, y), (W/2 + half_width, y)], fill=colour, width=width)

# Outer frame: double rule, the classic period-history look
M = 110
d.rectangle([M, M, W - M, H - M], outline=RULE, width=4)
d.rectangle([M + 18, M + 18, W - M - 18, H - M - 18], outline=RULE, width=2)

# Title block
center('JAVA', f(bold, 250), 430, spacing=18)
rule(790, 300)
center('The Sailing Ship', f(ital, 82), 860)
center('1813–1940', f(ital, 82), 985)
rule(1140, 300)

# Descriptive subtitle — the book's own framing
center('The voyage of the East Indiaman', f(reg, 54), 1290, fill=RULE)
center('to South Australia, 1839–1840', f(reg, 54), 1380, fill=RULE)

# Author
center('STEPHEN MICHAEL BARNETT', f(reg, 66), 1900, spacing=6)

# Imprint
center('TEN BRAT PRESS', f(reg, 44), H - 300, fill=FAINT, spacing=8)

img.save('images/cover.jpg', quality=92)
print('wrote images/cover.jpg', img.size)
