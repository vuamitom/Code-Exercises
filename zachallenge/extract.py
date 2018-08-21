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
NO_FRAME = 500
N_MFCC = 13
N_MELS = 26
FEATURE_SIZE = N_MFCC * 2 + N_MELS
SAMPLE_PER_FRAME = 512

def extract():
    try:        
        # make output dir
        os.mkdir(TRAIN_TEMP, mode=0o755)
    except FileExistsError:
        pass

    if len(os.listdir(TRAIN_TEMP)) > 0:
        print ('Already extracted')
        return None

    file_list = os.listdir(TRAIN_INPUT)
    dataset = np.ndarray(shape=(len(file_list), FEATURE_SIZE, NO_FRAME),
                         dtype=np.float32)
    m = dict()
    for l in file_list:
        p = os.path.join(TRAIN_INPUT, l) 
        
        for r in os.listdir(p):
            fp = os.path.join(p, r)
            # start = datetime.datetime.now()
            features = extract_voice_feature(fp)
            # print ('extract takes ', (datetime.datetime.now() - start).total_seconds())
            features = fix_size(features)
            # print (features)
            c = len(features[0])
            m[c] = 0 if c not in m else m[c]
            m[c] += 1
        print (m)
            # break
        # break 
    print (m)

def fix_size(features):
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
    # mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, 
    #                     hop_length=SAMPLE_PER_FRAME, 
    #                     fmin=MIN_VOICE_FREQ, 
    #                     fmax=MAX_VOICE_FREQ,
    #                     n_mels=N_MELS,
    #                     n_mfcc=N_MFCC)
    # delta = librosa.feature.delta(mfccs)

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
    return spectrogram
    
def encode_label(l):
    return (1, 1, 2)


if __name__ == '__main__':
    extract()
