#!/usr/bin/python
# vim: cc=80:


import scipy.stats as stats
import os, fnmatch


# Here is how a line is organised
#  [0:11]  : static MFCC values
#  [12]    : static energy
#  [13:24] : dynamic MFCC values
#  [25]    : Dynamic energy

COL_STATIC_E = 12
COL_DYNAMIC_E = 25

class Preprocessing:
    def __init__(self, filename, count):
        """
        Takes a CSV like file and converts it to a
        list of list of floats for easier processing
        """
        lines = open(filename).readlines()
        self.filename = filename
        self.count = count
        self.data = [ [ float(x) for x in line.split() ] for line in lines ]


    def get_column(self, column):
        return [ x[column] for x in self.data ]


    def start_point_detection(self, ratio):
        c = 0
        for i in self.get_column(COL_STATIC_E):
            if i < ratio:
                c += 1
            else:
                break

        self.data = self.data[c:]


    def start_point_delta_detection(self, ratio):
        d = self.get_column(COL_STATIC_E)
        c = 0
        prv = 0
        for idx, val in enumerate(d):

            if (val - prv) < ratio:
                c += 1
            else:
                break

        self.data = self.data[c:]


    def fit(self):
        if len(self.data) > self.count:
            self.data = self.data[0:self.count]
        else:
            pad = [0] * len(self.data[0])
            pad[COL_STATIC_E] = min(self.get_column(COL_STATIC_E))
            self.data += [pad] * (self.count - len(self.data))


    def save(self, prefix):
        out = os.path.join(prefix, self.filename)

        if not os.path.exists(os.path.dirname(out)):
            os.makedirs(os.path.dirname(out))

        f = open(out, 'w')
        for line in self.data:
            for i in line:
                f.write(str(i) + ' ')
            f.write('\n')
        f.close()











def get_filelist(input_dir, number):

    pattern = str(number) + '*'
    fileList = []

    for dName, sdName, fList in os.walk(input_dir):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, pattern):
                fileList.append(os.path.join(dName, fileName))

    return fileList




def main():
    for num in range(1, 10):
        for i in get_filelist('raw', num):
            data = Preprocessing(i, 40)
            data.start_point_detection(0.8)
            data.fit()
            data.save('out')



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user.")
