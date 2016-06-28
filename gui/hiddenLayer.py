#!/usr/bin/env python3.4
from PyQt5 import QtCore,QtWidgets,QtSvg,QtGui

from PyQt5.QtGui import QTextCursor,QColor,QBrush,QPen
from PyQt5.QtWidgets import QApplication, QMainWindow ,QWidget,QGridLayout,QGraphicsView,QGraphicsScene,QGraphicsRectItem
from PyQt5.QtCore import QRect,QRectF



class neuralNetworkWidget():
    def __init__(self,neurone_dimension,distance,layer):
        self.di=distance
        self.nd=neurone_dimension
        self.scene=QGraphicsScene()
        self.l=self.setLayer(layer)
        self.p=self.lineStyle()


    def lineStyle(self):
   
        pen=QPen()
        #pen.setStyle(QtCore.Qt.DashLine)
        pen.setWidth(0.5)
        pen.setBrush(QtCore.Qt.red)
        pen.setCapStyle(QtCore.Qt.RoundCap);
        pen.setJoinStyle(QtCore.Qt.RoundJoin)
        return pen


    def getScene(self):
        return self.scene
    
    def setLayer(self,layer):
        if len(layer)<2:
            print("Error layer size must be greater ")
        else:
            return layer

    def setNeuroneDimension(self,neurone_dim):
        self.nd=neurone_dim
#
    def setDistance(self,distance):
        self.di=distance

    
    def drawNeurones(self):
        for l in range(len(self.l)):
            for n in range(self.l[l]):
#                self.plainTextEdit.insertPlainText ("l:{} n:{}\n".format(l,n))
                self.scene.addRect(QRectF((l)*self.di ,(n)*self.di , self.nd, self.nd))
    
    def drawLines(self):
        for c in range(len(self.l)): #nb layer
            #self.plainTextEdit.insertPlainText ("column c:{} value:{} len:{}\n".format(c,self.hm[c],len(self.hm)))
            for n in range(self.l[c]): #nb neurone
                #self.plainTextEdit.insertPlainText ("n        :{}\n".format(n))
                if c<len(self.l)-1:#do not draw for the last layer
                    #self.plainTextEdit.insertPlainText ("c         {}\n".format(c))
                    for m in range(self.l[c+1]): #layer +1
                        #self.plainTextEdit.insertPlainText ("m       {}\n".format(m))
                        self.scene.addLine(self.nd+(c*self.di),self.nd-(self.nd//2)+(n*self.di),self.di*(c+1),self.di*(m)+(self.nd//2),self.p)
