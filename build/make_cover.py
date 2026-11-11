# Generate the photographic covers: images/cover.jpg (book, 1600x2560) and
# images/cover-square.jpg (audiobook, 2400x2400 as audiobook stores ask) and
# images/cover-pdf.jpg (the PDF, A4 proportions).
#
# The photograph is Fildes 637, p.80, Victoria University of Wellington Library,
# used by permission; see PERMISSIONS.md. Sky and sea are extended beyond its
# edges and darkened behind the lettering.
#
# Title and author are set in IM Fell English SC (build/fonts, SIL Open Font
# License) and cast in the same copper-gold as the title on theshipjava.uk.
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageFilter, ImageOps

CREAM = (247, 242, 230)
FAINT = (205, 198, 180)
FELL = 'build/fonts/IMFellEnglishSC.ttf'
PHOTO = 'images/hulk-gibraltar-fildes.jpg'

# Copper to gold, matching the .gilt gradient on the website
GILT = [(0, (122, 67, 24)), (.18, (201, 138, 69)), (.30, (247, 226, 166)), (.42, (215, 160, 79)), (.58, (143, 82, 32)),
        (.74, (233, 189, 112)), (.82, (249, 231, 180)), (1, (154, 91, 34))]

def f(name, size):
    return ImageFont.truetype(f'C:/Windows/Fonts/{name}', size)

reg, ital = 'georgia.ttf', 'georgiai.ttf'

def backdrop(W, H, top, fade, dark_sky, dark_sea):
    """The photograph at full width from y=top, with sky above it, mirrored open water below it, darkened."""
    src = Image.open(PHOTO).convert('L')
    w, h = src.size
    src = src.crop((int(w * .012), int(h * .012), int(w * .988), int(h * .988)))
    ph = round(W * src.height / src.width)
    photo = src.resize((W, ph), Image.LANCZOS)
    c = photo.crop((0, 0, W, 12)).filter(ImageFilter.GaussianBlur(40)).resize((W, H), Image.BICUBIC)
    m = Image.new('L', (W, ph), 255)
    md = ImageDraw.Draw(m)
    for y in range(fade):
        md.line([(0, y), (W, y)], fill=int(255 * y / fade))
    c.paste(photo, (0, top), m)
    overlap = W * 90 // 1600
    need = H - top - ph + overlap
    if need > overlap:
        assert need < ph * .36   # the hull ends about 62% down: mirror only open water
        sea = ImageOps.flip(photo.crop((0, ph - need, W, ph)))
        m = Image.new('L', sea.size, 255)
        md = ImageDraw.Draw(m)
        for y in range(overlap):
            md.line([(0, y), (W, y)], fill=int(255 * y / overlap))
        c.paste(sea, (0, top + ph - overlap), m)
    c = ImageChops.add(c, Image.effect_noise((W, H), 5).point(lambda v: max(0, v - 128)))   # hides banding in the sky
    img = ImageOps.colorize(c, (16, 18, 22), (238, 234, 224))
    shade = Image.new('L', (W, H))
    sd = ImageDraw.Draw(shade)
    for y in range(H):
        v = .66 * max(0, 1 - y / dark_sky) + .92 * min(1, max(0, (y - dark_sea) / (H * .117)))
        sd.line([(0, y), (W, y)], fill=int(min(.88, v) * 255))
    return Image.composite(Image.new('RGB', (W, H), (14, 24, 34)), img, shade)

def cover(W, H, s, photo, y, path):
    """Draw the cover at W x H; s scales sizes, y holds each line's top edge."""
    img = backdrop(W, H, **photo)
    d = ImageDraw.Draw(img)
    S = lambda n: round(n * s)

    def center(text, fnt, top, fill=CREAM, spacing=0, draw=d):
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
        shadow = mask.filter(ImageFilter.GaussianBlur(depth * 2)).point(lambda v: int(v * .6))
        img.paste((0, 0, 0), (0, depth * 3), shadow)
        for dy, col in ((depth, (75, 40, 13)), (depth * 5 // 8, (92, 50, 17)), (depth * 3 // 8, (110, 61, 21))):
            img.paste(col, (0, dy), mask)
        img.paste(grad, (0, 0), mask)

    gilt('Java', ImageFont.truetype(FELL, S(330)), y['title'], S(40), S(8))
    center('The Sailing Ship', f(ital, S(82)), y['ship'])
    center('1811–1940', f(ital, S(82)), y['dates'])
    center('The voyage of the East Indiaman', f(reg, S(48)), y['sub1'])
    center('to South Australia, 1839–1840', f(reg, S(48)), y['sub2'])
    gilt('Stephen Michael Barnett', ImageFont.truetype(FELL, S(96)), y['author'], S(6), S(4))
    center('TEN BRAT PRESS', f(reg, S(38)), y['imprint'], fill=FAINT, spacing=S(8))

    img.save(path, quality=92)
    print('wrote', path, img.size)

cover(1600, 2560, 1, dict(top=1140, fade=420, dark_sky=1100, dark_sea=1880),
      dict(title=120, ship=560, dates=675, sub1=2030, sub2=2098, author=2200, imprint=2400),
      'images/cover.jpg')

# Same design tightened to fit a square: the photograph alone reaches the foot
cover(2400, 2400, 1.06, dict(top=680, fade=500, dark_sky=950, dark_sea=1720),
      dict(title=20, ship=455, dates=550, sub1=1880, sub2=1950, author=2070, imprint=2260),
      'images/cover-square.jpg')

# A4 proportions, so the PDF's cover page fills edge to edge
cover(1810, 2560, 1, dict(top=1140, fade=420, dark_sky=1100, dark_sea=1880),
      dict(title=120, ship=560, dates=675, sub1=2030, sub2=2098, author=2200, imprint=2400),
      'images/cover-pdf.jpg')
