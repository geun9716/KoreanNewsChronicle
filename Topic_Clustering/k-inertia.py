import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style

df = pd.read_csv('20190101-20190131_topic.csv')

# topic이 없는 행 삭제
s = df['topics'].dropna()
df = s.to_frame()

content = df['topics'].tolist()

# CountVectrizer로 토큰화
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(content)
# l2 정규화
X = normalize(X)

# k-means 알고리즘 적용
sse = []    # 오차 제곱 합
for i in range(10, 200):   # k 계수 range 바꿔서 쓰기
    print("waiting for KMeans : ", i)
    km = KMeans(n_clusters=i, init='k-means++')
    km.fit(X)
    sse.append(km.inertia_)

plt.plot(range(100, 110), sse, marker='o') # 위에 range랑 동일한 range 사용
plt.xlabel('number of clusters')
plt.ylabel('SSE')
plt.show()