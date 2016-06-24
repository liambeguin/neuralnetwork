#!/usr/bin/python

# use yaml to store configuration easily
import yaml
# Use numpy and matices to speed up the processing
import numpy as np



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







if __name__ == "__main__":

    # training set
    i = [[3,5], [5,1], [10,2]]

    a = Network([2, 3, 1])


# vim: set cc=80:
