#!/usr/bin/python

import lib.utils as u
import network

lab = 1




# Get input data
import mnist_loader
training_data_ini, validation_data_ini, test_data_ini = mnist_loader.load_data_wrapper()
training_data_lvb, test_data_lvb = u.extract_datasets(size=40)

f = open('out/learning', 'w')

f.write("Header\n")
f.write('len training: {}\n'.format(len(training_data_lvb)))
f.write('len test: {}\n'.format(len(test_data_lvb)))

# print " *** lvb *** "
# u.inspect_dataset(training_data_lvb)
# print
# print
# print " *** ini *** "
# u.inspect_dataset(training_data_ini)

if lab:
    input_size = len(training_data_lvb[0][0])
    output_size = len(training_data_lvb[0][1])
    layers = [input_size, 100, output_size]
    training_data = training_data_lvb
    test_data = test_data_lvb

    net = network.Network(layers, activation='sigmoid', cost='cross-entropy', regularization='L2',
            learning_rate=0.1)
    net.train(training_data, 30, 10, test_data=test_data)

    foo = test_data[0]



else:
    layers = [784, 30, 10]
    eta = 0.5
    training_data = training_data_ini
    test_data = test_data_ini

    net = network.Network(layers, activation='sigmoid', cost='cross-entropy', regularization='L2',
            learning_rate=eta)
    net.train(training_data, 30, 10, lambda_=2.0, test_data=test_data)

    foo = (test_data[0][0], u.vectorize_output(test_data[0][1]))



print foo[1]
print net(foo[0])
print
print "learned in {}".format(net.learn_time)
f.write('learned in {}\n'.format(net.learn_time))

f.write('\n\n')
f.write('error rate\n')
for i in net.err:
    f.write(str(i)+'\n')


f.close()
