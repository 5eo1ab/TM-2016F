# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 05:08:45 2016
Modified on Tue Feb 21 2017

@author: Hanbin Seo
"""

import pandas as pd
from pandas import DataFrame as df

f_dir = "D:/Paper_2017/workspace/data/"
dataset = pd.read_csv(f_dir+"dataset_ini.csv", encoding='cp437', error_bad_lines=False)

# (1) 토픽모델링 결과 호출, 불필요 인덱싱 제거
w_dir = "D:/Paper_2017/workspace/topic_model/"
doc_topic = pd.read_csv(w_dir+"result/probability_doc-topic_t10_i1000.csv")
topic_term = pd.read_csv(w_dir+"result/probability_topic-term_t10_i1000.csv")
del doc_topic[list(doc_topic.columns.values)[0]]
del topic_term[list(topic_term.columns.values)[0]]


# (2) 연도단위 토픽확률분포 병합
doc_topic['year'] = dataset['Year']
year_topic = doc_topic.groupby(['year']).mean()
year_topic.columns = ["T{0}".format(t) for t in list(year_topic.columns.values)]
#del doc_topic['year']
year_topic = year_topic.loc[year_topic.index<2017]
year_topic.to_csv(w_dir+"topic_analysis_by_year.csv")


# (3) 시각화
import matplotlib.pyplot as plt
from random import shuffle
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
linest = ['-', '--']    # , '-.', ':'
params = ['{0}{1}'.format(c,l) for c in colors for l in linest]
shuffle(params)
          
plt.figure(figsize=(15,7))
for t in list(year_topic.columns.values) :
    idx = list(year_topic.columns.values).index(t)
    plt.plot(year_topic.index, year_topic[t], params[idx])
plt.legend(loc='higher right')
plt.show()

