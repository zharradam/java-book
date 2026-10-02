# Best-guess repairs to the relief return (ch. 7), made at Michael's request
# on 29 September 2026 and listed in QUERIES-FOR-STEPHEN.md for confirmation.
# Unlike the earlier passes these DO alter characters, so each is logged.
import re, sys

PATH = 'manuscript/07-medical-board-enquiry.md'
text = open(PATH, encoding='utf-8').read()
lines = text.split('\n')
log = []

def change(i, new, why):
    log.append((lines[i], new, why)); lines[i] = new

for i, l in enumerate(lines):
    if not l.startswith('| '):
        continue
    n = l
    # a correction note for "husbands" that was pasted into the text
    n = n.replace("husbands HUSBAND'Sillness.", 'husbands illness.')
    n = re.sub(r"\s*HUSBAND'S(?=\s*\|\s*$)", '', n)
    if n != l:
        change(i, n, "stray HUSBAND'S removed")

EXACT = [
    ('| Bennett Johns | 1 8/3/40 - 13/5/40 |', '| Bennett Johns | 18/3/40 - 13/5/40 |', 'space inside the date closed up'),
    ('| Thomas Chanter | 31/3/40 - 7/4/4 |',   '| Thomas Chanter | 31/3/40 - 7/4/40 |',  'year completed: every date in the return is 1840'),
    ('| Robert Dunstan | 27/5/40-11/6/40 |',   '| Robert Dunstan | 27/5/40 - 11/6/40 |', 'spacing made consistent'),
]
for old, new, why in EXACT:
    hits = [i for i, l in enumerate(lines) if l.startswith(old)]
    if len(hits) != 1:
        sys.exit(f'ABORT: {old!r} matched {len(hits)}x')
    change(hits[0], new + lines[hits[0]][len(old):], why)

out = '\n'.join(lines)
if "HUSBAND'S" in out:
    sys.exit("ABORT: a HUSBAND'S remains")
open(PATH, 'w', encoding='utf-8', newline='\n').write(out)

for old, new, why in log:
    name = old.split('|')[1].strip()
    print(f'{name:18} {why}')
print(f'{len(log)} rows changed')

with open('docs/conversion-log.txt', 'a', encoding='utf-8', newline='\n') as f:
    f.write('\n--- Relief return: best-guess repairs (29 Sep 2026, to be confirmed by Stephen) ---\n')
    for old, new, why in log:
        f.write(f'{why}\n   was: {old}\n   now: {new}\n')
