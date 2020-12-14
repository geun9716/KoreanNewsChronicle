from wordcloud import WordCloud
import matplotlib.pyplot as plt
import csv
import pandas as pd
import sys
from collections import Counter

df = pd.read_csv("./Visualize/201901_cluster_DBSCAN.csv", encoding="utf-8")

df.dropna()
for i in range(0, 20, 1):
    topics = []
    for index, row in df.iterrows():
        if(row['labels'] == i):
            topics.extend(row['topics'].split(', '))

    hot_topic_index = Counter(topics).most_common(20)
    hot_topic = dict(hot_topic_index)

    print(hot_topic)
    wordcloud = WordCloud(font_path='Visualize/malgun.ttf', background_color='white').generate_from_frequencies(dict(hot_topic))

    plt.figure(figsize=(22,22)) #이미지 사이즈 지정
    plt.imshow(wordcloud, interpolation='lanczos') #이미지의 부드럽기 정도
    plt.axis('off') #x y 축 숫자 제거
    # plt.show()
    plt.savefig('cluster_' + str(i) + '.png')
