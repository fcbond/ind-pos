def read_tagged (tagged):
    fh = open(tagged)
    sents = []
    sentence = []
    for l in fh:
        #print(l)
        if len(l) > 1:
            (word, tag) = l.strip().split('\t')
            sentence.append((word, tag))
        else:
            sents.append(sentence)
            sentence=[]
    sents.append(sentence)
    return sents
