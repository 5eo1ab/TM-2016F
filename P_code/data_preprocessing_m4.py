# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 02:45:54 2016

@author: Hanbin Seo
"""

import pandas as pd
from pandas import DataFrame as df

file_dir = "../P_data/dataset_v3.csv"
dataset = pd.read_csv(file_dir)
data = [lemma.split(" ") for lemma in dataset["lemma"]]
           
import csv
save_dir = "../P_data/"
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
# After the lemma process, remove the stopwords
########################################

f = open(save_dir+"stopwords_lemma.txt", "rb")
stopwords = []
tmp_txt = f.read().split("\n")
for row in tmp_txt :
    stopwords.append(str(row).strip())
f.close()

def check_in_num(txt) :
    for a in txt :
       if a.isdigit() is True :
           return True
    return False

    
    
data_lemma_v1 = []
for doc in data :
    tmp_li = []
    for word in doc :
        if word in abbr_dic.keys() :
            tmp_li.append(word)
        elif word not in stopwords and len(word)>1 and check_in_num(word) is False:
            tmp_li.append(word)
    data_lemma_v1.append(tmp_li)

import collections
word_list = [word for data in data_lemma_v1 for word in data]    
word_count=collections.Counter(word_list)
word_set = [word for word in set(word_list) if word_count[word]>1] # 명사 기준 2785개  

data_lemma_v2 = [[word for word in data if word in word_set] for data in data_lemma_v1]
data_lemma_v3 = [" ".join(data) for data in data_lemma_v2]
dataset["lemma"] = data_lemma_v3
dataset.to_csv(save_dir+"dataset_v4.csv", index=False)







     