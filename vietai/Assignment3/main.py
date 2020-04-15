import numpy as np
import os
import tensorflow as tf
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import datetime

# LƯU Ý: CẦN PHẢI CHỈNH LẠI ĐƯỜNG DẪN NÀY THÀNH THƯ MỤC CHỨA CÁC FILE ASSIGNMENT3
# CHỮ 'drive' có nghĩa là thư mục mặc định của Google drive
currentDir = '.'

wordsList = np.load(os.path.join(currentDir, 'wordsList.npy'))
print('Simplified vocabulary loaded!')
wordsList = wordsList.tolist()
#wordsList = [word.decode('UTF-8') for word in wordsList] #Encode words as UTF-8
wordVectors = np.load(os.path.join(currentDir, 'wordVectors.npy'))
wordVectors = np.float32(wordVectors)
print ('Word embedding matrix loaded!')

print('Size of the vocabulary: ', len(wordsList))
print('Size of the word embedding matrix: ', wordVectors.shape)

ngon_idx = wordsList.index('ngon')
print('Index of `ngon` in wordsList: ', ngon_idx)
ngon_vec = wordVectors[ngon_idx]
print('Vector representation of `ngon` is: ', ngon_vec)

maxSeqLength = 180   #Maximum length of sentence
numDimensions = 300 #Dimensions for each word vector

def test_word_vec():
    sentenceIndexes = np.zeros((maxSeqLength), dtype='int32')
    sentence = 'món này ăn hoài không biết chán'
    # TODO 3.1: Gán chỉ số của các từ trong câu và 'sentenceIndexes'
    widx = [wordsList.index(w) for w in sentence.split(' ')]
    sentenceIndexes[:len(widx)] = widx 

    # Các chỉ số 7, 8, 9 của sentenceIndexes  vẫn được gán bằng 0 như cũ
    print(sentenceIndexes.shape)
    print('Row index for each word: ', sentenceIndexes)

    # Ma trận biểu diễn:
    print('Sentence representation of word vectors:')
    with tf.Session() as sess:
        print(tf.nn.embedding_lookup(wordVectors,sentenceIndexes).eval().shape)

def load_raw_data(examine = False):
    folder = '/home/tamvm/Downloads/Assignment3-SentimentAnalysis-LSTM'
    positiveFiles = [join(folder, 'positiveReviews', f) for f in listdir(join(folder, 'positiveReviews')) if isfile(join(folder, 'positiveReviews', f))]
    negativeFiles = [join(folder, 'negativeReviews', f) for f in listdir(join(folder, 'negativeReviews')) if isfile(join(folder, 'negativeReviews', f))]
    numWords = []
    for pf in positiveFiles:
        with open(pf, "r", encoding='utf-8') as f:
            line=f.readline()
            counter = len(line.split())
            numWords.append(counter)       
    print('Positive files finished')

    for nf in negativeFiles:
        with open(nf, "r", encoding='utf-8') as f:
            line=f.readline()
            counter = len(line.split())
            numWords.append(counter)  
    print('Negative files finished')

    numFiles = len(numWords)
    print('The total number of files is', numFiles)
    print('The total number of words in the files is', sum(numWords))
    print('The average number of words in the files is', sum(numWords)/len(numWords))
    if examine:
        plt.hist(numWords, 50)
        plt.xlabel('Sequence Length')
        plt.ylabel('Frequency')
        plt.axis([0, 1200, 0, 8000])
        plt.show()

        print('A positive sentence: ')
        fname = positiveFiles[3] # Randomly select a positive file to view
        with open(fname, encoding='utf-8') as f:
            for lines in f:
                print(lines)

        print('A negative sentence: ')
        fname = negativeFiles[10] # Randomly select a negative file to view
        with open(fname, encoding='utf-8') as f:
            for lines in f:
                print(lines)
    return numFiles, positiveFiles, negativeFiles


# Removes punctuation, parentheses, question marks, etc., and leaves only alphanumeric characters
import re
strip_special_chars = re.compile("[^\w0-9 ]+")

def cleanSentences(string):
    string = string.lower().replace("<br />", " ")
    return re.sub(strip_special_chars, "", string.lower())

def create_sentence_matrix():
    numFiles, positiveFiles, negativeFiles = load_raw_data()
    ids = np.zeros((numFiles, maxSeqLength), dtype='int32')
    nFiles = 0
    # Index of Unknow word
    unk_idx = wordsList.index('UNK')

    for pf in positiveFiles:
        with open(pf, "r", encoding="utf-8") as f:
            nIndexes = 0
            line=f.readline()
            cleanedLine = cleanSentences(line)
            split = cleanedLine.split()
            for word in split:
                # TODO 3.2: Nếu 'word' thuộc tập 'wordsList' thì gán chỉ số của 'word' vào ma trận ids

                # Ngược lại: gán 'unk_idx' vào ma trận ids
                try:
                    ids[nFiles][nIndexes] = wordsList.index(word)
                except:
                    ids[nFiles][nIndexes] = unk_idx
                nIndexes = nIndexes + 1
                if nIndexes >= maxSeqLength:
                    break
            nFiles = nFiles + 1 

    print('Positive files are indexed!')
    for nf in negativeFiles:
        with open(nf, "r", encoding="utf-8") as f:
            nIndexes = 0
            line=f.readline()
            cleanedLine = cleanSentences(line)
            split = cleanedLine.split()
            for word in split:
                # ToDo 3.2: tương tự như trên. Không khác gì hết.
                try:
                    ids[nFiles][nIndexes] = wordsList.index(word)
                except:
                    ids[nFiles][nIndexes] = unk_idx
                
                nIndexes = nIndexes + 1
                if nIndexes >= maxSeqLength:
                    break
            nFiles = nFiles + 1 

    print('Negative files are indexed!')
    # Save ids Matrix for future uses.
    np.save(os.path.join(currentDir,'idsMatrix.npy'), ids)


# create_sentence_matrix()

from random import randint

def getTrainBatch():
    ids = np.load(os.path.join(currentDir, 'idsMatrix.npy'))
    labels = []
    arr = np.zeros([batchSize, maxSeqLength])
    for i in range(batchSize):
        if (i % 2 == 0): 
            # Pick positive samples randomly
            num = randint(1,13999)
            labels.append([1,0])
        else:
            # Pick negative samples randomly
            num = randint(15999,29999)
            labels.append([0,1])
        arr[i] = ids[num-1:num]
    return arr, labels

def getTestBatch():
    ids = np.load(os.path.join(currentDir, 'idsMatrix.npy'))
    labels = []
    arr = np.zeros([batchSize, maxSeqLength])
    for i in range(batchSize):
        num = randint(13999,15999)
        if (num <= 14999):
            labels.append([1,0])
        else:
            labels.append([0,1])
        arr[i] = ids[num-1:num]
    return arr, labels

# Initialize paramters
numDimensions = 300
batchSize = 64
lstmUnits = 128
nLayers = 2
numClasses = 2

tf.reset_default_graph()

# TODO 3.3: Khởi tạo hai biến 'inputs' và 'labels'
inputs = tf.placeholder(np.int32, shape=(batchSize, maxSeqLength))
labels = tf.placeholder(np.float32)

data = tf.nn.embedding_lookup(wordVectors, inputs)

def generate_a_lstm_layer():
    # Khởi tạo một LSTM layer với 'lstmUnits' unit sử dụng hàm tf.contrib.rnn.BasicLSTMCell
    # maybe check CudnnLSTM for perf on GPU
    layer = tf.nn.rnn_cell.LSTMCell(lstmUnits) 
    # Sau đó tạo một lớp dropout để chống overfitting với hệ số out_keep_prob bằng 0.75
    # Sử dụng hàm tf.contrib.rnn.DropoutWrapper    

    return tf.nn.rnn_cell.DropoutWrapper(layer, output_keep_prob=0.75)

# Sau khi đã có hàm tạo một LSTM Layer, ta sử dụng hàm này để chồng các LSTM lên
# Stack các LSTM layer với hàm tf.nn.rnn_cell.MultiRNNCell
stacked_lstm = tf.nn.rnn_cell.MultiRNNCell([generate_a_lstm_layer() for _ in range(0, 2)])
# Feed data variable vào mạng LSTM sử dụng hàm tf.nn.dynamic_rnn
outputs, state = tf.nn.dynamic_rnn(stacked_lstm, data, dtype=tf.float32)
print(outputs)

weight = tf.Variable(tf.truncated_normal([lstmUnits, numClasses]))
bias = tf.Variable(tf.constant(0.1, shape=[numClasses]))

# Lấy giá trị output tại LSTM cell cuối cùng (it's more like taking output of last input word to LSTM)
outputs = tf.transpose(outputs, [1, 0, 2])
print(outputs)
last = tf.gather(outputs, int(outputs.get_shape()[0]) - 1)
print(last)
# Đưa qua mạng Fully Connected mà không có activation function
prediction = (tf.matmul(last, weight) + bias)
print(prediction)
# Để xác định độ chính xác của hệ thống, ta đếm số lượng labels khớp với giá trị dự đoán (prediction). Sau đó tính độ chính xác bằng cách tính giá trị trung bình của các kết quả trả về đúng.
correctResult = tf.equal(tf.argmax(prediction,1), tf.argmax(labels,1))
accuracy = tf.reduce_mean(tf.cast(correctResult, tf.float32))

# Sau đó chúng ta sẽ xác định hàm độ lỗi sử dụng softmax cross entropy được tính từ dữ liệu dự đoán và tập labels. Cuối cùng là chọn thuật toán tối ưu với tham số learning rate mặc định là 0.001. 
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=labels))
optimizer = tf.train.AdamOptimizer().minimize(loss)


def train():
    iterations = 1
    tf.summary.scalar('Loss', loss)
    tf.summary.scalar('Accuracy', accuracy)
    merged = tf.summary.merge_all()
    logdir = "tensorboard/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "/"

    sess = tf.InteractiveSession()
    writer = tf.summary.FileWriter(logdir, sess.graph)
    saver = tf.train.Saver()
    sess.run(tf.global_variables_initializer())

    for i in range(iterations):
        # TODO 3.5
        # Get next training batch
        nextBatch, nextBatchLabels = getTrainBatch()
        # Feed to optimizer
        sess.run(optimizer, feed_dict={inputs: nextBatch, labels: nextBatchLabels})
        #Write summary to Tensorboard
        if (i % 50 == 0):
            summary = sess.run(merged, {inputs: nextBatch, labels: nextBatchLabels})
            writer.add_summary(summary, i)

        # Save model every 2000 training iterations
        if (i % 2000 == 0 and i != 0):
            save_path = saver.save(sess, os.path.join(currentDir,"models/pretrained_lstm.ckpt"), global_step=i)
            print("saved to %s" % save_path)
    writer.close()

def evaluate():
    sess = tf.InteractiveSession()
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint(os.path.join(currentDir,'models')))
    # Test on 10 batches
    iterations = 10
    for i in range(iterations):
        nextBatch, nextBatchLabels = getTestBatch()
        # TODO 3.6: Tính độ chính xác 'accuracy' trên các test batch và gán vào 'test_acc'
        test_acc = sess.run(accuracy, feed_dict={inputs: nextBatch, labels: nextBatchLabels})
        print("Accuracy for this batch:", test_acc)

def emotion_classify(sentence):
    cleanedLine = cleanSentences(sentence)
    ids = np.zeros([batchSize, maxSeqLength])
    split = cleanedLine.split()
    nIndexes = 0
    for word in split:
        # ToDo 3.2: tương tự như trên. Không khác gì hết.
        try:
            ids[0][nIndexes] = wordsList.index(word)
        except:
            ids[0][nIndexes] = unk_idx
        
        nIndexes = nIndexes + 1
        if nIndexes >= maxSeqLength:
            break

    sess = tf.InteractiveSession()
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint(os.path.join(currentDir,'models')))

    result = sess.run(prediction, feed_dict={inputs:ids})
    # print('result: ', result)
    print('prediction result: ', 'positive' if np.argmax(result[0]) == 0 else 'negative')

emotion_classify('Món này ăn ngon mê ly luôn. Vị ngọt và thơm quá trời quá đất.')