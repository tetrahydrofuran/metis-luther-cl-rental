import tensorflow as tf

def model(X, w, b):
    return tf.matmul(X, w) + b


X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)
w = tf.Variable()
b = tf.Variable()
y_model = model(X, w, b)

cost = tf.square(Y-y_model)
train_op = tf.train.GradientDescentOptimizer(0.01).minimize(cost)

with tf.Session() as sess:
    tf.global_variables_initializer().run()
    for i in range(100):
        for (x, y) in zip(trX, trY):
            sess.run(train_op, feed_dict={X: x, Y: y})
        print(sess.run(w))