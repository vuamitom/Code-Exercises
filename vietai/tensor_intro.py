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