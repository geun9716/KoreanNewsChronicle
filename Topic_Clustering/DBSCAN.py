from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

import numpy as np
import pandas as pd
import csv
import math
from collections import Counter
import matplotlib.pyplot as plt

df=pd.read_csv('C:/Users/geun/KoreanNewsChronicle/Topic_Abstract/Data/201901.csv',encoding='utf-8')

# 결측지 행 제거 후 topics에 있는 것을 추출
s = df.dropna()
news_topic = s['topics'].tolist()

# # CountVectrizer로 토큰화
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(news_topic)

X = normalize(X)

# neigh = NearestNeighbors(n_neighbors=2)
# nbrs = neigh.fit(X)
# distances, indices = nbrs.kneighbors(X)


m = DBSCAN(eps=0.7, min_samples = 10)

m.fit(X)

labels = m.labels_

s['labels'] = labels

hot_topic_index = Counter(s['labels']).most_common()
hot_topic = dict(hot_topic_index)

print(hot_topic)

index = []
for row in s['labels']:
    index.append(hot_topic[row])

s['cnt'] = index
s.sort_values(by='cnt', ascending=False).to_csv('./Topic_Clustering/201901_cluster_DBSCAN.csv', index=False, header=True,encoding="utf-8-sig")
