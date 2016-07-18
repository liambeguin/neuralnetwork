#!/usr/bin/python


import numpy as np

def sigmoid(z, prime=False):
    if prime:
        return sigmoid(z)*(1-sigmoid(z))
    else:
        return 1.0 / (1.0 + np.exp(np.negative(np.clip(z, -50, 50))))

def tanh(z, prime=False):
    if prime:
        return 1.0 - np.square(tanh(z))
    else:
        return np.tanh(z)

def softplus(z, prime=False):
    """NOTE: this is a smoothed approximation of the ReLU
    activation function. It's easier to implement using
    numpy."""
    if prime:
        return sigmoid(z)
    else:
        return np.log(1 + np.exp(np.clip(z, -50, 50)))


# Activation functions
class ActivationFunction():

    activation_functions = {
            'sigmoid' : sigmoid,
            'tanh'    : tanh,
            'softplus': softplus,
            }

    def __init__(self,func='sigmoid'):
        self.function = ActivationFunction.activation_functions[func]
        self.type = func

    def __call__(self, z):
        return self.function(z)

    def derivative(self, z):
        return self.function(z, prime=True)


