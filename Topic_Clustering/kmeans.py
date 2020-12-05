import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
import csv
import math

# 11줄 filename, 36줄 df = pd.read_csv, 75줄 file_write = open() 파일명 바꿔쓰기
# 54줄 n_clusters k 계수 바꿔쓰기

filename = "201901.csv"
news_press = []
news_category = []
news_headline = []
news_url = []
news_date = []
news_text = []

f = open(filename, "r", encoding='utf-8')
rdr = csv.reader(f)
for row in rdr:
    news_date.append(row[0])
    news_press.append(row[1])
    news_category.append(row[2])
    news_headline.append(row[3])
    news_url.append(row[4])
    news_text.append(row[5])
del news_press[0]
del news_category[0]
del news_headline[0]
del news_url[0]
del news_date[0]
del news_text[0]
f.close()

df = pd.read_csv(filename)
news_topic = df['topics'].tolist()

j = 0
for i in range(0, len(news_press), 1):
    a = news_topic[j]
    if(type(a) == type(1.1)):
        del news_press[j]
        del news_category[j]
        del news_headline[j]
        del news_url[j]
        del news_date[j]
        del news_topic[j]
        del news_text[j]
        j = j - 1
    j = j + 1

# 군집화 할 그룹의 갯수 정의
n_clusters = 500

s = df['topics'].dropna()
df = s.to_frame()
# CountVectrizer로 토큰화
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(news_topic)
# l2 정규화
X = normalize(X)
# k-means 알고리즘 적용
print("waiting for KMeans")
kmeans = KMeans(n_clusters=n_clusters).fit(X)

# trained labels and cluster centers
labels = kmeans.labels_
centers = kmeans.cluster_centers_
# labels에 merge
df['labels'] = labels

l = df['labels'].tolist()

file_write = open("201901_clustered_" + str(n_clusters) + ".csv",'w', encoding='utf-8', newline = '')
writer = csv.writer(file_write)
writer.writerow(["cluster_number", "date", "press", "category", "headline", "topic", "url", "text"])
for i in range(0, len(news_topic), 1):
    writer.writerow([l[i], news_date[i], news_press[i], news_category[i], news_headline[i], news_topic[i], news_url[i], news_text[i]])
file_write.close()
