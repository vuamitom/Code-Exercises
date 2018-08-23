import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pickle
import constants 

BASE = constants.BASE
TRAIN_INPUT = os.path.join(BASE, 'train')
TRAIN_TEMP = os.path.join(BASE, 'raw_features')
TRAIN_FEATURES =constants.TRAIN_FEATURES
MIN_VOICE_FREQ = 70
MAX_VOICE_FREQ = 280
NO_FRAME = constants.NO_FRAME
N_MFCC = constants.N_MFCC
N_MELS = constants.N_MELS
FEATURE_SIZE = constants.FEATURE_SIZE
SAMPLE_PER_FRAME = 256

# Gender: Female: 0, Male: 1
# Accent: North: 0, Central: 1, South: 2
GENDER_M = constants.GENDER_M
GENDER_F = constants.GENDER_F
ACCENT_N = constants.ACCENT_N
ACCENT_C = constants.ACCENT_C
ACCENT_S = constants.ACCENT_S

TEST_RATIO = 0.2
VALID_RATIO = 0

def get_mean():
    # voice_list = []
    all_data = None

    for l in os.listdir(TRAIN_TEMP):
        p = os.path.join(TRAIN_TEMP, l) 
        print ('process ', l)
        for r in os.listdir(p):

            fp = os.path.join(p, r)
            # voice_list.append(fp)
            print (' --- process ', fp)
            dataset = None
            with open(fp, 'rb') as f:
                dataset = pickle.load(f)

            all_data = dataset if all_data is None else np.concatenate((all_data, dataset), axis=1)
    print ('All data count = ', all_data.shape)
    means = np.mean(all_data, axis=1)
    print ('Mean per coefs = ', means)
    stds = np.std(all_data, axis=1)
    print ('std per coefs = ', stds)
    assert len(means) == FEATURE_SIZE
    assert len(stds) == FEATURE_SIZE
    stat = np.vstack((means, stds))
    stat_file = os.path.join(BASE, 'feature_mean_std.pickle')
    with open(stat_file, 'wb') as f:
        pickle.dump(stat, f, pickle.HIGHEST_PROTOCOL)

def extract():
    try:        
        # make output dir
        os.mkdir(TRAIN_TEMP, mode=0o755)
    except FileExistsError:
        pass

    if len(os.listdir(TRAIN_TEMP)) > 0:
        print ('Already extracted')
        return None

    for l in os.listdir(TRAIN_INPUT):
        try:
            os.mkdir(os.path.join(TRAIN_TEMP, l), mode=0o755)
        except FileExistsError:
            pass            
        p = os.path.join(TRAIN_INPUT, l)
        voice_list = os.listdir(p)
        # dataset = np.ndarray(shape=(FEATURE_SIZE, NO_FRAME),
        #                  dtype=np.float64)        
        for idx, r in enumerate(voice_list):            
            fp = os.path.join(p, r)
            print ('process: ', fp)
            # start = datetime.datetime.now()
            features = extract_voice_feature(fp)
            # print ('extract takes ', (datetime.datetime.now() - start).total_seconds())
            features = fix_size(features)
            print (features.shape)
            row, col = features.shape        
            assert row == FEATURE_SIZE
            assert col == NO_FRAME
            # dataset[idx, :, :] = features
            temp_filename = os.path.join(TRAIN_TEMP, l, str(idx) + '.pickle')            
            try:
                with open(temp_filename, 'wb') as f:
                    pickle.dump(features, f, pickle.HIGHEST_PROTOCOL)
                    print ('done extract for file ', r)
            except Exception as e:
                print('Unable to save data to', temp_filename, ':', e)                

def fix_size(features):
    _, c = features.shape
    if c < NO_FRAME:
        while c < NO_FRAME:
            add = NO_FRAME - c
            add = add if add < c else c
            features = np.concatenate((features, features[:, :add]), axis=1)
            _, c = features.shape
    elif c > NO_FRAME:
        return features[:, :NO_FRAME]
    return features

def extract_voice_feature(fp):
    X, sample_rate = librosa.load(fp, res_type='kaiser_fast')
    # plt.figure(figsize=(12, 4))  
    # plt.subplot(3, 1, 1)
    # librosa.display.waveplot(X, sr=sample_rate)
    # mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)

    spectrogram = librosa.feature.melspectrogram(y=X, sr=sample_rate, 
                        hop_length=SAMPLE_PER_FRAME, 
                        fmin=MIN_VOICE_FREQ, 
                        fmax=MAX_VOICE_FREQ, 
                        power=1, # energy instead of power
                        n_mels=N_MELS)
    mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, 
                        hop_length=SAMPLE_PER_FRAME, 
                        fmin=MIN_VOICE_FREQ, 
                        fmax=MAX_VOICE_FREQ,
                        n_mels=N_MELS,
                        n_mfcc=N_MFCC)
    delta = librosa.feature.delta(mfccs)

    # print (mfccs.shape)
    # print (spectrogram.shape)
    # print ("first frame", np.transpose(mfccs)[0])
    # print (len(mfccs))
    # print (np.mean(mfccs.T, axis=0))
    # librosa.display.specshow(mfccs, x_axis='time')
    # plt.colorbar()
    # plt.tight_layout()
    # mfccs = 
    # plt.show()
    return np.vstack((spectrogram, mfccs, delta))

def standardize_and_save():
    try:        
        # make output dir
        os.mkdir(TRAIN_FEATURES, mode=0o755)
    except FileExistsError:
        pass

    if len(os.listdir(TRAIN_FEATURES)) > 0:
        print ('Already extracted')
        return None

    mean_std = None
    with open(os.path.join(BASE, 'feature_mean_std.pickle'), 'rb') as f:
        mean_std = pickle.load(f)
    means = mean_std.take(0, axis=0)
    stds = mean_std.take(1, axis=0)
    # print (means)
    for l in os.listdir(TRAIN_TEMP):
        print ('load data for ', l)

        p = os.path.join(TRAIN_TEMP, l)
        voice_list = os.listdir(p)
        data_per_type = np.ndarray(shape=(len(voice_list), FEATURE_SIZE, NO_FRAME),
                         dtype=np.float64)
        for voice_number, v in enumerate(voice_list):
            vp = os.path.join(p, v)
            dataset = None
            with open(vp, 'rb') as f:
                dataset = pickle.load(f)
            # standardize features
            dataset = ((dataset.T - means) / stds).T
            r, c = dataset.shape
            assert r == FEATURE_SIZE
            assert c == NO_FRAME
            data_per_type[voice_number, :, :] = dataset
        feature_file = os.path.join(TRAIN_FEATURES, l + '.pickle')
        print ('done standardize data for ', l, ' shape = ', data_per_type.shape)

        with open(feature_file, 'wb') as f:
            pickle.dump(data_per_type, f, pickle.HIGHEST_PROTOCOL)
            print ('dump data to file ', feature_file)
# def make_arrays(nb_rows):
#   if nb_rows:
#     dataset = np.ndarray((nb_rows, FEATURE_SIZE, NO_FRAME), dtype=np.float64)
#     labels = np.ndarray(nb_rows, dtype=np.int32)
#   else:
#     dataset, labels = None, None
#   return dataset, labels

def gender_accent(label):
    g, a = label.split('_')
    gn, an = -1, -1
    if g == 'male':
        gn = GENDER_M
    elif g == 'female':
        gn = GENDER_F
    if a == 'north':
        an =  ACCENT_N
    elif a == 'south':
        an = ACCENT_S
    elif a == 'central':
        an = ACCENT_C
    if an < 0:
        print (label)
    assert gn >= 0
    assert an >= 0
    return (gn, an)

def randomize(dataset, labels):
  permutation = np.random.permutation(labels.shape[0])
  shuffled_dataset = dataset[permutation,:,:]
  shuffled_labels = labels[permutation]
  return shuffled_dataset, shuffled_labels

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


def split_train_valid_test(dtype='accent'):
    test_input, test_labels = None, []
    train_input, train_labels = None, []
    valid_input, valid_labels = None, []
    for l in os.listdir(TRAIN_FEATURES):
        data = None
        with open(os.path.join(TRAIN_FEATURES, l), 'rb') as f:
            data = pickle.load(f)
        no_voice = data.shape[0]
        test_count = round(TEST_RATIO * no_voice)
        valid_count = round(VALID_RATIO * no_voice)
        train_count = no_voice - test_count - valid_count
        gender, accent = gender_accent(l.replace('.pickle', ''))
        label = get_label(gender, accent, dtype)

        np.random.shuffle(data)
        ti = data[:test_count,:,:]
        assert ti.shape[0] == test_count
        test_input = np.vstack((test_input, ti)) if test_input is not None else ti        
        test_labels = np.concatenate((test_labels, np.full((test_count, ), label, dtype=np.int32)))

        vi = data[test_count:(test_count + valid_count),:,:]
        assert vi.shape[0] == valid_count
        valid_input = np.vstack((valid_input, vi)) if valid_input is not None else vi
        valid_labels = np.concatenate((valid_labels, np.full((valid_count, ), label, dtype=np.int32)))

        tri = data[(test_count + valid_count):,:,:]
        assert tri.shape[0] == train_count
        train_input = np.vstack((train_input, tri)) if train_input is not None else tri
        train_labels = np.concatenate((train_labels, np.full((train_count, ), label, dtype=np.int32)))

    print ('train input ', train_input.shape, ' label ', train_labels.shape)
    print ('test input ', test_input.shape, ' label ', test_labels.shape)
    print ('valid input ', valid_input.shape, ' label ', valid_labels.shape)
    # randomize
    train_input, train_labels = randomize(train_input, train_labels)
    test_input, test_labels = randomize(test_input, test_labels)
    valid_input, valid_labels = randomize(valid_input, valid_labels)

    output_file = 'randomized_' + dtype + '_data.pickle'
    dataset = dict(train_input=train_input,
        train_labels=train_labels,
        valid_input=valid_input,
        valid_labels=valid_labels,
        test_input=test_input,
        test_labels=test_labels)
    with open(os.path.join(TRAIN_FEATURES, output_file), 'wb') as f:
        pickle.dump(dataset, f, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    split_train_valid_test('combined')
    # standardize_and_save()
    # features = extract_voice_feature('/media/tamvm/DATA/AiChallenge/train/female_central/6056354cd5b14a8d99183ab9e5fc638d_01771.mp3')
    # print ('extract takes ', (datetime.datetime.now() - start).total_seconds())
    # features = fix_size(features)
    # print ('---', features.shape)
