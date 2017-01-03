### Data Descriptions

##### science.txt
- Initial data from sciencedirect.com(export search)
- Search keyword is "product service" W/5 system
  - it means "product service" and "system" within 5 space in words
- All of documents have been published since 2000.
- And limited to journal documents.
- 3526 documents were searched and there were 799 abstracts in the document.
  - We think that missing information will exist in the parsing process

##### dataset_v1.csv (799 by 7)
- Extract important bibliographic information
  - Year / Journal / Title / Author
  - partially extracted manually. 

##### dataset_v2.csv (799 by 7)
- Standardization of notation such as abbreviations

##### dataset_v3.csv (799 by 8)
- After the text preprocessing process, append lemmatization result

##### dataset_v4.csv (799 by 8)
- After lemmatization process, additional remove stopwords


