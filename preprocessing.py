#!/usr/bin/python
# vim: cc=80:


import os, fnmatch


# Here is how a line is organised
#  [0:11]  : static MFCC values
#  [12]    : static energy
#  [13:24] : dynamic MFCC values
#  [25]    : Dynamic energy
A=1
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


    def start_point_detection(self, threshold_s, threshold_d):
        c = 0
        for line in self.data:
            if line[COL_STATIC_E] < threshold_s and line[COL_DYNAMIC_E] < threshold_d:
                c += 1
            else:
                break

        self.data = self.data[c:]


    def static_energy_threshold(self, threshold):
        self.data = [ x for x in self.data if x[COL_STATIC_E] > threshold ]


    def threshold_filer(self, threshold, column=COL_STATIC_E):
        self.data = [ x for x in self.data if x[column] > threshold ]


    def static_energy_keep_nmax(self):

        test = [ abs(x) for x in self.get_column(COL_STATIC_E) ]
        test.sort()
        test.reverse()
        a = test[self.count]

        self.data = [ x for x in self.data if abs(x[COL_STATIC_E]) >= a]


    def start_stat(self, threshold, n=2):
        static = self.get_column(COL_STATIC_E)
        dyn = self.get_column(COL_DYNAMIC_E)
        d = []

        for idx, line in enumerate(self.data):
            win_s = static[idx:idx+(n+1)]
            avg_s = sum(win_s)/len(win_s)
            win_d = dyn[idx:idx+(n+1)]
            avg_d = sum(win_d)/len(win_d)

            if avg_s > threshold and avg_d > 0:
                d = self.data[idx:]
                break

        self.data = d

    def cut_arround_max(self, n_before, n_after, column=COL_DYNAMIC_E):
        col = self.get_column(column)
        pos = col.index(max(col))
        self.data = self.data[pos-n_before:pos+n_after]


    def cut_arround_first_max(self, n=40, column=COL_DYNAMIC_E):

        col = self.get_column(column)[0:n]
        pos = col.index(max(col))
        self.data = self.data[pos:]



    def moving_average_fit(self, delta_min, threshold, column, n=2):
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

                if err < delta_min:
                    d.append(line)

                if line[column] > threshold :
                    d += self.data[idx:]
                    break

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
        for i in get_filelist('train', num):
            data = Preprocessing(i, 60)
            if len(data.data) < data.count:
                print " *** Not enough lines [%d/%d] in file: " %(len(data.data), data.count)  + data.filename

            data.start_stat(0.5, n=10)
            data.cut_arround_first_max(20)
            data.fit()

            if len(data.data) < data.count:
                print "after fit ", len(data.data), data.filename
            data.save('out')



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user.")
