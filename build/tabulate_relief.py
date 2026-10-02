# Set the "Return of sick and destitute Emigrants" (ch. 7) as a table.
#
# The four column headings are the ones printed in the source. Every entry
# is carried across exactly as it stands, oddities included (the stray
# "HUSBAND'S", "1 8/3/40", "7/4/4", a period that ends before it begins).
# Aborts unless the letters and digits of the chapter are unchanged.
import re, sys

PATH = 'manuscript/07-medical-board-enquiry.md'
lines = open(PATH, encoding='utf-8').read().split('\n')

DATE = r'\d{1,2}/\d{1,2}/\d{1,2}'
ROW = re.compile(r'^(?P<name>.+?)\s+(?P<period>(?:\d\s)?' + DATE + r'\s*-\s*' + DATE + r')\s+(?P<num>\d+)(?:\s+(?P<remarks>.*))?$')

s = next(i for i, l in enumerate(lines) if re.match(r'^Name\s+Period of Relief\s+Numbers\s+Remarks\s*$', l))
e = max(i for i, l in enumerate(lines) if i > s and ROW.match(l))

# nothing but entries and blank lines may sit between the heading and the last entry
for l in lines[s + 1:e + 1]:
    if l.strip() and not ROW.match(l):
        sys.exit(f'ABORT: line inside the list is not an entry: {l[:80]!r}')

table = ['| Name | Period of Relief | Numbers | Remarks |',
         '|:----------------------|:----------------------|:-------:|:-----------------------------------------------|']
for l in lines[s + 1:e + 1]:
    m = ROW.match(l)
    if m:
        table.append(f"| {m['name']} | {m['period']} | {m['num']} | {(m['remarks'] or '').strip()} |")

new = lines[:s] + table + lines[e + 1:]
alnum = lambda t: re.sub(r'[^A-Za-z0-9]', '', t)
if alnum('\n'.join(lines)) != alnum('\n'.join(new)):
    sys.exit('ABORT: letters or digits changed')
open(PATH, 'w', encoding='utf-8', newline='\n').write('\n'.join(new))
withrem = sum(1 for r in table[2:] if not r.rstrip().endswith('|  |'))
print(f'{len(table) - 2} entries set as a table ({withrem} with remarks); letters and digits unchanged')
