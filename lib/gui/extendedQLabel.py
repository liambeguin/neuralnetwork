#!/usr/bin/python

from __future__ import unicode_literals
import os
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QColor,QPixmap,QRegion
from PyQt5.QtCore import Qt,pyqtSignal,pyqtSlot



class clickableLabel(QLabel):
    """Re implemented QLabel: clickable QLabel
    Parameters:
    pixmap - path to image
    color  - color label
    
    """
    
    trigger=pyqtSignal()

    def __init__(self,pixmap="",color=""):
        super(clickableLabel,self).__init__()
        if pixmap:
            self.setPixmap(QPixmap(os.path.dirname(os.path.abspath(__file__))  + pixmap))
        if color:
            self.setStyleSheet("background: {}".format(color))
       
        self.setAlignment(Qt.AlignCenter) 
    
    def mouseReleaseEvent(self, ev):
        self.trigger.emit()

    def scaleRegion(self,x,y,w,h,region):
        reg=QRegion(x,y,w,h,region)
        self.setMask(reg)
