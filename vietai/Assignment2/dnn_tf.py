"""dnn_tf_sol.py
Solution of deep neural network implementation using tensorflow
Author: Kien Huynh 
"""

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from util import * 
from dnn_np import test
import pdb


def bat_classification():
    # Load data from file
    # Make sure that bat.dat is in data/
    train_x, train_y, test_x, test_y = get_bat_data()
    train_x, _, test_x = normalize(train_x, train_x, test_x)    

    test_y  = test_y.flatten().astype(np.int32)
    train_y = train_y.flatten().astype(np.int32)
    num_class = (np.unique(train_y)).shape[0]
 
    # DNN parameters
    hidden_layers = [100, 100, 100]
    learning_rate = 0.1
    batch_size = 200
    steps = 2000
   
    # Specify that all features have real-value data
    feature_columns = [tf.feature_column.numeric_column("x", shape=[train_x.shape[1]])]


    # Available activition functions
    # https://www.tensorflow.org/api_guides/python/nn#Activation_Functions
    # tf.nn.relu
    # tf.nn.elu
    # tf.nn.sigmoid
    # tf.nn.tanh
    activation = None
    
    # [TODO 1.7] Create a neural network and train it using estimator

    # Some available gradient descent optimization algorithms
    # https://www.tensorflow.org/api_docs/python/tf/train#classes
    # tf.train.GradientDescentOptimizer
    # tf.train.AdadeltaOptimizer
    # tf.train.AdagradOptimizer
    # tf.train.AdagradDAOptimizer
    # tf.train.MomentumOptimizer
    # tf.train.AdamOptimizer
    # tf.train.FtrlOptimizer
    # tf.train.ProximalGradientDescentOptimizer
    # tf.train.ProximalAdagradOptimizer
    # tf.train.RMSPropOptimizer
    # Create optimizer
    optimizer = None

    # optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
    # optimizer = tf.train.MomentumOptimizer(learning_rate=0.01, momentum=0.005)
    
    # build a deep neural network
    # https://www.tensorflow.org/api_docs/python/tf/estimator/DNNClassifier
    classifier = None 
    
    # Define the training inputs
    # https://www.tensorflow.org/api_docs/python/tf/estimator/inputs/numpy_input_fn
    train_input_fn = None 
    
    # Train model.
    classifier.train(
        input_fn=train_input_fn,
        steps=steps)
    
    # Define the test inputs
    test_input_fn = tf.estimator.inputs.numpy_input_fn(
                                    x={"x": test_x},
                                    y=test_y,
                                    num_epochs=1,
                                    shuffle=False)
    
    # Evaluate accuracy. 
    predict_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": test_x},
      num_epochs=1,
      shuffle=False)
    y_hat = classifier.predict(input_fn=predict_input_fn)
    y_hat = list(y_hat)
    y_hat = np.asarray([int(x['classes'][0]) for x in y_hat]) 
    test(y_hat, test_y)


def mnist_classification():
    # Load data from file
    # Make sure that fashion-mnist/*.gz is in data/
    train_x, train_y, val_x, val_y, test_x, test_y = get_mnist_data(1)
    train_x, val_x, test_x = normalize(train_x, train_x, test_x)    

    train_y = train_y.flatten().astype(np.int32)
    val_y = val_y.flatten().astype(np.int32)
    test_y = test_y.flatten().astype(np.int32)
    num_class = (np.unique(train_y)).shape[0]
    pdb.set_trace()

    # DNN parameters
    hidden_layers = [100, 100, 100]
    learning_rate = 0.1
    batch_size = 200
    steps = 500
   
    # Specify that all features have real-value data
    feature_columns = [tf.feature_column.numeric_column("x", shape=[train_x.shape[1]])]


    # Choose activation function
    activation = None
    
    # Some available gradient descent optimization algorithms 
    # TODO: [YC1.7] Create optimizer
    optimizer = None 
    
    # build a deep neural network
    classifier = None 
    
    # Define the training inputs
    # https://www.tensorflow.org/api_docs/python/tf/estimator/inputs/numpy_input_fn
    train_input_fn = None
    
    # Train model.
    classifier.train(
        input_fn=train_input_fn,
        steps=steps)
    
    # Define the test inputs
    test_input_fn = tf.estimator.inputs.numpy_input_fn(
                                    x={"x": test_x},
                                    y=test_y,
                                    num_epochs=1,
                                    shuffle=False)
    
    # Evaluate accuracy. 
    predict_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": test_x},
      num_epochs=1,
      shuffle=False)
    y_hat = classifier.predict(input_fn=predict_input_fn)
    y_hat = list(y_hat)
    y_hat = np.asarray([int(x['classes'][0]) for x in y_hat]) 
    test(y_hat, test_y)


if __name__ == '__main__':
    np.random.seed(2017) 

    plt.ion()
    bat_classification()
    mnist_classification()
