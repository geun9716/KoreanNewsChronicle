from gensim.models import Word2Vec
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

model = Word2Vec.load('C:/Users/ghdtk/Project_test/ko.bin')


def plot_2d_graph(vocabs, xs, ys):
    plt.figure(figsize = (8,6))
    plt.scatter(xs, ys, marker = 'o')
    for i, v in enumerate(vocabs):
        plt.annotate(v, xy=(xs[i], ys[i]))

sentences = [['이것', '좋은', '제품'], 
              ['그것', '훌륭한', '제품'], 
              ['그것', '나쁜', '제품'], 
              ['저것', '최악', '제품'], 
              ]

word_vectors = model.wv

vocabs = word_vectors.vocab.keys()
word_vectors_list = [word_vectors[v] for v in vocabs]

print(word_vectors.similarity(w1='이것', w2='저것'))

from sklearn.decomposition import PCA
pca = PCA(n_components = 2)
xys = pca.fit_transform(word_vectors_list)
xs = xys[:, 0]
ys = xys[:, 1]

# plot_2d_graph(vocabs, xs, ys)
