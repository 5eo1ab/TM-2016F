# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 20:10:01 2016

@author: Hanbin Seo
"""

import pandas as pd
from pandas import DataFrame as df

file_dir = "../P_data/dataset_v1.csv"
dataset = pd.read_csv(file_dir)
data = dataset['abstract']

########################################
# Standardization of concept words

# Expression standardization by hand(abbr_dic_v1.csv)
# This process can take a very long time.
# processing time(sec):   170.260000229 @ Desktop PC
########################################

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

import time
t0 = time.time()
for key in abbr_dic.keys() :
    if len(abbr_dic[key]['other_exp']) > 1 :
        #print key, "\t", res_abbr_dic[key]['standard_exp']
        for idx in range(len(data)) :
            if str("("+key) in data[idx] :
                for exp in abbr_dic[key]['other_exp'] :
                    data[idx] = data[idx].replace(exp, abbr_dic[key]['standard_exp'])
                    data[idx] = data[idx].replace("\xe2\x80\x93", " ")
t1 = time.time() - t0
print "processing time(sec):\t", t1

dataset['abstract'] = data
dataset.to_csv(save_dir+"dataset_v2.csv", index=False)
