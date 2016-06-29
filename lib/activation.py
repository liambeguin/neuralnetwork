#!/usr/bin/python


import numpy as np

def sigmoid(z, prime=False):
    if prime:
        return sigmoid(z)*(1-sigmoid(z))
    else:
        return 1.0 / (1.0 + np.exp(np.negative(np.clip(z, -50, 50))))

def tanh(z, prime=False):
    if prime:
        return 1.0 / np.square(np.cosh(z))
    else:
        return np.tanh(z)

activation_functions = {
        'sigmoid' : sigmoid,
        'tanh'    : tanh
        }

# Activation functions
class ActivationFunction():
    def __init__(self,func='sigmoid'):
        self.function = activation_functions[func]
        self.type = func

    def __call__(self, z):
        return self.function(z)

    def derivative(self, z):
        return self.function(z, prime=True)


