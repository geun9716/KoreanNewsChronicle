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
sw = 0
i = 0

for index in range(len(df)):
    if sw==0:    
        if(df.iloc[i]['date'] == '2019/02/01'):
            sw = 1
            s1 = df.head(i)
            df = df.tail(len(df) - i)
            i = 0
            print("1")
    elif sw==1:
        if(df.iloc[i]['date'] == '2019/03/01'):
            sw = 2
            s2 = df.head(i)
            df = df.tail(len(df) - i)
            i = 0
            print("2")
                        
    elif sw==2:
        if(df.iloc[i]['date'] == '2019/04/01'):
            sw = 3
            s3 = df.head(i)
            df = df.tail(len(df) - i)
            i = 0
            print("3")
                        
    elif sw==3:
        if(df.iloc[i]['date'] == '2019/05/01'):
            sw = 4
            s4 = df.head(i)
            df = df.tail(len(df) - i)
            i = 0
            print("4")
                        
    elif sw==4:
        if(df.iloc[i]['date'] == '2019/06/01'):
            sw = 5
            s5 = df.head(i)
            s6 = df.tail(len(df) - i)
            i = 0
            print("56")    
    i+=1

mylist = []
mylist.append(s1)
mylist.append(s2)
mylist.append(s3)
mylist.append(s4)
mylist.append(s5)
mylist.append(s6)

i = 0
for s in mylist:
    i+=1
    filename = "C:/Users/ghdtk/Project_test/Data/2019{0:02}_cluster_DBSCAN_eps6.csv".format(i)
    news_topic = s['topics'].tolist()
    
                
    news_topic = s['topics'].tolist()
    
    # # CountVectrizer로 토큰화
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(news_topic)
    
    X = normalize(X)
    
    # neigh = NearestNeighbors(n_neighbors=2)
    # nbrs = neigh.fit(X)
    # distances, indices = nbrs.kneighbors(X)
    
    
    m = DBSCAN(eps=0.6)
    
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
    s.sort_values(by='cnt', ascending=False).to_csv(filename, index=False, header=True,encoding="utf-8-sig")
    print(i)
