#!/usr/bin/python
# vim: set cc=80:

import numpy as np

def euclidean(x, w):
    return np.linalg.norm(x - w)

class DistanceFunction:
    available_functions = {'euclidean': euclidean,}

    def __init__(self, func='euclidian'):
        self.function = DistanceFunction.available_functions[func]
        self.type     = func

    def __call__(self, x, w):
        return self.function(x, w)
