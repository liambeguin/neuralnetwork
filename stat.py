#!/usr/bin/python
# vim: cc=80:


import numpy, pylab
import scipy.stats as stats
import os


# Here is how a line is organised
#  [0:11]  : static MFCC values
#  [12]    : static energy
#  [13:24] : dynamic MFCC values
#  [25]    : Dynamic energy

COL_LABELS = ['static 1', 'static 2', 'static 3', 'static 4', 'static 5', 'static 6', \
              'static 7', 'static 8', 'static 9', 'static 10', 'static 11', 'static 12', \
              'static Energy', \
              'dynamic 1', 'dynamic 2', 'dynamic 3', 'dynamic 4', 'dynamic 5', 'dynamic 6', \
              'dynamic 7', 'dynamic 8', 'dynamic 9', 'dynamic 10', 'dynamic 11', 'dynamic 12', \
              'dynamic Energy' ]

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
    return "TBD"




def get_filelist(number):
    import fnmatch

    inDIR = 'test_data'
    pattern = str(number) + '*'
    fileList = []

    for dName, sdName, fList in os.walk(inDIR):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, pattern):
                fileList.append(os.path.join(dName, fileName))

    return fileList


def extract_full_data(num):
    data = []
    for file in get_filelist(num):
        for line in extract_data(file):
            data.append(line)

    return data







def qqplot(data):

    for i in range(len(data[0])):
        col = [ x[i] for x in data ]

        stats.probplot(col, dist="norm", plot=pylab)
        pylab.title(COL_LABELS[i])
        pylab.show()




def get_static_info(data):

    print "Number_of_OBS Min Max Mean Variance Skewness Kurtosis"

    for i in range(13):
        col = [ float(x[i]) for x in data ]
        print stats.describe(col)






if __name__ == "__main__":

    # get data from files
    data = extract_full_data(1)
    # remove lines where dynamic energy is 0
    new = filter_dynamic(data)
    # Convert back to non log scale
    foo = convert_log(new)
    # Keep quantiles depending on size of array

    # get_static_info(new)
    qqplot(new)
