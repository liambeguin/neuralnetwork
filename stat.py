#!/usr/bin/python
# vim: cc=80:


import numpy, pylab
import scipy.stats as stats


# Here is how a line is organised
#  [0:11]  : static MFCC values
#  [12]    : static energy
#  [13:24] : dynamic MFCC values
#  [25]    : Dynamic energy

# FILE = 'test_data/man/kr/1a.txt'
FILE = 'test_data/man/nf/6b.txt'




def extract_data(filename):
    """
    Takes a CSV like file and converts it to a
    list of list of floats for easier processing
    """
    lines = open(filename).readlines()
    return [ [ float(x) for x in line.split() ] for line in lines ]




def extract_single_column(data, n):
    """
    takes a file converted into a list of lists
    and returnes a single column
    """
    return [ x[n] for x in data ]




def filter_dynamic(data):
    """
    Remove lines with no dynamic energy
    """
    return [ x for x in data if x[25] != 0 ]




def convert_log(data):
    """
    converts MFCC values to non log scale
    """
    print "TBD"













def qqplot(data):

    for i in range(12):
        col = [ x[i] for x in data ]

        stats.probplot(col, dist="norm", plot=pylab)
        pylab.show()




def get_info(data):

    print "Number_of_OBS Min Max Mean Variance Skewness Kurtosis"

    for i in range(12):
        col = [ float(x[i]) for x in data ]
        print stats.describe(col)




if __name__ == "__main__":
# get data from file
    data = extract_data(FILE)
# remove lines where dynamic energy is 0
    new = filter_dynamic(data)
# Convert back to non log scale
    foo = convert_log(new)
# Keep quantiles depending on size of array

    get_info(new)
