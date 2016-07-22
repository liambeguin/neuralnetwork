#!/usr/bin/python
# vim: cc=80:
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
    # NOTE: in prime form, w is a single set of weights whereas in normal form,
    #       w is the whole list !!
    if prime:
        return (lambda_ / n) * w
    else:
        ret = np.sum([ np.sum(np.square(wi)) for wi in w ])
        return (lambda_ / (2 * n)) * ret


def l1_reg(w, lambda_, n, prime=False):
    if prime:
        return (lambda_ / n) * np.sign(w)
    else:
        return (lambda_ / n) * np.sum(np.absolute(w))


class RegularizationFunction():

    available_functions = {
            'none': noreg,
            'L1': l1_reg,
            'L2': weightdecay,
            'weight-decay': weightdecay,
            }

    def __init__(self, func='none', lambda_=0.0):
        self.function = RegularizationFunction.available_functions[func]
        self.type     = func
        self.lambda_  = lambda_

    def __call__(self, w, n):
        return self.function(w, self.lambda_, n, prime=False)

    def derivative(self, w, n):
        return self.function(w, self.lambda_, n, prime=True)
