#!/usr/bin/python

import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import network

dataset = 'IRIS'
dataset = 'MNIST'
dataset = 'TIDIGITS'


print " ** Extracting the {} dataset...".format(dataset)
if dataset == 'TIDIGITS':
    import lib.utils as u
    training_data, validation_data, test_data = u.extract_datasets(size=50, out_size=2)
    # training_data = training_data[:100]
    # validation_data = validation_data[:10]
    input_size  = len(training_data[0][0])
    output_size = len(training_data[0][1])

    layers  = [input_size, 120, output_size]
    etas     = [0.01]
    lmb     = 10.1
    epoch   = 30
    batch_s = 10
    es = None


elif dataset == 'MNIST':
    import mnist_loader
    training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
    training_data = training_data[:1000]
    validation_data = validation_data[:100]
    input_size  = 784
    output_size = 10

    layers  = [input_size, 100, output_size]
    etas     = [0.5]
    lmb     = 1.1
    epoch   = 100
    batch_s = 10
    es = 50


elif dataset == 'IRIS':
    from sklearn import datasets
    from sklearn.cross_validation import train_test_split
    import numpy as np
    from lib.utils import vectorize_output

    iris = datasets.load_iris()
    X_iris = iris.data
    y_iris = iris.target
    training_data_X, validation_data_X, training_data_y, validation_data_y = train_test_split(X_iris, y_iris, test_size=0.2)

    training_data = []
    validation_data = []
    for (x,y) in zip(training_data_X, training_data_y):
        label = vectorize_output(y, size=(3,1))
        training_data.append((x.reshape(4, 1), label))

    for (x,y) in zip(validation_data_X, validation_data_y):
        label = vectorize_output(y, size=(3,1))
        validation_data.append((x.reshape(4, 1), label))


    input_size  = len(training_data[0][0])
    output_size = len(training_data[0][1])

    layers  = [input_size, 100, 100, output_size]
    etas     = [0.1]
    lmb     = 0.0001
    epoch   = 100
    batch_s = 1
    es = 20


else:
    pass

print " ** Initializing Network..."
net = network.Network(layers,
        activation='sigmoid',
        cost='quadratic',
        regularization='L2',
        learning_rate=etas[0],
        lambda_=lmb)
print net



tr_err, tr_cost, va_err, va_cost = [], [], [], []
for eta in etas:
    net.eta = eta
    print " ** Starting training [{}]...".format(eta)
    tr_err_i, tr_cost_i, va_err_i, va_cost_i = net.train(training_data,
            epochs=epoch,
            batch_size=batch_s,
            va_d=validation_data,
            early_stop_n = es,
            monitoring={'error':True, 'cost':True})

    tr_err.extend(tr_err_i)
    tr_cost.extend(tr_cost_i)
    va_err.extend(va_err_i)
    va_cost.extend(va_cost_i)



print " ** Generating image output..."
# Two subplots, the axes array is 1-d
f, axarr = plt.subplots(2, sharex=True)
axarr[0].set_ylabel('Error rate')
axarr[0].grid()
axarr[0].plot(tr_err, label='training')
axarr[0].plot(va_err, label='validation')
axarr[0].set_ylim([-0.1, 1.1])

axarr[1].set_ylabel('cost')
axarr[1].grid()
axarr[1].plot(tr_cost, label='training')
axarr[1].plot(va_cost, label='validation')

axarr[0].set_title(dataset)
plt.xlabel('Epoch')
plt.legend(loc="upper right")
plt.savefig('out/learning.png')

print " ** Done"
