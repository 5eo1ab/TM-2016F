# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 20:54:20 2016

@author: Hanbin Seo
"""

import pandas as pd
from pandas import DataFrame as df

file_dir = "D:/course_2016_fall/Unstructured_Data_Analysis/Project/data/dataset_v2.csv"
dataset = pd.read_csv(file_dir)
data = dataset['abstract']

import csv
save_dir = "D:/course_2016_fall/Unstructured_Data_Analysis/Project/data/"
f = open(save_dir+"abbr_dic_v1.csv", "rb")
csvReader = csv.reader(f)
abbr_dic = {}
for row in csvReader :
    if row[0] not in abbr_dic.keys() :
        abbr_dic[row[0]] = {"standard_exp":row[2], "other_exp":[row[1]]}
    else :
        abbr_dic[row[0]]["other_exp"].append(row[1])
f.close()

########################################
# Basic preprocessing: tokenization, removing stopwords, POS-tagging, lemmatization
########################################

### removing punctuation(v1)
import string
def remove_punc(txt) :
    for punc in set(string.punctuation) :
        txt = txt.replace(punc, " ")
    return txt    
data_v1 = [remove_punc(txt) for txt in data] 

### tokenization(v2)
from nltk.tokenize import word_tokenize
data_v2 = [word_tokenize(txt) for txt in data_v1] 

### removing stopwords(v3)
from nltk.corpus import stopwords
stopword_li = [str(word) for word in stopwords.words('english')]
data_v3 = []
for doc in data_v2 :
    tmp_li = []
    for token in doc :
        if token in abbr_dic.keys() : 
            tmp_li.append(token)    #keep abbr_words
        elif token.lower() not in stopword_li :
            tmp_li.append(token.lower())
    data_v3.append(tmp_li)

### POS-tagging(v4)
from nltk import pos_tag
data_v4 = [pos_tag(txt) for txt in data_v3]          
           
### lemmatization(v5)
import time
from nltk.stem import WordNetLemmatizer
wn_lemma = WordNetLemmatizer()

from nltk.data import load
tagdict = load('help/tagsets/upenn_tagset.pickle')
#tagdict['JJ'][0]
#tagdict.keys()
def get_format(tag) :
    tag_info = tagdict[tag][0]
    if 'noun' in tag_info :
        return "n"
    elif 'verb' in tag_info :
        return "v"
    elif 'adjective' in tag_info or 'adverb' in tag_info :
        return "a" 
    else:
        return None

import re
t0, data_v5, lemma = time.time(), [], ""
for token_tags in data_v4 :
    tmp_li = []
    for word, pos_tag in token_tags :
        if word in abbr_dic.keys() :
            lemma = word
        if get_format(pos_tag) is not None :
            lemma = wn_lemma.lemmatize(re.sub(r'[^\x00-\x7F]','', word), get_format(pos_tag))
        tmp_li.append(str(lemma))
    data_v5.append(tmp_li)
t1 = time.time() - t0
print "processing time(sec):\t", t1

### save and import for remove stopwords(final)
data_final = [" ".join(li) for li in data_v5]
dataset["lemma"] = data_final
dataset.to_csv(save_dir+"dataset_v3.csv", index=False)






