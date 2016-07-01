#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import lib.utils as u
import network

lab = 0




# Get input data
import mnist_loader
print " ** Extracting DATA ..."
training_data_lvb, test_data_lvb = u.extract_datasets(size=40)

input_size = len(training_data_lvb[0][0])
output_size = len(training_data_lvb[0][1])

print " ** lvb input size : {}".format(input_size)
print " ** Starting training ..."


if lab:
    layers = [input_size, 10, output_size]
    training_data = training_data_lvb
    test_data = test_data_lvb

    net = network.Network(layers,
            activation='sigmoid',
            cost='cross-entropy',
            regularization='L2',
            learning_rate=0.2,
            lambda_=0.0)

    tr_acc, tr_err, tr_cost, va_acc, va_err, va_cost = net.train(training_data,
            epochs=50,
            batch_size=20,
            va_d=test_data,
            monitoring={'error':True, 'accuracy':True, 'cost':False})


else:
    training_data_ini, validation_data_ini, test_data_ini = mnist_loader.load_data_wrapper()
    layers = [784, 100, 10]
    training_data = training_data_ini
    test_data = test_data_ini

    net = network.Network(layers,
            activation='sigmoid',
            cost='cross-entropy',
            regularization='L2',
            learning_rate=0.5,
            lambda_=1.1)

    tr_acc, tr_err, tr_cost, va_acc, va_err, va_cost = net.train(training_data,
            epochs=30,
            batch_size=10,
            va_d=test_data,
            monitoring={'error':True, 'accuracy':True, 'cost':False})



plt.xlabel('Epoch')
plt.ylabel('Error rate')
plt.plot(tr_err, label='error on training')
plt.plot(va_err, label='error on validation')
plt.legend(loc="lower right")
plt.savefig('out/learning.png')
