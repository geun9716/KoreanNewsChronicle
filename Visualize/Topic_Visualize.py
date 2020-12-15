from wordcloud import WordCloud
import matplotlib.pyplot as plt
import csv
import pandas as pd
import sys
from collections import Counter

lists=[]

df = pd.read_csv("2019.csv", encoding="utf-8")

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
            hot_topic_index = Counter(topics).most_common(20)
            hot_topic = dict(hot_topic_index)
            lists.append(hot_topic)

            wordcloud = WordCloud(font_path='Visualize/malgun.ttf', background_color='white').generate_from_frequencies(dict(hot_topic))

            plt.figure(figsize=(30,30)) #이미지 사이즈 지정
            plt.imshow(wordcloud, interpolation='lanczos') #이미지의 부드럽기 정도
            plt.axis('off') #x y 축 숫자 제거
            # plt.show()
            plt.savefig('month_' + str(i) + '_cluster_' + str(j) + '.png')
        elif(count == 0):
            break
