#!/usr/bin/python

from __future__ import unicode_literals

from lib.gui.extendedQLabel import clickableLabel

from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtGui import QRegion
from PyQt5.QtWidgets import QWidget, \
                QGridLayout, \
                QLabel
from PyQt5.QtCore import Qt,pyqtSignal,pyqtSlot

class neuronManagerWidget(QWidget):
    """ 
    neuron manager interface
    ----------------------
    structure
    +---------------------------------------------------+
    |          (+)            |            (-)          |
    +---------------------------------------------------|
    |                   (X) Neurones                    |
    +---------------------------------------------------+
    """
    def __init__(self):
        super(neuronManagerWidget,self).__init__()


        self.setFixedSize(100,60)
        self.i=1

        self.extendLabelPlus=clickableLabel(
                pixmap="/ressource/icons/pluss.png"
            #    color="grey"
            )
        self.extendLabelPlus.scaleRegion(8,2,34,34,QRegion.Ellipse)
        
        self.extendLabelMinus=clickableLabel(
                pixmap="/ressource/icons/minuss.png"
           #     color="yellow"
                )
        self.extendLabelMinus.scaleRegion(8,2,34,34,QRegion.Ellipse)
        

        self.extendLabelTitle=QLabel("{} Neurons".format(self.i))

        self.extendLabelPlus.setObjectName("plus")
        self.extendLabelMinus.setObjectName("minus")
        self.extendLabelTitle.setObjectName("title")
        
        # Layout     
        self.layout=QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.extendLabelPlus ,0,0     ,Qt.AlignHCenter)
        self.layout.addWidget(self.extendLabelMinus,0,1     ,Qt.AlignHCenter)
        self.layout.addWidget(self.extendLabelTitle,1,0,-1,-1,Qt.AlignHCenter)
        debug=0
        if debug:
            self.setStyleSheet(
                    "border-style: outset; "+
                    "border-width: 1px;    "+
                    "border-color: green;  "
                    )
