import os

BASE = '/media/tamvm/DATA/AiChallenge'
TRAIN_FEATURES = os.path.join(BASE, 'features')

NO_FRAME = 259
N_MFCC = 13
N_MELS = 26
FEATURE_SIZE = N_MFCC * 2 + N_MELS

GENDER_M = 1
GENDER_F = 0
ACCENT_N = 0
ACCENT_C = 1
ACCENT_S = 2