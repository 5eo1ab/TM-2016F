# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 19:42:59 2016

@author: Hanbin Seo
"""

## data import
import csv
dir_ = "~"
file_ = open(dir_+'letm_100.csv')
csvReader = csv.reader(file_)
documents = []
for row in csvReader :
    documents.append(row[1].replace("\n", " "))
file_.close()


## calculate TF-IDF for Clustering Analysis ===================
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
countvector = CountVectorizer(decode_error='ignore')
vertorizer = TfidfVectorizer(decode_error='ignore')
tf = countvector.fit_transform(documents)
tfidf_cl = vertorizer.fit_transform(documents)

## Document Clustering
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3)
km.fit(tfidf_cl)
print "labels >>> ", km.labels_
print "cluster_centers >>> ", km.cluster_centers_

from collections import Counter
print Counter(km.labels_)

## calculate Keyword Frequency ===================
import numpy as np
count_word = np.sum(tf.A.T, axis=1)

from pandas import DataFrame as df
words = df()
words['word'] = list(countvector.get_feature_names())
words['count'] = count_word
words_sort = words.sort('count', ascending=False)
print words_sort[:10]  # pick frequency keyword : system(119), virtual(100)

## calculate TF-IDF for Plotting ===================
wishwords = ['system', 'virtual']
texts = [[word for word in doc.split() if word in wishwords] for doc in documents]
result_doc = [" ".join(line) for line in texts]

tfidf = vertorizer.fit_transform(result_doc)
print tfidf.A

## Document Plotting
import matplotlib.pyplot as plt
#plt.scatter(tfidf.A[:,0], tfidf.A[:,1])
for i in range(len(documents)) :
    if km.labels_[i] == 0 :
        plt.scatter(tfidf.A[i,0], tfidf.A[i,1], c='red', s=50)
    elif km.labels_[i] == 1 :
        plt.scatter(tfidf.A[i,0], tfidf.A[i,1], c='green', s=50)
    else :
        plt.scatter(tfidf.A[i,0], tfidf.A[i,1], c='blue', s=50)
plt.xlabel(wishwords[0])
plt.ylabel(wishwords[1])
plt.text(0.8, 1.0, "Doc.Cluster 0: red\nDoc.Cluster 1: green\nDoc.Cluster 2: blue")
plt.show()



