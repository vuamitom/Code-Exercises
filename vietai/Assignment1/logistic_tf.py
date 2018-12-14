"""
This file is for binary classification using TensorFlow
Author: Kien Huynh
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from util import get_vehicle_data 
from logistic_np import *

def compute_loss_builtin(y, logits):
    # gt_zero = (x > zeros)
    # relu_logits = tf.where(gt_zero, x, zeros)
    # neg_abs = tf.where(gt_zero, -x, x)    
    # c = tf.reduce_mean(relu_logits - tf.multiply(x, L) + tf.log(1 + tf.exp(neg_abs)))
    return tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
        labels=y,
        logits=logits))
    

if __name__ == "__main__":
    np.random.seed(2018)
    tf.set_random_seed(2018)

    # Load data from file
    # Make sure that vehicles.dat is in data/
    train_x, train_y, test_x, test_y = get_vehicle_data()
    num_train = train_x.shape[0]
    num_test = test_x.shape[0]  
    
    #generate_unit_testcase(train_x.copy(), train_y.copy()) 
    #logistic_unit_test()

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
   
    # [TODO 1.11] Create TF placeholders to feed train_x and train_y when training
    x = tf.placeholder(np.float32) 
    y = tf.placeholder(np.float32) 

    # [TODO 1.12] Create weights (W) using TF variables
    w_shape = (train_x.shape[1],1)
    w = tf.get_variable("weights", w_shape) 

    # [TODO 1.13] Create a feed-forward operator
    logits = tf.matmul(x, w, transpose_a=False, transpose_b=False, name='logits')
    zeros_like = tf.zeros_like(logits)
    pred = tf.where(tf.sigmoid(logits, name='pred') - 0.5 > zeros_like, tf.ones_like(logits), zeros_like)
    # [TODO 1.14] Write the cost function
    cost = compute_loss_builtin(y, logits)    
    # Define hyper-parameters and train-related parameters
    num_epoch = 2000
    learning_rate = 0.001

    # [TODO 1.15] Create an SGD optimizer
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost) 

    # Some meta parameters
    epochs_to_draw = 100
    all_loss = []
    plt.ion()

    # Start training
    init = tf.global_variables_initializer()
    
    with tf.Session() as sess:

        sess.run(init)

        for e in range(num_epoch):
            # [TODO 1.16] Compute loss and update weights here
            loss, _ = sess.run([cost, optimizer], feed_dict={x: train_x, y: train_y})
            # Update weights...
            # sess.run([optimizer], feed_dict={x: train_x, y: train_y})
            all_loss.append(loss)

            if (e % epochs_to_draw == epochs_to_draw-1):
                plot_loss(all_loss)
                plt.show()
                # plt.pause(0.1)     
                print("Epoch %d: loss is %.5f" % (e+1, loss))
        
        y_hat = sess.run(pred, feed_dict={x: test_x})
        test(y_hat, test_y)
