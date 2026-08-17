# One-off cleanup: remove phantom bullet artifacts left by the Blogger
# conversion (empty italic paragraphs became lone "*" lines = empty
# Markdown list items). Verifies word-for-word identity against git HEAD.
import re, glob, subprocess, os

changed = {}
for f in glob.glob('manuscript/*.md'):
    t = open(f, encoding='utf-8').read()
    orig = t
    t = re.sub(r'^\*\s*$\n?', '', t, flags=re.M)   # lone "*" lines
    t = re.sub(r'^\* (\*)', r'\1', t, flags=re.M)  # stray "* " before an italic para
    t = re.sub(r'\n{3,}', '\n\n', t)
    if t != orig:
        open(f, 'w', encoding='utf-8', newline='\n').write(t)
        changed[f] = orig.count('\n') - t.count('\n')

for f, n in sorted(changed.items()):
    print(f'{f}: removed {n} junk lines')

def words(t):
    t = re.sub(r'^#.*$', '', t, flags=re.M).replace('**', '').replace('*', '')
    return re.findall(r'[A-Za-z0-9]+', t)

ok = True
for f in changed:
    path = f.replace(os.sep, '/')
    old = subprocess.run(['git', 'show', 'HEAD:' + path],
                         capture_output=True, text=True, encoding='utf-8').stdout
    if words(old) != words(open(f, encoding='utf-8').read()):
        ok = False
        print('WORD MISMATCH in', f)
print('verbatim check:', 'PASS - zero word changes' if ok else 'FAIL')
