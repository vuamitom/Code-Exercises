import os
import keras
import common
import lstm
import cnn
import constants
import pickle
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import csv

PUBLIC_TEST = constants.TEST_PROCCESSED_DIR# os.path.join(constants.BASE, 'test_preprocessed_long')
TEST_DIR = constants.TEST_DIR

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
    d = 'long_model4'
    cnns = [os.path.join(d, l) for l in os.listdir(d) if l.startswith('cnn_')]
    lstms = [os.path.join(d, l) for l in os.listdir(d) if l.startswith('lstm_')]
    # evaluate_cnns(cnns, test_input, test_labels)    
    evaluate_lstm(lstms, test_input, test_labels)


def run_on_gender_accent_test():
    
    input_names = os.listdir(PUBLIC_TEST)
    input_names.sort(key=lambda x: int(x.split('.')[0]))
    # print (input_names[:10])
    # print (input_names[len(input_names) - 10:])
    # assert False
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

    gender_model = keras.models.load_model('long_model_gender/cnn_3x3_3layers_001lr_512.h5')
    accent_model = keras.models.load_model('long_model_accent/cnn_3x3_3layers_001lr_512.h5')

    output_gender = gender_model.predict_classes(input_data_cnn)
    output_accent = accent_model.predict_classes(input_data_cnn)
    test_list = os.listdir(TEST_DIR)
    assert len(input_names) == len(test_list)
    assert len(output_cnn) == len(test_list)
    output_csv([l.replace('.pickle', '') for l in input_names], output_cnn, 'long_model_separate_cnn_3x3_3layers_001lr_512')    

def run_on_test_data():
    model = keras.models.load_model('/model/lstm_final.h5')
    # cnn_model = keras.models.load_model('long_model4/cnn_3x3_3layers_001lr_512.h5')
    input_names = os.listdir(PUBLIC_TEST)
    input_names.sort(key=lambda x: int(x.split('.')[0]))
    # print (input_names[:10])
    # print (input_names[len(input_names) - 10:])
    # assert False
    input_data = np.ndarray(shape=(len(input_names), constants.FEATURE_SIZE, constants.NO_FRAME), dtype=np.float64)
    for i, l in enumerate(input_names):
        p = os.path.join(PUBLIC_TEST, l)
        voice_data = None
        with open(p, 'rb') as f:
            voice_data = pickle.load(f)
        input_data[i, :, :] = voice_data

    input_data_lstm = lstm.reshape_input(input_data)
    output = model.predict_classes(input_data_lstm)
    # del input_data_lstm
    # input_data_cnn = cnn.reshape_input(input_data)
    # output_cnn = cnn_model.predict_classes(input_data_cnn)
    # del input_data_cnn
    # del input_data
    # diff = sum([1 for i in range(0, len(output)) if not output[i] == output_cnn[i]])
    # print ('diff % = ', (diff / len(output) * 100.0))
    # input_names, output_cnn = merge_segment(input_names, output_cnn)
    # test_list = os.listdir(TEST_DIR)
    # assert len(input_names) == len(test_list)
    # assert len(output) == len(test_list)
    output_csv([l.replace('.pickle', '') for l in input_names], output, 'lstm_256_mfccs_delta_02dropout_with_pt')

def merge_segment(input_names, output):
    n_output, n_names = [], []
    cur = None
    n_classes = common.get_n_classes('combined')
    pending = []
    parts = []
    for i, n in enumerate(input_names):
        name, later = n.split('_')
        part = later.split('.')[0]
        # ext = later[len(part):].replace('.pickle', '')
        # name = name + ext                
        if not name == cur:
            if cur is not None:
                assert len(pending) > 0
                # count occurrences 
                occs = [(x, pending.count(x)) for x in range(0, n_classes)]
                final_cls, count = max(occs, key=lambda x: x[1])
                n_names.append(cur)
                n_output.append(final_cls)
                if (len(pending) > 1):
                    print ('aggregate result for ', cur, ' to ', final_cls, ' occurrences ', count, ' all parts ', parts)
            else:
                assert len(pending) == 0
            pending = [output[i]]
            parts = [part]
            cur = name            
        else:
            # pass
            pending.append(output[i])
            parts.append(part)
    if cur is not None and len(pending) > 0:
        occs = [(x, pending.count(x)) for x in range(0, n_classes)]
        final_cls, count = max(occs, key=lambda x: x[1])
        n_names.append(cur)
        n_output.append(final_cls)
        if (len(pending) > 1):
            print ('aggregate result for ', cur, ' to ', final_cls, ' occurrences ', count)
    return n_names, n_output


def output_csv(input_names, classes, model_name):
    with open('/result/submission.csv', 'w', newline='') as csvfile:
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
    # evaluate_all()
    run_on_test_data()

    