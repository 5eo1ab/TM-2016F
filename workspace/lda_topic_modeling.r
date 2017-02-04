##########################################
########### Topic Modeling for PSS  ###########
########## 2017.1.25 @ Inno LAB ######
##########################################

library(topicmodels)
library(gistr)
library(NLP)
library(tm)

############################################################
################## read meta data #####################
getwd()
setwd("D:/Paper_2017/workspace/data") # /Users/seo/lab
final_data <- read.csv("dataset_lemma.csv") # INPUT : meta dataset
dim(final_data)

idx_lemma = dim(final_data)[2]
lemma <- final_data[,idx_lemma]
final_data <- final_data[-idx_lemma]
dim(final_data)
AbsCorpus <- Corpus(VectorSource(lemma))
rm(lemma)
rm(idx_lemma)

#AbsDTM <- read.csv("doc-term_matrix_freq.csv")

AbsDTM <- DocumentTermMatrix(AbsCorpus, control = list(minWordLength = 2))
dfMatrix <- inspect(AbsDTM)
DF <- as.data.frame(dfMatrix, stringsAsFactors = FALSE)




##########################################
############## Topic Modeling ##############

setwd("../topic_model")
getwd()

num_topic <- c(5,10) #토픽 수
start.time <- Sys.time()
for (t in 1:length(num_topic)){
  NTopic <- num_topic[[t]] # Topic Modeling: LDA의 토픽수 정의
  
  ptm <- proc.time()
  for (l in c(1000,5000,10000)){ #c(1000,5000,10000)
    Gibbs_LDA <-LDA(AbsDTM, NTopic, method = "Gibbs", control = list(iter = l))
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
    write.csv(Top20Papers,  paste("topic-doc_list_t",NTopic,"_i",l,".csv",sep=""))
    print(paste("topic-doc_list_t",NTopic,"_i",l,".csv",sep=""))
    
  }
}
end.time <- Sys.time()
end.time - start.time
getwd()

##########################################


