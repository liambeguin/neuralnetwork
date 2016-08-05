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

        va_err = []
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
                if bmu == y:
                    self.weights[bmu] += eta * (x - self.weights[bmu])
                else:
                    self.weights[bmu] -= eta * (x - self.weights[bmu])

            # Validation
            if va_d:
                va_err.append(self.eval_error_rate(va_d))

        self.learn_time = datetime.datetime.now() - self.learn_time
        return va_err



    def feedforward(self, x):
        d = []
        for w in self.weights:
            # Compute distances
            dist = np.linalg.norm(x - w)
            d.append(dist)
        # find closest centroid
        return np.argmin(d)



    def eval_accuracy(self, data):
        """Evaluate accuracy on a given dataset. """
        count = 0
        for (x, y) in data:
            if self.feedforward(x) == y:
                count += 1

        return count



    def eval_error_rate(self, data):
        """Evaluate error rate on a given dataset. """
        return 1.0 - float(self.eval_accuracy(data)) / len(data)


