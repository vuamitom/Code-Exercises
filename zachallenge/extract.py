import os
import librosa
import numpy as np

BASE = '/media/tamvm/DATA/AiChallenge'
TRAIN_INPUT = os.path.join(BASE, 'train')
TRAIN_TEMP = os.path.join(BASE, 'temp')

def extract():
    for l in os.listdir(TRAIN_INPUT):
        p = os.path.join(TRAIN_INPUT, l)
        gen, loc, c = encode_label(l)
        for r in os.listdir(p):
            fp = os.path.join(p, r)
            mfcc = extract_mfcc(fp)
            print (mfcc)
            break
        break


def extract_mfcc(fp):
    X, sample_rate = librosa.load(fp, res_type='kaiser_fast') 
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
    return mfccs
    
def encode_label(l):
    return (1, 1, 2)


if __name__ == '__main__':
    extract()
