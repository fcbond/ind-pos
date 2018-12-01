from nltk.corpus import wordnet as wn
import pickle

lex = {}
lex['adj'] = set() # adjectives
lex['non'] = {'nonya'} #nouns
lex['vrb'] = set() # verbs
lex['dup'] = set() # lexical reduplication
lex['ber'] = {'berdiri', 'belaja', 'bersama'}
lex['all'] = {'setidaknya'} # all the words
### prepositions from the web
lex['prep'] = {'atas', 'setelah', 'sekitar', 'di', 'karena', 'sebelum', 'samping', 'antara', 'tapi', 'dekat ke', 'turun', 'selama', 'untuk', 'dari', 'di', 'depan', 'dalam', 'daripada', 'seperti', 'dekat', 'berdekatan', 'puncak', 'keluar', 'luar', 'diatas', 'seberang', 'tentang', 'sejak', 'daripada', 'ke', 'bawah', 'sampai', 'naik', 'tanpa', 'tentang'} 


lex['all'] = lex['all'].union(lex['ber']).union(lex['non']).union(lex['prep'])

print('Reading Indonesian Wordnet (through OMW)')
for ss in wn.all_synsets():
    lp = ss.pos()
    for lemma in ss.lemmas(lang='ind'):
        ln = lemma.name().replace('_', ' ')
        if ' ' in ln:  # we only need single words
            continue
        lex['all'].add(ln)
        if "-" in ln:
            lex['dup'].add(ln)
        if lp == 'a' or lp == 's':
            lex['adj'].add(ln)
        elif lp == 'v':
            lex['vrb'].add(ln)
        elif lp == 'n':
            lex['non'].add(ln)

print('Pickling Lex to lex_id.pickle')
f = open('lex_id.pickle', 'wb')
pickle.dump(lex, f)
print('Done!')
