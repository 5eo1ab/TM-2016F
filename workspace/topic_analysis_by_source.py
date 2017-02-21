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
doc_topic = pd.read_csv(f_dir+"probability_doc-topic_t10_i1000.csv")
topic_term = pd.read_csv(f_dir+"probability_topic-term_t10_i1000.csv")
del doc_topic[list(doc_topic.columns.values)[0]]
del topic_term[list(topic_term.columns.values)[0]]


# (2) 출판사(SourceTitle)단위 토픽확률분포 병합
doc_topic['SourceTitle'] = dataset['SourceTitle']
pub_topic = doc_topic.groupby(['SourceTitle']).mean()
pub_topic.columns = ["T{0}".format(t) for t in list(pub_topic.columns.values)]
pub_topic['Count'] = dataset['SourceTitle'].value_counts()
#del doc_topic['SourceTitle'] 
pub_topic.to_csv(f_dir+"topic_analysis_by_source.csv")


