#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import random
import sys
import tensorflow as tf
import cv2


class DataSet:
    def __init__(self):
        mnist = tf.contrib.learn.datasets.load_dataset("mnist")
        self.train_data = mnist.train.images  # Returns np.array
        self.train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
        self.eval_data = mnist.test.images  # Returns np.array
        self.eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)

        self.curr_training_step = 0
        self.curr_test_step = 0

    def get_train_set_size(self):
        return self.train_data.shape[0]

    def get_test_set_size(self):
        return self.eval_data.shape[0]

    def to_one_hot(self, X):
        one_hot = np.zeros((len(X), 10))
        for i in range(len(X)):
            np.put(one_hot[i, :], X[i], 1)

        return one_hot
    
    def next_batch(self, batch_size):
        X_train_bs = self.train_data[self.curr_training_step * batch_size:self.curr_training_step * batch_size + batch_size,:]
        Y_train_bs = self.train_labels[self.curr_training_step * batch_size:self.curr_training_step * batch_size + batch_size]

        self.curr_training_step = self.curr_training_step + 1
        self.curr_training_step = self.curr_training_step if (
            self.curr_training_step * batch_size < self.get_train_set_size()) else 0

        return (X_train_bs, self.to_one_hot(Y_train_bs))

    def next_batch_test(self, batch_size):
        X_test_bs = self.eval_data[self.curr_test_step * batch_size:self.curr_test_step * batch_size + batch_size,:]
        Y_test_bs = self.eval_labels[self.curr_test_step * batch_size:self.curr_test_step * batch_size + batch_size]
        

        self.curr_test_step = self.curr_test_step + 1
        self.curr_test_step = self.curr_test_step if (self.curr_test_step * batch_size < self.get_test_set_size()) else 0

        return (X_test_bs, self.to_one_hot(Y_test_bs))
    
    def visualize_train_sample(self, idx):
        img = np.reshape(self.train_data[idx,:], [28,28])
        cv2.imshow('train sample', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
