import pandas as pd
from collections import Counter
from pandas import Series, DataFrame

#필요없는 것을 먼저 제거후 돌리기

cluster_num=500

filename = "201901_cluster500.csv"
file = pd.read_csv(filename,engine='python')

index=file['labels']
topics=file['topics']



high_cluster=[]


def frequency_sort(data):
	rt_data = []
	for d, c in Counter(data).most_common():
		for i in range(c):
			rt_data.append(d)
            
	return rt_data

lista=[]
listb=[]

for j in range(0,cluster_num-1):
    cluster_count=0
    all=""
    for i in range(0,index.size):
        if(index[i]==j):
            all+=topics[i]
            cluster_count=cluster_count+1
            
    cluster_topics=all.split(',')    
    count=Counter(cluster_topics).most_common()
    result=int(count[0][1])/cluster_count
    if(result>=0.9):
        print(str(j)+":"+count[0][0] + ",[나온 횟수 :"+str(count[0][1]) + "]," +"[cluster 개수 :"+ str(cluster_count)+"]" + ", [확률 : "+str(result)+"]")
        lista.append(j)
        listb.append(cluster_count)

df = pd.DataFrame([ x for x in zip(lista,listb)])
df.to_csv("clusters3.csv", mode='w')

#나온 csv는 정렬해서 확인해본 결과 맘에 안듦. 일단 왼쪽순으로 index, cluster 파일 index, cluster 개수
        




         
                         

