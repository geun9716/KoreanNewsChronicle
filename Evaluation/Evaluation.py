import numpy as np
import tomotopy as tp
from konlpy.utils import pprint
from kiwipiepy import Kiwi, Option
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
kiwi=Kiwi()
kiwi.prepare()


file = open("한국어불용어100.txt", 'r', encoding="utf-8")
stopword=[]

while True:
    line = file.readline()
    if not line: break
    wordlist = line.split('\t')
    if (wordlist[1].startswith('N')):
        stopword.append(wordlist[0])

stopwords = set(stopword)     

def tokenize(sent): # 파일의 라인을 분석할 tokenize 함수
    res, score = kiwi.analyze(sent)[0] # 첫번째 결과를 사용한다, 분석할때 나오는 결과에서 단어만 추출
    return [word
            for word, tag, _, _ in res
            if tag.startswith('N') and word not in stopwords] #불용어사전 적용


doc_nouns_list=['지소미아 한국 미국 종료 정부 결정 미 일본']

#코사인 유사도 계산
def cos_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    l2_norm = (np.sqrt(sum(np.square(v1))) * np.sqrt(sum(np.square(v2))))
    similarity = dot_product / l2_norm     
    
    return similarity

model = tp.LDAModel(k=1, alpha=0.1, eta=0.01, min_cf=2)

filename='test.txt'
for i, line in enumerate(open(filename, encoding='utf-8')):
    model.add_doc(tokenize(line)) 

model.train(0) 

for i in range(200):
    print('Iteration {}\tLL per word: {}'.format(i, model.ll_per_word))
    model.train(1)

oasis_topic=[]

for i in range(model.k):
    # 토픽 개수가 총 20개이니, 0~19번까지의 토픽별 상위 단어 10개를 뽑아봅시다.
    res = model.get_topic_words(i, top_n=7)
    
    for w, p in res:
       oasis_topic.append(w)
    
    

oasis=' '.join(oasis_topic)

print("KNC_topic : ",doc_nouns_list[0])
print("Oasis_topic : ",oasis)

doc_nouns_list.append(oasis)

tfidf_vect_simple = TfidfVectorizer(min_df=1)
feature_vect_simple = tfidf_vect_simple.fit_transform(doc_nouns_list)

# TFidfVectorizer로 transform()한 결과는 Sparse Matrix이므로 Dense Matrix로 변환. 
feature_vect_dense = feature_vect_simple.todense()

#첫번째 문장과 두번째 문장의 feature vector  추출
vect1 = np.array(feature_vect_dense[0]).reshape(-1,)
vect2 = np.array(feature_vect_dense[1]).reshape(-1,)

#첫번째 문장과 두번째 문장의 feature vector로 두개 문장의 Cosine 유사도 추출
similarity_simple = cos_similarity(vect1, vect2)

print('KNC_topic, Oasis_topic Cosine 유사도: {0:.3f}'.format(similarity_simple))