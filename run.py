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
sex_classification = True



print(" ** Extracting dataset...")
training_data, validation_data, test_data = utils.extract_datasets(
        vectorize=False,
        size=dataset_size,
        sex=sex_classification,
        )

input_size  = len(training_data[0][0])
if sex_classification:
    output_size = 18
else:
    output_size = 9

print(" ** Initializing Network...")
lvq = lvq.LVQ(input_size,
        output_size,
        prototypes_per_class = 20,

        dist_function='euclidean')

if os.path.exists('autoload.save.gz'):
    print(" *** Found autoload, loading config...")
    # net.load('autoload.save.gz')

print(lvq)
print(" ** Starting training...")
training_tr_err, training_va_err = lvq.train(training_data,
        eta = 0.1,
        epochs = 5,
        eta_decay = True,
        va_d = validation_data)

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
    print "  ** Accuracy on train      dataset : {}/{} -> error: {:.3%}".format(
            lvq.eval_accuracy(training_data),
            len(training_data),
            lvq.eval_error_rate(training_data)
            )
    print "  ** Accuracy on validation dataset : {}/{} -> error: {:.3%}".format(
            lvq.eval_accuracy(validation_data),
            len(validation_data),
            lvq.eval_error_rate(validation_data)
            )
    print "  ** Accuracy on test       dataset : {}/{} -> error: {:.3%}".format(
            lvq.eval_accuracy(test_data),
            len(test_data),
            lvq.eval_error_rate(test_data)
            )
    print



print(" ** Evaluating confusion on test dataset..")
confusion = lvq.get_confusion(test_data)



if evalsample:
    print(" ** evaluate single input...")
    (feat, lab) = utils.extract_sample(
            sample_file,
            vectorize=False,
            size=dataset_size,
            sex=sex_classification)

    yhat = lvq([feat])
    print("    * prediction  : {}".format(utils.unpack_prediction(
        yhat, sex=sex_classification, vectorized=False)))
    print("    * actual value: {}".format(utils.unpack_prediction(
        lab, sex=sex_classification, vectorized=False)))
    print


print(" ** Generating image output...")
utils.plot_training_summary2('test', training_tr_err, training_va_err, \
        lvq.eval_error_rate(test_data))
utils.plot_confusion_matrix('test', confusion, interpolation='none', style=None)


print(" ** Done")
