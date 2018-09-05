import os
import pickle
import constants
import numpy as np

BASE = constants.BASE
TRAIN_FEATURES = constants.TRAIN_FEATURES
PUBLIC_TEST = constants.TEST_PROCCESSED_DIR

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
    return get_data(constants.PROCESSED_ACCENT_FILE)

def get_gender_data():
    return get_data(constants.PROCESSED_GENDER_FILE)

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

def randomize(dataset, labels):
  permutation = np.random.permutation(labels.shape[0])
  shuffled_dataset = dataset[permutation,:,:]
  shuffled_labels = labels[permutation]
  return shuffled_dataset, shuffled_labels

def get_public_test_data():
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

    res = None
    with open(os.path.join(os.path.dirname(__file__), 'results', 'public_test_gt.csv'), 'r') as f:
        res = f.readlines()
    assert len(res) == 5560
    labels = []
    for l in res[1:]:
        _, gender, accent = l.split(',')
        gender = int(gender)
        accent = int(accent)
        labels.append(get_label(gender, accent, 'combined'))
    return randomize(input_data, np.array(labels))


def get_label(gender, accent, dtype):
    assert 0 <= gender <= 1
    assert 0 <= accent <= 2
    if dtype == 'accent':
        return accent
    elif dtype == 'gender':
        return gender
    elif dtype == 'combined':
        return accent * 2 + gender
    else:
        assert False
