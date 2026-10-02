# Convert the flattened Appendix B passenger rows into a proper table.
#
# Column placement (Male / Female / Child) for entries 3517-3561 is taken
# from Stephen's scan of the original page (IMG_20260912_0019), and every
# such row is cross-checked against the digits already in the manuscript.
# Entries after 3561 follow a stated rule (see QUERIES-FOR-STEPHEN.md).
import re, sys

PATH = 'manuscript/14-appendix-b-passenger-list.md'
lines = open(PATH, encoding='utf-8').read().split('\n')

# From the scan: which of Male/Female/Child are filled, keyed (emb no, first name token).
SCAN = {
 ('3517','RICHARD'):'MFC', ('3518','?'):'MFC', ('3519','JAS.'):'MF', ('3520','Wm.'):'MFC', ('3521',''):'',
 ('3522','ROBT.'):'MFC', ('3523','SAMSON'):'MFC', ('3524','ELIZABETH'):'F', ('3525','SAMSON'):'M', ('3526','JANE'):'F',
 ('3527','WILLIAM'):'MFC', ('3527','JOHN'):'M', ('3528','MAHALOE'):'M', ('3529','THOS.'):'MF', ('3530','ELIZA'):'F',
 ('3531','NICHOLAS'):'MFC', ('3532',''):'', ('3533','RICHD.'):'MFC', ('3534','WM.'):'MFC', ('3535','WM.'):'M',
 ('3536','THOS.'):'M', ('3537','JOSEPH'):'MFC', ('3538','JAMES'):'M', ('3539','JOSEPH'):'M', ('3540','WM.'):'M',
 ('3541','JOHN'):'MFC', ('3542','JANE'):'F', ('3543','JAS.'):'MFC', ('3544','RICH.'):'MFC', ('3545','GEO.'):'MF',
 ('3546','JOHN'):'MFC', ('3547','WM.'):'MFC', ('3548','JAS.'):'MF', ('3549','ELIZA'):'F', ('3550','THOS.'):'MFC',
 ('3551','JOHN'):'MFC', ('3552','ROBERT'):'MFC', ('3553','ANNA'):'F', ('3554','JAMES'):'MFC', ('3555','WM.'):'MFC',
 ('3556','JAMES'):'MFC', ('3557','WM.'):'MFC', ('3558','RICHD.'):'MF', ('3559','JOHN'):'M', ('3560','BENJAMIN'):'MFC',
 ('3561','GRACE'):'FC',
}
FEMALE = {'MARY','ELIZABETH','ELIZA','ELIZ','JANE','ANN','ANNE','ANNA','GRACE','SARAH','MARGARET','HELEN','CATHERINE',
 'CATH','MARIA','HANNAH','SUSAN','SUSANNAH','MARTHA','JOANNA','CHARLOTTE','EMMA','HARRIET','FANNY','ELLEN','LOUISA',
 'JEMIMA','PHILIPPA','PHILLIPA','PHILIPIA','AMELIA','ALICE','AGNES','BETSY','KITTY','NANCY','HONOR','JENEFER',
 'CHRISTIANA','DOROTHY','LYDIA','ISABELLA','MRS','ELINOR','ELEANOR','RACHEL','REBECCA','ESTHER','PRISCILLA',
 'THOMASINA','MATILDA','SALLY','CONSTANCE','MGT','EMILY','JEMINA'}

ROW = re.compile(r'^3[5-9]\d\d\)?( |$)')
DATE = re.compile(r'^\d{1,2}/\d{1,2}/\d{2}$')

start = next(i for i, l in enumerate(lines) if l.strip() == 'EMBARKATION')
rows_idx = [i for i, l in enumerate(lines) if ROW.match(l)]
end = rows_idx[-1]
block = lines[start:end + 1]

# a date that wrapped onto its own line ("Pays own" / "passage 16/5/39")
merged = []
for l in block:
    if l.strip() == 'passage 16/5/39':
        j = len(merged) - 1
        while merged[j] == '':
            j -= 1
        merged[j] += ' passage 16/5/39'
        continue
    merged.append(l)
raw = [l for l in merged if ROW.match(l)]

out = []
stats = {'scan': 0, 'rule3': 0, 'rule2': 0, 'rule1F': 0, 'rule1M': 0, 'blank': 0, 'none': 0}
used = set()
for l in raw:
    tok = l.split(); emb = tok[0]; rest = tok[1:]
    date = app = ''
    if rest and DATE.match(rest[-1]):
        date = rest.pop()
    if len(rest) >= 3 and rest[-3:] == ['Pays', 'own', 'passage']:
        date = 'Pays own passage ' + date; rest = rest[:-3]
    if rest and re.fullmatch(r'\d{4}', rest[-1]):
        app = rest.pop()
    counts = []
    while rest and re.fullmatch(r'\d{1,2}', rest[-1]):
        counts.insert(0, rest.pop())
    ship = 'JAVA' if 'JAVA' in rest else ''
    src = 'BISA' if 'BISA' in rest else ''
    name = ' '.join(t for t in rest if t not in ('JAVA', 'BISA'))
    first = name.split()[0] if name else ''
    key = (emb, first)
    M = F = C = ''
    if key in SCAN:
        pat = SCAN[key]; used.add(key)
        if len(pat) != len(counts):
            sys.exit(f'ABORT: scan says {pat!r} but manuscript has {len(counts)} figures: {l!r}')
        for p, v in zip(pat, counts):
            if p == 'M': M = v
            elif p == 'F': F = v
            else: C = v
        stats['scan'] += 1
    elif len(counts) == 3:
        M, F, C = counts; stats['rule3'] += 1
    elif len(counts) == 2:
        M, F = counts; stats['rule2'] += 1
    elif len(counts) == 1:
        if re.sub(r'[^A-Z]', '', first.upper()) in FEMALE:
            F = counts[0]; stats['rule1F'] += 1
        else:
            M = counts[0]; stats['rule1M'] += 1
    elif not name:
        stats['blank'] += 1
    else:
        stats['none'] += 1
    out.append(f'| {emb} | {name} | {ship} | {src} | {M} | {F} | {C} | {app} | {date} |')

missing = [k for k in SCAN if k not in used]
if missing:
    sys.exit(f'ABORT: scan rows not matched in manuscript: {missing}')

table = [
    'The Male, Female and Child columns give the number of applicants in each class.', '',
    '| Emb. No. | Name of applicant | Ship | Source | Male | Female | Child | App. No. | Date |',
    # dash counts set the relative column widths (Pandoc pipe-table rule)
    '|-------:|:------------------------------|:------|:-------|-----:|------:|-----:|-------:|:-------------|',
] + out

new = lines[:start] + table + lines[end + 1:]
text = '\n'.join(new).replace('applications for free\n\npassage and matched',
                              'applications for free passage and matched')
open(PATH, 'w', encoding='utf-8', newline='\n').write(text)
print(f'rows: {len(out)}   ' + '  '.join(f'{k}={v}' for k, v in stats.items()))
