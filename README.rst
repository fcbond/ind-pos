Indonesian Part of Speech Tagger and Tokenizer
==============================================

Based on tagged text from UI:
http://bahasa.cs.ui.ac.id/postag/corpus

And using the frameworks from NLTK.

Tokenization
------------

* use the default nltk tagger with some fixes
* remove clitics if it leaves you with a word
** prefixes se|ku|kau
** suffixes ku|mu|nya and lah|kah
* the wordlist is from the Wordnet Bahasa


Part-of-speech tagging
----------------------

* use NLTK's perceptron tagger trained on the UI corpus


Lemmatization
-------------

Not done yet! Should work with Hiroki

 * deduplicate  X-X ->X pos2 if not in WN
 * strip superlative
 ** te+adj -> ter- | adj (if adj in WN)
 ** ter+adj -> ter- |adj (if adj in WN)
 * diX -> di- + X if not in wn


Training and Setup
------------------


If you want to train the tagger, use train.py.

Training Data:
https://github.com/famrashel/idn-tagged-corpus

Tagset:
http://bahasa.cs.ui.ac.id/postag/downloads/Tagset.pdf

Citation:
Arawinda Dinakaramani, Fam Rashel, Andry Luthfi, and Ruli Manurung.
Designing an Indonesian Part of speech Tagset and Manually Tagged 
Indonesian Corpus. International Conference on Asian Language 
Processing (IALP 2014). 

http://bahasa.cs.ui.ac.id/postag/downloads/Designing%20an%20Indonesian%20Part%20of%20speech%20Tagset.pdf

We also add a few sentences to give some examples of clitics.

If you want to setup the vocabulary for the tokenizer, run setup.py.

It uses Wordnet Bahasa through the OMW.


ToDo
----

* Add tagset for NLTK
** at least pull out the short description in EN and ID
** list of tags and most frequent 3 in ```tagset.tsv```
* Make into a proper module

* Push into NLTK

* Lemmatize with Nomoto-san's tool
  https://github.com/matbahasa/MALINDO_Morph

* Add extra training sentences for weird punctuation and clitics
```
punct=['•', '>', '/', '?', '!', '-', '–', '—', ';', ':', 
       '"', '”',  '“', ')', '(', ',', '.', '``', "''", "'"] 
```

* Add mapping to UPOS
```
UPOS	Definition	Mapped POS
ADJ	adjective	jj, jj2
ADP	adposition	in
ADV	adverb	prl, rb
AUX	auxiliary verb	md
CONJ	coordinating conjunction	cc
NOUN	noun	nn, nn2, nnc, nnc2, nng, nnu
NUM	numeral	cdc, cdi, cdo, cdp, prn
PRON	pronoun	prp, wp, wp2
PROPN	proper noun	nnp
PRT	particle	neg, rp
PUNCT	punctuation	pu!, pu", pu&, pu(, pu), pu,, pu-, pu., pu/, pu:, pu;, pu>, pu?, pu©, pu–, pu“, pu”, pu•
SCONJ	subordinating conjunction	sc
VERB	verb	vbi, vbt
X	other	., dt, dt2, fw, nns2, wrb
```


Maybe ToDo
----------

These things are useful for tagging, but are done by INDRA.
Maybe add add a wsd mode?

After POS tagging, ...

* Split ter/ber/di
* Un-reduplicate

``` python
### Note, now use lex['adj'], lex['ber'], ...

notber=['berdiri', 'belaja', 'bersama']
dup = re.compile(r'^(.*)-\1$')

## check for superlative te(r)-
            if lemma.startswith('ter'): # and lemma not in lexall:
                if lemma[2:] in lexadj:
                    lemma = lemma[2:]
                    pos = 'jjs'
                elif lemma[3:].lower() in lexadj:
                    lemma = lemma[3:]
                    pos = 'jjs'
            ## check for 'ber'
            elif lemma.startswith('ber') and lemma not in notber:
                if lemma[2:] in lexvrb:
                    lemma = lemma[2:]
                    pos = 'vbb'
                elif lemma[2:] in lexnon:
                    ### fixme add  'ber'
                    lemma = lemma[2:].lower() 
                    pos = 'vnb'
                elif  lemma[3:] in lexvrb:
                    lemma = lemma[3:]
                    pos = 'vbb'
                elif lemma[3:] in lexnon:
                    ### fixme add noun
                    lemma = lemma[3:]
                    pos = 'vnb'
              ## check for passive di-
            elif lemma.startswith('di') and lemma.lower() not in lexall:
                lemma = lemma[2:]
                pos = 'vbd' # di

            ### check for reduplication
            if lemma.lower() not in lexdup:
                d = dup.match(lemma.lower())
                if d:
                    pos = pos + "2"
                    lemma = d.group(1)

```
