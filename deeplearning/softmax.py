"""Softmax."""


scores = [3.0, 1.0, 0.2]

import numpy as np
import math

# def softmax(x):
#     """Compute softmax values for each sets of scores in x."""
#     if type(x) is list or len(x.shape) == 1:
#         r = [math.exp(y) for y in x]
#         s = sum(r)
#         return [y / s for y in r]
#     else:
#         print x.shape
#         r, c = x.shape
#         res = np.array(x, dtype = np.dtype(float))
#         for nc in xrange(0, c):
#             s = 0
#             for nr in xrange(0, r):
                
#                 res[nr][nc] = math.exp(x[nr][nc])
#                 s += res[nr][nc]
#             for nr in xrange(0, r):
#                 res[nr][nc] = res[nr][nc] /s 
#         return res

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

print(softmax(scores))

# Plot softmax curves
import matplotlib.pyplot as plt
x = np.arange(-2.0, 6.0, 0.1)
print (x)
scores = np.vstack([x, np.ones_like(x), 0.2 * np.ones_like(x)])
print(softmax(scores))
plt.plot(x, softmax(scores).T, linewidth=2)
plt.show()