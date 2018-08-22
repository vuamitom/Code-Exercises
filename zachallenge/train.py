from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os
import numpy as np
import datetime

BASE = '/media/tamvm/DATA/AiChallenge'
TRAIN_FEATURES = os.path.join(BASE, 'features')

def CNN(train_input, train_labels, test_input, test_labels):
    pass

def random_forest(train_input, train_labels, test_input, test_labels):
    # Out-of-bag score estimate: 0.571
    # Mean accuracy score: 0.597
    v_c = train_input.shape[0]
    t_c = test_input.shape[0]
    rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123456)
    start_time = datetime.datetime.now()
    rf.fit(train_input.reshape(v_c, -1), train_labels)
    print ('done training in seconds: ', (datetime.datetime.now() - start_time).total_seconds())
    start_time = datetime.datetime.now()
    predicted = rf.predict(test_input.reshape(t_c, -1))
    print ('done predict in seconds: ', (datetime.datetime.now() - start_time).total_seconds())
    accuracy = accuracy_score(test_labels, predicted)
    print(f'Out-of-bag score estimate: {rf.oob_score_:.3}')
    print(f'Mean accuracy score: {accuracy:.3}')

def get_data():
    dataset = None
    with open (os.path.join(TRAIN_FEATURES, 'randomized_accent_data.pickle'), 'rb') as f:
        dataset = pickle.load(f)
    train_input = dataset['train_input']
    train_labels = dataset['train_labels']
    valid_input = dataset['valid_input']
    valid_labels = dataset['valid_labels']
    test_input = dataset['test_input']
    test_labels= dataset['test_labels']
    assert valid_input.shape[0] == 0
    assert len(valid_labels) == 0
    # train_input = np.vstack((train_input, valid_input))
    # train_labels = np.concatenate((train_labels, valid_labels))
    del dataset
    return train_input, train_labels, test_input, test_labels

if __name__ == '__main__':
    train_input, train_labels, test_input, test_labels = get_data()
    # print (test_labels)
    random_forest(train_input, train_labels, test_input, test_labels)