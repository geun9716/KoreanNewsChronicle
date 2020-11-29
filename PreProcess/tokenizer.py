import csv
import sys
import io
import re # 정규표현식 패키지
from kiwipiepy import Kiwi, Option
import tomotopy as tp

class Reader:
    def __init__(self, filePath):
        self.file = open(filePath,'r',encoding='UTF-8')
    
    def read(self, id):
        if id == 0: self.file.seek(0)
        return self.file.readline()

reader = Reader('datas.txt')

file = open("한국어불용어100.txt", 'r', encoding="utf-8")
stopword=[]

while True:
    line = file.readline()
    if not line: break
    wordlist = line.split('\t')
    if (wordlist[1].startswith('N')):
        stopword.append(wordlist[0])

print(stopword)
filename="201901_tokenize.txt"  #파일 경로
file = open(filename, 'r', encoding="UTF-8")
kiwi=Kiwi()
kiwi.extract_add_words(reader.read)
kiwi.prepare()
stopwords = set(stopword)


def tokenize(sent): # 파일의 라인을 분석할 tokenize 함수
    res, score = kiwi.analyze(sent)[0] # 첫번째 결과를 사용한다, 분석할때 나오는 결과에서 단어만 추출
    return [word
            for word, tag, _, _ in res
                if tag.startswith('N') and word not in stopwords] #불용어사전 적용


#LDA 모델을 적용해서 토픽 추출, k는 topic 개수
#alpha는 문헌-토픽 디리클레 분포의 하이퍼 파라미터
#eta는 토픽-단어 디리클레 분포의 하이퍼 파라미터 두개다 상수인듯하다
#min_cf는 단어의 최소 장서 빈도수, 전체 문헌내 출현빈도
#min_df는 단어의 최서 문헌 빈도수, 출현한 문헌 숫자수 의미
#tw는 용어 가중치 기법으로, ONE, IDF, PMI를 사용가능, ONE 보다는 PMI나 IDF 둘중 하나 사용 

file = open("201901_token.csv", "w", encoding='utf-8', newline = '')
writer = csv.writer(file)
writer.writerow(['Morp Analize'])
for i, line in enumerate(open(filename, encoding='utf-8')): #해당 경로의 파일을 받아와 한 라인씩 model에 추가