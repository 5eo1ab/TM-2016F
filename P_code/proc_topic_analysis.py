# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 05:08:45 2016

@author: Hanbin Seo
"""

import pandas as pd
from pandas import DataFrame as df

save_dir = "D:/course_2016_fall/Unstructured_Data_Analysis/Project/data/"
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

"""
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans, MiniBatchKMeans

svd=TruncatedSVD(n_components=2)
svd_result=svd.fit_transform(pub_topic) 
print svd_result
 
km=KMeans(n_clusters=3)
km.fit(svd_result)

print "labels>>>>", km.labels_
print "cluster_centers>>>>", km.cluster_centers_

from pylab import plot,show, legend
color = ['or', 'og', 'ob', 'oc', 'om', 'oy', 'ok', 'ow']
for num in range(0, 3):
	plot(svd_result[km.labels_==num,0],svd_result[km.labels_==num,1],color[num%7], label='group'+str(num))
legend(loc='upper right')
show()
"""



 