from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
import cv2
from dataset import DataSet

model_dir = './model'
tf.logging.set_verbosity(tf.logging.INFO)

class LeNet():
  def __init__(self, weights=None, sess=None, log=True):
    self.X = tf.placeholder(tf.float32, [None, 28, 28, 1], name='X')
    self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')
    self.log = log
    self.sess = sess

    self.conv_layers()
    self.fc_layers()

    self.probs = tf.nn.softmax(self.logits, name='softmax')

    if weights is not None and sess is not None:
      self.load_weights(weights, sess)

  def conv_layers(self):
    self.parameters = []
    images = self.X

    # Layer 1: Conv
    with tf.name_scope('conv1') as scope:
      kernel = tf.Variable(tf.random_normal([3, 3, 1, 32], dtype=tf.float32, stddev=1e-1, 
        name='weights'))
      conv = tf.nn.conv2d(images, kernel, [1, 1, 1, 1], padding='SAME')
      biases = tf.Variable(tf.constant(0.0, shape=[32], dtype=tf.float32),
        trainable=True, name='biases')
      out = tf.nn.bias_add(conv, biases)
      self.conv1 = tf.nn.relu(out, name=scope)
      self.parameters += [kernel, biases]

    # Layer 1: Pooling
    self.pool1 = tf.nn.max_pool(self.conv1,
      ksize=[1,2,2,1],
      strides=[1,2,2,1],
      padding='SAME',
      name='pool1')

    # Layer 2: Conv
    with tf.name_scope('conv2') as scope:
      kernel = tf.Variable(tf.random_normal([3, 3, 32, 64], dtype=tf.float32, stddev=1e-1, name='weights'))
      conv = tf.nn.conv2d(self.pool1, kernel, [1, 1, 1, 1], padding='SAME')
      biases = tf.Variable(tf.constant(0.0, shape=[64], dtype=tf.float32),
        trainable=True, name='biases')
      out = tf.nn.bias_add(conv, biases)
      self.conv2 = tf.nn.relu(out, name=scope)
      self.parameters += [kernel, biases]

    # Layer 2: Pooling
    self.pool2 = tf.nn.max_pool(self.conv2,
      ksize=[1,2,2,1],
      strides=[1,2,2,1],
      padding='SAME',
      name='pool2')

  def fc_layers(self):
    # fc1
    with tf.name_scope('fc1') as scope:
      shape = int(np.prod(self.pool2.get_shape()[1:]))
      fc1w = tf.Variable(tf.random_normal([shape, 128],
        dtype=tf.float32, stddev=1e-1), name='weights')
      fc1b = tf.Variable(tf.constant(1.0, shape=[128], dtype=tf.float32),
        trainable=True, name='biases')
      pool2_flat = tf.reshape(self.pool2, [-1, shape])
      fc1l = tf.nn.bias_add(tf.matmul(pool2_flat, fc1w), fc1b)
      self.fc1 = tf.nn.relu(fc1l)
      self.dropout1 = tf.nn.dropout(self.fc1, keep_prob=self.keep_prob, name='dropout1')
      self.parameters += [fc1w, fc1b]

    # fc2
    with tf.name_scope('fc2') as scope:
      fc2w = tf.Variable(tf.random_normal([128, 10],
        dtype=tf.float32, stddev=1e-1), name='weights')
      fc2b = tf.Variable(tf.constant(1.0, shape=[10], dtype=tf.float32),
        trainable=True, name='biases')
      fc2l = tf.nn.bias_add(tf.matmul(self.dropout1, fc2w), fc2b)
      self.logits = tf.nn.relu(fc2l)
      self.parameters += [fc2w, fc2b]

  def load_weights(weights, sess):
    None

  def train(self, learning_rate, training_epochs, batch_size, keep_prob):
    # Load dataset for training and testing
    self.dataset = DataSet()

    # Define size of output
    self.Y = tf.placeholder(tf.float32, [None, 10], name='Y')
    # Define cost function
    self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels=self.Y))
    # Define optimization method
    self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.cost)

    # Start logger
    if self.log:
        tf.summary.scalar('cost', self.cost)
        self.merged = tf.summary.merge_all()
        self.train_writer = tf.summary.FileWriter('./log_train', self.sess.graph)

    self.sess.run(tf.global_variables_initializer())
    self.sess.run(tf.local_variables_initializer())

    print('Training...')
    weights = []
    # For each epoch, feed training data and perform updating parameters
    for epoch in range(training_epochs):
        avg_cost = 0
        # Number of batches = size of training set / batch_size
        total_batch = int(self.dataset.get_train_set_size() / batch_size)

        # For each batch 
        for i in range(total_batch + 1):
            # Get next batch to feed to the network
            batch_xs, batch_ys = self.dataset.next_batch(batch_size)
            feed_dict = {
                self.X: batch_xs.reshape([batch_xs.shape[0], 28, 28, 1]),
                self.Y: batch_ys,
                self.keep_prob: keep_prob
            }

            weights, summary, c, _ = self.sess.run([self.parameters, self.merged, self.cost, self.optimizer],
                                                   feed_dict=feed_dict)
            avg_cost += c / total_batch

        if self.log:
            self.train_writer.add_summary(summary, epoch + 1)

        print('Epoch:', '%02d' % (epoch + 1), 'cost =', '{:.9f}'.format(avg_cost))

    print('Training finished!')

    saver = tf.train.Saver()
    save_path = saver.save(self.sess, model_dir + "/mnist_lenet.ckpt")
    print("Trainned model is saved in file: %s" % save_path)

  def evaluate(self, batch_size, keep_prob):

    self.correct_prediction = tf.equal(tf.argmax(self.logits, 1), tf.argmax(self.Y, 1))
    self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, tf.float32))

    N = self.dataset.get_test_set_size()
    print('test.size', N);
    correct_sample = 0
    for i in range(0, N, batch_size):
        batch_xs, batch_ys = self.dataset.next_batch_test(batch_size)

        N_batch = batch_xs.shape[0]

        feed_dict = {
            self.X: batch_xs.reshape([N_batch, 28, 28, 1]),
            self.Y: batch_ys,
            self.keep_prob: keep_prob
        }

        correct = self.sess.run(self.accuracy, feed_dict=feed_dict)
        correct_sample += correct * N_batch

    test_accuracy = correct_sample / N

    print("\nAccuracy Evaluates")
    print("-" * 30)
    print('Test Accuracy:', test_accuracy)

def main(unused_argv):
  tf.reset_default_graph()
  sess = tf.Session()
  lenet = LeNet(sess=sess, weights=None)

  lenet.train(learning_rate=0.001, training_epochs=40, batch_size=1000, keep_prob=0.7)
  lenet.evaluate(batch_size=1000, keep_prob=0.7)

if __name__ == "__main__":
  tf.app.run()
