# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 22:20:15 2016

@author: Hanbin Seo
"""

### data import  ==============
""" Patent data about 'virtualization technology'
    their collect keywords are ['hypervisor', 'virtual_machine', 'virtualization']  """
import csv
documents = []
file_dir = "./dataset_sample.csv"
tmp_file = open(file_dir)
csvReader = csv.reader(tmp_file)
pass_row = True
for row in csvReader :
    if pass_row is True :
        pass_row = False
        continue
    tmp_dic = {'doc_num':row[1], 'title':row[2], 'abstract':row[3], 'category':row[0]}
    documents.append(tmp_dic)
tmp_file.close()
print(len(documents))

from pandas import DataFrame as df
data = df(documents)['abstract']


### data preprocessing  ==============
from nltk import tokenize
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
#punctuations = [',', '.', ';', '(', ')', '']

docs = []   # doc list in word list structure
for txt in data :
    tokens = tokenize.word_tokenize(txt)
    tokens_stem = [stemmer.stem(token.lower()) for token in tokens if token.lower() not in stopwords and len(token)>1]
    docs.append(tokens_stem)
words = [word for doc in docs for word in doc] # plain word list structure
print "num of words >>\t", len(words), "\nnum of words set >>\t", len(set(words))


### analysis most appear word @ total category data  ==============
import nltk
fd = nltk.FreqDist(words)
#many_word = [word for word in vocab if fd[word]>100]
most_word = fd.most_common(30)
print most_word
pick_wordlist = ['system', 'virtual', 'hypervisor', 'host', 'guest'] # i guess it...
pick_wordlist.sort()

wordlist = [word for word in words if word in pick_wordlist]
res_fd = nltk.FreqDist(wordlist)
res_fd.tabulate()   # table structure
res_fd.plot()       # distribution plot


### conditional frequency distribution ==============
data = zip(df(documents)['category'], df(documents)['abstract'])
docs = []   # doc list in tuple(category name, word list) structure
for categoty, txt in data :
    tokens = tokenize.word_tokenize(txt)
    tokens_stem = [stemmer.stem(token.lower()) for token in tokens if token.lower() not in stopwords and len(token)>1]
    docs.append((categoty, tokens_stem))
words = [word for doc in docs for word in doc[1]] # plain word list structure
print "num of words >>\t", len(words), "\nnum of words set >>\t", len(set(words))

c_words = [(c, word) for c, txt in docs for word in txt if word in pick_wordlist]
    # list in tuple(category name, picked word) structure
cfd = nltk.ConditionalFreqDist(c_words)
print cfd.conditions()
cfd.tabulate()      # table structure
cfd.plot()          # distribution plot


