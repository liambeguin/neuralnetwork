#!/usr/bin/python

import numpy as np

def quadratic(a, y, prime=False):
    if prime:
        return (a - y)
    else:
        # TODO: replace this with numpy.linalg.norm
        return 0.5 * sum((a-y)**2)



cost_functions = {
        'quadratic' : quadratic
        }

class CostFunction():
    def __init__(self, func='quadratic'):
        self.function = cost_functions[func]

    def __call__(self, a, y):
        return self.function(a, y, prime=False)

    def derivative(self, a, y):
        return self.function(a, y, prime=True)
