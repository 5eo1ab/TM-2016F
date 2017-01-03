# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 05:08:45 2016

@author: Hanbin Seo
"""

import pandas as pd
from pandas import DataFrame as df

save_dir = "../P_data/"
dataset = pd.read_csv(save_dir+"dataset_v4.csv")
doc_topic = pd.read_csv(save_dir+"lda_prob_doc-topic.csv")
topic_term = pd.read_csv(save_dir+"lda_prob_topic-term.csv")

doc_topic['year'] = dataset['year']
year_topic = doc_topic.groupby(['year']).mean()
year_topic.columns = ["T1", "T2", "T3", "T4", "T5"]
del doc_topic['year']
year_topic = year_topic.loc[year_topic.index<2017]
year_topic.to_csv(save_dir+"res_year_topic.csv")

import matplotlib.pyplot as plt
plt.figure(figsize=(15,7))
plt.plot(year_topic.index, year_topic['T1'])
plt.plot(year_topic.index, year_topic['T2'])
plt.plot(year_topic.index, year_topic['T3'])
plt.plot(year_topic.index, year_topic['T4'])
plt.plot(year_topic.index, year_topic['T5'])
plt.legend(loc='lower right')
plt.show()

dataset['publication'].value_counts()

doc_topic['publication'] = dataset['publication']
pub_topic = doc_topic.groupby(['publication']).mean()
del doc_topic['publication']
pub_topic.to_csv(save_dir+"res_pub_topic.csv")


import numpy as np
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine
dist_out = 1-pairwise_distances(pub_topic, metric="cosine")
df(dist_out, columns=pub_topic.index).to_csv(save_dir+"pub_cosine_matrix.csv", index=False)

 
