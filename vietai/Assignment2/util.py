"""
This files helps you read data from data files
Author: Kien Huynh
"""
import pickle
import gzip
import glob
import numpy as np
import sys

import matplotlib.pyplot as plt
import pdb


def load_npy(file_name):
    """load_npy
    Load numpy data file. This is needed as python 2.7 pickle uses ascii as default encoding method but python 3.x uses utf-8.abs

    :param file_name: npy file path
    
    :return obj: loaded numpy object
    """
    
    if (sys.version_info[0] >= 3):
        obj = np.load(file_name, encoding='latin1')
    elif (sys.version_info[0] >=2):
        obj = np.load(file_name)
    
    return obj


def load_list(file_name):
    """load_list
    Load a list object to file_name.

    :param file_name: string, file name.
    """
    end_of_file = False
    list_obj = [] 
    f = open(file_name, 'rb')
    python_version = sys.version_info[0]
    while (not end_of_file):
        try:
            if (python_version >= 3):
                list_obj.append(pickle.load(f, encoding='latin1'))
            elif (python_version >=2):
                list_obj.append(pickle.load(f))
        except EOFError:
            end_of_file = True
            print("EOF Reached")

    f.close()
    return list_obj 


def save_list(list_obj, file_name):
    """save_list
    Save a list object to file_name
    
    :param list_obj: List of objects to be saved.
    :param file_name: file name.
    """

    f = open(file_name, 'wb')
    for obj in list_obj:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    f.close() 


def get_vehicle_data():
    """
    Load vehicle data and return it as a list: [train_x, train_y, test_x, test_y]
    """
    print('Reading vehicle data...')
    train_x, train_y, test_x, test_y = load_list('./data/vehicles.dat')
    train_x = np.transpose(train_x, (2,0,1))
    test_x = np.transpose(test_x, (2,0,1)) 

    print('Done reading')
    return train_x, train_y, test_x, test_y


def get_bat_data():
    """
    Load bat data and return it as a list: [train_x, train_y, test_x, test_y]
    """
    print('Reading bat data...')
    train_x, train_y, test_x, test_y = load_list('./data/bat.dat')

    print('Done reading')
    return train_x, train_y, test_x, test_y


def read_mnist_gz(data_path, offset):
    with gzip.open(data_path, 'rb') as f:
        dataset = np.frombuffer(f.read(), dtype=np.uint8, offset=offset)

    return dataset


def get_mnist_data(sampling_step=20):
    print('Reading fashion MNIST data...')
    train_x = read_mnist_gz('./data/fashion-mnist/train-images-idx3-ubyte.gz', 16)
    train_y = read_mnist_gz('./data/fashion-mnist/train-labels-idx1-ubyte.gz', 8)
    test_x = read_mnist_gz('./data/fashion-mnist/t10k-images-idx3-ubyte.gz', 16)
    test_y = read_mnist_gz('./data/fashion-mnist/t10k-labels-idx1-ubyte.gz', 8)
    num_train = len(train_y)
    num_test = len(test_y)

    train_x = train_x.reshape((num_train, 28*28))
    test_x = test_x.reshape((num_test, 28*28))

    val_x = train_x[50000:,:]
    val_y = train_y[50000:]
    train_x = train_x[:50000,:]
    train_y = train_y[:50000]

    train_x = train_x[0::sampling_step,:]
    train_y = train_y[0::sampling_step]
    val_x = val_x[0::sampling_step,:]
    val_y = val_y[0::sampling_step]
    test_x = test_x[0::sampling_step,:]
    test_y = test_y[0::sampling_step]
 
    print("Done reading")
    return train_x.astype(np.float32), train_y, val_x.astype(np.float32), val_y, test_x.astype(np.float32), test_y


def visualize_point(x, y, y_hat, fig=1):
    """visualize_point
    
    This funciton scatter data points (in x) and color them according to y and y_hat for comparison
    Both figures should be similar
    :param x: data points, each point has two dimensions (x1, x2)
    :param y: actual labels of the data points
    :param y_hat: predicted labels of the data points
    """
    
    color_map = np.asarray([
            [0,0,0],
            [1,1,0],
            [0,0,1]
            ])
    
    fig = plt.figure(fig, figsize = (12,6))
    plt.clf()
   
    if (y.ndim == 2):
        if (y.shape[1] > 1 and np.unique(y) == 2):
            # One-hot, probably
            color_list = color_map[np.argmax(y,1), :]
        else:
            # int label
            color_list = color_map[y.flatten(), :]
    elif (y.ndim == 1):
        color_list = color_map[y,:]
    else:
        raise ValueError("y should be of shape (batch_size, ) or (batch_size, num_class)")

    color_list = color_map[y,:]
    ax = plt.subplot(1,2,1)
    ax.set_title("Actual classes")
    ax.scatter(x[:,0], x[:,1], color = color_list)
    plt.axis('equal')

    c = np.copy(y_hat)
    c = np.argmax(c, 1)
    color_list = color_map[c,:]
    ax = plt.subplot(1,2,2)
    ax.set_title("Prediction")
    ax.scatter(x[:,0], x[:,1], color = color_list)

    plt.axis('equal')
    plt.ion() 
    plt.draw()
    plt.show()


def plot_loss(loss, fig=1, color='b'):
    plt.figure(fig)
    plt.clf()
    plt.plot(loss, color='b')


def normalize(train_x, val_x, test_x):
    """normalize
    This function computes train mean and standard deviation on all pixels then applying data scaling on train_x, val_x and test_x using these computed values

    :param train_x: train samples, shape=(num_train, num_feature)
    :param val_x: validation samples, shape=(num_val, num_feature)
    :param test_x: test samples, shape=(num_test, num_feature)
    """
    # train_mean and train_std should have the shape of (1, 1)
    train_mean = np.mean(train_x, axis=(0,1), dtype=np.float64, keepdims=True)
    train_std = np.std(train_x, axis=(0,1), dtype=np.float64, keepdims=True)

    train_x = (train_x-train_mean)/train_std
    val_x = (val_x-train_mean)/train_std
    test_x = (test_x-train_mean)/train_std
    return train_x, val_x, test_x


def create_one_hot(labels, num_k=10):
    """create_one_hot
    This function creates a one-hot (one-of-k) matrix based on the given labels

    :param labels: list of labels, each label is one of 0, 1, 2,... , num_k - 1
    :param num_k: number of classes we want to classify
    """
    eye_mat = np.eye(num_k)
    return eye_mat[labels, :].astype(np.float32)


def add_one(x):
    """add_one
    
    This function add ones as an additional feature for x
    :param x: input data
    """
    x = np.concatenate((x, np.ones((x.shape[0], 1))), axis=1)
    return x


if __name__ == '__main__':
    get_mnist_data()
