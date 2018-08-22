import os
import pickle
import constants

BASE = constants.BASE
TRAIN_FEATURES = constants.TRAIN_FEATURES



def get_accent_data():
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