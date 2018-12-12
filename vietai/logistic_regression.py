import matplotlib.pyplot as plt
import numpy as np
import time
import tensorflow as tf
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.python import debug as tf_debug
np.random.seed(2011)
tf.set_random_seed(2011)

def generate_data(x1_root_pos, x2_root_pos, x1_root_neg, x2_root_neg, n_sample, test_raito=0.3):
    # Generate two sets of data point and label

    x1_pos = np.random.rand(n_sample) + x1_root_pos
    x2_pos = np.random.rand(n_sample) + x2_root_pos
    x1_neg = np.random.rand(n_sample) + x1_root_neg
    x2_neg = np.random.rand(n_sample) + x2_root_neg
    label = np.concatenate([np.ones(n_sample, dtype=float), np.zeros(n_sample, dtype=float)])
    
    # Combine features and shuffle
    x1_data = np.expand_dims(np.concatenate([x1_pos, x1_neg]), axis=1)
    x2_data = np.expand_dims(np.concatenate([x2_pos, x2_neg]), axis=1)
    x_data = np.concatenate([x1_data, x2_data], axis=1)
    
    # Split train test set
    x_train, x_test, label_train, label_test = train_test_split(x_data, label, test_size=test_raito, random_state=42)
    return x_train, x_test, label_train, label_test


def visualize_data(x, label, title=''):
    # Plot data using matplot lib
    for i in range(len(label)):
        if label[i] == 0:
            plt.plot(x[i][0], x[i][1], 'b+')
        elif label[i] == 1:
            plt.plot(x[i][0], x[i][1], 'ro')
    
    plt.ylabel('X1 Feature')
    plt.xlabel('X2 Feature')
    plt.title(title)
    plt.show()

def draw_model(a, b, c):
    # Draw line ax + by + c = 0
    x = np.arange(-2, 2, 0.2)
    y = (-a * x - c) / b
    plt.plot(x, y)


def test_data_range(x1, x2):
    # x1 = np.array(X1)
    # x2 = np.array(X2)
    print ('x1 shape = ', x1.shape)
    print ('x2 shape = ', x2.shape)
    h = x1 * 10 + x2 * 10 + 10
    print ('h = ', h, ' shape = ', h.shape)
    h = 1/ ( 1 + np.exp(-h))
    print (h)

def define_parameters():
    # TODO 1: Initialize parameters of logistic model 
    # named: 'a', 'b' and 'c' by value of 10
    a = tf.Variable(initial_value=10, dtype=tf.float32)
    b = tf.Variable(initial_value=10, dtype=tf.float32)
    c = tf.Variable(initial_value=10, dtype=tf.float32)
    return a, b, c

def define_cost_func_with_builtin(X1, X2, L, a, b, c, n_sample):
    logits = X1 * a + X2 * b + c
    return tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
        labels=L,
        logits=logits))

def define_cost_func_with_workedout_equation_v2(X1, X2, L, a, b, c, n_sample):
    # version 2 does not use while_loop. learn from tensorflow's own implementation
    x = X1 * a + X2 *b + c
    zeros = tf.zeros_like(x)
    gt_zero = (x > zeros)
    relu_logits = tf.where(gt_zero, x, zeros)
    neg_abs = tf.where(gt_zero, -x, x)    
    c = tf.reduce_mean(relu_logits - tf.multiply(x, L) + tf.log(1 + tf.exp(neg_abs)))
    return c

def define_cost_func_with_workedout_equation(X1, X2, L, a, b, c, n_sample):
    # https://www.tensorflow.org/api_docs/python/tf/nn/sigmoid_cross_entropy_with_logits
    # max(x, 0) - x * z + log(1 + exp(-abs(x)))
    x = X1 * a + X2 *b + c
    data_size = tf.shape(L)[0]
    temp = tf.TensorArray(dtype=tf.float32, size=data_size)
    i, temp = tf.while_loop(lambda i, _: i < data_size,
                    lambda i, temp: (i + 1, temp.write(i, tf.cond(x[i] > 0, lambda: x[i], lambda: 0.0))),
                    (tf.constant(0), temp))
    m = temp.stack()
    c = tf.reduce_mean(m - tf.multiply(x, L) + tf.log(1 + tf.exp(-tf.abs(x))))
    return c


def define_cost_func(X1, X2, L, a, b, c, n_sample):
    # this is suffering from overflow
    # TODO 2: define hypothesis 'h' and cost function cost 'cost'
    H = tf.sigmoid(X1 * a + X2 *b  + c)
    # pH = tf.Print(H, [H, a, b, c], ' sigmoid output and weights ')
    pH = tf.Print(H, [H[:10]], 'H = ')
    logH = tf.log(pH)
    logNH = tf.log(1 - pH)
    logPH = tf.Print(logH, [logH], ' log possitive probability ')
    logPNH = tf.Print(logNH, [logNH], ' log negative probability ')
    pp = tf.multiply(L, logPH)
    np = tf.multiply(1- L, logPNH)
    pp_print = tf.Print(pp, [pp], ' possitive prob')
    np_print = tf.Print(np, [np], ' negative prob')
    sum_p = tf.reduce_sum(pp_print + np_print)
    sum_print = tf.Print(sum_p, [sum_p], ' reduce_sum = ')
    d = sum_print / n_sample

    cost = 0 - tf.Print(d, [d], ' max likelihood = ')
    return tf.Print(cost, [cost], ' cost = ')

def define_cost_func_with_loop(X1, X2, L, a, b, c, n_sample):
    # this is suffering from overflow too
    H = tf.sigmoid(X1 * a + X2 *b  + c)
    i = tf.constant(0)
    ta = tf.TensorArray(dtype=tf.float32, size=n_sample)
    c = lambda i, _: i < n_sample 
    b = lambda i, ta: (i + 1, ta.write(i, H[i] if L[i] == 1 else 1 - H[i]))
    i, ta = tf.while_loop(c, b, (i, ta))
    hh = ta.stack()
    ph = tf.Print(hh, [hh], ' class score = ')
    lh = tf.log(ph)

    i = tf.constant(0)
    ta = tf.TensorArray(dtype=tf.float32, size=n_sample)
    c = lambda i, _: i < n_sample 
    b = lambda i, ta: (i + 1, ta.write(i, tf.cond(lh[i] >= -10000, lambda: lh[i], lambda:-10000.0)))
    i, ta = tf.while_loop(c, b, (i, ta))
    lh = ta.stack()

    lph = tf.Print(lh, [lh], ' log class score = ')
    cost = 0 - tf.reduce_sum(lph) / n_sample 
    return cost

def svm_hinge_loss(X1, X2, L, a, b, c, n_sample):
    # TODO: implement SVM hinge loss function
    # which make sure that score of correct class is at least delta more than wrong class
    # otherwise, accumulate loss
    # .however, we would need another set of a2, b2, c2 for the negative class
    # since it no longer has the statistic implication
    pass


def define_optimizer(l_rate, cost_func):
    # Define optimizer and initializer
    optimizer = tf.train.GradientDescentOptimizer(l_rate).minimize(cost_func)
    initializer = tf.global_variables_initializer()
    return optimizer, initializer

# Step 1: Generate and visualize training data
n_sample = 30

x_train, x_test, label_train, label_test = generate_data(3, 5, 4, 4, n_sample)
n_train_size = label_train.shape[0]

visualize_data(x_train, label_train, "Data train raw")

# Step 1b: Normalize Xs and re-visualize training data
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# test_data_range(x_train[:, 0], x_train[:, 1])
# exit(0)

visualize_data(x_train, label_train, "Data train scaled")
visualize_data(x_test, label_test, "Data test scaled")

# Step 2: Initialize Placeholders for input data
X1 = tf.placeholder(np.float32)
X2 = tf.placeholder(np.float32)
L = tf.placeholder(np.float32)

### Step 3: Build up your first model: LOGISTIC REGRESSOR
a, b, c = define_parameters()
# cost = define_cost_func_with_builtin(X1, X2, L, a, b, c, n_train_size)
# print ('X shape = ', x_train.shape)
# print ('label shape = ', label_train.shape)
cost = define_cost_func_with_workedout_equation_v2(X1, X2, L, a, b, c, n_train_size)
# cost = define_cost_func_with_loop(X1, X2, L, a, b, c, n_train_size)
# Step 4: Create optimizer
l_rate = 0.5
optimizer, initializer = define_optimizer(l_rate, cost)
sess = tf.Session()
# sess = tf_debug.LocalCLIDebugWrapperSession(sess)
with sess:
    # sess.add_tensor_filter("has_inf_or_nan", tf_debug.has_inf_or_nan)
    sess.run(initializer)
    for i in range(200):
        _, train_cost = sess.run([optimizer, cost], feed_dict={X1: x_train[:, 0], X2: x_train[:, 1], L: label_train})
        print('train cost = ', train_cost)
        a_op = sess.run(a)
        b_op = sess.run(b)
        c_op = sess.run(c)
        print ('a = ', a_op, ' b = ', b_op, ' c = ', c_op)
        draw_model(a_op, b_op, c_op)
        if i % 20 == 0 or i == 99:
            visualize_data(x_train, label_train,"Step {}, loss = {:.4f}".format(i, train_cost))

    test_cost = sess.run(cost, feed_dict={X1: x_test[:, 0], X2: x_test[:, 1], L: label_test})
    print('Optimized variable: a_op = ', a_op)
    print('Optimized variable: b_op = ', b_op)
    print('Optimized variable: c_op = ', c_op)
    draw_model(a_op, b_op, c_op)
    visualize_data(x_test, label_test, "Final prediction cost {:.4f}".format(test_cost))