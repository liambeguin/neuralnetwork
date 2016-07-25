#!/usr/bin/python
# vim: set cc=80:

import numpy as np

def quadratic(a, y, prime=False):
    if prime:
        return (1.0 / len(a)) * (a - y)
    else:
        return (np.linalg.norm(a-y)**2) / (2 * len(a))


def crossentropy(a, y, prime=False):
    if prime:
        return (1.0 / len(a)) * (a - y)
    else:
        return (-1.0 / len(a)) * np.sum(np.nan_to_num(y*np.log(a) + (1-y)*np.log(1-a)))

# TODO: Add log-likelihood to be used with softmax output layer
# This outputs a probability distribution


class CostFunction():

    available_functions = {
            'quadratic': quadratic,
            'cross-entropy': crossentropy
            }

    def __init__(self, func='quadratic'):
        self.function = CostFunction.available_functions[func]
        self.type = func

    def __call__(self, a, y):
        return self.function(a, y, prime=False)

    def derivative(self, a, y):
        return self.function(a, y, prime=True)
