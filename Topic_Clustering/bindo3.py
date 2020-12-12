import pandas as pd
from collections import Counter
from pandas import Series, DataFrame

#필요없는 것을 먼저 제거후 돌리기

cluster_num=500

filename = "201901_clustered_500.csv"
file = pd.read_csv(filename,engine='python')

index=file['cluster_number']
topics=file['topic']



high_cluster=[]


def frequency_sort(data):
	rt_data = []
	for d, c in Counter(data).most_common():
		for i in range(c):
			rt_data.append(d)
            
	return rt_data

lista=[]
listb=[]
listc=[]

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

    check1=count[0][0]
    check2=""
    check3=""
    if(len(count)>1):
        check2=count[1][0]

    count_match=0

    if(result>=0.9 and cluster_count>1):

        for i in range(0,index.size):
            if(index[i]==j):
                if(topics[i].find(check1)>-1 and topics[i].find(check2)>-1 ):
                    count_match=count_match+1


        if(count_match==cluster_count):
            temp=check1+","+check2+","+check3
            print(str(j)+":"+count[0][0] + ",[나온 횟수 :"+str(count[0][1]) + "]," +"[cluster 개수 :"+ str(cluster_count)+"]" + ", [확률 : "+str(result)+"]")
            lista.append(j)
            listb.append(cluster_count)
            listc.append(temp)


        
df1 = pd.DataFrame(lista)
df2 = pd.DataFrame(listb)
df3 = pd.DataFrame(listc)

df=pd.concat([df1,df2,df3],axis=1)

df.to_csv("clusters2.csv", mode='w')

#나온 csv는 정렬해서 확인해본 결과 맘에 안듦. 일단 왼쪽순으로 index, cluster 파일 index, cluster 개수
        




         
                         

