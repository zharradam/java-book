# Set the crew list (ch. 11) and the Emigration Office return (ch. 6) as tables.
#
# Purely positional: every word and figure stays in the order it was printed.
# Only the leader dots ("... ... ...") are dropped - they are alignment filler,
# which the table now does. No column meanings are asserted that the source
# does not give: the trades table keeps its printed heading whole and leaves
# the figure columns unlabelled. Aborts unless the letters and digits of each
# file are identical before and after.
import re, sys

def alnum(t):
    return re.sub(r'[^A-Za-z0-9]', '', t)

def swap(path, start_pred, end_pred, build):
    lines = open(path, encoding='utf-8').read().split('\n')
    s = next(i for i, l in enumerate(lines) if start_pred(l))
    e = next(i for i, l in enumerate(lines) if i >= s and end_pred(l))
    block = [l for l in lines[s:e + 1] if l.strip()]
    new = lines[:s] + build(block) + lines[e + 1:]
    before, after = '\n'.join(lines), '\n'.join(new)
    if alnum(before) != alnum(after):
        a, b = alnum(before), alnum(after)
        i = next((k for k, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
        sys.exit(f'ABORT {path}: text changed near ...{a[max(0,i-40):i+40]} / ...{b[max(0,i-40):i+40]}')
    open(path, 'w', encoding='utf-8', newline='\n').write(after)
    print(f'{path}: {len(block)} lines -> table, letters and digits unchanged')

# ---------------------------------------------------------------- crew list
def crew(block):
    rows = []
    tail = ''
    for l in block:
        m = re.match(r'^(.*?)\s+(1st Mate|2nd Mate|3rd Mate|4th Mate|Surgeon|Carpenter|Boatswain)(.*)$', l)
        if not m:
            sys.exit(f'ABORT: unrecognised crew line {l!r}')
        rows.append(f'| {m.group(1)} | {m.group(2)} |')
        tail = m.group(3).strip() or tail
    out = ['| | |', '|:---|:---|'] + rows
    if tail:
        out += ['', tail]
    return out

swap('manuscript/11-crew-list-1840.md',
     lambda l: l.startswith('J.H.Bird'),
     lambda l: l.startswith('Thomas Johnson'),
     crew)

# ------------------------------------------------- Emigration Office return
RETURN = [
    '|  | Adults | Male | Female | Total |',
    '|---:|:---|---:|---:|---:|',
    '| 180 | Married | 90 | 90 | 180 |',
    '| 75 | Single | 36 | 39 | 75 |',
    '|  | Children: |  |  |  |',
    '| 5 | 14 years and under 15 | 5 | 5 |  |',
    '| 41 | 7 years and under 14 | 18 | 23 |  |',
    '| 80 | 1 years and under 7 | 41 | 39 |  |',
    '| 32 | Under 1 yr. not counted | 23 | 9 |  |',
    '| 37 |  |  |  |  |',
    '| 413 | Adults 307 |  |  |  |',
]

def returns(block):
    i = next(k for k, l in enumerate(block) if l.startswith('CLASSIFIED LIST'))
    trades = ['| ' + block[i] + ' |  |  |  |', '|:---|---:|---:|---:|']
    for l in block[i + 1:]:
        tok = [t for t in l.split() if not re.fullmatch(r'\.+', t)]
        tok = [re.sub(r'\.+$', '', t) if not t[0].isdigit() and t.endswith('..') else t for t in tok]
        figs = [t for t in tok if re.fullmatch(r'\d+', t)]
        label = ' '.join(t for t in tok if not re.fullmatch(r'\d+', t))
        cells = figs + [''] * (3 - len(figs))
        trades.append(f'| {label} | ' + ' | '.join(cells) + ' |')
    return RETURN + [''] + trades

swap('manuscript/06-java-leaves-london.md',
     lambda l: l.strip() == 'Adults Male Female Total',
     lambda l: l.strip() == '90 35 36',
     returns)
