#!/usr/bin/python

# use yaml to store configuration easily
import yaml
# Use numpy and matices to speed up the processing
import numpy as np
import random

from lib.activation import ActivationFunction
from lib.cost import CostFunction
from lib import utils




class Network:
    def __init__(self, struct, \
            activation='sigmoid', cost='quadratic', \
            learning_rate=3.0, momentum=0.5):
        """Generate the network's architecture based on a list.

        ex: [2, 3, 1]
        this will generate a 2 layer network with 2 input, 3 neurons on the
        hidden layer and one output.

        The input is assumed to be a (n, 1) array where n is the number of
        inputs of the network

        notation:
        we'll use w^l_{jk} to denote the weight of the connection from the k^th
        neuron in the (l-1)^th layer to the j^th neuron in the l^th layer
        """

        if cost == 'cross-entropy' and activation != 'sigmoid':
            raise Exception("cross-entropy can only be used with a sigmoid activation")

        self.n_layers = len(struct)
        self.struct = struct
        self.activation = ActivationFunction(func=activation)
        self.cost = CostFunction(func=cost)
        self.eta = learning_rate
        self.alpha = momentum

        self.a = [ np.random.randn(layer,1) for layer in struct ]
        self.z = [ np.random.randn(layer,1) for layer in struct ]

        self.biases  = [ np.random.randn(y, 1) for y in struct[1:] ]
        self.weights = [ np.random.randn(y, x) \
                        for x, y in zip(struct[:-1], struct[1:]) ]


    def feedforward(self, X):
        """Propagate input data through the network and store z and a values."""
        act = X
        z_list = []
        a_list = [act]

        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, act) + b
            z_list.append(z)
            act = self.activation(z)
            a_list.append(act)

        self.a = a_list
        self.z = z_list
        return self.a[-1]


    # if batch_size is 1 this is called online learning
    def train(self, training_dataset, epochs, batch_size, test_data=None):
        """Train the network using stichastic gradient descent."""
        for i in xrange(epochs):
            # Select a random mini batch in the training dataset
            random.shuffle(training_dataset)

            for mini_batch in zip(*[iter(training_dataset)]*batch_size):
                nabla_b = [ np.zeros(b.shape) for b in self.biases  ]
                nabla_w = [ np.zeros(w.shape) for w in self.weights ]

                for x, y in mini_batch:
                    delta_nabla_b, delta_nabla_w = self.backpropagation(x, y)
                    nabla_b = [ nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b) ]
                    nabla_w = [ nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w) ]

                # Update weights
                self.biases  = [ b - (self.eta / len(mini_batch)) * nb \
                        for b, nb in zip(self.biases, nabla_b) ]
                self.weights = [ w - (self.eta / len(mini_batch)) * nw \
                        for w, nw in zip(self.weights, nabla_w) ]

            if test_data:
                print "Epoch {}: {} {}/{}".format(i, self.error_rate(test_data), \
                        self.evaluate(test_data), len(test_data))
            else:
                print "Epoch {}".format(i)


    def backpropagation(self, X, y):

        nabla_b = [ np.zeros(b.shape) for b in self.biases  ]
        nabla_w = [ np.zeros(w.shape) for w in self.weights ]

        self.feedforward(X)

        # Before the for loop, delta = delta_L
        if self.cost.type == 'cross-entropy':
            delta = self.cost.derivative(self.a[-1], y)
        else:
            delta = self.cost.derivative(self.a[-1], y) * \
                    self.activation.derivative(self.z[-1])

        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, self.a[-2].transpose())

        # l goes through layers from the end
        for l in xrange(2, self.n_layers):
            delta = np.dot(self.weights[-l+1].transpose(), delta) * \
                    self.activation.derivative(self.z[-l])

            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, self.a[-l-1].transpose())

        return (nabla_b, nabla_w)


    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)


    def error_rate(self, test_data):
        """Returns the error rate of the network while using a given set of
        weights and biases.

        Note: the network's output is assumed to be the neuron with the highest
        activation. """
        test_results = [ (np.argmax(self.feedforward(x)), y) \
                for (x, y) in test_data ]

        return 100 * (1 - (float(sum(int(x == y) \
                for (x, y) in test_results)) / len(test_results)))




# vim: set cc=80:
