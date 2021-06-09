import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

doc_nouns_list=[]

#코사인 유사도 계산
def cos_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    l2_norm = (np.sqrt(sum(np.square(v1))) * np.sqrt(sum(np.square(v2))))
    similarity = dot_product / l2_norm     
    
    return similarity
cluster_topic = ['도널드트럼프', '북한', '정상회담', '미국', '김정은', '핵', '중국', '협상', '회담', '북미' ,'차' ,'대통령' ,'정상' ,'하노이' ,'대화']
oasis_topic= ['북한', '정상회담', '미국', '위원장', '대통령', '도널드트럼프', '회담', '김정은', '북미', '북미정상', '협상', '하노이', '한반도', '대화', '정상']

doc_nouns_list.append(' '.join(cluster_topic))
doc_nouns_list.append(' '.join(oasis_topic))

print("KNC_topic : ",doc_nouns_list[0])
print("Oasis_topic : ",doc_nouns_list[1])

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