# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 02:47:05 2016

@author: Hanbin Seo
"""

import pandas as pd
from pandas import DataFrame as df

file_dir = "../P_data/dataset_v1.csv"
dataset = pd.read_csv(file_dir)
data = dataset['abstract']

#####################################################
# Abbreviation Extraction Using Parsing Technique
#####################################################

abbr_dic = {}
#for doc_idx in range(432, len(data)) :
for doc_idx in range(0, len(data)) :
    # except case
    if doc_idx == 432 :
        continue
    tmp_li = data[doc_idx].split(")")[:-1]
    if doc_idx == 429 :
        ini_idx = 4
    else :
        ini_idx = 0
    # except case(end)
    for idx in range(ini_idx,len(tmp_li)) :
        try :
            tmp_abbr = tmp_li[idx][tmp_li[idx].rindex("(")+1:]
        except :
            continue
        if tmp_abbr[0].isupper() is False or len(tmp_abbr.split(" "))>1:
            continue
        elif tmp_abbr is not "PSS" and tmp_abbr[-1] in tmp_abbr[:-2] :
            tmp_txt = tmp_li[idx].split("(")[0].strip()
            try :
                full_abbr = tmp_txt[tmp_txt.index(" "+tmp_abbr[0]):].strip()
            except :
                full_abbr = tmp_txt[tmp_txt.index(" "+tmp_abbr[0].lower()):].strip()
            print "\ncatch except case!!!!!:\n", doc_idx,"\t", tmp_abbr, "\t",full_abbr
            continue
        tmp_txt = tmp_li[idx].split("(")[0].strip()
        try :
            full_abbr = tmp_txt[tmp_txt.rindex(tmp_abbr[0]):].strip()
        except :
            #tmp_cutoff = tmp_txt.rindex(" "+tmp_abbr[0].lower())
            full_abbr = tmp_txt[tmp_txt.rindex(" "+tmp_abbr[0].lower()):].strip()
            print "\nexcept case:\t", tmp_abbr, "\t", full_abbr               
        print doc_idx, "\t", tmp_abbr, "\t", full_abbr
        if tmp_abbr not in abbr_dic.keys() :
            abbr_dic[tmp_abbr] = [full_abbr]
        elif full_abbr not in abbr_dic[tmp_abbr] :
            abbr_dic[tmp_abbr].append(full_abbr)
    #doc_idx += 1

save_dir = "../P_data/"
f = open(save_dir+"abbr_dic_v0.csv", "w")
for key in abbr_dic.keys() :
    for val in abbr_dic[key] :
        #print key, val
        row = str(key+","+val.replace(",","")+"\n")
        f.write(row)
f.close()

