# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 22:34:20 2016

@author: Hanbin Seo
"""

import pandas as pd
from pandas import DataFrame as df

save_dir = "../P_data/"
df_mat = pd.read_csv(save_dir+"doc-term_matrix_freq.csv")

f = open(save_dir+"word_list_v1.txt")
word_list = f.read().split("\t")[:-1]
f.close()

#df_mat = pd.read_csv(save_dir+"pub_cosine_matrix.csv")
#word_list = df_mat.columns

########################################
# Co-occurrence matrix Process
# inputs : Occurrence matrix (m by n)
# outputs : Co-occurrence matrix (n by n or m by m), Network Edge list, Network Node list
########################################

import numpy as np
coo_mat = np.matmul(df_mat.T, df_mat)   # co-occurance matrix
print df_mat.T.shape, "\t*",  df_mat.shape, "\t=", coo_mat.shape
coo_mat_df = df(coo_mat, columns=word_list, index=word_list)

diagonal_value=list(np.diag(coo_mat))
np.fill_diagonal(coo_mat,0)                     
asso_matrix=np.tril(coo_mat,0)                # 삼각행렬로 바꿈
class_matrix=pd.DataFrame(asso_matrix)              
column_name=pd.DataFrame(word_list) 

#class_matrix.to_csv(path+'coci_matrix.csv',index=False)
id_=[]
for i in range(len(column_name)):
    name='n{c}'
    name=name.format(c=i)
    id_.append(name)
column_name['id']=id_
class_matrix.columns=id_
##node id reviese
#class_matrix.to_csv(path+'patent_matrix_min_5.csv',index=False)
class_matrix=class_matrix.convert_objects(convert_numeric=True)
class_matrix=class_matrix.fillna(0)
from scipy import sparse
b=sparse.csr_matrix(class_matrix)
bt=b.tocoo()
row_list=[]
col_list=[]
for i in bt.row:
    c='n'+str(i)
    row_list.append(c)
for i in bt.col:
    c='n'+str(i)
    col_list.append(c)

##edge source, target label revise
edge_df=pd.DataFrame({'source':row_list,#bt.row
                      'target':col_list,#bt.col
                      'weight':bt.data})
edge_df['type']='undirected'
edge_df=edge_df.loc[edge_df['weight'] > 1]
node_df=pd.DataFrame({'id':id_,
                      'label':word_list,
                      'count':diagonal_value})

edge_df.to_csv(save_dir+'keyword_edge.csv',index=False)
node_df.to_csv(save_dir+'keyword_node.csv',index=False)

#edge_df.to_csv(save_dir+'publication_edge.csv',index=False)
#node_df.to_csv(save_dir+'publication_node.csv',index=False)

