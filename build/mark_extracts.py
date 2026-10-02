# Make the quoted extracts recognisable as such, so the build can set them
# apart. Markers and paragraph breaks only - no words change, and the script
# aborts unless each chapter's letters and digits are identical afterwards.
#
# Three kinds of repair:
#   split   an introduction (or Stephen's comment) shared a paragraph with
#           the extract it belongs to; they are given a paragraph each
#   extend  the italic began late, leaving the first word(s) of an extract
#           outside it ("**21st**. E. *Ahead, ..." - E. is the wind)
#   mark    an extract that Stephen interrupts with an aside is marked as a
#           block quotation (">"), since it is not italic throughout
import re, sys

EDITS = {
 '03-introduction.md': [
    ('I quote: *"Country ships', 'I quote:\n\n*"Country ships'),
 ],
 '06-java-leaves-london.md': [
    ('has the following information: *“Mr. Conigrave', 'has the following information:\n\n*“Mr. Conigrave'),
    ('he soon flaged."* (Authors note', 'he soon flaged."*\n\n(Authors note'),
    ('West long."* William made similar observations', 'West long."*\n\nWilliam made similar observations'),
    ('**21st**. E. *Ahead,', '**21st**. *E. Ahead,'),
    ('"Christmas Eve(sic) *A double allowance', '> "*Christmas Eve*(sic) *A double allowance'),
    ('**December 31** st. *I have been', '**December 31st.** *I have been'),
    ('fine breeze."* and on the next', 'fine breeze."*\n\nand on the next'),
    ('"The "JAVA"--Mr. Smith surgeon of the JAVA', '*"The "JAVA"--Mr. Smith surgeon of the JAVA'),
    ('11th inst., *"referring to him', '11th inst., "referring to him'),
 ],
 '07-medical-board-enquiry.md': [
    ('*"... Captain Dutton* (Kerr had it wrong', '> *"... Captain Dutton* (Kerr had it wrong'),
 ],
 '08-new-opportunities.md': [
    ('TYWARDREATH - *On Tuesday evening', '*TYWARDREATH - On Tuesday evening'),
    ('been recently sent home.*\n*The Rev. T. Pearce', 'been recently sent home. The Rev. T. Pearce'),
 ],
}
# the one that needs a pattern: an extract followed by Stephen's bracketed comment
REGEX = {
 '06-java-leaves-london.md': [
    (r'\*[ \t]*(\\\[It was this entry, of course)', r'*\n\n\1'),
 ],
}

alnum = lambda t: re.sub(r'[^A-Za-z0-9]', '', t)
for name, edits in EDITS.items():
    path = 'manuscript/' + name
    text = old = open(path, encoding='utf-8').read()
    for a, b in edits:
        # a run of spaces in the pattern matches any run of spaces or line breaks
        pat = re.compile(r'\s+'.join(re.escape(tok) for tok in a.split(' ')))
        n = len(pat.findall(text))
        if n != 1:
            near = text.find(a.split(' ')[0] + ' ' + a.split(' ')[1]) if ' ' in a else -1
            sys.exit(f'ABORT {name}: {a[:50]!r} found {n} times; nearby text: {text[near:near+90]!r}')
        text = pat.sub(lambda m: b, text)
    for pat, rep in REGEX.get(name, []):
        if len(re.findall(pat, text)) != 1:
            sys.exit(f'ABORT {name}: pattern {pat!r} found {len(re.findall(pat, text))} times')
        text = re.sub(pat, rep, text)
    if alnum(text) != alnum(old):
        sys.exit(f'ABORT {name}: letters or digits changed')
    open(path, 'w', encoding='utf-8', newline='\n').write(text)
    print(f'{name:40} {len(edits) + len(REGEX.get(name, []))} repairs, letters and digits unchanged')
