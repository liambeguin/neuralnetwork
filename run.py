#!/usr/bin/python
# vim: cc=80:

import os
import numpy as np

import lvq
from lib import utils

autosave  = False
dosummary = True
# NOTE: the higher this is, the more the network will log information
#       0 - Print nothing
#       2 - Print epoch number
#       3 - Print epoch number and summary
net_verbose  = 2

evalsample         = True
sample_file        = 'test/woman/nh/5b.txt'
dataset_size       = 40
sex_classification = False



print(" ** Extracting dataset...")
training_data, validation_data, test_data = utils.extract_datasets(
        vectorize=False,
        size=dataset_size,
        sex=sex_classification,
        )

input_size  = len(training_data[0][0])
if sex_classification:
    output_size = 16
else:
    output_size = 8

print(" ** Initializing Network...")
lvq = lvq.LVQ(input_size, output_size)

if os.path.exists('autoload.save.gz'):
    print(" *** Found autoload, loading config...")
    # net.load('autoload.save.gz')

print(lvq)
print(" ** Starting training...")
lvq.train(training_data, 0.1, 200)

print
print
print
print(" ** Learned in : {} days, {} seconds and {} us".format(
    lvq.learn_time.days,
    lvq.learn_time.seconds,
    lvq.learn_time.microseconds,
    ))



if autosave:
    print(" ** Saving state of the Network...")
    # net.save('conf.save.gz')



if dosummary:
    print
    print " ** Summary : "



print(" ** Evaluating confusion on test dataset..")
# confusion = net.get_confusion(test_data)



if evalsample:
    print(" ** evaluate single input...")
    (feat, lab) = utils.extract_sample(
            sample_file,
            vectorize=False,
            size=dataset_size,
            sex=sex_classification)

    print "******************"
    yhat = lvq([feat])
    print "expected value : {}".format(lab)
    print "prediction     : {}".format(yhat)
    # print("    * prediction  : {}".format(utils.unpack_prediction(yhat)) )
    # print("    * actual value: {}".format(utils.unpack_prediction(lab)) )
    # print



print(" ** Done")
