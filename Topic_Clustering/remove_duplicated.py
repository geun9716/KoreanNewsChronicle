import csv
import pandas as pd

filename = '201912.csv'

df=pd.read_csv(filename,encoding='utf-8')
print('원래 기사 수 : ',len(df))
df = df.dropna()        #토픽이 없는 기사 제거
print('토픽이 없는 기사 제거후 기사수 : ',len(df))
stopword = ['A씨', '만', '억', '조', '차', '그', '시', '대', '위', '분', '측', '곳']
for index, row in df.iterrows():
    topic = row['topics'].split(', ')
    for str in topic:
        if(str in stopword):
            topic.remove(str)
    topic_str = ", ".join(topic)
    df.loc[index, 'topics'] = topic_str
dp = df.duplicated(['headline'], keep='first')
count = 0
for b in dp:            #중복된 기사 제거
    if(b == True):
        df.drop(df.index[count], inplace = True)
        count -= 1
    count += 1
print('중복된 기사 제거후 기사수 : ',len(df))
tmp_index=[]
for index, row in df.iterrows():
    tmp = row['topics'].split(',')
    if len(tmp) < 4:
        tmp_index.append(index)
df = df.drop(tmp_index)
print('토픽이 3개 이하 밖에 없는 기사 제거후 기사수 : ',len(df))
df.to_csv(filename, index=False, header=True, encoding="utf-8-sig")
print(filename + 'done')