#!/usr/bin/python
# vim: set cc=80:

import os
import yaml, tarfile
import random
import datetime
import logging
# this is not very pretty but meh..
logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)


# Use numpy and matices to speed up the processing
import numpy as np

from lib.regularization import RegularizationFunction
from lib.activation import ActivationFunction
from lib.cost import CostFunction
from lib import utils

# NOTE: This allows us to always use the same random numbers. used for debug
# np.random.seed(1)


class Network:
    options = {}
    options['cost'] = CostFunction.available_functions.keys()
    options['activation'] = ActivationFunction.available_functions.keys()
    options['regularization'] = RegularizationFunction.available_functions.keys()

    def __init__(self, struct, \
            activation='sigmoid', cost='quadratic', regularization='none', \
            learning_rate=3.0, lambda_=0.1,
            verbose=3):
        """Generate a neural network based on a tuple of integers.
        ex: (2, 3, 1)
        this will generate a 2 layer network with 2 input, 3 neurons on the
        hidden layer and one output.

        The input is assumed to be a (n, 1) array where n is the number of
        inputs of the network

        notation:
        we'll use w^(l)_{jk} to denote the weight of the connection from
        the k^{th} neuron in the (l-1)^{th} layer to the j^{th} neuron in
        the l^{th} layer.

        parameters:
         * activation     : type of activation function,
         * cost           : type of cost function,
         * regularization : type of regularization function,
         * learning_rate  : \eta, learning rate parameter,
         * lambda_        : \lambda, regularization parameter.
         * verbose        : Verbose level.
        """

        if cost == 'cross-entropy' and activation != 'sigmoid':
            raise Exception("cross-entropy can only be used with" +
            " a sigmoid activation")

        self.n_layers = len(struct)
        self.struct   = struct
        self.verbose  = verbose

        self.lambda_ = lambda_
        self.eta     = learning_rate

        self.regularization = RegularizationFunction(func=regularization, lambda_=lambda_)
        self.activation     = ActivationFunction(func=activation)
        self.cost           = CostFunction(func=cost)

        self.a = [ np.random.randn(layer,1) for layer in struct ]
        self.z = [ np.random.randn(layer,1) for layer in struct ]

        self.biases  = [ np.random.randn(y, 1) for y in struct[1:] ]
        self.weights = [ np.random.randn(y, x) / np.sqrt(x) \
                        for x, y in zip(struct[:-1], struct[1:]) ]


    def __repr__(self):
        """Returns a representation of the Network."""
        ret  = "Neural Network      : {}\n".format(self.struct)
        ret += "Activation function : {}\n".format(self.activation.type)
        ret += "Cost function       : {}\n".format(self.cost.type)
        ret += "Regularization func : {}\n".format(self.regularization.type)
        ret += "learning rate       : {}\n".format(self.eta)
        ret += "Regularization rate : {}\n\n".format(self.lambda_)
        if max(self.struct) <= 35:
            for idx, val in enumerate(self.struct):
                ret += 'L{:>0{n}} {:^{num}}\n'.format(str(idx), \
                        '* '*val, n=len(str(len(self.struct))), \
                        num=2*max(self.struct))
        return ret


    def __call__(self, X):
        """Propagate input data through the network."""
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
                "struct"         : self.struct,
                "eta"            : self.eta,
                "lambda"         : self.lambda_,

                "cost"           : self.cost.type,
                "activation"     : self.activation.type,
                "regularization" : self.regularization.type,

                "weights"        : [ w.tolist() for w in self.weights ],
                "biases"         : [ b.tolist() for b in self.biases  ],
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

        self.struct         = data['struct']
        self.eta            = data['eta']
        self.lambda_        = data['lambda']

        self.cost           = CostFunction(func=data['cost'])
        self.activation     = ActivationFunction(func=data['activation'])
        self.regularization = RegularizationFunction(
                func=data['regularization'],
                lambda_=self.lambda_)

        self.biases  = [ np.array(b) for b in data['biases']  ]
        self.weights = [ np.array(w) for w in data['weights'] ]


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


    def feedforward(self, X):
        """Propagate input data through the network and store z and a values."""
        act = X
        z_list = []
        a_list = [act]

        for (b, w) in zip(self.biases, self.weights):
            z = np.dot(w, act) + b
            z_list.append(z)
            act = self.activation(z)
            a_list.append(act)

        self.a = a_list
        self.z = z_list
        return self.a[-1]


    def train(self, tr_d, epochs, batch_size, \
            va_d=None, early_stop_n=None, \
            monitoring={'error':True, 'cost':True}):
        """Train the network using mini-batch stochastic gradient descent.

        As opposed to batch gradient descent, stochastic gradient descent
        uses a single sample of the training set (selected at random!) to
        compute the gradient. Since the expected value of a single random
        pick is close to the actual value, this allows us to speed up the
        whole process while not loosing in precision.
        The mini-batch version allows us to seedup a little more by taking
        advantage of large martix calculation modules available with python.
        Instead of computing the gradient N times on a single sample, we
        compute it (N/batch_size) times on a matrix of N samples.
        Note that if batch_size=1, this performs a regular SGD.

        Parameters:
         * tr_d         : Training set to be used,
         * epochs       : Maximum number of epochs,
         * batch_size   : Size of the mini-batch
         * va_d         : Validation set,
         * early_stop_n : number of epochs to consider for early stopping,
         * monitoring   : dict of what to monitor.
        """

        tr_err, tr_cost = [], []
        va_err, va_cost = [], []

        self.learn_time = datetime.datetime.now()

        for i in xrange(epochs):
            # Select a random mini batch in the training dataset
            random.shuffle(tr_d)

            # NOTE: `zip(*[iter(tr_d)]*batch_size)` is used to cut
            #       tr_d into n batch_size elements.
            for mini_batch in zip(*[iter(tr_d)]*batch_size):
                # Create copies of the weights and biases and init to 0.
                nabla_bC = np.multiply(np.array(self.biases,  copy=True), 0)
                nabla_wC = np.multiply(np.array(self.weights, copy=True), 0)

                for x, y in mini_batch:
                    # Sum all the gradients over the mini-batch
                    self.feedforward(x)
                    nabla_bC_i, nabla_wC_i = self.backpropagation(y)
                    nabla_bC = np.add(nabla_bC, nabla_bC_i)
                    nabla_wC = np.add(nabla_wC, nabla_wC_i)

                # Update weights and biases
                # NOTE: the weights and biases should be averaged over the size
                #       of the mini-batch here but since it is done in the cost
                #       function so there is no need for it.
                self.biases  = [ b - self.eta * nb \
                        for b, nb in zip(self.biases, nabla_bC) ]
                self.weights = [ w - self.eta * (nw + \
                    self.regularization.derivative(w) ) \
                        for w, nw in zip(self.weights, nabla_wC) ]

            self.log(1, "Epoch {:2d} training done.".format(i) )

            self.log(2, " * Training   set accuracy   : {}/{}".format( \
                    self.eval_accuracy(tr_d), len(tr_d)) )
            self.log(2, " * Validation set accuracy   : {}/{}".format( \
                    self.eval_accuracy(va_d), len(va_d)) )

            if monitoring['error']:
                self.log(2, " * Training   set error rate : {:.3%}"\
                        .format(self.eval_error_rate(tr_d)) )
                tr_err.append(self.eval_error_rate(tr_d))
                if va_d:
                    error_rate = self.eval_error_rate(va_d)
                    self.log(2, " * Validation set error rate : {:.3%}"\
                            .format(error_rate) )
                    va_err.append(error_rate)

            if monitoring['cost']:
                self.log(2, " * Training   set cost       : {}"\
                        .format(self.eval_cost(tr_d)) )
                tr_cost.append(self.eval_cost(tr_d))
                if va_d:
                    self.log(2, " * Validation set cost       : {}"\
                            .format(self.eval_cost(va_d)) )
                    va_cost.append(self.eval_cost(va_d))

            # If we do not improve, stop training !
            if self.eval_error_rate(va_d) < 0.01 or \
                    early_stop_n and i > early_stop_n and \
                    error_rate - np.mean(va_err[-early_stop_n:]) < 0.05:
                        break

            # Print empty line if monitoring for easy reading
            if monitoring:
                self.log(2, "")

        self.learn_time = datetime.datetime.now() - self.learn_time
        return tr_err, tr_cost, va_err, va_cost


    # TODO: transform this so that it works with a matrix and not just a vector
    #       this would be a little more efficient since it takes advantage full
    #       advantage of numpy.
    def backpropagation(self, y):
        """Backpropagate the errors through the Network.

        This returns a tuple of matrices of derivatives of the cost function
        with respect to biases and weights.
        Here, nabla_wC is used to refer to dC/dW, the derivative of the cost
        function with respect to the weights (same for nabla_bC).

        ref: https://en.wikipedia.org/wiki/Matrix_calculus

        Parameters:
         * y : vector of labels
        """
        # Create copies of the weights and biases and init to 0.
        nabla_bC = np.multiply(np.array(self.biases,  copy=True), 0)
        nabla_wC = np.multiply(np.array(self.weights, copy=True), 0)

        # Before the for loop, delta = delta_L, the error on the last layer
        # NOTE: array[-1] refers to the last element.
        if self.cost.type == 'cross-entropy':
            # Since (for now?) this only works with sigmoid, remove act'
            delta = self.cost.derivative(self.a[-1], y)
        else:
            delta = self.cost.derivative(self.a[-1], y) * \
                    self.activation.derivative(self.z[-1])

        nabla_bC[-1] = delta
        nabla_wC[-1] = np.dot(delta, self.a[-2].transpose())

        # Compute delta vectors and derivatives starting from layer (L-1)
        for l in xrange(2, self.n_layers):
            delta = np.dot(self.weights[-l+1].transpose(), delta) * \
                    self.activation.derivative(self.z[-l])

            nabla_bC[-l] = delta
            nabla_wC[-l] = np.dot(delta, self.a[-l-1].transpose())

        return (nabla_bC, nabla_wC)


    def get_confusion(self, data):
        """Generate a confusion matrix on a given dataset. """
        dim, _ = data[0][1].shape
        mat = np.zeros(shape=(dim,dim))
        for (x, y) in data:
            a = np.argmax(self.feedforward(x))
            y = np.argmax(y)
            mat[y][a] += 1.0

        return mat

    def eval_accuracy(self, data):
        """Evaluate accuracy on a given dataset. """
        count = 0
        for (x, y) in data:
            # Since y is a vector get the index of it's max
            # this assumes a one-hot vector !!
            if np.argmax(self.feedforward(x)) == np.argmax(y):
                count += 1

        return count


    def eval_error_rate(self, data):
        """Evaluate error rate on a given dataset. """
        return 1.0 - float(self.eval_accuracy(data)) / len(data)


    def eval_cost(self, data):
        """Evaluate cost on a given dataset. """
        # Compute C0, the cost function alone
        total_cost = np.sum([ self.cost(self.feedforward(x), y) for (x, y) in data ])
        # Add \Omega(h), the regularization term
        total_cost += np.sum([ self.regularization(w) for w in self.weights ])

        return total_cost







