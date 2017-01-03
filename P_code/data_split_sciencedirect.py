# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 16:17:17 2016

@author: Hanbin Seo
"""

import pandas as pd
from pandas import DataFrame as df

file_dir = "../P_data/science.txt"
f = open(file_dir, 'rb')
raw_data = f.read()
f.close()

"""
split_data = raw_data.split("Keywords:")
idx =6
items = split_data[idx].split("\n\n")
doc_info, abstract = split_data[idx].split("\n\n")[-1].split("Abstract:")
tmp_dic= {"doc_info": doc_info.strip(), "abstract": abstract.strip()} 
doc_info
          
keywords = split_data[idx+1].split("\n")[0].strip()
tmp_dic["keywords"] = [word.strip() for word in keywords.split(";")]
"""

documents, skip_cnt, skip_doc = [], 0, []
split_data = raw_data.split("Keywords:")
for idx in range(len(split_data)) :
#for idx in range(200,len(split_data)) :
    if idx == 0 :
        items = split_data[idx].split("Abstract:")  
    else :
        if len(split_data[idx].split("\n\n")[1].split("Abstract:")) == 2 :
            items = split_data[idx].split("\n\n")[1].split("Abstract:")
        else :
            print "\n\n\n===========================\n",idx,"\n",split_data[idx]
            tmp1 = split_data[idx].split("Abstract:")[0].split("\n\n")[-1]
            tmp2 = split_data[idx].split("Abstract:")[1]
            items = [tmp1, tmp2]
            skip_cnt += 1
            print "skip doc:\t", split_data[idx].split("Abstract:")[0].split("\n\n")[1:-1]
            skip_doc.append(split_data[idx].split("Abstract:")[0].split("\n\n")[1:-1])
    #print idx, "\t info: \t", items[0], "\n", items[1], "\nkeywords:\t", keywords
    tmp_dic = {"doc_info":items[0].strip(), "abstract":items[1].strip()}
    if idx == len(split_data)-1 :
        documents.append(tmp_dic)
        continue
    tmp_dic["keywords"] = split_data[idx+1].split("\n\n")[0].strip()
    documents.append(tmp_dic)
    
data_df = df(documents)
skip_doc = [tmp2 for tmp1 in skip_doc for tmp2 in tmp1]
print "\n\n\nshape of result:\t", data_df.shape, "\tskip count:\t", skip_cnt

# function library ====================================
def get_year(tmp1) :
    for year in range(2000, 2017+1) :
        tmp2 = str(year) in tmp1
        if tmp2 is True :
            return year

save_dir = "../P_data/"
f = open(save_dir+"publication_list.txt")
pub_li = f.read().split("\n")[1:]
f.close()
def get_publication(tmp1) :
    for pub in pub_li :
        tmp2 = pub in tmp1
        if tmp2 is True :
            return pub
            
# function library (end) ============================

import time
t0 = time.time()
tmp_years, tmp_pubs, tmp_authors, tmp_ttl = [], [], [], []
for idx in range(len(data_df)) :
    data_df['abstract'][idx] = data_df['abstract'][idx].replace("Abstract\n", "").replace("\n", " ")
    tmp1 = data_df['doc_info'][idx].split("ISSN")[0]
    tmp_years.append(get_year(tmp1))
    tmp_pub = get_publication(tmp1)
    tmp_pubs.append(tmp_pub)
    if tmp_pub is not None :
        tmp2 = tmp1.split(tmp_pub)[0].split(",")[:-1]
        tmp_authors.append(";".join(tmp2[:-1]))
        tmp_ttl.append(tmp2[-1].strip())
    else :
        tmp_authors.append(None)
        tmp_ttl.append(None)
data_df['year'] = tmp_years
data_df['publication'] = tmp_pubs
data_df['authors'] = tmp_authors
data_df['title'] = tmp_ttl
t1 = time.time()-t0
print t1    # 22.5339999199 @ Desktop
    
save_dir = "../P_data/"
data_df.to_csv(save_dir+"dataset_v1.csv", index=False)
f = open(save_dir+"skip_doc_v1.txt", "w")
for row in skip_doc :
    f.write(row)
    f.write("\n\n")
f.close()

