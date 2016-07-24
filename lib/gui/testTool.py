#!/usr/bin/python
from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
# Make sure that we are using QT5

from mplCanvas import DynamicMplCanvas
from mplCanvas import StaticMplCanvas
from PyQt5 import QtCore,QtWidgets,QtSvg,QtGui
from PyQt5.QtGui import QTextCursor,QColor,QBrush,QPen,QPixmap,QPainter,QPainterPath,QRegion
from PyQt5.QtWidgets import QApplication, QMainWindow ,QWidget,QListWidget,QListWidgetItem, QDesktopWidget, \
                QGridLayout,QHBoxLayout, \
                QGraphicsView,QGraphicsScene,QGraphicsRectItem, \
                QPushButton,QLabel,QPlainTextEdit,QComboBox, \
                QSpacerItem,QSizePolicy,QGraphicsPixmapItem

from PyQt5.QtCore import QRect,QRectF,pyqtSignal,pyqtSlot


class listWidget(QListWidgetItem):
    def __init__(self):
        super(QListWidgetItem,self).__init__()
        pass


class MainWindow(QMainWindow):
    """Re implemented QLabel: clickable QLabel"""
    currentIndexChanged=pyqtSignal()
    sig=pyqtSignal(list)
    saveFigure   = pyqtSignal(str)
    clearFigure  = pyqtSignal()
    clearPlot    = pyqtSignal()

    #trigger=pyqtSignal(str)
    def __init__(self):
        super(QMainWindow,self).__init__()
        self.cw = QWidget()
        self.gl = QGridLayout(self.cw)
        
        self.pt=QPlainTextEdit()       
        self.widget=QWidget()
        #self.dc=MyStaticMplCanvas(self.widget)

        self.lay=QComboBox()

        self.dc1=DynamicMplCanvas()
        self.dc1.color='green'
        #self.dc2=DynamicMplCanvas(self.widget)
        #self.dc3=DynamicMplCanvas(self.widget)
        #self.dc4=DynamicMplCanvas(self.widget)
        
        #self.lis=[1,2,3,4]


        #self.lis=[self.dc1,self.dc2,self.dc3,self.dc4]


        self.dc1.setObjectName("dc1")
        #self.dc2.setObjectName("dc2")
        #self.dc3.setObjectName("dc3")
        #self.dc4.setObjectName("dc4")
        
        #self.lis.append(str(self.findChild(MyDynamicMplCanvas,"dc")))
        #self.lis.addItem(self.dc2)
        #self.lis.addItem(self.dc3)
        #self.lis.addItem(self.dc4)
        
        
        
        self.lay=QComboBox()
        self.lay.insertItem(0,"dc1")
        self.lay.insertItem(1,"dc2")
        self.lay.insertItem(2,"dc3")
        self.lay.insertItem(3,"dc4")
        
        


        self.c=0
        self.b=QComboBox()
        self.b.setObjectName("aaa")
        self.gl.addWidget(self.lay,0,0) 
        self.gl.addWidget(self.dc1,1,0) 
        #self.gl.addWidget(self.pt ,self.c+3,0)
        #self.gl.addWidget(self.dc1 ,self.c+2,0)
        #self.gl.addWidget(self.b,self.c+1,0)
        self.setCentralWidget(self.cw)
        self.p=None
        self.sig.connect(self.dc1.update_figure2)
        self.lay.currentIndexChanged.connect(self.on_newgraph)       
        self.saveFigure.connect(self.dc1.on_saveFigure)
        self.clearFigure.connect(self.dc1.on_clearAxes)
        self.clearPlot.connect(self.dc1.on_clearPlot)
        #self.lay.currentIndexChanged.emit(0)
    #@pyqtSlot(str)
    def on_newgraph(self,val):
        #self.pt.insertPlainText("{}\n".format(val))
        tmp=val
        print(val)
        i=0
        while i<10:

            self.sig.emit([i,i*2])    
            i+=1
            
        if val == 3: 
            self.saveFigure.emit("graph.png")
        elif val == 2:
            self.clearPlot.emit()

    


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
