# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 00:08:52 2017

@author: Hanbin Seo
"""

import pandas as pd
from pandas import DataFrame as df

f_dir = "D:/Paper_2017/workspace/data/"
dataset = pd.read_csv(f_dir+"scopus.csv", encoding='cp437', error_bad_lines=False)

"""
# 데이터셋 1차 정제
# scopus 데이터 ~ 변수 너무 많고, 불필요한 변수 다수 존재
# 필요 변수 : 'Authors', 'Title', 'Year', 'SourceTitle', 'Abstract', 'References'
# 추가적으로, 초록(Abstract) 값이 [No abstract available]인 데이터 삭제, 29개 존재했음
"""

### (1) 필요 변수 추출 
colnames = list(dataset.columns.values)
data = dataset[[colnames[0], 'Title', 'Year', 'Source title', 'Abstract', 'References']]
data.columns = ['Authors', 'Title', 'Year', 'SourceTitle', 'Abstract', 'References']

### (2) 초록 값 누락데이터 제거
pass_val = "[No abstract available]" # 29
tmp_data = data.loc[data['Abstract'] != pass_val]
print("Count of [No abstract available] : {0}".format(len(data)-len(tmp_data)) )

### (3) 초록 불용패턴 제거
import re
#pattern = '\┬\⌐\s\d{4}\s\w*'
pattern = '\┬\⌐\s\d{4}'
res_abst = []
for idx in tmp_data.index.tolist() :
    tmp_abst = tmp_data['Abstract'][idx]
    #print(idx, "\n", re.findall(pattern, tmp_data['Abstract'][idx]))
    tmp_abst = re.split(pattern, tmp_data['Abstract'][idx])[0]
    res_abst.append(tmp_abst)
tmp_data['Abstract'] = res_abst

### (4) 저장
res_data = tmp_data
res_data.to_csv(f_dir+"dataset_ini.csv", index=False)

