#!/usr/bin/python
# vim: set cc=80:

import os, sys
import yaml, tarfile
import datetime


# Use numpy and matices to speed up the processing
import numpy as np

from lib import utils

def euclidean(x, w):
    return np.linalg.norm(x - w)

class DistanceFunction:
    available_functions = {'euclidean': euclidean,}

    def __init__(self, func='euclidian'):
        self.function = DistanceFunction.available_functions[func]
        self.type     = func

    def __call__(self, x, w):
        return self.function(x, w)




class LVQ:
    def __init__(self, input_size, output_size, prototypes_per_class=1,
            dist_function='euclidean', verbose=3):
        """
        """
        self.input_size  = input_size
        self.output_size = output_size
        self.ppc         = prototypes_per_class

        self.distance = DistanceFunction(func=dist_function)
        self.verbose  = verbose

        self.weights = [ np.zeros(shape=(input_size, 1)) ] * (output_size * self.ppc)
        self.init    = False


    def __repr__(self):
        ret  = "Learning Vector Quatizer:\n"
        ret += "initialized          : {}\n".format(self.init)
        ret += "N inputs             : {}\n".format(self.input_size)
        ret += "N outputs            : {}\n".format(self.output_size)
        ret += "Prototypes per class : {}\n".format(self.ppc)
        ret += "distance function    : {}\n".format(self.distance.type)
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
            match = np.where(self.tr_dY == w_idx%self.output_size)[0][0]
            self.weights[w_idx] = self.tr_dX[match]

        self.init = True



    def train(self, tr_d, eta, epochs, eta_decay=False, va_d=None):
        if not self.init:
            self.init_weights(tr_d)

        va_err, tr_err = [], []
        self.learn_time = datetime.datetime.now()
        for i in xrange(0, epochs):
            self.log(1, "Epoch {:2d} training done.".format(i) )
            for x, y in tr_d:
                d = []
                for w in self.weights:
                    # Compute distances
                    d.append(self.distance(x, w))

                # find closest centroid
                bmu = np.argmin(d)
                # Update closest weight: Best Matching Unit
                if bmu%self.output_size == y: s = 1
                else: s = -1
                self.weights[bmu] += s * eta * (x - self.weights[bmu])

            if eta_decay:
                self.log(1, " * eta = {}.".format(eta) )
                eta -= eta/100.0

            # Validation
            if va_d:
                va_err.append(self.eval_error_rate(va_d))
                self.log(2, " * Validation set error rate : {:.3%}"\
                .format(va_err[-1]))

        self.learn_time = datetime.datetime.now() - self.learn_time
        return tr_err, va_err



    def feedforward(self, x):
        d = []
        for w in self.weights:
            # Compute distances
            d.append(self.distance(x, w))
        # find closest centroid
        return np.argmin(d)



    def eval_accuracy(self, data):
        """Evaluate accuracy on a given dataset. """
        count = 0
        for (x, y) in data:
            if self.feedforward(x) == y: count += 1
        return count



    def eval_error_rate(self, data):
        """Evaluate error rate on a given dataset. """
        return 1.0 - float(self.eval_accuracy(data)) / len(data)


