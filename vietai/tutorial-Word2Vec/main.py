from gensim.models import KeyedVectors
en_vectors = KeyedVectors.load_word2vec_format('data/wiki-news-300d-1M.vec', binary=False)

from gensim.models import Word2Vec
vi_vectors = Word2Vec.load('data/vi.bin').wv

# # Lưu ý: đối với model glove, cần chuyển về format word2vec
# # Ví dụ
# from gensim.scripts.glove2word2vec import glove2word2vec
# glove2word2vec('data/glove.6B.50d.txt', 'data/en.vec')

en_vectors.vocab

en_vectors["cat"]

print ("vector size: ", en_vectors.vector_size)
print ("vocab size: ", len(en_vectors.vocab))

print ("vector size: ", vi_vectors.vector_size)
print ("vocab size: ", len(vi_vectors.vocab))

en_vectors.most_similar("cat")


vi_vectors.most_similar("mèo")


sim_words = en_vectors.most_similar(positive=['queen', 'man'], negative=['king'])
print('Queen is a: ', sim_words[0][0])

sim_words = en_vectors.most_similar(negative=['king'], positive=['kings', 'queen'])
print('Plural form of `queen` is : ', sim_words[0][0])

sim_words = vi_vectors.most_similar(positive=['con_gái', 'đàn_ông'], negative=['con_trai'])
print('Con Gái is a: ', sim_words[0][0])

# c. Biểu diễn Word Embedding trên không gian 2D

# Để biểu diễn một cách trực quan kết quả của mô hình Word Embedding, ta sử dụng giải thuật T-SNE , giúp làm giảm số chiều của vector đặc trưng từ mà vẫn giữ được mối quan hệ tương đối giữa các từ.

# Trong mục này, các bạn nên cài đặt thêm thư viện MulticoreTSNE để tăng tốc độ giải thuật T-SNE, hoặc dùng module sẵn có trong thư viện scikit-learn (xem thêm bên dưới) nhưng sẽ chậm hơn tương đối nhiều.

import numpy as np

def get_sub_embedding(word_vectors, vocabs):
    
    sub_embeddings = []
    for word in vocabs:
        if word in word_vectors:
            sub_embeddings.append(word_vectors[word])
        else:
            vocabs.remove(word)
    return np.array(sub_embeddings), vocabs

# Chỉ sử dụng 10000 từ thông dụng trong tiếng anh 
# để train TSNE model
with open("data/10000_common_words.txt") as f:
    en_vocabs = f.read().splitlines() 
    en_vocabs = [word.strip() for word in en_vocabs]
en_sub_embedding, en_vocabs = get_sub_embedding(en_vectors, en_vocabs)


vi_vocabs = vi_vectors.vocab
vi_sub_embedding, vi_vocabs = get_sub_embedding(vi_vectors, vi_vocabs)

from MulticoreTSNE import MulticoreTSNE as TSNE
# # Có thể dùng class TSNE trong scikit-learn, nhưng sẽ chậm hơn
# from sklearn.manifold import TSNE
np.random.seed(2018)

def get_2D_vector(vectors):
    """
        Sử dụng giải thuật TSNE để ánh xạ vectors nhiều chiều về 2 chiều
        http://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
        https://distill.pub/2016/misread-tsne/
    """
    tsne = TSNE(perplexity=25, n_components=2, init='random', n_iter=1000, n_jobs=-1)
    return tsne.fit_transform(vectors)

en_vector_2D = get_2D_vector(en_sub_embedding)
vi_vector_2D = get_2D_vector(vi_sub_embedding)


from matplotlib import pylab, rcParams
import random

def plot(embeddings, labels, drawn_vocabs):
    """
        Sử dụng thư viện matplotlib để biểu diễn từ lên mặt phẳng tọa độ
    """
    pylab.figure(figsize=(50,50)) 
    rcParams.update({'font.size': 40}) 
    for i, label in enumerate(labels):
        if label in drawn_vocabs:
            x, y = embeddings[i,:]
            pylab.scatter(x, y)
            xt = random.randint(0,200)
            yt = random.randint(0,200)
            pylab.annotate(label, xy=(x, y), xytext=(xt, yt), textcoords='offset points',
                       ha='right', va='bottom')
    pylab.show()
    
en_drawn_vocabs = ["cat", "dog", "bird", "mouse",
                "woman", "man", "women", "men", "girl", "boy",
                "student", "teacher", "doctor",
                "one", "two", "three", "four", "five",
                "play", "jump", "go",
                "monday", "tuesday", "wednesday", "sunday",
                "usa", "uk", "canada", "china", "vietnam"]
plot(en_vector_2D, en_vocabs, en_drawn_vocabs)

vi_drawn_vocabs = ["mèo", "chó", "chim", "chuột",
                "phụ_nữ", "đàn_ông", "đàn_bà", "trai", "con_trai", "gái", "con_gái",
                "học_sinh", "giáo_viên", "thầy_giáo", "cô_giáo", "bác_sĩ",
                "một", "hai", "ba", "bốn", "năm",
                "chơi", "nhảy", "chạy",
                "thứ_hai", "thứ_ba", "thứ_tư", "thứ_năm",
                "mỹ", "anh", "canada", "trung_quốc", "việt_nam"]
plot(vi_vector_2D, vi_vocabs, vi_drawn_vocabs)






# Sử dụng Pretrained Word Embedding¶

import numpy as np
def create_embedding_matrix(word_vectors):
    """
        Chuyển KeyedVectors về ma trận embedding
        và từ điển chứa các cặp word - index

        @param      word_vectors        Dữ liệu word embedding lưu dưới định dạng KeyedVectors
        @return     embedding_matrix    ma trận word embedding với shape = (num_words,embedding_dim)
                    word2index          từ điển chứa cặp word - index
                    num_words           kích thước tập từ vựng
                    embedding_dim       số chiều vector embedding
                    
    """

    # --------------- TODO ---------------------------
    embedding_matrix = np.zeros((len(word_vectors.vocab), word_vectors.vector_size))
    word2index = {}
    num_words = len(word_vectors.vocab)
    embedding_dim = word_vectors.vector_size

    i = 0
    for w in word_vectors.vocab:
        word2index[w] = i
        embedding_matrix[i,:] = word_vectors[w]
        i += 1
    # ------------------------------------------------

    return embedding_matrix, word2index, num_words, embedding_dim

import nltk
def to_index(sentence, word2index):
    """
        Chuyển câu thành index vector
        @param      sentence       câu
        @param      word2index     từ điển chứa cặp word - index

        e.g: "hello world" => [0, 1]
    """

    sentence = nltk.word_tokenize(sentence)
    index_vector = []
    # --------------- TODO ---------------------------
    for w in sentence:
        index_vector.append(word2index[w])
   
    # ------------------------------------------------

    return index_vector

def to_embedding_vectors(sentence, word2index, embedding_matrix):
    """
        Chuyển câu thành ma trận của các embedding vector
        @param      sentence       câu
        @param      word2index     từ điển chứa cặp word - index

        e.g: "hello world" => [0, 1] => [[00..00], [00..01]]
    """

    # --------------- TODO ---------------------------
    indices = to_index(sentence, word2index)
    embedding_vectors = embedding_matrix[indices]

    # ------------------------------------------------

    return embedding_vectors