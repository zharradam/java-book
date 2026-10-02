# Apply the image credits Stephen supplied on 29 September 2026.
# Each credit is keyed on the image file; the italic credit at the end of
# that figure's caption is replaced. Every image must match exactly once.
import re, glob, sys

CREDITS = {
    'portrait-william-frederick-richards.jpg': 'Courtesy of Glenda Richards.',
    'portrait-william-richards-1819.jpg':      'Courtesy of Glenda Richards.',
    'poster-free-emigration-java.jpg':         'State Library of South Australia, D 6029(L).',
    'sailing-card-java-1839.jpg':              'Courtesy of Leila Conigrave.',
    'engraving-between-decks.jpg':             'Courtesy of Don Charlwood.',
    'engraving-emigrant-family.jpg':           'Courtesy of Don Charlwood.',
    'hulk-stern-java-london.jpg':              'Photograph courtesy of Peter Staveley, R.N.',
    'hulk-starboard-bow-sepia.jpg':            'Photograph courtesy of Peter Staveley, R.N.',
    'hulk-port-broadside.jpg':                 'Photograph courtesy of Peter Staveley, R.N.',
    'portrait-thomasina-crowle.jpg':           'Barnett family collection.',
}

texts = {p: open(p, encoding='utf-8').read() for p in glob.glob('manuscript/*.md')}
for fname, credit in CREDITS.items():
    pat = re.compile(r'\*[^*\n]*\*(\]\(images/' + re.escape(fname) + r'\))')
    hits = [(p, len(pat.findall(t))) for p, t in texts.items() if pat.search(t)]
    if len(hits) != 1 or hits[0][1] != 1:
        sys.exit(f'ABORT: {fname} matched {hits}')
    p = hits[0][0]
    texts[p] = pat.sub('*' + credit + r'*\1', texts[p])
    print(f'{fname:44} -> {credit}')
for p, t in texts.items():
    open(p, 'w', encoding='utf-8', newline='\n').write(t)

left = [m for t in texts.values() for m in re.findall(r'\*[^*\n]*to be confirmed[^*\n]*\*\]\(images/([^)]+)\)', t)]
print('still unconfirmed:', left)
