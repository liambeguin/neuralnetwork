#!/usr/bin/python
# vim: cc=80:
"""
Regularisation techniques are used to reduce overfitting.
"""

import numpy as np

def noreg(w, lambda_, prime=False):
    return 0


def weightdecay(w, lambda_, prime=False):
    """L2 is used to make it so the network prefers to learn small weights.

    The relative importance of this to the rest of the cost function depends on
    the value of lambda_. A small value will give more importance to a smaller
    original cost and a large value will give more importance to small weights"""
    if prime:
        return (lambda_ / len(w)) * w
    else:
        return (lambda_ / (2 * len(w))) * np.sum(np.square(w))


def l1_reg(w, lambda_, prime=False):
    if prime:
        return (lambda_ / len(w)) * np.sign(w)
    else:
        return (lambda_ / len(w)) * np.sum(np.absolute(w))


class RegularizationFunction():

    available_functions = {
            'L1': l1_reg,
            'none': noreg,
            'weight-decay': weightdecay,
            'L2': weightdecay,
            }

    def __init__(self, func='none', lambda_=0.0):
        self.function = RegularizationFunction.available_functions[func]
        self.type     = func
        self.lambda_  = lambda_

    def __call__(self, w):
        return self.function(w, self.lambda_, prime=False)

    def derivative(self, w):
        return self.function(w, self.lambda_, prime=True)
