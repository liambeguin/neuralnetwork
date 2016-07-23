#!/usr/bin/python
# vim: cc=80:

import os, fnmatch, re
import numpy as np

import preprocessing as prep



def vectorize_output(n, shape=(9, 1)):
    v =  np.zeros(shape)
    v[n] = 1.0
    return v



def extract_datasets(basename='', size=60, sex=False, verbose=False):
    tr_d = _extract(basename + 'train',      size=size, sex=sex)
    va_d = _extract(basename + 'validation', size=size, sex=sex)
    te_d = _extract(basename + 'test',       size=size, sex=sex)

    if verbose:
        print(" *** Training")
        inspect_dataset(tr_d, size=size)
        print

        print(" *** Validation")
        inspect_dataset(va_d, size=size)
        print

        print(" *** Testing")
        inspect_dataset(te_d, size=size)
        print

    return tr_d, va_d, te_d



def _extract(dirname='train', size=60, sex=False, out_size=9):
    """Takes a folder containing training data and returns a
    list of tuples (input, output)"""
    dataset = []
    for num in xrange(1, out_size+1):
        for file_ in get_filelist(dirname, num):
            sample = extract_sample(file_, size=size, sex=sex)
            dataset.append(sample)

    return dataset



def extract_sample(file_, size=60, sex=False, out_size=9):
    # Preprocess file ...
    x = prep.Preprocessing(file_, size)
    x.start_point_detection(threshold=0.5, n=10)
    x.cut_first_max(n=20)
    x.normalize()
    x.fit()
    x.get_subset('static')

    num = int(re.search(r'(?=.*)[0-9](?=.*)', file_).group(0))

    # make a column of the whole array
    features = x.data.reshape((len(x.data)*len(x.data[0]), 1) )

    if sex:
        if re.search(r'.*woman.*', file_):
            labels = vectorize_output( num - 1 + out_size, shape=(out_size*2, 1))
        else:
            labels = vectorize_output(num-1, shape=(out_size*2, 1))
    else:
        labels = vectorize_output(num-1, shape=(out_size, 1))

    return (features, labels)



def unpack_prediction(yhat):
    p = np.argmax(yhat)+1
    if len(yhat) != 9:
    # classifying M/W
        if p > 8:
            return "woman - {}".format(p-9)
        else:
            return "man   - {}".format(p)
    else:
        return str(p)



def inspect_dataset(dataset, size=60):
    print("    * size : {}".format(len(dataset)))
    print("    * input  shape: {} -> {}x{}".format(dataset[0][0].shape, dataset[0][0].shape[0]/size, size) )
    if isinstance(dataset[0][1], np.ndarray):
        print("    * output shape: {}".format(dataset[0][1].shape) )
    else:
        print("    * output shape: {}".format(type(dataset[0][1])) )

    print("    * input type: {}".format(type(dataset[0][0])) )



def get_filelist(input_dir, number):
    """ Returns a list of files  for a given number."""

    pattern = str(number) + '*'
    fileList = []

    for dName, sdName, fList in os.walk(input_dir):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, pattern):
                fileList.append(os.path.join(dName, fileName))

    return fileList



def make_cmap(colors, position=None, bit=False):
    '''
    make_cmap takes a list of tuples which contain RGB values. The RGB
    values may either be in 8-bit [0 to 255] (in which bit must be set to
    True when called) or arithmetic [0 to 1] (default). make_cmap returns
    a cmap with equally spaced colors.
    Arrange your tuples so that the first color is the lowest value for the
    colorbar and the last is the highest.
    position contains values from 0 to 1 to dictate the location of each color.
    '''
    import matplotlib as mpl
    import numpy as np
    bit_rgb = np.linspace(0,1,256)
    if position == None:
        position = np.linspace(0,1,len(colors))
    else:
        if len(position) != len(colors):
            sys.exit("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            sys.exit("position must start with 0 and end with 1")
    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],
                    bit_rgb[colors[i][1]],
                    bit_rgb[colors[i][2]])
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
    return cmap



def plot_training_summary(basename, tr_err, tr_cost,
        va_err=None, va_cost=None, te_err=None, te_cost=None):
    """
    basename is a suffix for the name of the output file
    tr_err, tr_cost vectors returned by Network.train
    va_err, va_cost vectors returned by Network.train
    te_err, te_cost single value evaluated after training on test set
    """

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    # import matplotlib.gridspec as gridspec


    # fig = plt.figure(figsize=(10,20), dpi=700)
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].set_ylabel('Error rate')
    axarr[0].grid(True)
    axarr[0].set_ylim(ymin=-0.1)

    axarr[0].plot(tr_err, label='training')
    if va_err:
        axarr[0].plot(va_err, label='validation')
    if te_err:
        axarr[0].plot([te_err]*len(tr_err), label='test')


    axarr[1].set_ylabel('cost')
    axarr[1].grid(True)
    axarr[1].plot(tr_cost, label='training')
    if va_cost:
        axarr[1].plot(va_cost, label='validation')
    if te_cost:
        axarr[1].plot([te_cost]*len(tr_cost), label='test')



    axarr[0].set_title('TIDIGITS training summary')
    plt.xlabel('Epoch')
    plt.legend(loc='best')
    plt.tight_layout()

    out = os.path.join('out', 'plots', basename, 'training.png')
    if not os.path.exists(os.path.dirname(out)):
        os.makedirs(os.path.dirname(out))

    plt.savefig(out)
    plt.clf()

def plot_confusion_matrix(basename, matrix, interpolation=None, style=None):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    # plt.xkcd()

    if style == 'simple':
        inter = 'none'
        cm    = 'Grays'
    else:
        inter = 'bicubic'
        # NOTE: this is a list containing color, position
        color_data = [
                [ (1.0, 1.0, 1.0), 0.00],
                [ (0.5, 0.5, 0.5), 0.05],
                [ (0.4, 0.2, 0.0), 0.20],
                [ (0.4, 0.2, 0.0), 0.60],
                [ (0.0, 0.3, 0.4), 0.80],
                [ (0.0 ,0.4, 0.3), 1.00]]

        colors, position = [], []
        for elt in color_data:
            colors.append(elt[0])
            position.append(elt[1])

        cm = make_cmap(colors, position=position)

    if interpolation:
        inter = interpolation

    conf = plt.imshow(matrix, interpolation=inter, cmap=cm, aspect='auto')

    plt.ylabel('Actual value $(y)$')
    plt.xlabel('Prediction $(\hat{y})$')
    plt.colorbar(conf)

    # If classifying M/W
    labels = []
    if len(matrix[0]) > 9:
        for l in xrange(1, len(matrix[0])+1):
            if l <= 9:
                l = '{:2}M'.format(l)
            else:
                l = '{:2}W'.format(l-9)
            labels.append(l)
    else:
        labels = range(1, len(matrix[0])+1)

    plt.tight_layout(pad=2)
    plt.xticks(xrange(0, len(matrix[0])), labels)
    plt.yticks(xrange(0, len(matrix[1])), labels)
    plt.grid(True)
    plt.title('Confusion Matrix')

    out = os.path.join('out', 'plots', basename, 'confusion.png')
    if not os.path.exists(os.path.dirname(out)):
        os.makedirs(os.path.dirname(out))

    plt.savefig(out)
    plt.clf()



LOGLEVEL = 0
def set_level(lvl):
    LOGLEVEL = lvl

def log_print(lvl, msg):
    if lvl > LOGLEVEL:
        print("{}".format(msg))

