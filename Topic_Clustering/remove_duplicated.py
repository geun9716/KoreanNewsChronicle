import csv
import pandas as pd

df=pd.read_csv('C:/Users/ghdtk/OneDrive/Desktop/VSCode/Python/Korean_News_Chronicle/KoreanNewsChronicle/Topic_Abstract/Data/201901.csv',encoding='utf-8')

print(len(df))

dp = df.duplicated(['headline'], keep='first')
count = 0
for b in dp:
    if(b == True):
        df.drop(df.index[count], inplace = True)
        count -= 1
    count += 1

print(len(df))