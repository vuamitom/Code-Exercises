import os
import hashlib
from six.moves import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt
import imageio

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
        test_labels = dataset['test_labels']
    check_dup_cosine_sim(train_data, test_data)
    # check_dup_md5(train_data, test_data, -1)

def get_mag(X):
    mX = np.sqrt(np.sum(X ** 2, axis = 1))
    mX = mX.reshape(mX.shape[0], 1)
    return mX

def get_prod(X, Y):
    mX = get_mag(X)
    mY = get_mag(Y)
    return np.inner(mX, mY)


# %%time
def check_dup_cosine_sim(source_dataset, target_dataset):
    X = source_dataset.reshape(source_dataset.shape[0], -1)
    Y = target_dataset.reshape(target_dataset.shape[0], -1)
    print('X shape ', X.shape, ' Y Shape ', Y.shape)
    assert(X.shape[1] == Y.shape[1])

    # calculate cos_sim matrix 
    # X.Y = |X||Y| cos O
    print('cal sim matrix')
    cos_sim = np.inner(X, Y) 
    print ('cal mag')
    mag = get_prod(X, Y)
    print('dividee shape ', cos_sim.shape, ' divider Shape ', mag.shape)
    print ('cal cos sim ')
    cos_sim = cos_sim / mag    
    # absolute similarity has a cosine similarity of 1
    print('DONE cal sim matrix')
    r = cos_sim.shape[0]
    c = cos_sim.shape[1]
    simi = sum([1 for ri in range(0, r) for ci in range(0, c) if cos_sim[ri][ci] == 1])
    print ('similarity ', simi)

def denorm_img(imgdata):
    return imgdata.astype(float) * 255 + 255/2

def md5(img):
    m = hashlib.md5()
    for r in range(0, image_size):
        for c in range(0, image_size):
            m.update(img[r][c])
    return m.digest()

def check_dup_md5(source_dataset, target_dataset, max_dup_count = 15):
    # md5 source
    check = set()
    inverse = {}
    remove_from_source = []
    remove_from_target = []
    for img_idx in range(0, target_dataset.shape[0]):
        h = md5(target_dataset[img_idx])
        check.add(h)
        inverse[h] = img_idx
    for img_idx in range(0, source_dataset.shape[0]):
        h = md5(source_dataset[img_idx])
        if h in check:
            target_idx = inverse[h]
            remove_from_source.append(img_idx)
            remove_from_target.append(target_idx)
    return remove_from_source, remove_from_target

# def hardcode_verify(h, ar):
#     print ('hardcode verify', ar)
#     data_file = 'J'   
#     train_data, val_data, test_data = None, None, None
#     dir = os.path.join(root_dir, 'notMNIST_small', data_file)
#     names = os.listdir(dir)
#     for f in names:
#         if os.path.isfile(os.path.join(dir, f)):
#             image_data = (imageio.imread(os.path.join(dir, f)).astype(float) - 
#                     255.0  / 2) / 255.0
#             # nh = md5(image_data)
#             # if h == nh:
#             #     print ('FOUND ', f)
#             # print (image_data.shape, ar.shape)
#             if np.array_equal(image_data, ar):
#                 print ('FOUND', f)

def filter_duplicate(train_data, train_label, test_data, test_label):
    rm_src, rm_target = check_dup_md5(train_data, test_data)
    print ('delete from training because of duplicate', len(rm_src))
    if len(rm_src) > 0:
        train_data = np.delete(train_data, rm_src, 0)
        train_label = np.delete(train_label, rm_src, 0)
        # test_data = np.delete(test_data, rm_target, 0)
        # test_label = np.delete(test_label, rm_target, 0)

    return train_data, train_label

def filter_purely_black_or_white(data, label):
    toremove = []
    for s in range(0, label.shape[0]):
        d = data[s]
        if is_single_color(d, 0.5) or is_single_color(d, -0.5):
            # delete
            toremove.append(s)
    if len(toremove) > 0:
        print ('remove pure black or white', len(toremove))
        data = np.delete(data, toremove, 0)
        label = np.delete(label, toremove, 0)
        
    return data, label

def is_single_color(data, color_code):
    singluar = True
    for r in range(0, data.shape[0]):
        for c in range(0, data.shape[1]):
            if not (data[r][c] <= color_code + 0.000001 and data[r][c] >= color_code - 0.000001):
                singluar = False
                break
        if not singluar:
            break
    return singluar          

def sanitize_data():
    # remove img that is just purely black and white
    # and remove dup occur in test and validation set from training
    data_file = 'notMNIST.pickle'   
    train_data, val_data, test_data = None, None, None
    with open(os.path.join(root_dir, data_file), 'rb') as f:
        dataset = pickle.load(f)
        train_data = dataset['train_dataset']
        test_data = dataset['test_dataset']
        val_data = dataset['valid_dataset']
        test_labels = dataset['test_labels']
        train_labels = dataset['train_labels']
        valid_labels = dataset['valid_labels']
    print ('filter out purely back white training, label: ', train_data.shape, train_labels.shape)
    train_data, train_labels = filter_purely_black_or_white(train_data, train_labels)
    print ('--- after filter out purely back white training, label: ', train_data.shape, train_labels.shape)
    print ('filter out purely back white test, label: ', test_data.shape, test_labels.shape)
    test_data, test_labels = filter_purely_black_or_white(test_data, test_labels)
    print ('--- after filter out purely back white test, label: ', test_data.shape, test_labels.shape)
    print ('filter out purely back white valid, label: ', val_data.shape, valid_labels.shape)
    val_data, valid_labels = filter_purely_black_or_white(val_data, valid_labels)  
    print ('--- after filter out purely back white valid, label: ', val_data.shape, valid_labels.shape)

    print ('filter out duplicate in training and test')
    train_data, train_labels = filter_duplicate(train_data, train_labels, test_data, test_labels)
    print ('--- train data after filter ', train_data.shape, train_labels.shape)
    print ('filter out duplicate in training and validation')
    train_data, train_labels = filter_duplicate(train_data, train_labels, val_data, valid_labels)
    print ('--- train data after filter ', train_data.shape, train_labels.shape)
    output_file = 'sanitized_notMNIST.pickle'   

    save = {
      'train_dataset': train_data,
      'train_labels': train_labels,
      'valid_dataset': val_data,
      'valid_labels': valid_labels,
      'test_dataset': test_data,
      'test_labels': test_labels,
    }
    with open(os.path.join(root_dir, output_file), 'wb') as f:
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)

sanitize_data()
# run_validate_data()
# quick_check_overlap()
# check_overlap_data()