#!/usr/bin/python

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

import matplotlib.pyplot as plt

from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import Qt,pyqtSignal,pyqtSlot,QThread

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig( filename=LOG_FILENAME, level=logging.DEBUG )

class MplCanvas(FigureCanvas):
    """
    Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.).
    

    Parameters:
    ----------
    dpi=dots per inch

    """
    clearFigure = pyqtSignal()
    def __init__(self, parent=None, width=100, height=10, dpi=80,pos=111,title=''):
        
        
        fig = Figure(figsize=(width, height), dpi=dpi)
        #fig.suptitle("Main title")
        self.axes = fig.add_subplot(pos)# two rows, one column, first plot
        self.axes.grid(True)
        self.axes.set_title(title)

        #axe.set_bg_color=set_facecolor
        # self.axes.set_facecolor('white')
        # We want the axes cleared every time plot() is called
        #self.axes.hold(True)

        #self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
#        FigureCanvas.updateGeometry(self)


class DynamicMplCanvas(MplCanvas):
    """A canvas that updates itself every second with a new plot."""
    
    def __init__(self, *args, **kwargs):
        MplCanvas.__init__(self, *args, **kwargs)
        #self.x
        #self.y
        #self.z
        self.color=''
        #self.axes.set_ylim([0,100])
        #self.axes.set_xlim([0,100])
        self.compute_initial_figure()
#        timer = QtCore.QTimer(self)
#        timer.timeout.connect(self.update_figure)
#        timer.start(1000)
    def get_color():
        return self.color

    def compute_initial_figure(self):
        self.x=np.array([])
        self.y=np.array([])
        self.z=np.array([])
        self.p1=''
        self.p2=''
        #self.axes.plot(self.x, self.y)
    
    
    @pyqtSlot(list)
    def update_figure(self,l):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        #self.axes.axhline(0, color='black', lw=2)
        sz=len(self.x)
        for i in range(len(l)):
            self.x=np.append(self.x,[sz+i])
            self.y=np.append(self.y,[l[i]*100])

        #self.axes.plot(self.x, self.y,self.color)
        self.axes.plot(self.x, self.y,)
        self.axes.plot(self.x, [1]*len(self.x),'b')
        self.axes.set_ylabel("Error %")
        self.axes.set_xlabel("Epoch")
        self.draw()

    @pyqtSlot(list)
    def update_figure2(self,l):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        #self.axes.axhline(0, color='black', lw=2)
        sz=len(self.x)
        #for i in range(len(l)):
        
        self.x = np.append(self.x,sz+1)
        
        
        self.y = np.append(self.y,l[0]*100)
        self.z = np.append(self.z,l[1]*100)
        p1, = self.axes.plot(self.x, self.y,'r', label="Training")
        p2, = self.axes.plot(self.x, self.z,'b', label="Validation" )
        #self.axes.legend(handles=[p1],loc='best')
        self.axes.legend(handles=(p1,p2),loc='best')
        #self.axes.legend(handles=[p1,p2])
        self.axes.set_ylabel("Error %")
        self.axes.set_xlabel("Epoch")
        self.draw()


    @pyqtSlot(str)
    def on_saveFigure(self,filename):
        self.axes.figure.savefig(filename)

    @pyqtSlot()
    def on_clearFigure(self):
        self.axes.figure.clf(keep_observers=False)
    @pyqtSlot()
    def on_clearAxes(self):
        self.axes.cla()

    @pyqtSlot()
    def on_clearPlot(self):
        print("sas")
        self.p1.pop(0).remove()
        del self.p1


class StaticMplCanvas(MplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)



