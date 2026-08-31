# Port Stephen's Ninth Edition content edits onto the clean Markdown.
#
# Stephen edited a copy of his own original document, so his RTF also
# re-introduces the formatting artifacts we had already fixed (soft-hyphen
# characters, spaces after opening quote marks, the de-tabulated Masters
# and Owners list). We therefore port his CONTENT changes across rather
# than adopting his file, keeping both his edits and our styling work.
#
# Every replacement must match exactly once or the script aborts.
import re, os, sys

EDITS = [
    # --- Preface -----------------------------------------------------
    ('01-preface.md', '# Preface to the Eighth Edition',
                      '# Preface to the Ninth Edition'),
    ('01-preface.md', 'and the author the reunion exceeded expectations and attracted well with over 200',
                      'and the author, the reunion exceeded expectations and attracted well over 200'),
    ('01-preface.md', 'Glenda,had come into possession',
                      'Glenda, had come into possession'),
    ('01-preface.md', 'her great, great,  great,grandfather  however on further investigation about George Richards diary,the likelihood',
                      'her great, great, great, grandfather, however, on further investigation about George Richards diary, the likelihood'),
    ('01-preface.md', 'William Richards. However, as the diary\'s authorship',
                      'William Richards. Nevertheless, as the diary\'s authorship'),
    ('01-preface.md', 'I will simply refer to it as the Richard\'s Diary.',
                      'I will simply regard it as the Richards Diary.'),
    # --- Acknowledgements --------------------------------------------
    ('02-acknowledgements.md', 'who sailed on another shipcalled "Java"',
                               'who sailed on another ship called "Java"'),
    # --- Introduction -------------------------------------------------
    ('03-introduction.md', 'in 1839 this book\\]will show why',
                           'in 1839 this book will show why'),
    ('03-introduction.md', 'however 30 men,women and children perished',
                           'however 30 men, women and children perished'),
    ('03-introduction.md', 'passengers. This is particularly true of the children.',
                           'passengers, (particularly true of the children who perished.)'),
    # Query 4: the figures were stated twice in consecutive paragraphs.
    # Drop the three restating sentences; keep every unique fact and fix
    # the doubled "the". "However" now contrasts with the paragraph above.
    ('03-introduction.md',
     'This then is a true, sad tale of the emigrant ship, the "JAVA", which left Plymouth after leaving London, with approximately 500 passengers. It arrived at Holdfast Bay with 30 men, women and children having perished on the voyage. The greatest loss of life had been amongst the steerage passengers, particularly the children.However, the The deaths did not stop',
     'This then, is a true, sad tale of the emigrant ship, the "JAVA", which left Plymouth after leaving London. However, the deaths did not stop'),
    ('03-introduction.md', '(in The Seafarers series), bythe editors',
                           '(in The Seafarers series), by the editors'),
    # --- Migration ------------------------------------------------------
    # Query 8: mismatched bracket.
    ('04-migration-to-south-australia.md', 'were &lt;at the time) ascribed',
                                           'were (at the time) ascribed'),
    # --- Emigrants to South Australia -----------------------------------
    ('05-emigrants-to-south-australia-1839.md', 'as servants to ladies going as cabinpassengers',
                                                'as servants to ladies going as cabin passengers'),
    ('05-emigrants-to-south-australia-1839.md', 'New South Wales and Van Dieman’s Land',
                                                'New South Wales and Van Diemen’s Land'),
    ('05-emigrants-to-south-australia-1839.md', 'many were encouraged to applyfor passage',
                                                'many were encouraged to apply for passage'),
    # --- "Java" leaves London --------------------------------------------
    # Stephen removed his own inline editorial note.
    ('06-java-leaves-london.md', ' Consistency needed here  October 12th 1839,  18thof October',
                                 ''),
    # Stephen resolved the truncated November 26th entry by cutting the
    # orphaned fragment rather than restoring the missing words.
    ('06-java-leaves-london.md',
     'recover his course again."would permit. 21 o 5\' South lat. 32 o 41\' West long. Isle of Trinidad bearing N.E. a quarter N. 139 miles.*',
     'recover his course again."*'),
    # --- Bibliography ------------------------------------------------------
    ('16-bibliography.md', 'The Practical Idealists of 1836-',
                           'The Practical Idealists of 1836-1846,'),
    # Stephen deleted this note; his Word edit left a stray "[" behind,
    # which we drop rather than carry across.
    ('16-bibliography.md', ' \\[called incorrectly the George Richards diary\\]',
                           ''),
    ('16-bibliography.md', 'Mortlock Library of SouthAustraliana',
                           'Mortlock Library of South Australiana'),
]

# Stephen deleted the standalone "Medical comforts?" section, which
# duplicated a passage already present in '"Java" leaves London'.
DELETE_FILES = ['manuscript/12-medical-comforts.md']

files = {}
for fname, old, new in EDITS:
    path = 'manuscript/' + fname
    if path not in files:
        files[path] = open(path, encoding='utf-8').read()
    n = files[path].count(old)
    if n != 1:
        sys.exit(f'ABORT: pattern occurs {n}x (need exactly 1) in {fname}:\n  {old[:90]!r}')
    files[path] = files[path].replace(old, new)

for path, text in files.items():
    open(path, 'w', encoding='utf-8', newline='\n').write(text)
print(f'applied {len(EDITS)} edits across {len(files)} files')

for path in DELETE_FILES:
    if os.path.exists(path):
        os.remove(path)
        print('deleted', path)
