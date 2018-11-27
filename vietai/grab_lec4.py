import numpy as np
import matplotlib.pyplot as plt


# utils function
def plot_polynomial(xmin, xmax, coef, color='C1'):
    #xs is an array of evenly spaced numbers between xmin and xmax
    xs = np.linspace(xmin, xmax, num=500)
    
    #ys is an array, each element is computed as a polynomial function of
    #the corresponding element of xs
    ys = np.zeros_like(xs)
    print('coef = ', coef.flatten())
    for p, c in enumerate(coef.flatten()):
        ys += c*np.power(xs, p)
    plt.plot(xs, ys, color=color)


X = np.array([2 ,  7 ,  9 ,  3 ,  10,  6 ,  1 ,  8]).reshape((8, 1))
Y = np.array([13,35,41,19,45,28,10,55 ]).reshape((8, 1))

print('X = ', X)
print('Y = ', Y)

 
plt.scatter(X, Y)


### Normal equation vs gradient descent

### Normal equation

def whynot_equation(X, Y):
    # this is a question of mine, derive from y = X.dot(theta). ==> theta = X.inv.dot(Y) 
    # but it would not be possible be cause inversion requires matrix of square dimension.
    # it will only works when no of. feature == no of samples
    X = np.concatenate((X, np.ones(shape=(8, 1))), axis=1)
    theta = np.linalg.inv(X.transpose()).dot(Y)
    return theta

# theta = np.linalg.inv dot dot 
def normal_equation(X, Y):
    # allow for biases
    # y = theta * x + b
    #   = [theta1 theta2] * transpose([x 1]) 
    X = np.concatenate((X, np.ones(shape=(8, 1))), axis=1)
    print('X with biases = ', X)        
    theta = np.linalg.inv(X.transpose().dot(X)).dot(X.transpose()).dot(Y)
    print('theta = ', theta)
    return theta

# plot_polynomial 

def _grad(X, Y, theta, m, alpha):
    g = 1/m * (X.transpose().dot(X.dot(theta) - Y))
    return theta - alpha * g

def _loss(X, Y, theta, m):
    return 1/(2*m) * (np.linalg.norm(X.dot(theta) - Y) ** 2)

def gradient_descent(X, Y):
    alpha = 0.01
    X = np.concatenate((X, np.ones(shape=(8, 1))), axis=1)
    theta = np.random.uniform(size=2).reshape((2,1))
    m = X.shape[0]
    for i in range(0, 10000):
        l = _loss(X, Y, theta, m)
        print('loss = ', l)
        theta = _grad(X, Y, theta, m, alpha)
    return theta
#gradient descent

# theta = whynot_equation(X, Y)
# print('theta = ', theta)

theta = normal_equation(X, Y)
plot_polynomial(0, 10, theta[::-1], 'C3')

theta = gradient_descent(X, Y)
plot_polynomial(0, 10, theta[::-1], 'C2')
plt.show()

