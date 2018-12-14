"""
This file is for two-class vehicle classification
Author: Kien Huynh
"""

import numpy as np
import matplotlib.pyplot as plt
from util import get_vehicle_data

import pdb


class LogisticClassifier(object):
    def __init__(self, w_shape):
        """__init__
        
        :param w_shape: create w with shape w_shape using normal distribution
        """

        mean = 0
        std = 1
        self.w = np.random.normal(0, np.sqrt(2./np.sum(w_shape)), w_shape)        

    def feed_forward(self, x):
        """feed_forward
        This function compute the output of your logistic classification model
        
        :param x: input
        
        :return result: feed forward result (after sigmoid) 
        """
        # [TODO 1.5]
        # Compute feedforward result
        y = x.dot(self.w)
        # to avoid overflow
        # sigmoid(y) = min(0, y) * (e**y / ( e** y + 1) + max(0, y) * (1 / (1 + e ** -y))
        #            = (1{y < 0} else e**-abs(y)) * ( 1 / (1 + e ** - abs(y)))
        neg_abs = np.exp(np.where(y > 0, -y, y))
        term = np.exp(np.where(y > 0, 0, y))
        result = np.multiply(term, 1 / (1 + neg_abs))
        return result


    def compute_loss(self, y, y_hat):
        """compute_loss
        Compute the loss using y (label) and y_hat (predicted class)

        :param y:  the label, the actual class of the samples
        :param y_hat: the propabilitis that the given samples belong to class 1
        
        :return loss: a single value
        """
        # [TODO 1.6]
        # Compute loss value (a single number)

        loss = 0 - np.mean(np.multiply(y, np.log(y_hat)) + np.multiply(1 - y, np.log( 1 - y_hat)))
        return loss


    def get_grad(self, x, y, y_hat):
        """get_grad
        Compute and return the gradient of w

        :param loss: computed loss between y_hat and y in the train dataset
        :param y_hat: predicted y
        
        :return w_grad: has the same shape as self.w
        """ 
        # [TODO 1.7]
        # Compute the gradient matrix of w, it has the same size of w

        w_grad = np.matmul(x.transpose(), (y_hat - y)) / y.shape[0]
        return w_grad


    def update_weight(self, grad, learning_rate):
        """update_weight
        Update w using the computed gradient

        :param grad: gradient computed from the loss
        :param learning_rate: float, learning rate
        """
        # [TODO 1.8]
        # Update w using SGD

        self.w = self.w - learning_rate * grad


    def update_weight_momentum(self, grad, learning_rate, momentum, momentum_rate):
        """update_weight with momentum
        Update w using the algorithm with momnetum

        :param grad: gradient computed from the loss
        :param learning_rate: float, learning rate
        :param momentum: the array storing momentum for training w, should have the same shape as w
        :param momentum_rate: float, how much momentum to reuse after each loop (denoted as gamma in the document)
        """
        # [TODO 1.9]
        # Update w using SGD with momentum
        momentum[:,:] = momentum_rate * momentum + learning_rate * grad
        self.w = self.w - momentum

    
def plot_loss(all_loss):
    plt.figure(1)
    plt.clf()
    plt.plot(all_loss)


def normalize_per_pixel(train_x, test_x):
    """normalize_per_pixel
    This function computes train mean and standard deviation on each pixel then applying data scaling on train_x and test_x using these computed values

    :param train_x: train images, shape=(num_train, image_height, image_width)
    :param test_x: test images, shape=(num_test, image_height, image_width)
    """
    # [TODO 1.1]
    # train_mean and train_std should have the shape of (1, image_height, image_width) 
    train_size, imgw, imgh = train_x.shape
    train_mean = np.mean(train_x, axis=0).reshape((1, imgw, imgh))
    train_std = np.sqrt(np.mean(np.power(train_x - train_mean, 2), axis=0)).reshape((1, imgw, imgh))
    # train_x = ...
    train_x = (train_x - train_mean) / train_std
    # test_x = ...
    test_x = (test_x - train_mean) / train_std
    return train_x, test_x


def normalize_all_pixel(train_x, test_x):
    """normalize_all_pixel
    This function computes train mean and standard deviation on all pixels then applying data scaling on train_x and test_x using these computed values

    :param train_x: train images, shape=(num_train, image_height, image_width)
    :param test_x: test images, shape=(num_test, image_height, image_width)
    """
    # [TODO 1.2]
    # train_mean and train_std should have the shape of (1, image_height, image_width) 
    train_mean = np.mean(train_x)
    train_std = np.sqrt(np.mean(np.power(train_x - train_mean, 2)))
    # train_x = ...    
    train_x = (train_x - train_mean) / train_std
    # test_x = ...
    test_x = (test_x - train_mean) / train_std

    return train_x, test_x


def reshape2D(tensor):
    """reshape_2D
    Reshape our 3D tensors to 2D. A 3D tensor of shape (num_samples, image_height, image_width) must be reshaped into (num_samples, image_height*image_width)
    """
    # [TODO 1.3]
    tensor = tensor.reshape((tensor.shape[0], tensor.shape[1] * tensor.shape[2]))
    return tensor


def add_one(x):
    """add_one
    
    This function add ones as an additional feature for x
    :param x: input data
    """
    # [TODO 1.4]
    x = np.concatenate((x, np.ones(shape=((x.shape[0], 1)))), axis=1)
    return x


def test(y_hat, test_y):
    """test
    Compute precision, recall and F1-score based on predicted test values

    :param y_hat: predicted values, output of classifier.feed_forward
    :param test_y: test labels
    """
    
    # [TODO 1.10]
    # Compute test scores using test_y and y_hat
    # print(y_hat)
    # print(test_y)
    y_hat = y_hat.reshape((y_hat.shape[0],)).astype(int)
    test_y = test_y.reshape((test_y.shape[0],)).astype(int)

    tp = y_hat.transpose().dot(np.where(y_hat - test_y == 0, 1, 0))
    # print ('tp = ', tp)
    precision = tp / np.sum(y_hat)
    recall = tp / np.sum(test_y)
    f1 = 2 / ( 1/precision + 1/recall)
    print("Precision: %.3f" % precision)
    print("Recall: %.3f" % recall)
    print("F1-score: %.3f" % f1)

    return precision, recall, f1


def generate_unit_testcase(train_x, train_y):
    train_x = train_x[0:5, :, :]
    train_y = train_y[0:5, :]
    
    testcase = {}
    testcase['output'] = []

    train_x_norm1, _ = normalize_per_pixel(train_x, train_x)
    train_x_norm2, _ = normalize_all_pixel(train_x, train_x)
    train_x = train_x_norm2

    testcase['train_x_norm1'] = train_x_norm1
    testcase['train_x_norm2'] = train_x_norm2

    train_x = reshape2D(train_x)
    testcase['train_x2D'] = train_x

    train_x = add_one(train_x)
    testcase['train_x1'] = train_x
    
    learning_rate = 0.001
    momentum_rate = 0.9

    for i in range(10): 
        test_dict = {}
        classifier = LogisticClassifier((train_x.shape[1], 1))
        test_dict['w'] = classifier.w
        
        y_hat = classifier.feed_forward(train_x)
        loss = classifier.compute_loss(train_y, y_hat)
        grad = classifier.get_grad(train_x, train_y, y_hat)
        classifier.update_weight(grad, 0.001)
        test_dict['w_1'] = classifier.w
        
        momentum = np.ones_like(grad)
        classifier.update_weight_momentum(grad, learning_rate, momentum, momentum_rate)
        test_dict['w_2'] = classifier.w

        test_dict['y_hat'] = y_hat
        test_dict['loss'] = loss
        test_dict['grad'] = grad
         
        testcase['output'].append(test_dict)
    
    np.save('./data/unittest', testcase)


if __name__ == "__main__":
    np.random.seed(2018)

    # Load data from file
    # Make sure that vehicles.dat is in data/
    train_x, train_y, test_x, test_y = get_vehicle_data()
    num_train = train_x.shape[0]
    num_test = test_x.shape[0]  
    
    # generate_unit_testcase(train_x.copy(), train_y.copy()) 

    # Normalize our data: choose one of the two methods before training
    #train_x, test_x = normalize_all_pixel(train_x, test_x) 
    train_x, test_x = normalize_per_pixel(train_x, test_x) 

    # Reshape our data
    # train_x: shape=(2400, 64, 64) -> shape=(2400, 64*64)
    # test_x: shape=(600, 64, 64) -> shape=(600, 64*64)
    train_x = reshape2D(train_x)
    test_x = reshape2D(test_x)
    
    # Pad 1 as the last feature of train_x and test_x
    train_x = add_one(train_x) 
    test_x = add_one(test_x)
    
    # Create classifier
    num_feature = train_x.shape[1]
    bin_classifier = LogisticClassifier((num_feature, 1))
    momentum = np.zeros_like(bin_classifier.w)

    # Define hyper-parameters and train-related parameters
    num_epoch = 1000
    learning_rate = 0.01
    momentum_rate = 0.9
    epochs_to_draw = 100
    all_loss = []
    plt.ion()
    for e in range(num_epoch):    
        y_hat = bin_classifier.feed_forward(train_x)
        loss = bin_classifier.compute_loss(train_y, y_hat)
        grad = bin_classifier.get_grad(train_x, train_y, y_hat)
        
        # Updating weight: choose either normal SGD or SGD with momentum
        # bin_classifier.update_weight(grad, learning_rate)
        bin_classifier.update_weight_momentum(grad, learning_rate, momentum, momentum_rate)

        all_loss.append(loss) 
        
        if (e % epochs_to_draw == epochs_to_draw-1):
            plot_loss(all_loss)
            plt.show()
            plt.pause(0.1)     
            print("Epoch %d: loss is %.5f" % (e+1, loss))
    
    y_hat = bin_classifier.feed_forward(test_x)
    test(np.where(y_hat > 0.5, 1, 0), test_y)
