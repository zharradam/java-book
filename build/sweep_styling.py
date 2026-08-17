# Systematic styling sweep - markers only, words untouched.
# Each fix must apply exactly once or the script aborts.
import re, glob, subprocess, os, sys

FIXES = [
    # --- Family 1: stray ** inside italic spans (rendered literal *) ---
    ('06-java-leaves-london.md',
     'information: *“**Mr. Conigrave has taken',
     'information: *“Mr. Conigrave has taken'),
    ('06-java-leaves-london.md',
     "paid out 25 pounds on account. Lachlan, Sons, 16/9/1839.' *",
     "paid out 25 pounds on account. Lachlan, Sons, 16/9/1839.'*"),
    ('08-new-opportunities.md',
     'if they make immediate **application.*',
     'if they make immediate application.*'),
    ('08-new-opportunities.md',
     'on the subject of **emigration, especially in reference',
     'on the subject of emigration, especially in reference'),
    ('08-new-opportunities.md',
     'which had been recently sent home. *\n',
     'which had been recently sent home.*\n'),
    ('08-new-opportunities.md',
     'not time to get breakfast, **or in the bustle',
     'not time to get breakfast, or in the bustle'),
    ('08-new-opportunities.md',
     'want a little light, **but you cannot obtain a candle',
     'want a little light, but you cannot obtain a candle'),
    ('08-new-opportunities.md',
     'his first letter to Mr. Crocker, **of Truro, spoke favourable',
     'his first letter to Mr. Crocker, of Truro, spoke favourable'),
    # --- Family 2: bold/italic markers slipped mid-word ---
    ('06-java-leaves-london.md',
     'N**ovember 7th.** Coats',
     '**November 7th.** Coats'),
    ('06-java-leaves-london.md',
     '**On the 11t**h, his diary noted',
     '**On the 11th**, his diary noted'),
    ('06-java-leaves-london.md',
     'for the period 1**2th to 21st of November.**',
     'for the period **12th to 21st of November.**'),
    ('06-java-leaves-london.md',
     '**December 28th** S*trong gale and squally',
     '**December 28th** *Strong gale and squally'),
    ('06-java-leaves-london.md',
     '**February 3rd**. T*his day we got the first sight',
     '**February 3rd**. *This day we got the first sight'),
    # --- Family 3: standalone diary/letter quotes -> italic, per the
    #     book's convention for displayed quotations ---
    ('03-introduction.md',
     '"October 28th... more disturbances amongst us. I begin to have a very bad opinion of our Plymouth Emigrants, the greater part of them are Cornish people, and many of them are miners, they are a very uncouth and dissatisfied lot of people."',
     '*"October 28th... more disturbances amongst us. I begin to have a very bad opinion of our Plymouth Emigrants, the greater part of them are Cornish people, and many of them are miners, they are a very uncouth and dissatisfied lot of people."*'),
    ('06-java-leaves-london.md',
     '"Rain, stormy petrel showed an approaching storm."',
     '*"Rain, stormy petrel showed an approaching storm."*'),
    ('06-java-leaves-london.md',
     '"Vivid lightening (squalls) heavy sea, ship labouring a good deal, lost our breakfast 2 mornings, teapot and cups rolled off the table.**"**',
     '*"Vivid lightening (squalls) heavy sea, ship labouring a good deal, lost our breakfast 2 mornings, teapot and cups rolled off the table."*'),
    ('06-java-leaves-london.md',
     '"Mr. Bernard, gentn. passenger died 7a.m.. Committed to the deep 5p.m. The carpenter only bored holes in the foot of the coffin, which when thrown overboard whent off erect, never sank."',
     '*"Mr. Bernard, gentn. passenger died 7a.m.. Committed to the deep 5p.m. The carpenter only bored holes in the foot of the coffin, which when thrown overboard whent off erect, never sank."*'),
    ('06-java-leaves-london.md',
     '"The provisions doled out to the emigrants are too often of the most inferior quality',
     '*"The provisions doled out to the emigrants are too often of the most inferior quality'),
    ('06-java-leaves-london.md',
     'immediately got the ship under weigh and set sail."\n',
     'immediately got the ship under weigh and set sail."*\n'),
    ('09-another-java.md',
     '"Charles expressed to me that he was sorry he left Penshurst',
     '*"Charles expressed to me that he was sorry he left Penshurst'),
    ('09-another-java.md',
     'deceived by the Commissioners at the nourishment for children."',
     'deceived by the Commissioners at the nourishment for children."*'),
    ('15-holdfast-bay-or-port-misery.md',
     '“ No sleep all night got up',
     '*“ No sleep all night got up'),
    ('15-holdfast-bay-or-port-misery.md',
     'We did not go ashore before Saturday afternoon”',
     'We did not go ashore before Saturday afternoon”*'),
]

files = {}
for fname, old, new in FIXES:
    path = 'manuscript/' + fname
    if path not in files:
        files[path] = open(path, encoding='utf-8').read()
    n = files[path].count(old)
    if n != 1:
        sys.exit(f'ABORT: pattern occurs {n}x (need exactly 1) in {fname}: {old[:60]!r}')
    files[path] = files[path].replace(old, new)

for path, t in files.items():
    open(path, 'w', encoding='utf-8', newline='\n').write(t)
print(f'applied {len(FIXES)} fixes across {len(files)} files')

# verify word-for-word identity vs HEAD (markers stripped)
def words(t):
    t = re.sub(r'^#.*$', '', t, flags=re.M).replace('**', '').replace('*', '')
    return re.findall(r'[A-Za-z0-9]+', t)

ok = True
for path in files:
    old = subprocess.run(['git', 'show', 'HEAD:' + path],
                         capture_output=True, text=True, encoding='utf-8').stdout
    if words(old) != words(open(path, encoding='utf-8').read()):
        ok = False
        print('WORD MISMATCH in', path)
print('verbatim check:', 'PASS - zero word changes' if ok else 'FAIL')
