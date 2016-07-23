#!/usr/bin/python
# vim: cc=80:

import os
import numpy as np
import network
from lib import utils

autosave  = False
dosummary = True
# NOTE: the higher this is, the more the network will log information
#       0 - Print nothing
#       2 - Print epoch number
#       3 - Print epoch number and summary
net_verbose  = 3

evalsample         = False
sample_file        = 'test/woman/nh/5b.txt'
dataset_size       = 50
sex_classification = True



print(" ** Extracting dataset...")
training_data, validation_data, test_data = utils.extract_datasets(
        size=dataset_size,
        sex=sex_classification,
        )

input_size  = len(training_data[0][0])
output_size = len(training_data[0][1])



print(" ** Initializing Network...")
net = network.Network(
        (input_size, 150, output_size),
        activation     = 'sigmoid',
        cost           = 'cross-entropy',
        regularization = 'L2',
        learning_rate  = 0.5,
        lambda_        = 0.001,
        verbose        = net_verbose,
        )

if os.path.exists('autoload.save.gz'):
    print(" *** Found autoload, loading config...")
    net.load('autoload.save.gz')
    if net.struct[0] != input_size:
        raise Exception("Autoload conf file does not match your dataset!")

print(net)



print(" ** Starting training...")
tr_err, tr_cost, va_err, va_cost = net.train(
        training_data,
        epochs       = 100,
        batch_size   = 10,
        va_d         = validation_data,
        early_stop_n = 30,
        monitoring   = {'error':True, 'cost':True},
        )



print
print
print
print(" ** Learned in : {} days, {} seconds and {} us".format(
    net.learn_time.days,
    net.learn_time.seconds,
    net.learn_time.microseconds
    ))



if autosave:
    print(" ** Saving state of the Network...")
    net.save('conf.save.gz')



if dosummary:
    print
    print " ** Summary : "
    print "  ** Accuracy on train      dataset : {}/{} -> error: {:.3%}".format(
            net.eval_accuracy(training_data),
            len(training_data),
            net.eval_error_rate(training_data)
            )
    print "  ** Accuracy on validation dataset : {}/{} -> error: {:.3%}".format(
            net.eval_accuracy(validation_data),
            len(validation_data),
            net.eval_error_rate(validation_data)
            )
    print "  ** Accuracy on test       dataset : {}/{} -> error: {:.3%}".format(
            net.eval_accuracy(test_data),
            len(test_data),
            net.eval_error_rate(test_data)
            )
    print



print(" ** Evaluating confusion on test dataset..")
confusion = net.get_confusion(test_data)



if evalsample:
    print(" ** evaluate single input...")
    (feat, lab) = utils.extract_sample(
            sample_file,
            size=dataset_size,
            sex=sex_classification)

    yhat = net(feat)
    print("    * prediction  : {}".format(utils.unpack_prediction(yhat)) )
    print("    * actual value: {}".format(utils.unpack_prediction(lab)) )
    print



print(" ** Generating image output...")
utils.plot_training_summary('test', tr_err, tr_cost, va_err, va_cost, \
        net.eval_error_rate(test_data), net.eval_cost(test_data))
utils.plot_confusion_matrix('test', confusion, interpolation='none', style=None)
print(" ** Done")

