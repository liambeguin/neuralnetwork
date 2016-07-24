#!/usr/bin/python

from __future__ import unicode_literals
import os
import sys
sys.setrecursionlimit(10000)
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QColor,QPixmap,QRegion,QTransform
from PyQt5.QtCore import Qt,pyqtSignal,pyqtSlot


class clickableLabel(QLabel):
    """Re implemented QLabel: clickable QLabel
    Parameters:
    pixmap - path to image
    color  - color label
    
    """
    
    trigger = pyqtSignal()

    def __init__(self,pixmap="",color="",toolTip=""):
        super(clickableLabel,self).__init__()
        self.color  = color
        self.pixmap = pixmap
        if self.pixmap:
            self.setPixmap(QPixmap(os.path.dirname(os.path.abspath(__file__))  + self.pixmap))
        if self.color:
            self.setStyleSheet("background: {}".format(color))
       
        self.setAlignment(Qt.AlignCenter) 
        self.setToolTip(toolTip)
        self.setFixedSize(60,60)
    def get_pixmap(self):
        return str(self.pixmap)
    
    def set_pixmap(self,pixmap=""):
        #print(os.path.dirname(os.path.abspath(__file__)))
        self.pixmap = pixmap
        if self.pixmap:
            self.setPixmap(QPixmap(os.path.dirname(os.path.abspath(__file__))  + str(self.pixmap)))
    def rotate_pixmap(self,radius):
        p = QPixmap(os.path.dirname(os.path.abspath(__file__))  + str(self.pixmap)) 
        p = p.transformed(QTransform().rotate(radius))
        self.setPixmap(p)

    def mouseReleaseEvent(self, ev):
        self.trigger.emit()

    def scaleRegion(self,x,y,w,h,region):
        reg=QRegion(x,y,w,h,region)
        self.setMask(reg)
