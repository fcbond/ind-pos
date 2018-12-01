###
### train a perceptron-based POS tagger for Indonesian
###
import nltk
from nltk import ConditionalFreqDist, FreqDist
from utils import read_tagged
# read a corpus
# from https://github.com/famrashel/idn-tagged-corpus
#
sents = []  # [(word, tag), ...
    
    
ind_tagged = 'idn-tagged-corpus/Indonesian_Manually_Tagged_Corpus.tsv'
sents = read_tagged(ind_tagged)


cfd = ConditionalFreqDist([(t,w) for s in sents for (w,t) in s])
fd = FreqDist([t for s in sents for (w,t) in s])

with open("tagset.tsv",'w') as out:
    out.write("Tag\tFreq\tExamples\n")
    for tag in sorted(fd.keys()):
        out.write("{}\t{:6,d}\t{}\n".format(tag,
                                     fd[tag],
                                     "; ".join(["{} ({:,d})".format(w,f) for (w,f) in cfd[tag].most_common(3)])))

##
## train and save the perceptron tagger
##

tp = nltk.tag.perceptron.PerceptronTagger(load=False)
tp.train(sents)
tp.model.save('averaged_perceptron_tagger_id.pickle')


#exit()


###
### check everything works
###

size = int(len(sents) * 0.95)
train_sents = sents[:size]
test_sents = sents[size:]
t0 = nltk.DefaultTagger('NNP')
t1 = nltk.UnigramTagger(train_sents, backoff=t0)
t2 = nltk.BigramTagger(train_sents, backoff=t1)
t2.evaluate(test_sents)
# 0.953646173969915


print (t2.evaluate(test_sents))

tp = nltk.tag.perceptron.PerceptronTagger(load=False)

tp.train(train_sents)
print(tp.evaluate(test_nts))
 

#0.9715500327011118
