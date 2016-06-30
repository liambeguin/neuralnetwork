#!/usr/bin/python
"""
Regularisation techniques are used to reduce overfitting.
"""

import numpy as np

def noreg(w, lambda_, n, prime=False):
    return 0


def weightdecay(w, lambda_, n, prime=False):
    """L2 is used to make it so the network prefers to learn small weights.

    The relative importance of this to the rest of the cost function depends on
    the value of lambda_. A small value will give more importance to a smaller
    original cost and a large value will give more importance to small weights"""
    if prime:
        return (lambda_ / n) * w
    else:
        return (lambda_ / (2 * n)) * np.square(np.linalg.norm(w))


def l1_reg(w, lambda_, n, prime=False):
    if prime:
        return (lambda_ / n) * np.sign(w)
    else:
        return (lambda_ / n) * np.sum(np.absolute(w))


class RegularizationFunction():

    regularization_functions = {
            'none': noreg,
            'L1': l1_reg,
            'L2': weightdecay,
            'weight-decay': weightdecay,
            }

    def __init__(self, func='none'):
        self.function = RegularizationFunction.regularization_functions[func]
        self.type = func

    def __call__(self, w, lambda_, n):
        return self.function(w, lambda_, n, prime=False)

    def derivative(self, w, lambda_, n):
        return self.function(w, lambda_, n, prime=True)
