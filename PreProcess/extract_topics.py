import tomotopy as tp
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
filename="datas.txt"  #파일 경로
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

file = open("20200101-20200131_topic_txt.csv", "w", encoding='utf-8', newline = '')
writer = csv.writer(file)
writer.writerow(['index', 'topics'])
for i, line in enumerate(open(filename, encoding='utf-8')): #해당 경로의 파일을 받아와 한 라인씩 model에 추가
    model = tp.LDAModel(k=1, alpha=0.1, eta=0.01, min_cf=3,min_df=1, tw=tp.TermWeight.PMI)
    model.add_doc(tokenize(line)) #추출하고 모델안의 문헌을 넣는다. 즉, 학습과정에 쓰일 문헌을 생성
    model.train(0) #학습 초기화
    s = ""
    for j in range(0,100):
        model.train(20) #문헌 학습, 안에 숫자는 깁스 샘플링의 반복횟수
		#이때 기본값으로 시스템내 가용한 모든 스레드의 개수사용, 그리고 병렬화 방법을 찾아서 실행시켜준다
    for k in range(model.k): #k는 토픽의 개수
        res = model.get_topic_words(k, top_n=10) #하위 토픽 i에 해당하는 top_n개의 단어 반환
        s = ', '.join(w for w, p in res)
    writer.writerow([i, s])
    print(i, s)
file.close()
print("End")