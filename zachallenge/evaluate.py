import os
import keras
import common
import lstm
import cnn
import constants
import pickle
import numpy as np
import csv

PUBLIC_TEST = constants.TEST_PROCCESSED_DIR# os.path.join(constants.BASE, 'test_preprocessed_long')

def evaluate_cnns(cnns, test_input, test_labels):
    test_input = cnn.reshape_input(test_input)
    max_acc, best_m = -1, None
    for p in cnns:
        print ('evaluate CNN ', p)
        model = keras.models.load_model(p)
        score, acc = model.evaluate(test_input, test_labels)
        print ('test score: ', score)
        print ('test accu : ', acc)
        if max_acc < acc:
            max_acc = acc 
            best_m = p
    print ('best m = ', best_m, ' acc = ', max_acc)

def evaluate_lstm(lstms, test_input, test_labels):
    test_input = lstm.reshape_input(test_input)
    max_acc, best_m = -1, None
    for p in lstms:
        print ('evaluate LSTMs ', p)
        model = keras.models.load_model(p)
        score, acc = model.evaluate(test_input, test_labels)
        print ('test score: ', score)
        print ('test accu : ', acc)
        if max_acc < acc:
            max_acc = acc
            best_m = p
    print ('best m = ', best_m, ' acc = ', max_acc)



def evaluate_all(test_input, test_labels):
    # d = os.path.dirname(__file__)
    # print (d)
    # print (__file__)
    d = '.'
    cnns = [os.path.join(d, l) for l in os.listdir(d) if l.startswith('cnn_')]
    lstms = [os.path.join(d, l) for l in os.listdir(d) if l.startswith('lstm_')]
    # evaluate_cnns(cnns, test_input, test_labels)    
    evaluate_lstm(lstms, test_input, test_labels)

def run_on_test_data():
    model = keras.models.load_model('lstm_256_mfccs_delta_02dropout_run9.h5')
    cnn_model = keras.models.load_model('cnn_3x3_3layers_001lr_256_run3.h5')
    input_names = os.listdir(PUBLIC_TEST)
    input_names.sort(key=lambda x: int(x.split('.')[0]))
    input_data = np.ndarray(shape=(len(input_names), constants.FEATURE_SIZE, constants.NO_FRAME), dtype=np.float64)
    for i, l in enumerate(input_names):
        p = os.path.join(PUBLIC_TEST, l)
        voice_data = None
        with open(p, 'rb') as f:
            voice_data = pickle.load(f)
        input_data[i, :, :] = voice_data

    # input_data_lstm = lstm.reshape_input(input_data)
    # output = model.predict_classes(input_data_lstm)
    # del input_data_lstm
    input_data_cnn = cnn.reshape_input(input_data)
    output_cnn = cnn_model.predict_classes(input_data_cnn)
    # del input_data_cnn
    # del input_data
    # diff = sum([1 for i in range(0, len(output)) if not output[i] == output_cnn[i]])
    # print ('diff % = ', (diff / len(output) * 100.0))
    output_csv([l.replace('.pickle', '') for l in input_names], output_cnn)

def output_csv(input_names, classes):
    with open('cnn_result.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',lineterminator='\n')
        writer.writerow(['id', 'gender', 'accent'])
        for i, n in enumerate(input_names):
            o = classes[i]
            gender, accent = common.label_to_gender_accent(o)
            writer.writerow([n, gender, accent])

if __name__ == '__main__':
    # train_input, train_labels, test_input, test_labels = common.get_combined_data()
    # del train_labels
    # del train_input
    # n_classes = common.get_n_classes('combined')
    # test_labels = keras.utils.to_categorical(test_labels, n_classes)
    # evaluate_all(test_input, test_labels)
    run_on_test_data()

    