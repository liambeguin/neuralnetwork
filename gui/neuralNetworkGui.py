#!/usr/bin/env python3.4

from __future__ import unicode_literals
import sys
import os

from neuralNetworkGraphicsView import drawNeuralNetworkWidget
from neuronManager import neuronManagerWidget
from extendedQLabel import clickableLabel


from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtGui import QTextCursor,QColor,QPixmap,QPainter,QPainterPath,QRegion
from PyQt5.QtWidgets import QApplication, QMainWindow ,QWidget, QDesktopWidget, \
                QGridLayout,QHBoxLayout, \
                QGraphicsView,QGraphicsScene,QGraphicsRectItem, \
                QPushButton,QLabel,QPlainTextEdit,QComboBox, \
                QSpacerItem,QSizePolicy,QGraphicsPixmapItem

from PyQt5.QtCore import Qt,pyqtSignal,pyqtSlot

class centralWidget(QWidget):
    """ 
    central widget for the main window
    ----------------------------------
    structure
    +-----------------------------------------------------------------------------+
    |                                   Settings                                  |
    +-----------------------------------------------------------------------------|
    |                                 Layer Manager                               |
    +-----------------------------------------------------------------------------+
    |                                Hidden Layers                                |
    +--------------------------------------+--------------------------------------+
    |          NN graphicsview             |              Graphs                  |
    +--------------------------------------+--------------------------------------+
    """

    hiddenLayerCreated     = pyqtSignal(int)
    drawHiddenLayerNeurone = pyqtSignal(int,int)


    def __init__(self):
        super(centralWidget, self).__init__()
        scr=QDesktopWidget()
        self.w=scr.width()
        self.h=scr.height()
        self.initUi()

        #self.dc = MyDynamicMplCanvas(self.widget, width=5, height=4, dpi=100)
        #self._Layout.addWidget(self.dc,0,0)

    def initUi(self):

        self.gridLayout=QGridLayout(self)
################################################################################ 
#
#       Settings top widget 0,0
#
################################################################################ 
        self.settingsWidget=QWidget()
        self.settingsWidget.setStyleSheet(
                "border-style: outset; "+
                "border-width: 1px;    "+
                "border-color: red;  "
                )

        
        self.settingsLayout=QGridLayout(self.settingsWidget)
        
        self.reloadLabel=clickableLabel()
        self.reloadLabel.setPixmap(QtGui.QPixmap(os.getcwd() + "/ressource/icons/reload.png"))
        self.settingsLayout.addWidget(self.reloadLabel,0,0,0,1)
        
        self.pauseLabel=clickableLabel()
        self.pauseLabel.setPixmap(QtGui.QPixmap(os.getcwd() + "/ressource/icons/pause.png"))
        self.settingsLayout.addWidget(self.pauseLabel,0,1,0,1)
        
        self.playLabel=clickableLabel()
        self.playLabel.setPixmap(QtGui.QPixmap(os.getcwd() + "/ressource/icons/play.png"))
        self.settingsLayout.addWidget(self.playLabel,0,2,0,1)
        
        self.iterationsLabel=QLabel("Iterations")
        self.iterationsInitValue=0
        self.iterationsComboBox=QLabel("{}".format(self.iterationsInitValue))
        self.settingsLayout.addWidget(self.iterationsLabel,0,4)
        self.settingsLayout.addWidget(self.iterationsComboBox,1,4)

        self.learningRateLabel=QLabel("Leanrning rate")
        self.learningRateComboBox=QComboBox()
        self.settingsLayout.addWidget(self.learningRateLabel,0,5)
        self.settingsLayout.addWidget(self.learningRateComboBox,1,5)

        self.activationLabel=QLabel("Activation")
        self.activationComboBox=QComboBox()
        self.settingsLayout.addWidget(self.activationLabel,0,6)
        self.settingsLayout.addWidget(self.activationComboBox,1,6)

        self.regularizationLabel=QLabel("Regularization")
        self.regularizationComboBox=QComboBox()
        self.settingsLayout.addWidget(self.regularizationLabel,0,7)
        self.settingsLayout.addWidget(self.regularizationComboBox,1,7)

        self.regularizationRateLabel=QLabel("Regularization rate")
        self.regularizationRateComboBox=QComboBox()
        self.settingsLayout.addWidget(self.regularizationRateLabel,0,8)
        self.settingsLayout.addWidget(self.regularizationRateComboBox,1,8)

################################################################################ 
#
#       Layers Mangaer  widget 1,0
#
################################################################################
        self.layerManager=QWidget()

        self.layerManager.setStyleSheet(
                "border-style: outset; "+
                "border-width: 1px;    "+
                "border-color: red;  "
                )
        self.layerManager.setFixedSize((self.w*2)//3,70)
        self.layerManagerLayout=QHBoxLayout(self.layerManager)
        #Features
        self.featuresManager =QLabel("Features")
        
        #Number hidden layout
        self.hiddenManagerLayer=QWidget()
        self.hiddenManagerLayer.setFixedSize((self.w//6)+80,50)
        self.hiddenManagerLayerLayout=QHBoxLayout(self.hiddenManagerLayer)
        
        self.i=0
        self.extendLabelHiddenManagerTitle=QLabel("{} HIDDEN LAYER".format(self.i))
        
        self.extendLabelHiddenManagerPlus=clickableLabel(pixmap="/ressource/icons/pluss.png")
        self.extendLabelHiddenManagerPlus.scaleRegion(48,8,36,34,QRegion.Ellipse)
        
        self.extendLabelHiddenManagerMinus=clickableLabel("/ressource/icons/minuss.png")
        self.extendLabelHiddenManagerMinus.scaleRegion(48,8,36,34,QRegion.Ellipse)
        self.hiddenManagerLayerLayout.setSpacing(0)
        self.hiddenManagerLayerLayout.setContentsMargins(0,0,0,0)
        
        self.hiddenManagerLayerLayout.addWidget(self.extendLabelHiddenManagerPlus)
        self.hiddenManagerLayerLayout.addWidget(self.extendLabelHiddenManagerMinus)
        self.hiddenManagerLayerLayout.addWidget(self.extendLabelHiddenManagerTitle)
        
        #Output
        self.outputManager = QLabel("Output")
        #Setup layer manager layout
        self.layerManagerLayout.addWidget(self.featuresManager,Qt.AlignLeft)
        self.layerManagerLayout.addWidget(self.hiddenManagerLayer,Qt.AlignHCenter)
        self.layerManagerLayout.addWidget(self.outputManager,Qt.AlignLeft)

################################################################################ 
#
#       Hidden Layers widget 2,0
#
################################################################################ 
        self.hiddenLayers=QWidget()       
        self.hiddenLayers.setStyleSheet(
                "border-style: outset; "+
                "border-width: 1px;    "+
                "border-color: red;  "
                )
        self.hiddenLayersLayout=QHBoxLayout(self.hiddenLayers)

################################################################################ 
#
#       NeuralNetwork Widget 3,0
#
################################################################################ 
        self.graphicsView=QGraphicsView()
        self.hm=[]

################################################################################ 
#
#       Debug 3,0
#
################################################################################ 
        self.plainTextEdit=QPlainTextEdit()
        self.plainTextEdit.setReadOnly(True)
        self.textCursor=QTextCursor()

################################################################################ 
#
#       Main Layout 
#
################################################################################ 
        self.spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding,QSizePolicy.Minimum)
        
        self.span=1
        self.gridLayout.addItem(    self.spacerItem     ,0,0,self.span,self.span)
        self.gridLayout.addWidget(  self.settingsWidget ,0,1,self.span,self.span,QtCore.Qt.AlignHCenter)
        self.gridLayout.addItem(    self.spacerItem     ,0,2,self.span,self.span)

        self.gridLayout.addItem(    self.spacerItem     ,1,0,self.span,self.span)
        self.gridLayout.addWidget(  self.layerManager   ,1,1,self.span,self.span,QtCore.Qt.AlignHCenter)
        self.gridLayout.addItem(    self.spacerItem     ,1,2,self.span,self.span)
        
        self.gridLayout.addItem(    self.spacerItem     ,2,0,self.span,self.span)
        self.gridLayout.addWidget(  self.hiddenLayers   ,2,1,self.span,self.span)
        self.gridLayout.addItem(    self.spacerItem     ,2,2,self.span,self.span)

        self.gridLayout.addWidget(  self.graphicsView   ,3,0,1,-1)
        self.gridLayout.addWidget(  self.plainTextEdit  ,4,0,2,-1)

################################################################################ 
#
#       Connection signal slot
#
################################################################################
        self.extendLabelHiddenManagerPlus.trigger.connect(self.on_extendLabelHiddenManagerPlusClicked)
        self.extendLabelHiddenManagerMinus.trigger.connect(self.on_extendLabelHiddenManagerMinusClicked)
        self.hiddenLayerCreated.connect(self.on_hiddenLayerCreated)
        self.drawHiddenLayerNeurone.connect(self.on_drawHiddenLayerNeurone)

#------------------------------------------------------------------------------- 
#
#       Hidden slots
#
#-------------------------------------------------------------------------------
    @pyqtSlot(int)
    def on_hiddenLayerCreated(self,val):
        #self.plainTextEdit.insertPlainText("{}\n".format(val))
        hLL=self.hiddenLayersLayout
        w=hLL.itemAt(val-1).widget()
        w.extendLabelPlus.trigger.connect(lambda: self.on_extendLabelHiddenPlusClicked(val))
        w.extendLabelMinus.trigger.connect(lambda: self.on_extendLabelHiddenMinusClicked(val))

    # not @pyqtSlot(int) because of lambda function when trigger is called
    @pyqtSlot()
    def on_extendLabelHiddenPlusClicked(self,val):
        hLL=self.hiddenLayersLayout
        w=hLL.itemAt(val-1).widget()
        w.i+=1 
        w.extendLabelTitle.setText("{} Neurones".format(w.i))
        self.drawHiddenLayerNeurone.emit(val,w.i)

    # not @pyqtSlot(int) because of lambda function when trigger is called
    @pyqtSlot()
    def on_extendLabelHiddenMinusClicked(self,val):
        hLL=self.hiddenLayersLayout
        w=hLL.itemAt(val-1).widget()
        if w.i>1:
            w.i-=1 
            w.extendLabelTitle.setText("{} Neurones".format(w.i))
            self.drawHiddenLayerNeurone.emit(val,w.i)
            
#------------------------------------------------------------------------------- 
#
#       Hidden Manager slots
#
#-------------------------------------------------------------------------------
    @pyqtSlot()
    def on_extendLabelHiddenManagerPlusClicked(self):
        if self.i <10:
            self.i+=1
            #self.extendLabelHiddenManagerTitle.setText("{} HIDDEN LAYER".format(self.i))
            hLL=self.hiddenLayersLayout
            hLL.addWidget(neuronManagerWidget())
            
            self.plainTextEdit.insertPlainText("Add -- layer number:{}--i={}\n".format(hLL.count(),self.i))
            self.hiddenLayerCreated.emit(self.i)
            self.drawHiddenLayerNeurone.emit(self.i,1)
    
    @pyqtSlot()
    def on_extendLabelHiddenManagerMinusClicked(self):
        if self.i > 0:
            self.i-=1
            #self.extendLabelHiddenManagerTitle.setText("{} HIDDEN LAYER".format(self.i))
            hLL=self.hiddenLayersLayout
            w=hLL.itemAt(hLL.count()-1).widget().deleteLater()
            #self.plainTextEdit.insertPlainText("Remove -- layer number{}--i={}\n".format(self.hiddenLayersLayout.count(),self.i))
            self.drawHiddenLayerNeurone.emit(self.i,0)

#------------------------------------------------------------------------------- 
#
#       drawing hidden layer  slot
#
#-------------------------------------------------------------------------------
    @pyqtSlot(int,int)
    def on_drawHiddenLayerNeurone(self,layer,neurone):
        #self.plainTextEdit.clear()
        self.plainTextEdit.insertPlainText("layer {}, neurone{} --len {}\n".format(layer,neurone,len(self.hm)))
        if len(self.hm)<layer:
            self.hm.append(neurone)

        ## when removing (minus clicked)
        elif not neurone:
            del self.hm[layer]
        else:
            self.hm[layer-1]=neurone
            self.plainTextEdit.insertPlainText("==rewrite {}\n")
        
        self.plainTextEdit.insertPlainText("len {}\n".format(self.hm))
        
        
        # focus at end of debug 
        self.textCursor=self.plainTextEdit.textCursor()
        self.textCursor.movePosition(QTextCursor.End)
        self.plainTextEdit.setTextCursor(self.textCursor)
        
        hl=drawNeuralNetworkWidget(20,120,self.hm)
        #draw if 2 layers
        if len(self.hm)>1:
            hl.drawNeurones()
            hl.drawLines()
        self.graphicsView.setScene(hl.getScene())
        
#------------------------------------------------------------------------------- 
#
#       Test slot
#
#-------------------------------------------------------------------------------
    @pyqtSlot(int)
    def on_test(self,val):
        self.plainTextEdit.insertPlainText("on_test slot -- item num: {}\n".format(val))

    def buttonClicked(self):

        QtCore.QCoreApplication.instance().quit()


class MainWindow(QMainWindow): #, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUi()
        # Set up the user interface from Designer.
    def initUi(self):

        self.setCentralWidget(centralWidget())




def main():
    app = QApplication(sys.argv)

    dw=QDesktopWidget()
    x=dw.width()
    y=dw.height()

    window = MainWindow()
    #window.setFixedSize(scr_x,scr_y)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
