import os
import pickle
import constants

BASE = constants.BASE
TRAIN_FEATURES = constants.TRAIN_FEATURES


def get_data(fn):
    dataset = None
    with open (os.path.join(BASE, fn), 'rb') as f:
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

def get_accent_data():
    return get_data('randomized_accent_data_long.pickle')

def get_combined_data():
    print ('get data from ', constants.EXTRACT_FEATURE_FILE)
    return get_data(constants.EXTRACT_FEATURE_FILE)

def get_n_classes(dtype='accent'):

    if dtype == 'accent':
        return 3
    elif dtype == 'gender':
        return 2
    elif dtype == 'combined':
        return 6
    else:
        assert False

def label_to_gender_accent(label):
    gender = label % 2
    accent = int(label / 2)
    return gender, accent

def get_validation_data(train_input, train_labels):
    no_recs = train_input.shape[0]
    valid_size = round(0.2 * no_recs)
    valid_input, valid_labels = train_input[:valid_size,:,:], train_labels[:valid_size]
    train_input, train_labels = train_input[valid_size:,:,:], train_labels[valid_size:]
    assert len(valid_labels) == valid_size
    assert len(train_labels) == no_recs - valid_size
    return train_input, train_labels, valid_input, valid_labels