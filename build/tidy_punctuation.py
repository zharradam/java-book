# Mechanical punctuation tidy — spacing and markers only, no words changed.
#
# Deliberately NOT touched:
#   * Run-together initials (J.H.Bird, W.H.Coates, A.W.Reed). Stephen sets
#     initials this way consistently; it is his style, not an error.
#   * "Through ,Jesus Christ, Our Lord" in the prayer — the fix there is to
#     delete a comma, not move it, which is an editorial decision for him.
#   * "3518 ? JAS. BIRELL" in the passenger list — the "?" stands in for an
#     unknown name.
#   * Ellipses in the tabulated trades/passenger lists ("Bakers ... ... 2")
#     and inside quotations ("...the reply was").
import re, glob, os, sys

# Protect the cases that must survive the generic rules untouched.
GUARDS = {
    'Through ,Jesus Christ': '\x00GUARD_PRAYER\x00',
    '3518 ? JAS. BIRELL':    '\x00GUARD_UNKNOWN\x00',
}

# (pattern, replacement, label) — applied in order.
RULES = [
    (r'[ \t]+,',              ',',      'space before comma'),
    (r',(?=[A-Za-z])',        ', ',     'missing space after comma'),
    (r'[ \t]+([;:?!])',       r'\1',    'space before ; : ? !'),
    (r'([a-z])[ \t]+\.(?!\.)', r'\1.',  'space before full stop'),
    (r'\([ \t]+',             '(',      'space after opening paren'),
    (r'[ \t]+\)',             ')',      'space before closing paren'),
]

# Individually judged one-offs.
LITERALS = [
    # Emphasis span opening one character late (same slip as S*trong/T*his).
    ('07-medical-board-enquiry.md', 'I*n consequence of', '*In consequence of'),
    ('07-medical-board-enquiry.md', 'I*n reference to',   '*In reference to'),
    # Sentence boundaries with no space.
    ('05-emigrants-to-south-australia-1839.md', 'on the "JAVA".This item', 'on the "JAVA". This item'),
    ('10-java-after-1840.md', 'East Indiamen".Coates, writing', 'East Indiamen". Coates, writing'),
    # Titles run into the following name (initials elsewhere are left alone).
    ('02-acknowledgements.md', 'thanks go to Dr.J.M.Tregenza', 'thanks go to Dr. J.M.Tregenza'),
    ('07-medical-board-enquiry.md', 'an application by Mr.Ward', 'an application by Mr. Ward'),
    ('08-new-opportunities.md', 'his profession at Mrs.Bathgates', 'his profession at Mrs. Bathgates'),
    ('14-appendix-b-passenger-list.md', 'Mr.J Crews', 'Mr. J Crews'),
    # Stray full stop after a comma.
    ('14-appendix-b-passenger-list.md', 'R.L Low,.Mrs S.Downs', 'R.L Low, Mrs S.Downs'),
    # Date run into the comma.
    ('01-preface.md', 'on February 6th,1840', 'on February 6th, 1840'),
]

changes = []

def apply_literals(name, text):
    for fname, old, new in LITERALS:
        if fname != name:
            continue
        if text.count(old) != 1:
            sys.exit(f'ABORT: {name}: literal not found exactly once: {old!r}')
        text = text.replace(old, new)
        changes.append((name, 'one-off', old, new))
    return text

for path in sorted(glob.glob('manuscript/*.md')):
    name = os.path.basename(path)
    original = open(path, encoding='utf-8').read()
    text = original

    text = apply_literals(name, text)
    for phrase, token in GUARDS.items():
        text = text.replace(phrase, token)

    for pat, repl, label in RULES:
        def record(m):
            out = m.expand(repl) if '\\' in repl else repl
            changes.append((name, label, m.group(0), out))
            return out
        text = re.sub(pat, record, text)

    for phrase, token in GUARDS.items():
        text = text.replace(token, phrase)

    if text != original:
        open(path, 'w', encoding='utf-8', newline='\n').write(text)

by_label = {}
for name, label, old, new in changes:
    by_label.setdefault(label, []).append((name, old, new))
total = 0
for label, items in sorted(by_label.items()):
    print(f'{len(items):3}  {label}')
    total += len(items)
print(f'{total:3}  TOTAL changes')
