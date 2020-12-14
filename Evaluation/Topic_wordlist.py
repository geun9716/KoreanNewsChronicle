from wordcloud import WordCloud
import matplotlib.pyplot as plt
import csv
import pandas as pd
import sys
from collections import Counter

lists=[]

df = pd.read_csv("./Visualize/2019.csv", encoding="utf-8")

df.dropna()
for i in range(1, 13, 1):
    for j in range(0, 100, 1):
        count = 0
        topics = []
        for index, row in df.iterrows():
            tmp = row['labels'].split(',')
            month = tmp[0]
            cluster_num = tmp[1]
            if(int(month) == i and cluster_num == str(j)):
                count+=1
                topics.extend(row['topics'].split(', '))
        if(count >= 40):
            print(i, j)
            hot_topic_index = Counter(topics).most_common(10)
            hot_topic = dict(hot_topic_index)
            tmp = ', '.join(list(hot_topic.keys()))
            print(tmp)
            lists.append(tmp)
        elif(count == 0):
            break

s = pd.DataFrame(lists, columns=['wordlist'])
s.to_csv('2019_wordlist.csv', index=False, header=True,encoding="utf-8-sig")