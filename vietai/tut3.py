import nltk
import numpy as np

sample_texts = [
    "I am playing with text",
    "It is a cat",
    "I like cat"
]

sample_texts = [nltk.word_tokenize(text) for text in sample_texts]
vocab = set(sum(sample_texts, []))
print (vocab)

word2index = {}
index2word = {}

for i, word in enumerate(vocab):
    # TODO: Tạo mapping cho tập từ vừng: từ -> chỉ số và ngược lại
    #
    # word2index : key   - từ thuộc vocab 
    #               value - chỉ số của từ trong vocab
    #               {'am': 0, 'I': 1, 'with': 2, ... } 
    # index2word : key   - chỉ số của từ trong vocab
    #               value - từ thuộc vocab 
    #               {0: 'am', 1: 'I', 2: 'with', ... }
    #
    word2index[word] = i
    index2word[i] = word
    # END
    
print (word2index)
print (index2word)

def to_index(text, word2index):
    text = nltk.word_tokenize(text)
    index_vector = [word2index[w] for w in text]
    
    # TODO: Chuyển dữ liệu text về dạng vector chỉ số
    #
    # @param    text          văn bản cần xử lý
    # @param    word2index    mapping word-index
    # @return   index_vector  vector chỉ số của văn bản
    # 
    # Ex: text = "a cat playing with a cat"
    #     word2index = {'am': 0, 'I': 1, 'with': 2, ...} 
    #     index_vector = [9, 7, 6, 2, 9, 7]
    
    # END
    
    return index_vector

text = "a cat playing with a cat"
print (text)

index_vector = to_index(text, word2index)
print (index_vector)


def to_onehot(index_vector, vocab):
    
    # Mỗi onehot vector sẽ có độ dài bằng vocab_size
    vocab_size = len(vocab)
    onehot_vectors = None
    
    # TODO: Chuyển giá trị chỉ số về giá trị vector
    # 
    # @param    index_vector    vector chỉ số của văn bản
    # @param    vocab           tập từ vựng
    # @return   onehot_vectors  vector đặc trưng dạng one-hot
    #
    # Ex: index_vector = [9, 7, 6, 2, 9, 7] 
    #     vocab = ['I', 'am', 'write', 'a', 'sampl', 'text', '.']
    #     onehot_vectors = [[0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
    #                       [0., 0., 0., 0., 0., 1., 0., 0., 0., 0.],
    #                       [0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
    #                       [0., 0., 0., 0., 0., 0., 1., 0., 0., 0.],
    #                       [0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
    #                       [0., 0., 0., 0., 0., 1., 0., 0., 0., 0.]]
    onehot_vectors = np.zeros(shape=(len(index_vector), vocab_size), dtype=int)
    for i, x in enumerate(index_vector):
        onehot_vectors[i][x] = 1.0
    # END
    
    return onehot_vectors

to_onehot(index_vector, vocab)

# bag of word
def to_count_vector(index_vector, vocab):
    
    # Mỗi vector đặc trưng sẽ có độ dài bằng vocab_size
    vocab_size = len(vocab)
    count_vector = None
    
    # TODO: Đếm tần suất xuất hiện của các từ 
    #
    # @param   index_vector
    # @param   vocab
    # @return  count_vector     vector đặc trưng là tần suất xuất hiện của các từ trong văn bản
    #
    # Ex:  index_vector = [9, 7, 6, 2, 9, 7]
    #      count_vector = [0. 0. 0. 1. 0. 2. 1. 0. 0. 2.]

    count_vector = np.zeros(shape=(vocab_size, ), dtype=float)
    for x in index_vector:
        count_vector[x] += 1

    s = np.sum(count_vector)
    count_vector = count_vector / s
    # END
    
    return count_vector
    
print (to_count_vector(index_vector, vocab))


# Sử dụng CountVectorizer từ thư viện scikit-learn
# http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html

from sklearn.feature_extraction.text import CountVectorizer

sample_texts = [
    "I am playing with text",
    "It is a cat",
    "I like cat"
]

count_vect = CountVectorizer(lowercase=True, stop_words="english")
vectorized_data = count_vect.fit_transform(sample_texts)

print ("vocab:", count_vect.vocabulary_)
print ("count vectorized format:\n",vectorized_data)
print ("array format:\n", vectorized_data.toarray())