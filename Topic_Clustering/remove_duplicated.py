import csv
import pandas as pd

df=pd.read_csv('C:/Users/ghdtk/OneDrive/Desktop/VSCode/Python/Korean_News_Chronicle/KoreanNewsChronicle/Topic_Abstract/Data/201905.csv',encoding='utf-8')

# print('원래 기사 수 : ' + str(len(df)))

# dp = df.duplicated(['headline'], keep='first')
# count = 0
# for b in dp:            #중복된 기사 제거
#     if(b == True):
#         df.drop(df.index[count], inplace = True)
#         count -= 1
#     count += 1

# print('중복된 기사 제거후 기사수 : ' + str(len(df)))

df = df.dropna()        #토픽이 없는 기사 제거

# print('토픽이 없는 기사 제거후 기사수 : ' + str(len(df)))

# count = 0
# for index, row in df.iterrows():        #토픽이 한개인 기사 제거
#     if(len(row['topics'].split(', ')) == 1):
#         df.drop(df.index[count], inplace = True)
#         count -= 1
#     count += 1

# print('토픽이 한개밖에 없는 기사 제거후 기사수 : ' + str(len(df)))

stopword = ['A씨', '만', '억', '조']

for index, row in df.iterrows():
    topic = row['topics'].split(', ')
    for str in topic:
        if(str in stopword):
            topic.remove(str)

    topic_str = ", ".join(topic)
    df.loc[index, 'topics'] = topic_str

print(df)
# topic에서 stopword 제거도 추가 예정
