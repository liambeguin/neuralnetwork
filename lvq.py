#!/usr/bin/python
# vim: set cc=80:

import os, sys
import yaml, tarfile
import datetime


# Use numpy and matices to speed up the processing
import numpy as np

from lib import utils


class LVQ:
    def __init__(self, input_size, output_size, verbose=3):
        """
        """
        self.input_size  = input_size
        self.output_size = output_size
        self.weights = [ np.zeros(shape=(input_size, 1)) ] * output_size
        self.init    = False


    def __repr__(self):
        ret  = "Learning Vector Quatizer:\n"
        ret += "N inputs    : {}\n".format(self.input_size)
        ret += "N outputs   : {}\n".format(self.output_size)
        ret += "initialized : {}\n".format(self.init)
        return ret


    def __call__(self,X):
        return self.feedforward(X)


    def verbose_level(self, level):
        self.verbose = level


    def log(self, lvl, msg):
        if lvl < self.verbose:
            print(msg)


    def init_weights(self, tr_d):
        if type(tr_d[0][1]) != int:
            # TODO: convert if it's not an int
            raise Exception("Output should be an int !")

        np.random.shuffle(tr_d)
        self.tr_dX = []
        self.tr_dY = []
        for x, y in tr_d:
            self.tr_dX.append(x)
            self.tr_dY.append(y)

        self.tr_dX = np.array(self.tr_dX)
        self.tr_dY = np.array(self.tr_dY)

        for w_idx, w in enumerate(self.weights):
            match = np.where(self.tr_dY == w_idx)[0][0]
            self.weights[w_idx] = self.tr_dX[match]

        self.init = True



    def train(self, tr_d, eta, epochs, va_d=None):
        if not self.init:
            self.init_weights(tr_d)

        self.learn_time = datetime.datetime.now()
        for _ in xrange(0, epochs):
            for x, y in tr_d:
                d = []
                for w in self.weights:
                    # Compute distances
                    dist = np.linalg.norm(x - w)
                    d.append(dist)

                # find closest centroid
                bmu = np.argmin(d)

                # Update closest weight: Best Matching Unit
                self.weights[bmu] += eta * (x - self.weights[bmu])

        self.learn_time = datetime.datetime.now() - self.learn_time



    def feedforward(self, X):
        ret = []
        # if X[0][0].shape != self.weights[0].shape:
        #     # NOTE: handle single inputs as well as array inputs
        #     X = [X]

        for x in X:
            d = []
            for w in self.weights:
                # Compute distances
                dist = np.linalg.norm(x - w)
                d.append(dist)

            # find closest centroid
            ret.append(np.argmin(d))
        return ret




if  __name__ == "__main__":

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    tr_d = [
        (np.array([[1.0], [4.0], [2.0]]), 0),
        (np.array([[2.0], [4.0], [2.0]]), 0),
        (np.array([[1.0], [5.0], [1.0]]), 0),
        (np.array([[2.0], [5.0], [0.0]]), 0),
        (np.array([[3.0], [5.0], [0.0]]), 0),

        (np.array([[4.0], [1.0], [2.0]]), 1),
        (np.array([[4.0], [2.0], [3.0]]), 1),
        (np.array([[5.0], [1.0], [1.0]]), 1),
        (np.array([[5.0], [2.0], [0.0]]), 1),
        (np.array([[5.0], [3.0], [1.0]]), 1),
        ]

    # te_d = [
    #     (np.array([[1.0], [6.0], [1.0]]), 0),
    #     (np.array([[4.0], [1.0], [6.0]]), 1),
    #     ]

    te_d = [
        np.array([[1.0], [6.0], [1.0]]),
        np.array([[4.0], [1.0], [6.0]]),
        ]
    eta = 0.1

    lvq = LVQ(3, 2)
    print lvq

    print lvq.weights

    lvq.init_weights(tr_d)
    print lvq.weights

    lvq.train(tr_d, eta, 1000)
    print lvq.weights

    print "******************"
    print te_d
    yhat = lvq(te_d)
    print "******************"
    print yhat

    # TODO: fix this graph to work with new format
    # for x, y in zip(te_d[:,0], yhat):
    #     if y < 1:
    #         ax.scatter(x[0], x[1], x[2], marker='x', c='b')
    #     else:
    #         ax.scatter(x[0], x[1], x[2], marker='x', c='g')
    #
    # for x, y in tr_d:
    #     if y < 1:
    #         ax.scatter(x[0], x[1], x[2], c='b')
    #     else:
    #         ax.scatter(x[0], x[1], x[2], c='g')
    #
    # for w in lvq.weights:
    #     ax.scatter(w[0], w[1], w[2], marker='^', c='r')
    # plt.show()
    # plt.savefig("lvq.png")

