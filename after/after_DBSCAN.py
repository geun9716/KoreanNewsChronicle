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

df=pd.read_csv('C:/Users/ghdtk/Project_test/Data/2019_after_LDA.csv', encoding = "ANSI")

# 결측지 행 제거 후 topics에 있는 것을 추출
df = df.dropna()
s = pd.DataFrame()
for i in range(len(df)):
    if len(df.iloc[i]['topics'].split(", ")) >= 3:
        s = s.append(df.iloc[i])
    if(i % 10000 == 0):
        print(i)

news_topic = s['topics'].tolist()

# # CountVectrizer로 토큰화
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(news_topic)

X = normalize(X)

# neigh = NearestNeighbors(n_neighbors=2)
# nbrs = neigh.fit(X)
# distances, indices = nbrs.kneighbors(X)


m = DBSCAN(eps=0.6, min_samples = 5)

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
len(s)
s = s[s['labels'] != -1]
s.sort_values(by='cnt', ascending=False).to_csv('C:/Users/ghdtk/Project_test/Data/2019_cluster_DBSCAN_eps6_topic3.csv', index=False, header=True,encoding="utf-8-sig")

