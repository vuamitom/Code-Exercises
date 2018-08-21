import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pickle

BASE = '/media/tamvm/DATA/AiChallenge'
TRAIN_INPUT = os.path.join(BASE, 'train')
TRAIN_TEMP = os.path.join(BASE, 'raw_features')

MIN_VOICE_FREQ = 70
MAX_VOICE_FREQ = 280
NO_FRAME = 259
N_MFCC = 13
N_MELS = 26
FEATURE_SIZE = N_MFCC * 2 + N_MELS
SAMPLE_PER_FRAME = 256

def get_mean():
    # voice_list = []
    all_data = None

    for l in os.listdir(TRAIN_INPUT):
        p = os.path.join(TRAIN_INPUT, l) 
        print ('process ', l)
        for r in os.listdir(p):
            fp = os.path.join(p, r)
            # voice_list.append(fp)
            dataset = None
            with open(fp, 'rb') as f:
                dataset = pickle.load(f)

            all_data = dataset if all_data is None else all_data.concatenate(dataset, axis=1)
    print ('All data count = ', all_data.shape)
    means = np.mean(all_data, axis=1)
    assert len(means) == FEATURE_SIZE
    print ('Mean per coefs = ', means)

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


if __name__ == '__main__':
    extract()
    # features = extract_voice_feature('/media/tamvm/DATA/AiChallenge/train/female_central/6056354cd5b14a8d99183ab9e5fc638d_01771.mp3')
    # print ('extract takes ', (datetime.datetime.now() - start).total_seconds())
    # features = fix_size(features)
    # print ('---', features.shape)
