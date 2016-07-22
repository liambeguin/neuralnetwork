#!/usr/bin/python
# vim: cc=80:

import os
import network
from lib import utils



print(" ** Extracting dataset...")
training_data, validation_data, test_data = utils.extract_datasets(size=50)

input_size  = len(training_data[0][0])
output_size = len(training_data[0][1])



print(" ** Initializing Network...")
net = network.Network(
        (input_size, 150, output_size),
        activation     = 'sigmoid',
        cost           = 'cross-entropy',
        regularization = 'L2',
        learning_rate  = 0.5,
        lambda_        = 0.01
        )
if os.path.exists('autoload.save.gz'):
    print(" *** Found autoload, loading config...")
    net.load('autoload.save.gz')

print(net)

print(" ** Starting training...")
tr_err, tr_cost, va_err, va_cost = net.train(
        training_data,
        epochs       = 50,
        batch_size   = 10,
        va_d         = validation_data,
        early_stop_n = None,
        monitoring   = {'error':True, 'cost':True}
        )

print("Learning took : {} days, {} seconds and {} us".format(net.learn_time.days, net.learn_time.seconds, net.learn_time.microseconds))
# net.save('net.save')

good = net.eval_accuracy(test_data)
print " ** Accuracy on test dataset : {}/{} -> {}".format(good, len(test_data), 100.0 * good / len(test_data))

confusion = net.get_confusion(test_data)
print confusion


print(" ** Generating image output...")
utils.plot_training_summary('test', tr_err, tr_cost, va_err, va_cost, \
        net.eval_error_rate(test_data), net.eval_cost(test_data))
utils.plot_confusion_matrix('test', confusion, interpolation='none',  style=None)
print(" ** Done")
