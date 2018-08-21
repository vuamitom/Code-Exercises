import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import datetime

BASE = '/media/tamvm/DATA/AiChallenge'
TRAIN_INPUT = os.path.join(BASE, 'train')
TRAIN_TEMP = os.path.join(BASE, 'temp')

MIN_VOICE_FREQ = 70
MAX_VOICE_FREQ = 280
NO_FRAME = 10
N_MFCC = 13
N_MELS = 26
FEATURE_SIZE = N_MFCC * 2 + N_MELS
SAMPLE_PER_FRAME = 256

def get_mean():
    file_list = os.listdir(TRAIN_INPUT)
    prev_mean = None
    for l in file_list:
        p = os.path.join(TRAIN_INPUT, l) 
        print ('process ', l)
        for r in os.listdir(p):
            fp = os.path.join(p, r)
            # start = datetime.datetime.now()
            features = extract_voice_feature(fp)
            print ('feature size = ', features.shape)
            # print ('extract takes ', (datetime.datetime.now() - start).total_seconds())
            features = fix_size(features)
            row, col = features.shape        
            assert row == FEATURE_SIZE
            assert col == NO_FRAME
            # print ('output feature = ', features.shape)
            local_mean = np.mean(features)
            break
            # print (features)
        break

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
            # start = datetime.datetime.now()
            features = extract_voice_feature(fp)
            # print ('extract takes ', (datetime.datetime.now() - start).total_seconds())
            features = fix_size(features)
            # print (features)
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
    r, c = features.shape
    if c < NO_FRAME:
        return np.concatenate((features, features[:, :(NO_FRAME-c)]), axis=1)
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
    get_mean()
