"""
This file provides functionalities for unit testing
Author: Kien Huynh
"""
import argparse
import numpy as np
import os.path
from util import *

import sys
import pdb


def testcase_check(your_arr, test_arr, testname, print_all, print_ind=None):
    eps = 0.00001
    if (type(your_arr) != type(test_arr)):
        print("Testing %s: Failed. Your arr should be %s but it is %s instead." % (testname, type(test_arr), type(your_arr)))
        return True
    
    if (your_arr.shape != test_arr.shape):
        print("Testing %s: Failed. Your arr should have a shape of %s but its shape is %s instead." % (testname, test_arr.shape, your_arr.shape))
        return True

    if (np.sum((your_arr-test_arr)**2) < eps):
        print("Testing %s: Passed." % testname)
    else:
        print("Testing %s: Failed." % testname)
        if (print_all): 
            print("Your array is")
            print(your_arr)
            print("\nWhile it should be")
            print(test_arr)
        else:
            print("The first few rows of your array are")
            print(your_arr[print_ind, 0])
            print("\nWhile they should be")
            print(test_arr[print_ind, 0])
        return True
    print("----------------------------------------")
    return False


def logistic_unit_test():
    """logistic_unit_test
    Test most functions in the logistic regression assignment
    """
    train_x, train_y, test_x, test_y = get_vehicle_data()
    testcase = load_npy('./data/logistic_unittest.npy')
    testcase = testcase[()]    

    train_x = train_x[0:5, :, :]
    train_y = train_y[0:5, :]
     
    train_x_norm1, _ = normalize_per_pixel(train_x, train_x)
    train_x_norm2, _ = normalize_all_pixel(train_x, train_x)
    train_x = train_x_norm2

    if (testcase_check(train_x_norm1, testcase['train_x_norm1'], "normalize_per_pixel", True)):
        return
    
    if (testcase_check(train_x_norm2, testcase['train_x_norm2'], "normalize_all_pixel", True)):
        return

    train_x = reshape2D(train_x)
    if (testcase_check(train_x, testcase['train_x2D'], "reshape2D", True)):
        return

    train_x = add_one(train_x)
    if (testcase_check(train_x, testcase['train_x1'], "add_one", True)):
        return
     
    train_x = testcase['train_x1']

    learning_rate = 0.001
    momentum_rate = 0.9

    for i in range(10): 
        test_dict = testcase['output'][i]
        classifier = LogisticClassifier((train_x.shape[1], 1))
        classifier.w = test_dict['w']
        
        y_hat = classifier.feed_forward(train_x)
        if(testcase_check(y_hat, test_dict['y_hat'], "feed_forward %d" % (i+1), True)):
            return

        loss = classifier.compute_loss(train_y, y_hat)
        if(testcase_check(loss, test_dict['loss'], "compute_loss %d" % (i+1), True)):
            return

        grad = classifier.get_grad(train_x, train_y, y_hat)
        if(testcase_check(grad, test_dict['grad'], "get_grad %d" % (i+1), True)):
            return

        classifier.update_weight(grad, 0.001)
        if(testcase_check(classifier.w, test_dict['w_1'], "update_weight %d" % (i+1), True)):
            return
        
        momentum = np.ones_like(test_dict['grad'])
        classifier.update_weight_momentum(grad, learning_rate, momentum, momentum_rate)
        if(testcase_check(classifier.w, test_dict['w_2'], "update_weight_momentum %d" % (i+1), True)):
            return
 
        testcase['output'].append(test_dict)


def softmax_unit_test():
    """softmax_unit_test
    Test most functions in the softmax regression assignment
    """
    
    train_x, train_y, _, _, _, _ = get_mnist_data()
    train_x = train_x[0:5, :]
    train_y = train_y[0:5]

    testcase = load_npy('./data/softmax_unittest.npy')
    testcase = testcase[()]    
    train_x, _, _ = normalize(train_x, train_x, train_x)

    if (testcase_check(train_x, testcase['train_x_norm'], "normalize", True)):
        return

    train_y = create_one_hot(train_y)

    if (testcase_check(train_y, testcase['one_hot'], "create_one_hot", True)):
        return

    learning_rate = 0.001
    momentum_rate = 0.9

    for i in range(10): 
        test_dict = testcase['output'][i]
        classifier = SoftmaxClassifier((train_x.shape[1], 10))
        classifier.w = test_dict['w']
        
        y_hat = classifier.feed_forward(train_x)
        loss = classifier.compute_loss(train_y, y_hat)
        grad = classifier.get_grad(train_x, train_y, y_hat) 

        if (testcase_check(y_hat, test_dict['y_hat'], "feed_forward / softmax", True)):
            return
   
        if (testcase_check(loss, test_dict['loss'], "compute_loss", True)):
            return

        if (testcase_check(grad, test_dict['grad'], "get_grad", True)):
            return 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform unitest on numpy logistic regression or softmax regression')
    parser.add_argument('choice', nargs='?', type=int, help='logistic or softmax', default=-1)
    parser.add_argument('sol', nargs='?', type=str, help='', default='')
    args = parser.parse_args()
    choice = args.choice
    sol = args.sol

    if (choice == -1):
        choice = input('Please enter 0 for logistic or 1 for softmax: ')
        if(sys.version_info[0] == 3):
            choice = int(choice)

    np.set_printoptions(precision=3, edgeitems=2)
    if (choice == 0):
        if (sol.lower() == 'sol'):
            from logistic_np_sol import *
        else:
            from logistic_np import *

        print('Running logistic np unit test...')
        logistic_unit_test() 

    elif (choice == 1):
        if (sol.lower() == 'sol'):
            from softmax_np_sol import *
        else:
            from softmax_np import *

        print('Running logistic np unit test...')
        softmax_unit_test()
