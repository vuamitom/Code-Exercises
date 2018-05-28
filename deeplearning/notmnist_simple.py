# sklearn.linear_model
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import os
from six.moves import cPickle as pickle

def load_dataset():
    root_dir = '.'
    df = os.path.join(root_dir, 'sanitized_notMNIST.pickle')   
    with open(df, 'rb') as f:
        dataset = pickle.load(f)
        return dataset

def train_model(train_data, train_labels, train_size = 50):
    td = train_data
    tl = train_labels
    if train_size > -1:
        td = train_data[:train_size, :, :]
        tl = train_labels[:train_size]
    td = td.reshape(td.shape[0], -1)
    
    print ('train input shape ', td.shape)
    logreg = linear_model.LogisticRegression(C=1e5)
    # we create an instance of Neighbours Classifier and fit the data.
    logreg.fit(td, tl)
    return logreg
    
def train_and_predict():
    train_size, test_size = 1000, 10
    train_data, val_data, test_data = None, None, None
    dataset = load_dataset()
    train_data = dataset['train_dataset']
    test_data = dataset['test_dataset']
    valid_data = dataset['valid_dataset']
    test_labels = dataset['test_labels']
    train_labels = dataset['train_labels']
    valid_labels = dataset['valid_labels']

    print('done load dataset')
    predictor = train_model(train_data, train_labels, train_size)
    print('done train model')
    
    test_input = test_data
    test_out = test_labels
    if test_size > -1:
        test_input = test_data[:test_size, :, :]
        test_out = test_labels[:test_size]
    
        
    test_input = test_input.reshape(test_input.shape[0], -1)
    
    print ('test_input shape ', test_input.shape)

    Z = predictor.predict(test_input)
    print('done predict')
    c = 0
    for s in range(0, Z.shape[0]):
        if Z[s] == test_out[s]:
            c += 1
    print('accuracy ', c * 100.0 / Z.shape[0], ' %')

train_and_predict()
        

    