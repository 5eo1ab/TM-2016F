##########################################
########### Topic Modeling in R ###########
########## 2016. 7.~ 8. @ Inno Lab ######
##########################################

# Require input : final dataset, result of lemmatization
##########################################
install.packages("devtools")
install.packages("data.table")
install.packages("servr")
install.packages("topicmodels")
install.packages("gistr")
install.packages("tm")

#library("XML")
library("foreach")
library("plyr")
library("data.table")
library("parallel")
#library(LDAvis)
#library(LDAvisData)
library(servr)
library(topicmodels)
library(gistr)
library(NLP)
library(tm)
#library(SnowballC)
library(httr)
#library(XML)
library(devtools)
devtools::install_github("tillbe/jsd")

############################################################
################## read meta data #####################
getwd()
setwd("D:/course_2016_fall/Unstructured_Data_Analysis/Project/data") # /Users/seo/lab
final_data <- read.csv("dataset_v4.csv") # INPUT : meta dataset
dim(final_data)

  analysis.type <- c("paper", "patent")
  TYPE <- analysis.type[1]
  rm(analysis.type)

lemma <- final_data[,8]
final_data <- final_data[-1]
AbsCorpus <- Corpus(VectorSource(lemma))
rm(lemma)

DF <- read.csv("doc-term_matrix_freq.csv")
  DF <- DF[-1]
AbsDTM <- DF


################################  analysis  #########################################
############################## topic modeling #######################################
#####################################################################################

  getwd()
  setwd("D:/inno_lab_proj/ETRI_Scopus") # /Users/seo/lab
  final_data <- read.csv("patent_table.csv") # INPUT : beta dataset
  dim(final_data)
  final_data <- final_data[-1]
  analysis.type <- c("paper", "patent")
  TYPE <- analysis.type[1]
  rm(analysis.type)
  
  ############  Letm_data 읽기 ##################
  letm_all <- read.csv("letm_re_all.csv") # INPUT : lemma data
  #lemmatization data을 copus형태로 다시 정의하는 것이 필요
  #lemma <- letm_all[,3]
  lemma <- letm_all[,2]
  AbsCorpus <- Corpus(VectorSource(lemma))
  rm(lemma)
  rm(letm_all)
  
  memory.limit()
  memory.limit(size=10000)

# term-document matrix 만들기
AbsDTM <- DocumentTermMatrix(AbsCorpus, control = list(minWordLength = 2))
dfMatrix <- inspect(AbsDTM)
DF <- as.data.frame(dfMatrix, stringsAsFactors = FALSE)

  # Each row of the input matrix needs to contain at least one non-zero entry (에러 처리)
  rowTotals <- apply(AbsDTM , 1, sum) #Find the sum of words in each Document
  dtm.new   <- AbsDTM[rowTotals> 0, ]           #remove all docs without words
  dim(dtm.new)[[1]]
  dim(DF)[[1]]
  dim(DF)[[1]] - dim(dtm.new)[[1]]
  
  
  # if number of doc isn't equal.
  mat <- as.matrix(dtm.new)
  DF <- as.data.frame(mat)
  AbsDTM <- dtm.new
  # if number of doc is equal.
  rm(dtm.new)
  
  write.csv(DF, "df_dfMatrix.csv") 



##########################################
############## Topic Modeling ##############

setwd("../topic_model")
getwd()

num_topic <- c(3,4,5,7,10,15) #토픽 수(20,30,50,100)
start.time <- Sys.time()
for (t in 1:length(num_topic)){
  NTopic <- num_topic[[t]] # Topic Modeling: LDA의 토픽수 정의
  
  ptm <- proc.time()
  for (l in c(1000)){ #c(1000,5000,10000)
    Gibbs_LDA <-LDA(AbsDTM, NTopic, method = "Gibbs", control = list(iter = l))
    # VEM_LDA <- LDA(AbsDTM, NTopic, method = "VEM")
    proc.time() - ptm
    
    NTerm <- 50
    Gibbs_terms <- terms(Gibbs_LDA, NTerm) # 각 토픽에 할당된 단어: Gibbs 추정
    write.csv(Gibbs_terms, paste("topic-term_list_t",NTopic,"_i",l,".csv",sep=""))# 각 토픽단어 저장
    print(paste("topic-term_list_t",NTopic,"_i",l,".csv",sep=""))
    
    # 각 설정별 토픽의 상위 특허 정보 추출 ## Topic 20개 상위 20개 특허 번호 #
    Gibbs_topics <- topics(Gibbs_LDA, 1)
    Topic_posterior <- posterior(Gibbs_LDA)$topics # 문서의 토픽 확률
    write.csv(Topic_posterior,paste("probability_doc-topic_t",NTopic,"_i",l,".csv",sep=""))
    print(paste("probability_doc-topic_t",NTopic,"_i",l,".csv",sep=""))
    
    Term_posterior <- posterior(Gibbs_LDA)$terms # 각 토픽의 단어 출현 확률
    write.csv(Term_posterior,paste("probability_topic-term_t",NTopic,"_i",l,".csv",sep=""))
    print(paste("probability_topic-term_t",NTopic,"_i",l,".csv",sep=""))
    
    
    Top20Papers <- data.frame()
    N_paper = 20 # 보고싶은 상위 토픽 확룰 문서 개수
    for (c in 1:NTopic){
      sel_idx <- order(Topic_posterior[,c],decreasing = TRUE)[1:N_paper] 
      tmp_posterior <- data.frame(sel_idx, Topic_posterior[sel_idx, c]) #####
      colnames(tmp_posterior) <- c("patent_idx", "posterior")
      tmp_posterior <- tmp_posterior[order(tmp_posterior$posterior, decreasing = TRUE),]
      tmp_topic <- rep(paste("Topic_",c, sep=""),20) 
      tmp_papers <- cbind(tmp_topic, tmp_posterior[1:20,2], final_data[tmp_posterior$patent_idx[1:20],])
      Top20Papers <- rbind(Top20Papers, tmp_papers)
    }
    write.csv(Top20Papers,  paste("topic-doc_list_t_",NTopic,"_i",l,".csv",sep=""))
    print(paste("topic-doc_list_t_",NTopic,"_i",l,".csv",sep=""))
    
    # Topic Probability (Total rate) ## is this only averagy of topic probability?????
    #Topic.Probability <- colSums(Topic_posterior)/dim(Topic_posterior)[[1]]
    #Topic.Probability <- as.data.frame(Topic.Probability)
    #write.csv(Topic.Probability,paste("topic-prob_list_t",NTopic,"_i",l,".csv",sep=""))
    #print(paste("topic-prob_list_t",NTopic,"_i",l,".csv",sep=""))
    
    #write.csv(DM, paste("topic_jsd_matrix/jsd_",TYPE,"_t",NTopic,"_i",l,".csv",sep=""))
    #print(paste("topic_jsd_matrix/jsd_",TYPE,"_t",NTopic,"_i",l,".csv",sep=""))
  }
}
end.time <- Sys.time()
end.time - start.time
getwd()

##########################################

