#!/usr/bin/env python3.4
from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
from mplCanvas import MyDynamicMplCanvas
from PyQt5 import QtCore,QtWidgets,QtSvg,QtGui
from PyQt5.QtGui import QTextCursor,QColor,QBrush,QPen,QPixmap,QPainter,QPainterPath,QRegion
from PyQt5.QtWidgets import QApplication, QMainWindow ,QWidget, QDesktopWidget, \
                QGridLayout,QHBoxLayout, \
                QGraphicsView,QGraphicsScene,QGraphicsRectItem, \
                QPushButton,QLabel,QPlainTextEdit,QComboBox, \
                QSpacerItem,QSizePolicy,QGraphicsPixmapItem

from PyQt5.QtCore import QRect,QRectF,pyqtSignal,pyqtSlot


class MainWindow(QMainWindow):
    """Re implemented QLabel: clickable QLabel"""
    trigger=pyqtSignal()
    def __init__(self):
        super(QMainWindow,self).__init__()
        self.cw=QWidget()
        self.gl=QGridLayout(self.cw)
        
        self.pt=QPlainTextEdit()       
        self.widget=QWidget()
        self.dc=MyDynamicMplCanvas(self.widget)
        
        self.gl.addWidget(self.dc,0,0)
        self.gl.addWidget(self.pt,1,0)
        self.setCentralWidget(self.cw)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.dc.update_figure)
        r=random.randint(20,100)
        self.pt.insertPlainText("{}\n".format(r))
        timer.start(r)



    


def main():
    app = QApplication(sys.argv)
    dw=QDesktopWidget()
    x=dw.width()
    y=dw.height()


    window = MainWindow()
    window.setFixedSize(x,y)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
