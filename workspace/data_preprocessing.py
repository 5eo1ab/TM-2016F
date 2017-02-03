# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 20:54:20 2016
Modified on Wed Jan 25 2017

@author: Hanbin Seo
"""

import pandas as pd
from pandas import DataFrame as df

f_dir = "D:/Paper_2017/workspace/data/"
dataset = pd.read_csv(f_dir+"dataset_ini.csv", encoding='cp437', error_bad_lines=False)
data = dataset['Abstract']

import re
pattern = '\(\w{2,}\)'
tmp_dic = {}
for idx in range(len(data)) :
    tmp_li = re.findall(pattern, data[idx])
    tmp_li = [item[1:-1] for item in tmp_li]
    for item in tmp_li :
        if len(re.findall('\d{4}', item)) > 0 : 
            continue
        elif len(re.findall('\i[\iv]{1,}', item)) > 0 :
            continue
        if item not in tmp_dic.keys() :
            tmp_dic[item] = 1
        else :
            tmp_dic[item] += 1
abbr_dic = {}
for k, v in tmp_dic.items() :
    if v > 5 :
        abbr_dic[k.lower()] = (k,v)
#abbr_lower = [item.lower() for item in list(abbr_dic.keys())]


########################################
"""
# Basic preprocessing: tokenization, removing stopwords, POS-tagging, lemmatization
# 기본적인 전처리 과정
"""
t0 = time.time()

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
data_v3, stopword_li = [], [str(word) for word in stopwords.words('english')]
for doc in data_v2 :
    tmp_li = []
    for token in doc :
        if len(token) < 2 :
            continue
        if token.lower() not in stopword_li :
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
data_v5, lemma = [], ""
for token_tags in data_v4 :
    tmp_li = []
    for word, pos_tag in token_tags :
        if word in abbr_dic.keys() :
            lemma = abbr_dic[word][0]
        elif get_format(pos_tag) is not None :
            lemma = wn_lemma.lemmatize(re.sub(r'[^\x00-\x7F]','', word), get_format(pos_tag))
        else :
            continue
        tmp_li.append(str(lemma))
    data_v5.append(tmp_li)



### 2회 미만 출현 단어 제거
import collections
word_list = [word for doc in data_v5 for word in doc]    
word_count=collections.Counter(word_list)
word_set = [word for word in set(word_list) if word_count[word]>1]
data_v6 = [[word for word in doc if word in word_set] for doc in data_v5]


### save and import for remove stopwords(final)
data_final = [" ".join(li) for li in data_v6]
dataset["lemma"] = data_final
dataset.to_csv(f_dir+"dataset_lemma.csv", index=False)

t1 = time.time() - t0
print("processing time(sec):\t", t1)
