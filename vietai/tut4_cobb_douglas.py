# In economics, the cobb-douglas functional form of production functions is widely used to represent the relationship
# of an output to inputs. IT was proposed by Knut wicksell and tested agaisnt statistical evidence by Charles cobb and Paul douglas in 1928. 
# They considered a simplified view of the economy in which production output is determined by 
# the amount of labor involved and the amount of capital invested.

# P(L, K) = b (L ** alpha) (K ** (1 - alpha))
import numpy as np


years = [y for y in range(1899, 1923)]
m = len(years)
P = [100, 101, 112, 122, 124, 122, 143, 152, 151, 126, 155, 159, 153, 177, 184, 169, 189, 225, 227, 223, 218, 231, 179, 240]
L = [100, 105, 110, 117, 122, 121, 125, 134, 140, 123, 143, 147, 148, 155, 156, 152, 156, 182, 198, 201, 196, 194, 146, 161]
K = [100, 107, 114, 122, 131, 138, 149, 163, 176, 185, 198, 208, 216, 226, 236, 244, 266, 298, 335, 366, 387, 407, 417,431]
assert len(P) == len(L) == len (K)
P = np.array(P).reshape((m, 1))
L = np.array(L).reshape((m, 1))
K = np.array(K).reshape((m, 1))


# todo: 
# plot the simple minded plot as well. by solving linear eq

def normal_equation():
    x1 = np.log(L) - np.log(K)
    x0 = np.ones(shape=(m,1))
    X = np.concatenate((x1, x0), axis=1)
    print ('input shape = ', X.shape)
    y = np.log(P) - np.log(K)
    print ('output shape = ', y.shape)
    # y = [x1 x0].[alpha logB]
    # use gradient descent to 
    theta = np.linalg.inv(X.transpose().dot(X)).dot(X.transpose()).dot(y)
    return theta
    
print('solve with normal_equation ', normal_equation())