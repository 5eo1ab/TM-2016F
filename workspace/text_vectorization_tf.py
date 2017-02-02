# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:50:44 2016
Modified on Wed Jan 25 2017

@author: Hanbin Seo
"""

import pandas as pd
from pandas import DataFrame as df

f_dir = "D:/Paper_2017/workspace/data/"
dataset = pd.read_csv(f_dir+"dataset_lemma.csv", encoding='cp437', error_bad_lines=False)
data = dataset["lemma"]

########################################
# Text Vectorization Process
# outputs : term-frequency matrix, wordlist
########################################

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
countvector=CountVectorizer()
tf=countvector.fit_transform(data)
print(len(countvector.get_feature_names()))
print(tf.A.shape)

tf_df = df(tf.A, columns=countvector.get_feature_names())
tf_df.to_csv(f_dir+"doc-term_matrix_freq.csv", index=False)


