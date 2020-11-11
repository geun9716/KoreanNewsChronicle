import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans

df = pd.read_csv('C:/Users/ghdtk/OneDrive/Desktop/VSCode/Python/Korean_News_Chronicle/KoreanNewsChronicle/PreProcess/20200101-20200131_topic.csv')

# topic이 없는 행 삭제
s = df['topics'].dropna()
df = s.to_frame()

content = df['topics'].tolist()

# 군집화 할 그룹의 갯수 정의
n_clusters = 30

# CountVectrizer로 토큰화
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(content)
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
hl = df['topics'].tolist()

# 1번 군집 출력
for i in range(0, len(hl), 1):
    if(l[i] == 1):
        print(l[i], hl[i])