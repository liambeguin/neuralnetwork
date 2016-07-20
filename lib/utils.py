#!/usr/bin/python
# vim: cc=80:

import os, fnmatch
import numpy as np

import preprocessing as prep



def vectorize_output(n, shape=(9, 1)):
    v =  np.zeros(shape)
    v[n] = 1.0
    return v



def extract_datasets(basename='', size=60, out_size=10, verbose=False):
    tr_d = _extract(basename + 'train',      size=size, out_size=out_size)
    va_d = _extract(basename + 'validation', size=size, out_size=out_size)
    te_d = _extract(basename + 'test',       size=size, out_size=out_size)

    if verbose:
        print(" *** Training")
        inspect_dataset(tr_d, size=size)
        print

        print(" *** Validation")
        inspect_dataset(va_d, size=size)
        print

        print(" *** Testing")
        inspect_dataset(te_d, size=size)
        print

    return tr_d, va_d, te_d



def _extract(dirname='train', size=60, out_size=9):
    """Takes a folder containing training data and returns a
    list of tuples (input, output)"""
    dataset = []
    for num in xrange(1, out_size+1):
        for file_ in get_filelist(dirname, num):
            x = prep.Preprocessing(file_, size)
            x.start_point_detection(threshold=0.5, n=10)
            x.cut_first_max(n=20)
            x.normalize()
            x.fit()
            x.get_subset('static')
            # make a column of the whole array
            input_ = x.data.reshape((len(x.data)*len(x.data[0]), 1) )

            dataset.append( (input_, vectorize_output(num-1, shape=(out_size, 1))) )

    return dataset



def inspect_dataset(dataset, size=60):
    print("    * size : {}".format(len(dataset)))
    print("    * input  shape: {} -> {}x{}".format(dataset[0][0].shape, dataset[0][0].shape[0]/size, size) )
    if isinstance(dataset[0][1], np.ndarray):
        print("    * output shape: {}".format(dataset[0][1].shape) )
    else:
        print("    * output shape: {}".format(type(dataset[0][1])) )

    print("    * input type: {}".format(type(dataset[0][0])) )



def get_filelist(input_dir, number):
    """ Returns a list of files  for a given number."""

    pattern = str(number) + '*'
    fileList = []

    for dName, sdName, fList in os.walk(input_dir):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, pattern):
                fileList.append(os.path.join(dName, fileName))

    return fileList



LOGLEVEL = 0
def set_level(lvl):
    LOGLEVEL = lvl

def log_print(lvl, msg):
    if lvl > LOGLEVEL:
        print("{}".format(msg))

