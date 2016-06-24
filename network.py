#!/usr/bin/python

# use yaml to store configuration easily
import yaml
# Use numpy and matices to speed up the processing
import numpy as np



# Activation functions
def sigmoid(z, prime=False):
    if prime:
        return np.exp(-z)/((1+np.exp(-z))**2)
    else:
        return 1.0 / (1.0 + np.exp(-z))

def tanh(s, prime=False):
    if prime:
        return 1.0/(np.cosh(z)**2)
    else:
        return np.tanh(z)



class Network:
    def __init__(self, struct, activation=sigmoid):
        """Generate the network's architecture based on a list.

        ex: [2, 3, 1]
        this will generate a 2 layer network with 2 input, 3 neurons on the
        hidden layer and one output.
        """
        self.n_layers = len(struct)
        self.struct = struct
        self.act = activation

        self.biases = [np.random.randn(y, 1) for y in struct[1:]]
        self.weights = [np.random.randn(x, y)
                        for x, y in zip(struct[:-1], struct[1:])]


    def feedforward(self, X):
        """Propagate input data through the network."""
        z = X
        for w in self.weights:
            z = self.act(np.dot(z, w))
        return z

    def cost_function(self, X, y):
        self.yHat = self.feedforward(X)
        J = 0.5 * sum((y-self.yHat)**2)
        return J


    def inspect(self):
        # n -1 because input layer does not count
        print "Number of layers : ", self.n_layers - 1

        print "-- Input Layer --"
        print self.struct[0], " Neurons"

        if self.n_layers > 2:
            for idx, val in enumerate(self.struct[1:-1]):
                print "-- Hidden Layer %d --" % (idx +1)
                print val, " Neurons"
                print "weights:"
                print self.weights[idx]

        print " -- Output Layer --"
        print self.struct[-1], " Neurons"
        print "weights:"
        print self.weights[-1]




if __name__ == "__main__":

    # training set
    i = [[3,5], [5,1], [10,2]]
    y = [75, 82, 93]
    y = np.multiply(y, 1.0/100)

    a = Network([2, 3, 1])
    yHat = a.feedforward(i)


# vim: set cc=80:
