# The sentence breaks that the general rule in join_broken_paragraphs.py
# deliberately would not touch (a comma followed by a capital could be a
# salutation), found by scanning the finished PDF and confirmed by eye.
# No words change. Aborts unless letters and digits are identical afterwards,
# with one declared exception: the orphaned "1846," in the bibliography.
import re, sys

def norm(s):
    for a, b in (('“', '"'), ('”', '"'), ('‘', "'"), ('’', "'")):
        s = s.replace(a, b)
    return s

def bare_end(a):   return re.sub(r'[*_\s]+$', '', a)
def bare_start(b): return re.sub(r'^[*_\s]+', '', b)

def join(a, b):
    a, b = a.rstrip(), b.lstrip()
    if re.search(r'(?<!\*)\*$', a) and re.match(r'^\*(?!\*)', b):
        return a[:-1].rstrip() + ' ' + b[1:].lstrip()
    return a + ' ' + b

# (file, how the earlier paragraph ends, how the later one begins)
PAIRS = [
    ('05-emigrants-to-south-australia-1839.md', 'and Tinmen, Smiths,', 'Shipwrights, Boat-builders'),
    ('05-emigrants-to-south-australia-1839.md', 'Cabinetmakers, Coopers,', 'Curriers, Farriers'),
    ('08-new-opportunities.md', 'esteem to father,', '&c. &c. &c.'),
    ('08-new-opportunities.md', 'a grave deep enough in the ocean;', 'and should you reach the land'),
    ('08-new-opportunities.md', 'meat, 9d. per lb;', 'potatoes, 3d. per lb.'),
    ('10-java-after-1840.md', '"Thomas Coutts",', '"Abercrombie Robinson"'),
    ('14-appendix-b-passenger-list.md', 'and five children,', 'James Pearce and wife'),
    ('14-appendix-b-passenger-list.md', 'Mrs Harding, Mr(?)', 'Mitchell and 460'),
    ('16-bibliography.md', 'Idealists of 1836-1846,', 'Adelaide, Rigby'),
    ('17-prayer-of-remembrance.md', 'journeyed across the seas', 'to the uttermost parts'),
    ('17-prayer-of-remembrance.md', 'in the face of sickness and', 'death, their determination'),
    ('17-prayer-of-remembrance.md', 'prepared to undertake', 'and their contribution'),
]
alnum = lambda t: re.sub(r'[^A-Za-z0-9]', '', t)
files = sorted({p[0] for p in PAIRS})
for name in files:
    path = 'manuscript/' + name
    text = open(path, encoding='utf-8').read()
    paras = re.split(r'\n[ \t]*\n', text)
    done = 0
    for _, a, b in [p for p in PAIRS if p[0] == name]:
        hits = [i for i in range(len(paras) - 1)
                if norm(bare_end(paras[i])).endswith(a) and norm(bare_start(paras[i + 1])).startswith(b)]
        if not hits and (a + ' ' + b) in re.sub(r'[*_\s]+', ' ', norm('\n\n'.join(paras))):
            continue                      # already joined on an earlier run
        if len(hits) != 1:
            sys.exit(f'ABORT {name}: {a!r} + {b!r} matched {len(hits)} times')
        i = hits[0]
        paras[i:i + 2] = [join(paras[i], paras[i + 1])]
        done += 1

    expected_loss = ''
    if name == '14-appendix-b-passenger-list.md':
        # pictures were placed inside a broken sentence: move them below it
        i = next((k for k, p in enumerate(paras) if norm(bare_end(p)).endswith('Jnr., Laura,')), None)
        if i is not None:                 # None = already moved on an earlier run
            j = i + 1
            while paras[j].lstrip().startswith('!['):
                j += 1
            if j == i + 1 or not paras[j].lstrip().startswith('George and Cyrus'):
                sys.exit('ABORT ch14: pictures / continuation not where expected')
            figures = paras[i + 1:j]
            paras[i:j + 1] = [join(paras[i], paras[j])] + figures
            done += 1
    if name == '16-bibliography.md':
        k = [i for i, p in enumerate(paras) if p.strip() == '1846,']
        if len(k) > 1:
            sys.exit(f'ABORT ch16: orphan "1846," found {len(k)} times')
        if k:                             # none = already removed on an earlier run
            del paras[k[0]]
            expected_loss = '1846'
            done += 1

    new = '\n\n'.join(paras)
    # pictures may move, so compare the prose and the pictures separately
    def split(t):
        ps = re.split(r'\n[ \t]*\n', t)
        return (alnum(''.join(p for p in ps if not p.lstrip().startswith('!['))),
                sorted(p.strip() for p in ps if p.lstrip().startswith('![')))
    (before, figs_before), (after, figs_after) = split(text), split(new)
    if figs_before != figs_after:
        sys.exit(f'ABORT {name}: a picture or its caption changed')
    if expected_loss:
        if len(before) - len(after) != len(expected_loss) or before.count('1846') - after.count('1846') != 1:
            sys.exit(f'ABORT {name}: more than the orphan changed')
    elif before != after:
        sys.exit(f'ABORT {name}: letters or digits changed')
    open(path, 'w', encoding='utf-8', newline='\n').write(new)
    print(f'{name:44} {done} repairs' + ('  (orphaned "1846," removed)' if expected_loss else ''))
