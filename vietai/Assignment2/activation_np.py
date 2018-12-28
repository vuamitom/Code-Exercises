"""activation_np.py
This file provides activation functions for the NN 
Author: Phuong Hoang
"""

import numpy as np


def sigmoid(x):
    """sigmoid
    TODO: 
    Sigmoid function. Output = 1 / (1 + exp(-x)).
    :param x: input
    """
    # [TODO 1.1]
    # return np.power(1 + np.exp(0-x), -1)
    # to avoid overflow. calculate exp(-|x|) instead of exp(-x)
    z = np.exp(0 - np.abs(x))
    t = np.where(x > 0, 1, z)
    return t / (1 + z)


def sigmoid_grad(a):
    """sigmoid_grad
    TODO:
    Compute gradient of sigmoid with respect to input. g'(x) = g(x)*(1-g(x))
    :param a: output of the sigmoid function
    """
    #[TODO 1.1]
    return np.multiply(a, 1 - a)


def reLU(x):
    """reLU
    TODO:
    Rectified linear unit function. Output = max(0,x).
    :param x: input
    """
    #[TODO 1.1]    
    return np.where(x > 0, x, 0)


def reLU_grad(a):
    """reLU_grad
    TODO:
    Compute gradient of ReLU with respect to input
    :param x: output of ReLU
    """
    #[TODO 1.1]
    grad = np.where(a > 0, 1, 0)
    return grad


def tanh(x):
    """tanh
    TODO:
    Tanh function.
    :param x: input
    """
    # [TODO 1.1]
    # to avoid overflow. calculate exp(-2|x|) instead of exp(2x)
    z = np.exp(0 - 2 * np.abs(x))
    return np.multiply(np.where(x > 0, -1, 1), (z - 1) / (z + 1))   


def tanh_grad(a):
    """tanh_grad
    TODO:
    Compute gradient for tanh w.r.t input
    :param a: output of tanh
    """
    #[TODO 1.1]
    return 1 - np.power(a, 2)


def softmax(x):
    """softmax
    TODO:
    Softmax function.
    :param x: input. Assuming x is of dimension MxD where M is no of samples. D is no dimens
    """
    z = np.exp(x)
    zs = np.sum(z, axis=1, keepdims=True)        
    return z / zs


def softmax_minus_max(x):
    """softmax_minus_max
    TODO:
    Stable softmax function.
    :param x: input
    """
    z = np.exp(x - np.amax(x, axis=1, keepdims=True))
    zs = np.sum(z, axis=1, keepdims=True)        
    return z / zs

if __name__ == '__main__':
    x = np.array([[1, -2], [3,-4]])
    a = sigmoid(x)
    print('sigmoid = ', a)
    g = sigmoid_grad(a)
    print('sigmoid_grad = ', g)
    a = reLU(x)
    print('reLU = ', a)
    g = reLU_grad(x)
    print('reLU_grad = ', g)
    a = tanh(x)
    print('tanh = ', a, ' np tanh = ', np.tanh(x))
    g = tanh_grad(a)
    print('tanh_grad = ', g)
