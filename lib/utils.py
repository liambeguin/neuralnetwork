#!/usr/bin/python


def inspect(network):
    # n -1 because input layer does not count
    print "Number of layers : ", network.n_layers - 1

    print "-- Input Layer --"
    print network.struct[0], " Neurons"

    if network.n_layers > 2:
        for idx, val in enumerate(network.struct[1:-1]):
            print "-- Hidden Layer %d --" % (idx +1)
            print val, " Neurons"
            print "weights:"
            print network.weights[idx]

    print " -- Output Layer --"
    print network.struct[-1], " Neurons"
    print "weights:"
    print network.weights[-1]
