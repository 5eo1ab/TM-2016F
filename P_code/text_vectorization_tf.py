# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:50:44 2016

@author: Hanbin Seo
"""

import pandas as pd
from pandas import DataFrame as df

file_dir = "D:/course_2016_fall/Unstructured_Data_Analysis/Project/data/dataset_v4.csv"
dataset = pd.read_csv(file_dir)
#data = [lemma.split(" ") for lemma in dataset["lemma"]]
data = dataset["lemma"]

########################################
# Text Vectorization Process
# outputs : term-frequency matrix, wordlist
########################################

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
countvector=CountVectorizer()
tf=countvector.fit_transform(data)

print len(countvector.get_feature_names())
print tf.A.shape

save_dir = "D:/course_2016_fall/Unstructured_Data_Analysis/Project/data/"
f = open(save_dir+"word_list_v1.txt", 'wb')
for word in countvector.get_feature_names() :
    f.write(word)
    f.write("\t")
f.close()

import csv
f = open(save_dir+"doc-term_matrix_freq.csv", 'wb')
cw = csv.writer(f, delimiter=',', quotechar='\n')
cw.writerow(countvector.get_feature_names())
cw.writerows(tf.A)
f.close()

countvector=CountVectorizer(binary=True)
tf_bin=countvector.fit_transform(data)
f = open(save_dir+"doc-term_matrix_bin.csv", 'wb')
cw = csv.writer(f, delimiter=',', quotechar='\n')
cw.writerow(countvector.get_feature_names())
cw.writerows(tf_bin.A)
f.close()


