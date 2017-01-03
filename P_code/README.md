### Code Descriptions

#### File List for Data Preprocessing
- data_split_sciencedirect.py
>- Input : science.txt ; publication_list.txt
>- Output : dataset_v1.csv ; skip_doc_v1.txt
>- Extract information of abstract / title / author / journal / year according to pattern of text document (bibliographic information - abstract information - keyword information)
>  - Directly modify csv partially exceptions cases

- data_preprocessing_m1.py
>- Input : dataset_v1.csv
>- Output : dataset_v1.csv ; abbr_dic_v0.csv
>- Extract abbreviations and abbreviated full name information according to the abbreviation pattern (ie, Product Service System (PSS)) used in the abstract

- data_preprocessing_m3.py
>- Input : dataset_v2.csv ; abbr_dic_v1.csv
>- Output : dataset_v3.csv
>- Key preprocessing process (punctuation removal - tokenization - elimination of stopwords - POS tagging - lemmatization)

- data_preprocessing_m4.py
>- Input : dataset_v3.csv ; abbr_dic_v1.csv ; stopwords_lemma.txt
>- Output : dataset_v4.csv
>- After lemmatization, second elimination of stopwords based on additionally constructed list of stopwords, and also remove the words appearing less than 2 times.

- text_vectorization_tf.py
>- Input : dataset_v4.csv 
>- Output : doc-term_matrix_freq.csv ; word_list_v1.txt
>- Build 'Term-Freqeuncy Matrix' using CountVectorizer of Sklearn.feature_extraction.text
>  - At this time, the Term-Frequency Matrix is the LDA's input
>  - The Term-Frequency Matrix, represented as a binary, is used as input to the Co-occurance matrix. And the co-occurrence matrix is used as the input of the keyword network.


#### Other File List
- tf2node-edge_list.py
>- Input : doc-term_matrix_freq.csv ; word_list_v1.txt
>- Output : keyword_node.csv ; keyword_edge.csv
>- Build 'Edge List' and 'Node List' from 'Term-Freqeuncy Matrix'
>  - Purpose of network analysis
>  - Unit is keyword

- ~~topic_modeling.r~~
>- Input : dataset_v4.csv ; doc-term_matrix_freq.csv
>- Output(each # of topic and iterations)
>  - probability_doc-topic
>  - probability_topic-term
>  - topic-term_list
>  - topic-doc_list
>- Topic Modeling using LDA algorithms

- topic_aggregation.py
>- Input : dataset_v4.csv ; lda_prob_doc-topic.csv ; lda_prob_topic-term.csv
>- Output : res_year_topic.csv ; res_pub_topic.csv
>- Topic probability distribution is aggregated.

