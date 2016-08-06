#!/usr/bin/python
# vim: set cc=80:

import numpy as np

def random_weight_init(input_size, output_size, ppc, tr_d):
    """ select codebooks at random within the dataset """

    weights = [ np.zeros(shape=(input_size, 1)) ] * (output_size * ppc)

    np.random.shuffle(tr_d)
    tr_dX = []
    tr_dY = []
    for x, y in tr_d:
        tr_dX.append(x)
        tr_dY.append(y)

    tr_dX = np.array(tr_dX)
    tr_dY = np.array(tr_dY)

    for w_idx, w in enumerate(weights):
        match = np.where(tr_dY == w_idx%output_size)[0][0]
        weights[w_idx] = tr_dX[match]

    return weights



def average_weight_init(input_size, output_size, ppc, tr_d):
    """ init codebooks using the mean point """

    weights = [ np.zeros(shape=(input_size, 1)) ] * (output_size * ppc)

    np.random.shuffle(tr_d)
    tr_dX = []
    tr_dY = []
    for x, y in tr_d:
        tr_dX.append(x)
        tr_dY.append(y)

    tr_dX = np.array(tr_dX)
    tr_dY = np.array(tr_dY)

    for w_idx, w in enumerate(weights):
        match = np.where(tr_dY == w_idx%output_size)
        weights[w_idx] = np.mean(tr_dX[match], axis=0)

    return weights


class WeightInitFunction:
    available_functions = {
                           'random': random_weight_init,
                           'average': average_weight_init,
                          }

    def __init__(self, func='average'):
        self.function = WeightInitFunction.available_functions[func]
        self.type     = func

    def __call__(self, input_size, output_size, ppc, training_data):
        return self.function(input_size, output_size, ppc, training_data)




