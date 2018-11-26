import tensorflow as tf 
a = tf.constant(2)
b = tf.constant(3)


s = a + b 
print(s)

sess = tf.Session()
print(sess.run(s))


ph = tf.placeholder(tf.int32)
c = tf.constant(3)
s = ph + c 
print(sess.run(s, feed_dict={ph: 7}))
s = ph / c
print(s)

tf.InteractiveSession()

a = tf.zeros((2,2))
b = tf.ones((2,2))
print(tf.reduce_sum(b, reduction_indices = 1).eval())
print(a.get_shape())

print(tf.reshape(a, (1,4)).eval())

# tim gia tri nho nhat cua j(w) = w**2 - 10 * w + 25

w = tf.Variable(initial_value=0, dtype=tf.float32)
c = tf.placeholder(dtype=tf.float32, shape=(3,))

cost = w ** 2 * c[0] + w * c[1] + c[2]
train = tf.train.GradientDescentOptimizer(0.01).minimize(cost)

init = tf.global_variables_initializer()
sess.run(init)

for _ in range(1000):
    sess.run(train, feed_dict={c:[1,-1,25.]})

print(sess.run(w))
sess.close()