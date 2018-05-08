import os
import hashlib
from six.moves import cPickle as pickle
import numpy as np

root_dir = '.'
image_size = 28

def quick_check_overlap():
    d = os.path.join(root_dir, 'notMNIST_large')
    datadirs =  os.listdir(d)
    check = set()

    for pd in datadirs:
        da = os.path.join(d, pd)
        if os.path.isdir(da):
            print ('checking === ', da)
            files = os.listdir(da)
            for f in files:
                if f in check:
                    print ('duplicate ', f)
                    print (len(check))
                    break
                else:
                    check.add(f)


def check_overlap_data():
    d = os.path.join(root_dir, 'notMNIST_large')
    datadirs =  os.listdir(d)
    check = set()
    for pd in datadirs:
        print('checking ', pd)
        da = os.path.join(d, pd)
        dupC = 0
        if not os.path.isdir(da):
            
            with open(da, 'rb') as f:
                # check if duplicate
                dataset = pickle.load(f)
                noimgs = dataset.shape[0]
                for c in range(0, noimgs):
                    data = dataset[c]
                    m = hashlib.md5()
                    for r in range(0, image_size):
                        for cc in range(0, image_size):
                            m.update(data[r][cc])
                    sig = m.digest()
                    # print('signature ', sig)
                    if sig in check:
                        # print('Found duplicate for file ', pd, ' count ', dupC)
                        dupC += 1
                        # break
                        
                    else:
                        check.add(sig)
            print ('done check, dup count ', dupC, ' for file ', pd)

def run_validate_data():
    data_file = 'notMNIST.pickle'   
    train_data, val_data, test_data = None, None, None
    with open(os.path.join(root_dir, data_file), 'rb') as f:
        dataset = pickle.load(f)
        train_data = dataset['train_dataset']
        test_data = dataset['test_dataset']
        val_data = dataset['valid_dataset']
    check_dup_cosine_sim(train_data, test_data)


# %%time
def check_dup_cosine_sim(source_dataset, target_dataset):
    X = source_dataset.reshape(source_dataset.shape[0], -1)
    Y = target_dataset.reshape(target_dataset.shape[0], -1)
    print('X shape ', X.shape, ' Y Shape ', Y.shape)
    assert(X.shape[1] == Y.shape[1])

    # calculate cos_sim matrix 
    # X.Y = |X||Y| cos O
    print('cal magnitude X')
    mX = np.sqrt(np.sum(X ** 2, axis = 1))
    mX = mX.reshape(mX.shape[0], 1)
    print('cal magnitude X')
    mY = np.sqrt(np.sum(Y ** 2, axis=1))
    mY = mY.reshape(mY.shape[0], 1)
    print('cal sim matrix')
    cos_sim = np.inner(X, Y) 
    print ('cal mag')
    mag = np.inner(mX, mY)
    print ('cal cos sim')
    cos_sim = cos_sim / mag    
    # absolute similarity has a cosine similarity of 1
    print('DONE cal sim matrix')
    r = cos_sim.shape[0]
    c = cos_sim.shape[1]
    simi = sum([1 for ri in range(0, r) for ci in range(0, c) if cos_sim[ri][ci] == 1])
    print ('similarity ', simi)

def sanitize_data():
    pass

run_validate_data()
# quick_check_overlap()
# check_overlap_data()