"""
The code associated with the Neural Network and the model created.
"""

import tensorflow as tf

def genModel(name, s='w'):
    if s == 'w':
        k = 1
    else:
        k = 0
    lS = [40, 30, 20]
    x = tf.placeholder(tf.float32, [None, 29+k])
    W1 = tf.Variable(tf.zeros([29+k, lS[0]]))
    b1 = tf.Variable(tf.zeros([lS[0]]))
    l1 = tf.nn.softmax(tf.matmul(x, W1) + b1)
    W2 = tf.Variable(tf.zeros([lS[0], lS[1]]))
    b2 = tf.Variable(tf.zeros([lS[1]]))
    l2 = tf.nn.softmax(tf.matmul(l1, W2) + b2)
    W3 = tf.Variable(tf.zeros([lS[1], lS[2]]))
    b3 = tf.Variable(tf.zeros([lS[2]]))
    l3 = tf.nn.softmax(tf.matmul(l2, W3) + b3)
    W4 = tf.Variable(tf.zeros([lS[2], 1]))
    b4 = tf.Variable(tf.zeros([1]))
    y = tf.nn.softmax(tf.matmul(l3, W4) + b4)
    y_ = tf.placeholder(tf.float32, [None, 1])
    cross_entropy = tf.reduce_mean(tf.square(tf.subtract(y, y_)))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)
    dat = [[float(y) for y in x.split(', ')] for x in open('/home/jonathan/Desktop/AIMarket/TrainingData/E6Train.csv').read().split('\n')][:950000]
    datx = [x[:-(2-k)] for x in dat]
    daty = [[y[-(2-k)]] for y in dat]
    for i in range(9500):
        batchx = datx[100*i:100*i+100]
        batchy = daty[100*i:100*i+100]
        sess.run(train_step, feed_dict = {x: batchx, y_: batchy})
    predQuality = tf.abs(tf.subtract(y, y_))
    accuracy = tf.reduce_mean(predQuality)
    dat = [[float(y) for y in x.split(', ')] for x in open('/home/jonathan/Desktop/AIMarket/TrainingData/E6Train.csv').read().split('\n')][950000:]
    datx = [x[:-(2-k)] for x in dat]
    daty = [[y[-(2-k)]] for y in dat]
    print(sess.run(accuracy, feed_dict = {x: batchx, y_: batchy}))
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    save_path = saver.save(sess, "/home/jonathan/Desktop/AIMarket/" + name + ".ckpt")
    print("Save successful")
    
def getPreds(name, vals):
    with tf.Session() as sess:
        new_saver = tf.train.import_meta_graph("/home/jonathan/Desktop/AIMarket/" + name + ".ckpt.meta")
        new_saver.restore(sess, tf.train.latest_checkpoint('./'))
        feed_dict = {x:vals}
        return(sess.run(y, feed_dict))