# -*- coding: utf-8 -*-
"""
Created on THU Dec 1 23:53:15 2016

@author: Hanbin Seo
"""
# dataset source url : http://www.dt.fee.unicamp.br/~tiago/smsspamcollection/

documents = []
file_dir = "./SMSSpamCollection.txt"
with open(file_dir, 'rt') as f :
    read_data = f.read().split('\n')
    for line in read_data :
        if len(line) > 0 :
            label = 'neg'.decode('utf8')
            if line.split('\t')[0] == 'ham' :
                label = 'pos'.decode('utf8')
            documents.append((line.split('\t')[1].decode('utf8'), label))
f.close()
documents = documents[:int(len(documents)*0.1)]
#print documents[0][0], "\n", documents[0][1]
documents[0][0]
type(documents[0][0])
len(documents)

cutoff = int(len(documents)*0.8)
train = documents[:cutoff]
test = documents[cutoff:]
print "length train:test =", len(train), len(test)



from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob as tb
cl = NaiveBayesClassifier(train)
res_li = []
for txt, l in test :
    dic_tmp = {}
    dic_tmp['decision'] = cl.classify(txt)
    prob_dist = cl.prob_classify(txt)
    dic_tmp['prob_pos'], dic_tmp['prob_neg'] = prob_dist.prob("pos"), prob_dist.prob("neg")
    dic_tmp['senti_score'] = tb(txt).sentiment.polarity
    res_li.append(dic_tmp)

idx = 0
correct = 0
for res in res_li :
    print res['decision'], res['prob_pos'], res['prob_neg']
    if res['decision'] == test[idx][1] :
        correct += 1
    idx += 1
print "Acc score >> ", correct/len(test)

from pandas import DataFrame as df
res_df = df(res_li)
res_df.to_csv("~/result.csv")


