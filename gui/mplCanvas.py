#!/usr/bin/env python3.4



from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from numpy import arange, sin, pi
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


from PyQt5 import QtWidgets,QtCore

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.x
        self.y
#        timer = QtCore.QTimer(self)
#        timer.timeout.connect(self.update_figure)
#        timer.start(1000)

    def compute_initial_figure(self):
        
        
        self.a=4
        self.e=100
        self.x=np.array([])
        self.y=np.array([])
        self.axes.plot(self.x, self.y, 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        self.x=np.append(self.x,[self.a])
        #print("a={}",self.a)
        self.a+=1
        if self.e>0:
            self.e-=1

        #print(self.x)
        #l = [random.randint(0, 10) for i in range(self.a)]
        #self.y=np.append(self.y,[random.randint(0, 10)])
        self.y=np.append(self.y,[self.e])
        #print(l)
        self.axes.plot(self.x, self.y, 'r')
        self.axes.set_ylabel("Error %")
        self.axes.set_xlabel("Epoch")
        self.draw()


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)



