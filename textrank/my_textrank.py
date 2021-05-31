from konlpy.tag import Komoran
import pandas as pd
from kss import split_sentences
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np
A2 = np.array([1,2,3,4])
df = pd.read_csv("C:/Users/ghdtk/OneDrive/Desktop/VSCode/Python/Korean_News_Chronicle/KoreanNewsChronicle/Topic_Clustering/Data/2019.csv")
df2 = df.head(257)
texts = df2['text']

# text = texts[0]
# for i in range(1, 257):
#     text = text + texts[i]


class SentenceTokenizer(object):
    def __init__(self):
        self.okt = Komoran()

    def text_to_sentences(self, text):
        sentences = split_sentences(text)
        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
               sentences[idx - 1] += (' ' + sentences[idx])
               sentences[idx] = ''
        
        while "" in sentences:
            sentences.remove("")
        
        return sentences

    def get_nouns(self, sentences):
        nouns = []
        for sentence in sentences:
            nouns.append(" ".join(noun for noun in self.okt.nouns(str(sentence))))
        
        return nouns

class GraphMatrix(object):
    def __init__(self):
        self.tfidf = TfidfVectorizer()
        self.cnt_vec = CountVectorizer()
        self.graph_sentence = []
        
    def build_sent_graph(self, sentence):
        tfidf_mat = self.tfidf.fit_transform(sentence).toarray()
        self.graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
        return self.graph_sentence
    
    def build_words_graph(self, sentence):
        cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
        vocab = self.cnt_vec.vocabulary_
        return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}


class Rank(object):
    def get_ranks(self, graph, d=0.85): # d = damping factor
        A = graph
        
        matrix_size = A.shape[0]
        for id in range(matrix_size):
            A[id, id] = 0 # diagonal 부분을 0으로
            link_sum = np.sum(A[:,id]) # A[:, id] = A[:][id]
            if link_sum != 0:
                A[:, id] /= link_sum
                A[:, id] *= -d
                A[id, id] = 1
        
        myList = []
        for a in A:
            tmpList = []
            for aa in a:
                tmpList.append(aa)
            myList.append(tmpList)

        i = 0
        for tmp in range(len(myList)):
            a = myList[i]
            sw = False
            for aa in a:
                if(aa > 0.000001 or aa < -0.000001):
                    sw = True
                    break
            if(sw == False):
                for j in range(len(myList)):
                    del myList[j][i]
                del myList[i]
                i -= 1
            i += 1
        
        A = np.array(myList)
        B = (1-d) * np.ones((len(A), 1))
        ranks = np.linalg.solve(A, B) # 연립방정식 Ax = b
        return {idx: r[0] for idx, r in enumerate(ranks)}
    
class TextRank(object):
    def __init__(self, text):
        self.text = text

    def make_sentences(self):
        self.sent_tokenize = SentenceTokenizer()
        
        self.sentences = self.sent_tokenize.text_to_sentences(self.text)

    def execute_textrank(self, sentences):
        self.nouns = self.sent_tokenize.get_nouns(self.sentences)
       
        self.graph_matrix = GraphMatrix()
        self.sent_graph = self.graph_matrix.build_sent_graph(self.nouns)
        self.words_graph, self.idx2word = self.graph_matrix.build_words_graph(self.nouns)
        
        self.rank = Rank()
        self.sent_rank_idx = self.rank.get_ranks(self.sent_graph)
        self.sorted_sent_rank_idx = sorted(self.sent_rank_idx, key=lambda k: self.sent_rank_idx[k], reverse=True)
        
        self.word_rank_idx = self.rank.get_ranks(self.words_graph)
        self.sorted_word_rank_idx = sorted(self.word_rank_idx, key=lambda k: self.word_rank_idx[k], reverse=True)

    def summarize(self, sent_num=3):
        summary = []
        index=[]
        for idx in self.sorted_sent_rank_idx[:sent_num]:
            index.append(idx)
        
        index.sort()
       
        for idx in index:
            summary.append(self.sentences[idx])
       
        return summary
       
    def keywords(self, word_num=10):
        rank = Rank()
        rank_idx = rank.get_ranks(self.words_graph)
        sorted_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True)
        keywords = []
        index=[]
        for idx in sorted_rank_idx[:word_num]:
           index.append(idx)
           
        #index.sort()
        for idx in index:
            keywords.append(self.idx2word[idx])
            
        return keywords


summarized_text = []
for i in range(257):
    text = texts[i]
    textrank = TextRank(text)
    textrank.make_sentences()
    textrank.execute_textrank(textrank.sentences)
    for sentence in textrank.summarize(3):
        summarized_text.append(sentence)
    
    

textrank.execute_textrank(summarized_text)

num = 1
for row in textrank.summarize(3):
    print(num, ":", row + "\n")
    num+=1

print('keywords :',textrank.keywords())


# text = texts[0]
# textrank = TextRank(text)
# textrank.make_sentences()
# textrank.execute_textrank(textrank.sentences)
# num = 0
# for sentence in textrank.summarize(3):
#     num += 1
#     print(num, ":", sentence, "\n")

