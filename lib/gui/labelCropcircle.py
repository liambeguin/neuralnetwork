#!/usr/bin/env python3.4
from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')

from hiddenLayer import neuralNetworkWidget
from PyQt5 import QtCore,QtWidgets,QtSvg,QtGui
from PyQt5.QtGui import QTextCursor,QColor,QBrush,QPen,QPixmap,QPainter,QPainterPath,QRegion
from PyQt5.QtWidgets import QApplication, QMainWindow ,QWidget, QDesktopWidget, \
                QGridLayout,QHBoxLayout, \
                QGraphicsView,QGraphicsScene,QGraphicsRectItem, \
                QPushButton,QLabel,QPlainTextEdit,QComboBox, \
                QSpacerItem,QSizePolicy,QGraphicsPixmapItem

from PyQt5.QtCore import QRect,QRectF,pyqtSignal,pyqtSlot

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class hiddenLayer(QWidget):
    """ creating a hidden layer interface"""
    def __init__(self):
        super(hiddenLayer,self).__init__()
        self.layout=QGridLayout(self)
        
        pix=QtGui.QPixmap(os.getcwd() + "/ressource/icons/pluss.png")
#        painter=QPainter()
#        painter.begin()
#        painter.setRenderHint(QPainter.Antialiasing)
#        path=QPainterPath()
# 
#        path.addEllipse(64, 64, 32, 32)
#        painter.setClipPath(path)
#        painter.drawPixmap(64, 64, 32, 32,pix);
#        painter.end()

        self.i=1
        self.extendLabelPlus=ExtendedQLabel()
        self.extendLabelPlus.setPixmap(pix)


#        self.extendLabelPlus.setFixedSize(64,64)
        pix=QtGui.QPixmap(os.getcwd() + "/ressource/icons/minuss.png")
        self.extendLabelMinus=ExtendedQLabel()
        self.extendLabelMinus.setPixmap(pix)
        reg=QRegion(47,247,32,32,QRegion.Ellipse)
        self.extendLabelMinus.setMask(reg)
        self.extendLabelMinus.setStyleSheet("background: red")
                #"background-image: url(:/ressource/icons/minuss.png);"+


                #"border-style: outset;"+
                #"border-width: 2px;"+
                #"border-radius: 10px;"+
                #"border-color: beige;"+
                #"font: bold 14px;"+
                #"padding: 6px;")
        #self.extendLabelMinus.setStyleSheet("background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); ")
#        self.extendLabelMinus.setFixedSize(32,32)
        
        self.extendLabelTitle=QLabel("w{} h{}".format(self.extendLabelMinus.width(),self.extendLabelMinus.height()))
        self.layout.addWidget(self.extendLabelPlus,0,0,QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.extendLabelMinus,0,1,QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.extendLabelTitle,1,0,1,-1,QtCore.Qt.AlignHCenter)
        #self.layout.addWidget(QLabel("w{} h{}".format(self.extendLabelMinus.width(),self.extendLabelMinus.height())),2,0,1,-1,QtCore.Qt.AlignHCenter)
        #self.setFixedSize(190,90)

        #self.setFixedSize(100,100)


class ExtendedQLabel(QLabel):
    """Re implemented QLabel: clickable QLabel"""
    trigger=pyqtSignal()
    def __init__(self):
        super(ExtendedQLabel,self).__init__()
 
    def mouseReleaseEvent(self, ev):
        self.trigger.emit()
def main():
    app = QApplication(sys.argv)
    dw=QDesktopWidget()
    x=dw.width()
    y=dw.height()


    window = hiddenLayer()
    window.setFixedSize(x,y)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
