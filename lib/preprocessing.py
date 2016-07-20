#!/usr/bin/python
# vim: cc=80:


import os, fnmatch
import numpy as np

import logging
logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

COL_STATIC_E = 12
COL_DYNAMIC_E = 25

class Preprocessing:
    def __init__(self, filename, count):
        """Takes a CSV like file and converts it to a 2D float array for easy
        processing."""
        self.count = count
        self.filename = filename
        # Get array from file
        self.data = np.fromfile(filename, sep=' ')
        # Resize to match the file format
        self.data = self.data.reshape((len(self.data)/26, 26))

        if len(self.data) < self.count:
            logger.warning("Not enough lines [%d/%d] in file: %s " \
                    %(len(self.data), self.count, self.filename))


    def __get_column(self, column):
        """Return a single column of the dataset."""

        return [ x[column] for x in self.data ]


    def __check_size(self, prefix=''):
        """Check the size of the dataset."""
        if len(self.data) < self.count - 10:
            logger.debug("%s Low count [%d/%d]..." %(prefix, len(self.data), self.count))


    def start_point_detection(self, threshold=0.5, n=10):
        """Detect beginning of voice activity using static energy."""

        col = self.__get_column(COL_STATIC_E)

        for idx, line in enumerate(self.data):
            win = col[idx:idx+(n+1)]
            avg = sum(win)/len(win)

            if avg > threshold:
                self.data = self.data[idx:]
                break

        self.__check_size()


    def cut_first_max(self, n=20, column=COL_DYNAMIC_E):
        """Ignore data before first local maximum."""

        col = self.__get_column(column)[0:n]
        pos = col.index(max(col))
        self.data = self.data[pos:]
        self.__check_size(prefix=self.cut_first_max.__name__)


    def moving_average_fit(self, delta_min, threshold, column, n=2):
        """Filter data using a symetrical moving average."""

        col = [0.0] * n + self.__get_column(column) + [0.0] * n
        d = []

        for idx, line in enumerate(self.data):
            # get window of 2n+1 values
            if idx >= n and idx < len(self.data) - (n+1):
                win = col[idx-n:idx+(n+1)]
                avg = sum(win)/len(win)
                err = abs(avg - line[column])

                if err < delta_min:
                    d.append(line)

                if line[column] > threshold :
                    d += self.data[idx:]
                    break

        self.data = d
        self.__check_size(prefix=self.moving_average_fit.__name__)


    def cutout_dynamics(self):
        self.data = np.delete(self.data, np.s_[COL_STATIC_E+1:COL_DYNAMIC_E], 1)


    def only_static_data(self):
        self.data = np.delete(self.data, np.s_[0:COL_STATIC_E], 1)

    def normalize(self):
       min_ = np.min(self.data, axis=0)
       max_ = np.max(self.data, axis=0)
       self.data = (self.data - min_) / (max_ - min_)


    def fit(self):
        """"Make sure data is the right length."""
        if len(self.data) > self.count:
            self.data = self.data[0:self.count]
        else:
            pad = np.zeros((self.count - len(self.data), len(self.data[0])))

            for line in pad:
                line[COL_STATIC_E] = min(self.__get_column(COL_STATIC_E))

            self.data = np.concatenate((self.data, pad))


    def save(self, prefix):
        """Save data to a new location."""

        out = os.path.join(prefix, self.filename)

        if not os.path.exists(os.path.dirname(out)):
            os.makedirs(os.path.dirname(out))

<<<<<<< HEAD:preprocessing.py
        f = open(out, 'w')
        for line in self.data:
            for i in line:
                f.write(str(i) + ' ')
            f.write('\n')
        f.close()




def get_filelist(input_dir, number):
    """ Returns a list of files  for a given number."""

    pattern = str(number) + '*'
    fileList = []

    for dName, sdName, fList in os.walk(input_dir):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, pattern):
                fileList.append(os.path.join(dName, fileName))

    return fileList




def main():
    for num in range(1, 10):
        for i in get_filelist('train', num):
            data = Preprocessing(i, 60)

#           data.moving_average_fit(0.1, 2.0, COL_DYNAMIC_E,3)
            data.start_point_detection(threshold=0.5, n=10)
#            data.cut_first_max(n=20)
            data.cut_first_max(n=20)
            data.fit()
            data.save('out')
=======
        np.savetxt(out, self.data, delimiter=' ')
>>>>>>> 6ab72a0f60965a50ef3d07299fcf038d3037d70c:lib/preprocessing.py



