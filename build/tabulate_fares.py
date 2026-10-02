# Set the two scales of children's fares (regulations 47 and 48, ch. 5) as
# tables. They sit inside the quoted regulations, so each table is marked as
# part of the extract (">") and stays indented with it. No headings are added:
# the source has none. Words after the last fare stay as running text.
# Aborts unless the chapter's letters and digits are unchanged.
import re, sys

PATH = 'manuscript/05-emigrants-to-south-australia-1839.md'
text = open(PATH, encoding='utf-8').read()
paras = re.split(r'\n[ \t]*\n', text)

def fare(p):
    """'*Two, and under six 5/-*'  ->  ('Two, and under six', '5/-', rest)"""
    s = p.strip().strip('*').strip()
    m = re.match(r'^(.*?)\s+(no charge|\d+/-)(.*)$', s)
    return (m.group(1), m.group(2), m.group(3).strip()) if m else None

def table(rows):
    return '\n'.join(['> |  |  |', '> |:---|:---|'] + [f'> | {a} | {b} |' for a, b in rows])

out, i, made = [], 0, 0
while i < len(paras):
    p = paras[i]
    if p.strip().strip('*').startswith('Under two years of age'):
        rows, tail = [], ''
        while i < len(paras):
            f = fare(paras[i])
            if not f or not re.match(r'^(Under|Two|Six|Seven)\b', f[0]):
                break
            rows.append((f[0], f[1])); tail = f[2]; i += 1
            if tail:
                break
        out.append(table(rows))
        if tail:
            out.append('*' + tail + '*')
        made += 1
        continue
    out.append(p); i += 1

new = '\n\n'.join(out)
alnum = lambda t: re.sub(r'[^A-Za-z0-9]', '', t)
if made != 2:
    sys.exit(f'ABORT: expected 2 fare scales, found {made}')
if alnum(new) != alnum(text):
    sys.exit('ABORT: letters or digits changed')
open(PATH, 'w', encoding='utf-8', newline='\n').write(new)
print(f'{made} fare scales set as tables; letters and digits unchanged')
