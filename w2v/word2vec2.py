import pandas as pd
from gensim.models import word2vec
from gensim.models import Word2Vec

df = pd.read_csv("C:/Users/ghdtk/Project_test/Data/201901_topic.csv")
df = df.append(pd.read_csv("C:/Users/ghdtk/Project_test/Data/201902_topic.csv"))
df = df.append(pd.read_csv("C:/Users/ghdtk/Project_test/Data/201903_topic.csv"))
df = df.append(pd.read_csv("C:/Users/ghdtk/Project_test/Data/201904_topic.csv"))
df = df.append(pd.read_csv("C:/Users/ghdtk/Project_test/Data/201905_topic.csv"))
df = df.append(pd.read_csv("C:/Users/ghdtk/Project_test/Data/201906_topic.csv"))
df = df.append(pd.read_csv("C:/Users/ghdtk/Project_test/Data/201907_topic.csv"))
df = df.append(pd.read_csv("C:/Users/ghdtk/Project_test/Data/201908_topic.csv"))
df = df.append(pd.read_csv("C:/Users/ghdtk/Project_test/Data/201909_topic.csv"))
df = df.append(pd.read_csv("C:/Users/ghdtk/Project_test/Data/201910_topic.csv"))
df = df.append(pd.read_csv("C:/Users/ghdtk/Project_test/Data/201911_topic.csv"))
df = df.append(pd.read_csv("C:/Users/ghdtk/Project_test/Data/201912_topic.csv"))

word_list = []
topics = df['topics']
topics = topics.dropna()
for topic in topics:
    word = topic.split(', ')
    for w in word:
        if(len(w) <= 1):
            word.remove(w)
    word_list.append(word)
# model = Word2Vec.load('C:/Users/ghdtk/Project_test/ko.bin')
# model.wv.save_word2vec_format('C:/Users/ghdtk/Project_test/ko.bin.gz', binary = False)

my_model = Word2Vec(word_list, window = 100, size = 200, min_count = 1, sg = 1)


# my_model.intersect_word2vec_format('C:/Users/ghdtk/Project_test/ko.bin.gz', binary = False)

word_vectors = my_model.wv
vocabs = word_vectors.vocab.keys()
word_vectors_list = [word_vectors[v] for v in vocabs]

# print(word_vectors.similarity(w1='정부', w2='대통령'))
print(word_vectors.most_similar("문재인"))
