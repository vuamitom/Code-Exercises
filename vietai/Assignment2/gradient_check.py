"""gradient_check.py
This file provides functions for you to check your gradient computation
"""

import numpy as np
import pdb


def rel_error(x, y):
    """
    function to determine relative error between expected output results from our actual implementation of a layer
    :param x: expected output, arbitrary shape
    :param y: output from our implementation
    :return:  relative error > 1e-2 means that the result is probably wrong
                             <= e-7, you should be happy
    """
    return np.max(np.abs(x - y)/ np.maximum(1e-8, np.abs(x) + np.abs(y)))


def eval_numerical_gradient(layer,x, df, verbose = True, h = 0.00001):
    """
    a naive implementation of numerical gradient of f at x
    :param f: should be a function that takes a single argument x
    :param x: is the point to evaluate the gradient at
    :param verbose:
    :param h:
    :return:
    """
    fw = layer.forward(x)
    grad = np.zeros_like(layer.w)
    it = np.nditer(layer.w, flags = ['multi_index'], op_flags = ['readwrite'])
    while not it.finished:

        ix = it.multi_index
        oldval = layer.w[ix].copy()
        layer.w[ix] = oldval + h
        fxph  = layer.forward(x) #evaluate f(x+h)
        layer.w[ix] = oldval - h
        fxmh  = layer.forward(x)
        layer.w[ix] = oldval.copy()

        grad[ix] = np.sum((fxph - fxmh)*df)/ (2*h)
        if verbose:
            print(ix, grad[ix])
        it.iternext()
    return grad

