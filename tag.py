#
# simple tokenization for Indonesian
#

import pickle
import re
import nltk
from nltk import word_tokenize
from nltk.tag.perceptron import PerceptronTagger

with open('lex_id.pickle', 'rb') as fh:
    lex = pickle.load(fh)


def tknz_id(sent, lex=lex, cm='⊝'):
    """Tokenize text for Indonesian NLP
    split final and initial clitics
    and some derviational affixes"""

    sf1 = ["nya", "ku", "kau", "mu"]
    sf2 = ["lah", "kah"]
    pf =  ["ku", "kau", "ke", "se"]
    redup = re.compile("^(.*)-\\1$", flags=re.IGNORECASE)
    rsf2  = re.compile("^(.*)({})$".format("|".join(sf2)), flags=re.IGNORECASE)
    rsf12 = re.compile("^(.*?)(-)?({})({})?$".format("|".join(sf1),"|".join(sf2)), flags=re.IGNORECASE)
    rpf   = re.compile("^({})(.*)$".format("|".join(pf)), flags=re.IGNORECASE)
    raf12 = re.compile("^({})(.*?)(-)?({})({})?$".format("|".join(pf), "|".join(sf1),"|".join(sf2)), flags=re.IGNORECASE)
    toks = []
    for word in nltk.word_tokenize(sent):
        rm = redup.match(word)
        if word.lower() in lex['all']:
            toks.append(word)
        elif rm and  rm.group(1).lower() in lex['all']:
            toks.append(word)
        else:
            m = rsf2.match(word)
            if m:
                toks.append(m.group(1))
                toks.append("{}{}".format(cm,m.group(2)))
                continue
            m = rpf.match(word)
            if m:
                toks.append("{}{}".format(m.group(1),cm))
                toks.append(m.group(2))
                continue
            m = rsf12.match(word)
            if m:
                toks.append(m.group(1))
                if m.group(2):
                    toks.append("{}{}".format(m.group(2),m.group(3)))
                else:
                    toks.append("{}{}".format(cm,m.group(3)))
                if m.group(4):
                    toks.append("{}{}".format(cm,m.group(4)))
                continue
            m = raf12.match(word)
            if m:
                toks.append("{}{}".format(m.group(1),cm))
                toks.append(m.group(2))
                if m.group(3):
                    toks.append("{}{}".format(m.group(3),m.group(4)))
                else:
                    toks.append("{}{}".format(cm,m.group(4)))
                if m.group(4):
                    toks.append("{}{}".format(cm,m.group(5)))
                continue
            toks.append(word)
    
    return toks


testsents = [  """Saya telah mempertanggungjawabkannya di hadapan penguji-penguji tersebut.""",
               """Dia menuliskan surat ini untukku dan untukmu.""",
               """Kue ini k""",
               """Sebuah kue ini kumasak untukmu, tetapi dua buah kue itu kaumasak untukku dan untuknya.""",
               """Apakah penumpang > 18 tahun yang belum memiliki KTP/SIM/paspor harus membayar Rp.100.000/penumpang/pax?""",
               """Dilarang masuk ke ruangan ini!""",
               """Pada tanggal 11/12/2016 10:05 WIB terjadi beberapa hal berikut ini: Adi makan buah-buahan, Budi pergi ke kantor, dan Tedi minum air :)""",
               """Ada diskon 25% di Bank Central Asia (BCA) pk 07.00-15.00.""",
               """Hubungi nomor telepon berikut ini: +6281736458 (rumah) / 081-7899-6578 (kantor).""",
               """Silakan pilih "Input", klik tombol "Enter", lalu masuk ke pilihan "Pilih" di bagian atas!""",
               """Manusia itu oleh Tuhan diangkat menjadi wakil-Nya di bumi yang fana ini.""",
               """buku buku-buku buku-bukunya"""]

TAGPICKLE='averaged_perceptron_tagger_id.pickle'
tagger = PerceptronTagger(load=TAGPICKLE)

for s in testsents:
    print(s)
    print(tknz_id(s))
    print(tagger.tag(tknz_id(s,cm='-')))
    print()

### POS tagger seems really bad at clitics.   '-nya' should be really, really easy as it only has one tag, ...
