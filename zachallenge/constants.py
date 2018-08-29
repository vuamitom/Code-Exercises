import os

BASE = '/media/tamvm/DATA/AiChallenge'
TRAIN_FEATURES = os.path.join(BASE, 'features_long2')

NO_FRAME = 259
N_MFCC = 13
N_MELS = 26
N_CENT = 1
N_CHROMA = 12
FEATURE_SIZE = N_MFCC * 2 + N_MELS + N_CENT + N_CHROMA

GENDER_M = 1
GENDER_F = 0
ACCENT_N = 0
ACCENT_C = 1
ACCENT_S = 2

MEAN_STD_FILE = 'feature_mean_std_long2.pickle'

EXTRACT_FEATURE_FILE = 'randomized_combined_data_long2.pickle'
TEST_PROCCESSED_DIR = os.path.join(BASE, 'test_preprocessed_long2')