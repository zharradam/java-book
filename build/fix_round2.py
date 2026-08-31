# Round 2 corrections (Michael's rulings, 2026-08-31).
#
# 1. Restore the duplicated passage in the Introduction — that is
#    Stephen's text and his call, not ours. Keep only the doubled-"the"
#    repair and add the missing space after the full stop.
# 2. Punctuate Stephen's new parenthetical correctly (marks only).
# 3. Fix the three genuine double commas in the manuscript.
import re, sys

EDITS = [
    # --- 1. Restore the duplication, keep the "the The" fix -----------
    ('03-introduction.md',
     'This then, is a true, sad tale of the emigrant ship, the "JAVA", which left Plymouth after leaving London. However, the deaths did not stop',
     'This then, is a true, sad tale of the emigrant ship, the "JAVA", which left Plymouth after leaving London, with approximately 500 passengers. '
     'It arrived at Holdfast Bay with 30 men, women and children having perished on the voyage. '
     'The greatest loss of life had been amongst the steerage passengers, particularly the children. '
     'However, the deaths did not stop'),
    # --- 2. Parenthetical: no comma before "(", stop outside ")" -------
    ('03-introduction.md',
     'passengers, (particularly true of the children who perished.)',
     'passengers (particularly true of the children who perished).'),
    # --- 3. Double commas ---------------------------------------------
    ('03-introduction.md',
     'on the 12th October, 1839, , the Java commenced',
     'on the 12th October, 1839, the Java commenced'),
    ('14-appendix-b-passenger-list.md',
     'Lightfoot, Candy, Harnagin,, Pleas ,McCanock,,E.Hailey,',
     'Lightfoot, Candy, Harnagin, Pleas, McCanock, E.Hailey,'),
]

files = {}
for fname, old, new in EDITS:
    path = 'manuscript/' + fname
    if path not in files:
        files[path] = open(path, encoding='utf-8').read()
    n = files[path].count(old)
    if n != 1:
        sys.exit(f'ABORT: pattern occurs {n}x (need exactly 1) in {fname}:\n  {old[:100]!r}')
    files[path] = files[path].replace(old, new)

for path, text in files.items():
    open(path, 'w', encoding='utf-8', newline='\n').write(text)
print(f'applied {len(EDITS)} edits across {len(files)} files')

# No double commas should remain anywhere.
import glob
left = []
for f in glob.glob('manuscript/*.md'):
    for m in re.finditer(r',\s*,', open(f, encoding='utf-8').read()):
        left.append(f)
print('double commas remaining:', len(left))
