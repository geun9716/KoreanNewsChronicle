import tomotopy as tp
import pandas as pd

stopwords = []
topics = []

def extract_topic(extracted_topic):
    model = tp.LDAModel(k=1, alpha=0.1, eta=0.001, min_cf=3,min_df=1, tw=tp.TermWeight.PMI)
    model.add_doc(extracted_topic) #추출하고 모델안의 문헌을 넣는다. 즉, 학습과정에 쓰일 문헌을 생성
    model.train(0) #학습 초기화
    s = ""
    for j in range(0,100):
        model.train(20) #문헌 학습, 안에 숫자는 깁스 샘플링의 반복횟수
		#이때 기본값으로 시스템내 가용한 모든 스레드의 개수사용, 그리고 병렬화 방법을 찾아서 실행시켜준다
    for k in range(model.k): #k는 토픽의 개수
        res = model.get_topic_words(k, top_n=10) #하위 토픽 i에 해당하는 top_n개의 단어 반환
        s = ', '.join(w for w, p in res)
    return s
    
df=pd.read_csv('C:/Users/ghdtk/Project_test/Data/2019_after.csv', encoding='ANSI')
N_list = df['modified_N_list']

nouns = []

for noun in N_list.tolist():
    noun = noun.strip("[]").replace("'", "")
    nouns.append(noun.split(", "))
    
    
f = open("C:/Users/ghdtk/Project_test/Data/한국어불용어100.txt", "r", encoding = 'utf-8')
for line in f:
    stopwords.append(line.split('\t')[0])
f.close()

for noun in nouns:
    Noun = [word for word in noun if word not in stopwords]
    topics.append(extract_topic(Noun))
    
df['topics'] = topics
df.to_csv("C:/Users/ghdtk/Project_test/Data/2019_after_LDA.csv", encoding="ANSI")
