#!/usr/bin/python

import os, fnmatch

import numpy as np

import preprocessing as prep

def vectorize_output(n, size=(9, 1)):
    v =  np.zeros(size)
    v[n] = 1.0
    return v


def extract_datasets(basename='', size=60, out_size=10):
    tr_d = _extract(basename + 'train', size=size, vectorize=True, out_size=out_size)
    va_d = _extract(basename + 'validation', size, out_size=out_size)
    te_d = _extract(basename + 'test', size=size, out_size=out_size)

    print "Training samples   (N): {}".format(len(tr_d))
    print "Validation samples (K): {}".format(len(va_d))
    print "Testing samples       : {}".format(len(te_d))
    print "Input shape : {}x{} -> (1, {})".format(size, len(tr_d[0][0])/size, len(tr_d[0][0]))
    print

    return tr_d, va_d, te_d


def _extract(dirname='train', size=60, vectorize=False, out_size=10):
    """Takes a folder containing training data and returns a
    list of tuples (input, output)"""
    dataset = []
    for num in xrange(1, out_size+1):
        for file_ in get_filelist(dirname, num):
            x = prep.Preprocessing(file_, size)
            x.start_point_detection(threshold=0.5, n=10)
            x.cut_first_max(n=20)
            x.only_static_data()
            x.normalize()
            x.fit()
            # make a column of the whole array
            input_ = x.data.reshape((len(x.data)*len(x.data[0]), 1) )

            if vectorize:
                dataset.append( (input_, vectorize_output(num-1)) )
            else:
                dataset.append( (input_, num) )

    return dataset



def inspect_dataset(dataset, size=60):
    print "-- Dataset inspection --"
    print "size : {}".format(len(dataset))
    print "input  shape: {}".format(dataset[0][0].shape)
    if isinstance(dataset[0][1], np.ndarray):
        print "output shape: {}".format(dataset[0][1].shape)
    else:
        print "output shape: {}".format(type(dataset[0][1]))

    print "input type: {}".format(type(dataset[0][0]))



def get_filelist(input_dir, number):
    """ Returns a list of files  for a given number."""

    pattern = str(number) + '*'
    fileList = []

    for dName, sdName, fList in os.walk(input_dir):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, pattern):
                fileList.append(os.path.join(dName, fileName))

    return fileList


def inspect_network(network, full=False):
    # n -1 because input layer does not count
    print "Number of layers : ", network.n_layers - 1

    print "-- Input Layer --"
    print network.struct[0], " Neurons"

    if network.n_layers > 2:
        for idx, val in enumerate(network.struct[1:-1]):
            print "-- Hidden Layer %d --" % (idx +1)
            print val, " Neurons"
            if full :
                print "weights:"
                print network.weights[idx]

    print " -- Output Layer --"
    print network.struct[-1], " Neurons"
    if full :
        print "weights:"
        print network.weights[-1]


LOGLEVEL = 0
def set_level(lvl):
    LOGLEVEL = lvl

def log_print(lvl, msg):
    if lvl > LOGLEVEL:
        print "{}".format(msg)

