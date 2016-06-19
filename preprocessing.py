#!/usr/bin/python
# vim: cc=80:


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


    def start_point_detection(self, ratio, column=COL_STATIC_E):
        c = 0
        for i in self.get_column(column):
            if i < ratio:
                c += 1
            else:
                break

        self.data = self.data[c:]


    def start_point_delta_detection(self, threshold, delta, column=COL_STATIC_E):
        d = self.get_column(column)
        c = 0
        prv = 0
        for idx, val in enumerate(d):
            if val <= threshold or (val - prv) <= delta:
                c += 1
                prv = val
            else:
                break


        self.data = self.data[c:]


    def static_energy_threshold(self, threshold):
        self.data = [ x for x in self.data if x[COL_STATIC_E] > threshold ]


    def static_energy_keep_nmax(self):

        test = [ abs(x) for x in self.get_column(COL_STATIC_E) ]
        test.sort()
        test.reverse()
        a = test[self.count]

        self.data = [ x for x in self.data if abs(x[COL_STATIC_E]) >= a]


    def moving_average_fit(self, delta_min, delta_max, column, n=2):
        """
        n symetric
        """
        col = [0.0] * n + self.get_column(column) + [0.0] * n
        d = []

        for idx, line in enumerate(self.data):
            # get window of 2n+1 values
            if idx >= n and idx < len(self.data) - (n+1):
                win = col[idx-n:idx+(n+1)]
                avg = sum(win)/len(win)
                err = abs(avg - line[column])

                if err < delta_min or err > delta_max :
                    d.append(line)


        self.data = d



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
            data = Preprocessing(i, 60)
            # data.moving_average_fit(0.1, 10, COL_DYNAMIC_E, n=4)
            data.moving_average_fit(0.1, 0.2, COL_STATIC_E, n=2)
            # data.start_point_detection(0.35)
            # data.start_point_delta_detection(0.01, 0.2)
            # data.fit()
            data.save('out')



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user.")
