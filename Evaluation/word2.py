import numpy as np

from konlpy.utils import pprint
from kiwipiepy import Kiwi, Option

kiwi=Kiwi()
kiwi.prepare()

mydoclist = ['북 미 정상회담' ,
            '2019 남 북 미 정상회담']

def tokenize(sent): # 파일의 라인을 분석할 tokenize 함수
    res, score = kiwi.analyze(sent)[0] # 첫번째 결과를 사용한다, 분석할때 나오는 결과에서 단어만 추출
    return [word
            for word, tag, _, _ in res
            if tag.startswith('N') and word] #불용어사전 적용

doc_nouns_list=[]

for doc in mydoclist:
       nouns=tokenize(doc)
       doc_nouns = ''

       for noun in nouns:
              doc_nouns+=noun+ ' '
       doc_nouns_list.append(doc_nouns)

for i in range(0,2):
       print('doc'+str(i+1)+' : '+str(doc_nouns_list[i]))              

def cos_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    l2_norm = (np.sqrt(sum(np.square(v1))) * np.sqrt(sum(np.square(v2))))
    similarity = dot_product / l2_norm     
    
    return similarity

from sklearn.feature_extraction.text import TfidfVectorizer


tfidf_vect_simple = TfidfVectorizer(min_df=1)
feature_vect_simple = tfidf_vect_simple.fit_transform(doc_nouns_list)

print(feature_vect_simple.shape)
print(type(feature_vect_simple))    


# TFidfVectorizer로 transform()한 결과는 Sparse Matrix이므로 Dense Matrix로 변환. 
feature_vect_dense = feature_vect_simple.todense()

#첫번째 문장과 두번째 문장의 feature vector  추출
vect1 = np.array(feature_vect_dense[0]).reshape(-1,)
vect2 = np.array(feature_vect_dense[1]).reshape(-1,)

#첫번째 문장과 두번째 문장의 feature vector로 두개 문장의 Cosine 유사도 추출
similarity_simple = cos_similarity(vect1, vect2)
print('문장 1, 문장 2 Cosine 유사도: {0:.3f}'.format(similarity_simple)) 