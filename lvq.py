#!/usr/bin/python
# vim: set cc=80:

import os, sys
import yaml, tarfile
import datetime


# Use numpy and matices to speed up the processing
import numpy as np

from lib import utils
from lib.lvq.distance import DistanceFunction
from lib.lvq.weight_init import WeightInitFunction

class LVQ:
    def __init__(self, input_size, output_size, eta=0.1, prototypes_per_class=1,
            dist_function='euclidean', init_function='average', verbose=3):
        """
        """
        self.input_size  = input_size
        self.output_size = output_size
        self.ppc         = prototypes_per_class

        self.distance    = DistanceFunction(func=dist_function)
        self.weight_init = WeightInitFunction(func=init_function)
        self.weights     = None
        self.verbose     = verbose

        self.init = False
        self.eta  = eta


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


    def save(self, filename):
        """Save the current state of the Network to a YAML file.
        YAML format is convenient since it has no dependency on
        python and can be edited by hand.
        If the filename has a '.gz' extension, it will be compressed
        automatically"""
        data = {
                "input_size"  : self.input_size,
                "output_size" : self.output_size,
                "ppc"         : self.ppc,

                "distance"    : self.distance.type,
                "weight_init" : self.weight_init.type,

                "init"        : self.init,
                "eta"         : self.eta,

                "weights"     : self.weights,
                }

        if filename.endswith('.gz'):
            with tarfile.open(filename, 'w:gz') as tar:
                tmp = filename.split('.gz')[0]
                with open(tmp, 'wb') as f:
                    f.write('# vim: set ft=yaml:\n')
                    yaml.dump(data, f)
                    tar.add(tmp)
                    os.remove(tmp)
        else:
            with open(filename, 'wb') as f:
                f.write('# vim: set ft=yaml:\n')
                yaml.dump(data, f)



    def _load_file(self, f):
        data = yaml.load(f)

        self.input_size     = data['input_size']
        self.output_size    = data['output_size']
        self.ppc            = data['ppc']


        self.distance       = DistanceFunction(func=data['distance'])
        self.weight_init    = WeightInitFunction(func=data['weight_init'])
        self.weights        = [ np.array(w) for w in data['weights'] ]

        self.init           = data['init']
        self.eta            = data['eta']


    def load(self, filename):
        """Load a Network configuration from a YAML file."""
        if filename.endswith('.gz'):
            with tarfile.open(filename, 'r:gz') as tar:
                # NOTE: this only uses the first file of the archive!
                f = tar.extractfile(tar.getmembers()[0])
                self._load_file(f)
        else:
            with open(filename, 'rb') as f:
                    self._load_file(f)



    def train(self, tr_d, eta, epochs, eta_decay=False, va_d=None, estop=True):
        if not self.init:
            self.weights = self.weight_init(self.input_size, self.output_size,
                    self.ppc, tr_d)
            self.init = True

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
                self.log(1, " * eta                       : {:.3}".format(eta))
                # Compute optimized learning rate
                eta = eta / (1 + s * eta) if eta < 1.0 else 1.0

            tr_err.append(self.eval_error_rate(tr_d))
            self.log(2, " * Training set error rate   : {:.3%}"\
                    .format(tr_err[-1]))

            # Validation
            if va_d:
                va_err.append(self.eval_error_rate(va_d))
                self.log(2, " * Validation set error rate : {:.3%}"\
                .format(va_err[-1]))
                # Stop early if validation error is very low
                if estop and va_err[-1] < 0.01: break

        self.learn_time = datetime.datetime.now() - self.learn_time
        self.eta        = eta

        return tr_err, va_err



    def feedforward(self, x):
        d = []
        for w in self.weights:
            # Compute distances
            d.append(self.distance(x, w))
        # find closest centroid
        return np.argmin(d)%self.output_size



    def get_confusion(self, data):
        """Generate a confusion matrix on a given dataset. """
        dim = self.output_size
        mat = np.zeros(shape=(dim,dim))
        for (x, y) in data:
            a = self.feedforward(x)
            mat[y][a] += 1.0

        return mat



    def eval_accuracy(self, data):
        """Evaluate accuracy on a given dataset. """
        count = 0
        for (x, y) in data:
            if self.feedforward(x) == y: count += 1
        return count



    def eval_error_rate(self, data):
        """Evaluate error rate on a given dataset. """
        return 1.0 - float(self.eval_accuracy(data)) / len(data)


