#!/usr/bin/python


import numpy as np

def sigmoid(z, prime=False):
    if prime:
        return sigmoid(z)*(1-sigmoid(z))
    else:
        return 1.0 / (1.0 + np.exp(-z))

def tanh(z, prime=False):
    if prime:
        return 1.0/(np.cosh(z)**2)
    else:
        return np.tanh(z)


# Activation functions
class ActivationFunction():
    activation_functions = {
            'sigmoid' : sigmoid,
            'tanh'    : tanh
            }
    def __init__(self,func='sigmoid'):
        self.function = activation_functions[func]
        self.type = func

    def __call__(self, z):
        return self.function(z)

    def derivative(self, z):
        return self.function(z, prime=True)


