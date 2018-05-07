import os
import hashlib
from six.moves import cPickle as pickle

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

def sanitize_data():
    pass

# quick_check_overlap()
check_overlap_data()