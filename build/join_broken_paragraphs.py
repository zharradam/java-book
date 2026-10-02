# Rejoin sentences that were split into separate paragraphs by the line
# wrapping of the original blog text. No words change: the script aborts
# unless each file's letters and digits are identical before and after.
#
#   python build/join_broken_paragraphs.py            dry run, report only
#   python build/join_broken_paragraphs.py --apply    write the changes
#
# A paragraph is joined to the one before it only when the earlier one stops
# without closing punctuation AND one of:
#   (a) the later one begins with a lower-case letter;
#   (b) the earlier one ends on a word that cannot end a sentence ("by the");
#   (c) the pair is named in EXPLICIT below (continuations that begin with a
#       capital, confirmed by eye).
# Never joined: headings, tables, figures, the prayer (deliberate verse
# lines), anything opening with a quotation mark (a displayed extract after
# its introduction), and anything after a bare comma ("Sir,").
import re, glob, os, sys

APPLY = '--apply' in sys.argv
SKIP_FILES = {'17-prayer-of-remembrance.md'}
TERMINAL = set('.!?:;"”’)\']')
QUOTES = set('"“”‘\'')
STOP = set('''the a an of and to in by for with was were is are that which from on at her his their
 this as or be been had has have not but it its our my your who whom into upon than very so if when
 where while would could should will shall may might must under towards between through
 south gbp'''.split())

FORCED = {'03-introduction.md': ('In his definitive work', 'India, the Far East and Australia')}

# (file, how the earlier paragraph ends, how the later one begins)
EXPLICIT = [
    ('08-new-opportunities.md', 'This is the fourth letter', 'I have written'),
    ('08-new-opportunities.md', 'lay before your readers', "Mr. Hall's last letter"),
    ('14-appendix-b-passenger-list.md', 'December/January', '1987/88'),
    ('14-appendix-b-passenger-list.md', 'whose daughter', 'Caroline died at sea'),
    ('16-bibliography.md', 'Laurie, Norrie', '&Wilson'),
]

def special(p):
    s = p.lstrip()
    return s.startswith(('|', '#', '![', '---')) or not s

def bare_end(a):   return re.sub(r'[*_\s]+$', '', a)
def bare_start(b): return re.sub(r'^[*_\s]+', '', b)
def unfinished(a):
    t = bare_end(a)
    return bool(t) and t[-1] not in TERMINAL
def last_word(a):
    m = re.search(r"([A-Za-z']+)$", bare_end(a))
    return m.group(1).lower() if m else ''

def join(a, b):
    a, b = a.rstrip(), b.lstrip()
    if re.search(r'(?<!\*)\*$', a) and re.match(r'^\*(?!\*)', b):   # two italic runs -> one
        return a[:-1].rstrip() + ' ' + b[1:].lstrip()
    return a + ' ' + b

alnum = lambda t: re.sub(r'[^A-Za-z0-9]', '', t)
total, record = 0, []
for path in sorted(glob.glob('manuscript/*.md')):
    name = os.path.basename(path)
    if name in SKIP_FILES:
        continue
    text = open(path, encoding='utf-8').read()
    paras = re.split(r'\n[ \t]*\n', text)
    lo, hi = FORCED.get(name, (None, None))
    in_forced = False
    out, n = [], 0
    for p in paras:
        if lo and p.lstrip().startswith(lo):
            in_forced = True
        prev = out[-1] if out else None
        why = ''
        if prev is not None and not special(prev) and not special(p) and unfinished(prev):
            comma = bare_end(prev).endswith(',')
            start = bare_start(p)
            if any(f == name and bare_end(prev).endswith(a) and start.startswith(b) for f, a, b in EXPLICIT):
                why = 'named'
            elif start[:1] in QUOTES:
                why = ''
            elif start[:1].islower():
                why = 'lower-case start'
            elif not comma and last_word(prev) in STOP:
                why = 'ends on "' + last_word(prev) + '"'
            elif in_forced and not comma:
                why = 'Hackman passage'
        if why:
            record.append(f'{name}  [{why}]\n      ...{bare_end(prev)[-60:]}\n      + {bare_start(p)[:60]}...')
            out[-1] = join(prev, p); n += 1
        else:
            out.append(p)
        if hi and p.lstrip().startswith(hi):
            in_forced = False
    new = '\n\n'.join(out)
    if alnum(new) != alnum(text):
        sys.exit(f'ABORT {name}: letters or digits changed')
    if n:
        print(f'{name:44} {n:3} joins')
    total += n
    if APPLY and n:
        open(path, 'w', encoding='utf-8', newline='\n').write(new)

if APPLY:
    with open('docs/paragraph-joins.txt', 'w', encoding='utf-8', newline='\n') as f:
        f.write('Every paragraph join made by build/join_broken_paragraphs.py\n'
                'No words were changed; letters and digits verified identical per chapter.\n\n')
        f.write('\n'.join(record) + '\n')
print(f'{total} joins', 'applied; full list in docs/paragraph-joins.txt' if APPLY else '(dry run - nothing written)')
