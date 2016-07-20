#!/usr/bin/env python3.4

from __future__ import unicode_literals
import sys
import os

from lib.gui.neuralNetworkGraphicsView import drawNeuralNetworkWidget
from lib.gui.neuronManager import neuronManagerWidget
from lib.gui.extendedQLabel import clickableLabel
from lib.gui.mplCanvas import DynamicMplCanvas
from lib.gui.mplCanvas import StaticMplCanvas

from lib.network.cost import CostFunction
from lib.network.activation import ActivationFunction
from lib.network.regularization import RegularizationFunction

from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtGui import QTextCursor,QColor,QPixmap,QPainter,QPainterPath,QRegion
from PyQt5.QtWidgets import QApplication, QMainWindow ,QWidget, QDesktopWidget, \
                QGridLayout, QHBoxLayout, QVBoxLayout, \
                QGraphicsView, QGraphicsScene, QGraphicsRectItem, \
                QPushButton, QLabel, QPlainTextEdit, QComboBox, \
                QSpacerItem, QSizePolicy, QGraphicsPixmapItem

from PyQt5.QtCore import Qt,pyqtSignal,pyqtSlot

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

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

    layerCreated      = pyqtSignal(int)
    drawNeuron              = pyqtSignal(int,int)
    textChanged             = pyqtSignal()

    def __init__(self):
        super(centralWidget, self).__init__()
        scr=QDesktopWidget()
        self.w=scr.width()
        self.h=scr.height()
        self.debug=1
        self.initUi()

        #self.dc = MyDynamicMplCanvas(self.widget, width=5, height=4, dpi=100)
        #self._Layout.addWidget(self.dc,0,0)

    def initUi(self):

        self.gridLayout=QGridLayout(self)

        self.spacerItem = QSpacerItem(500, 20, QSizePolicy.Expanding,QSizePolicy.Minimum)
################################################################################ 
#
#       Settings top widget 0,0
#
################################################################################ 
        self.settingsWidget=QWidget()
        if self.debug:
            self.settingsWidget.setStyleSheet(
                    "border-style: outset; "+
                    "border-width: 1px;    "+
                    "border-color: red;  "
                    )
        
        self.settingsLayout = QGridLayout(self.settingsWidget)
        
# 0-----------------------------------------------------------------------------
        self.reloadLabel = clickableLabel(pixmap="/ressource/icons/reload.png")
        self.settingsLayout.addWidget(self.reloadLabel                  ,0,0,0,1)
# 1-----------------------------------------------------------------------------
        self.pauseLabel = clickableLabel(pixmap="/ressource/icons/pause.png")
        self.settingsLayout.addWidget(self.pauseLabel                   ,0,1,0,1)
# 2-----------------------------------------------------------------------------
        self.playLabel=clickableLabel(pixmap="/ressource/icons/play.png")
        self.settingsLayout.addWidget(self.playLabel                    ,0,2,0,1)
# 4-----------------------------------------------------------------------------
        self.iterationsInitValue = 0
        self.iterationsComboBox  = QLabel("{}".format(self.iterationsInitValue))
        iterationsLabel          = QLabel("Iterations")
        
        self.settingsLayout.addWidget(iterationsLabel                   ,0,4)
        self.settingsLayout.addWidget(self.iterationsComboBox           ,1,4)
# 5-----------------------------------------------------------------------------
        self.learningRateComboBox = QComboBox()
        learningRateLabel         = QLabel("Leanrning rate")
        learningRateStrList       = ["0.00001","0.0001","0.001","0.003",\
                                "0.01","0.03","0.1","0.3","1","3","10"]
        
        self.learningRateComboBox.addItems(learningRateStrList)
        
        self.settingsLayout.addWidget(learningRateLabel                 ,0,5)
        self.settingsLayout.addWidget(self.learningRateComboBox         ,1,5)
# 6-----------------------------------------------------------------------------
        self.activationComboBox=QComboBox()
        activationLabel=QLabel("Activation")
        activationStrList=[]
        
        for key in ActivationFunction.activation_functions:
            activationStrList.append(str(key))
        self.activationComboBox.addItems(activationStrList)
        self.settingsLayout.addWidget(activationLabel                   ,0,6)
        self.settingsLayout.addWidget(self.activationComboBox           ,1,6)
# 7-----------------------------------------------------------------------------
        self.regularizationComboBox = QComboBox()
        regularizationLabel         = QLabel("Regularization")
        regularizationStrList       = []
        
        for key in RegularizationFunction.regularization_functions:
            regularizationStrList.append(str(key))
        self.regularizationComboBox.addItems(regularizationStrList)
        
        self.settingsLayout.addWidget(regularizationLabel               ,0,7)
        self.settingsLayout.addWidget(self.regularizationComboBox       ,1,7)
# 8-----------------------------------------------------------------------------
        self.regularizationRateComboBox = QComboBox()
        regularizationRateLabel         = QLabel("Regularization rate")
        regularizationRateStrList       = ["0","0.001","0.003","0.01",
                                        "0.03","0.1","0.3","1","3","10"]
        self.regularizationRateComboBox.addItems(regularizationRateStrList)
        
        self.settingsLayout.addWidget(regularizationRateLabel           ,0,8)
        self.settingsLayout.addWidget(self.regularizationRateComboBox   ,1,8)
# 9-----------------------------------------------------------------------------
        self.costComboBox = QComboBox()
        costLabel         = QLabel("Cost function")
        costStrList       = []
        
        for key in CostFunction.cost_functions:
            costStrList.append(str(key))
        self.costComboBox.addItems(costStrList)

        self.settingsLayout.addWidget(costLabel                         ,0,9)
        self.settingsLayout.addWidget(self.costComboBox                 ,1,9)
################################################################################ 
#
#       Layers Mangaer  widget 1,0
#
#    +-----------+--------------------------------+--------+
#    | Features  |     +  -    X hidden layers    |  out   |
#    +-----------+--------------------------------+--------+
################################################################################
        self.manager = QWidget()
        
        if self.debug:
            self.manager.setStyleSheet(
                    "border-style: outset; "+
                    "border-width: 1px;    "+
                    "border-color: red;  "
                    )

        self.managerLayout = QHBoxLayout(self.manager)
        #Features
        self.featuresManager         = QWidget()
        self.featuresManagerLayout   = QVBoxLayout(self.featuresManager)
        self.featuresManagerLabel    = QLabel("Features")
        self.featuresManagerComboBox = QComboBox()
        self.featuresManagerList     = ["","40","50","60"]

        self.featuresManagerComboBox.addItems(self.featuresManagerList)
        self.featuresManagerLayout.addWidget( self.featuresManagerLabel)
        self.featuresManagerLayout.addWidget( self.featuresManagerComboBox)
        self.featuresManagerLayout.setSpacing(0)
        self.featuresManagerLayout.setContentsMargins(0,0,0,0)
        #Number hidden layout
        self.hiddenManager = QWidget()
        #self.hiddenManager.setFixedSize(500,50)
        self.hiddenManagerLayout = QHBoxLayout(self.hiddenManager)
        
        self.countl = 0
        #label
        self.hiddenManagerTitle = QLabel("{} HIDDEN LAYER".format(self.countl))
        #Buttons
        self.hiddenManagerPlus = clickableLabel(pixmap="/ressource/icons/pluss.png")
        self.hiddenManagerPlus.scaleRegion(48,8,36,34,QRegion.Ellipse)

        self.hiddenManagerMinus = clickableLabel("/ressource/icons/minuss.png")
        self.hiddenManagerMinus.scaleRegion(48,8,36,34,QRegion.Ellipse)
        
        self.hiddenManagerLayout.setSpacing(0)
        self.hiddenManagerLayout.setContentsMargins(0,0,0,0)

        self.hiddenManagerLayout.addItem   (self.spacerItem)
        self.hiddenManagerLayout.addWidget (self.hiddenManagerPlus)
        self.hiddenManagerLayout.addWidget (self.hiddenManagerMinus)
        self.hiddenManagerLayout.addWidget (self.hiddenManagerTitle)
        self.hiddenManagerLayout.addItem   (self.spacerItem)
        #Output
        self.outputManager         = QWidget()
        self.outputManagerLayout   = QVBoxLayout(self.outputManager)
        self.outputManagerLabel    = QLabel("Output")
        self.outputManagerComboBox = QComboBox()
        self.outputManagerList     = ["","9"]

        self.outputManagerComboBox.addItems(self.outputManagerList)
        self.outputManagerLayout.addWidget( self.outputManagerLabel)
        self.outputManagerLayout.addWidget( self.outputManagerComboBox)
        self.outputManagerLayout.setSpacing(0)
        self.outputManagerLayout.setContentsMargins(0,0,0,0)
        #self.outputManager.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #Setup layer manager layout
        self.managerLayout.addWidget(self.featuresManager)
        self.managerLayout.addWidget(self.hiddenManager)
        self.managerLayout.addWidget(self.outputManager,Qt.AlignRight)

################################################################################ 
#
#       Layers widget 2,0
#
#    +-----+------------------------------------+-----+ <-layers
#    |-----|+----------------------------------+|-----|
#    |-----||                               <------------- hidden layers
#    | inp ||        8x hidden layers          || out |
#    | + - ||        8x + -                    || + - |
#    |-----|+----------------------------------+|-----|
#    +-----+------------------------------------+-----+
#
################################################################################ 
    
        
        self.hiddenLayers       = QWidget()
        self.hiddenLayersLayout = QHBoxLayout(self.hiddenLayers)       
        
        #self.hiddenLayersLayout.addItem(self.spacerItem)
        self.hiddenLayersLayout.setSpacing(0)
        self.hiddenLayersLayout.setContentsMargins(0,0,0,0)
       

        self.layers         = QWidget()
        self.layersLayout   = QHBoxLayout(self.layers)
        self.inpLayer       = neuronManagerWidget()
        self.outpLayer      = neuronManagerWidget()

        self.layersLayout.addWidget(self.hiddenLayers,QSizePolicy.Expanding)

        self.layersLayout.setSpacing(0)
        self.layersLayout.setContentsMargins(0,0,0,0)
        
        if self.debug:
            self.layers.setStyleSheet(
                    "border-style: outset; "+
                    "border-width: 1px;    "+
                    "border-color: red;  "
                    )
################################################################################ 
#
#       NeuralNetwork Widget 3,0
#
################################################################################ 
        self.graphicsView = QGraphicsView()
        #hidden manager: list layer's neurons
        self.hm = []
################################################################################ 
#
#        Matplotlib canvas 3,1
#
################################################################################
        self.widget = QWidget()
        self.dynamicCanvas = DynamicMplCanvas(self.widget)
################################################################################ 
#
#       Debug 4,0
#
################################################################################ 
        self.plainTextEdit = QPlainTextEdit()
        self.textCursor    = QTextCursor()
        self.plainTextEdit.setReadOnly(True)

        self.plainTextEdit.insertPlainText("w={} h={}\n".format(self.w,self.h))
################################################################################ 
#
#       Main Layout 
#
################################################################################ 
        # screen resolution
        if self.w>1920:
            self.manager.setFixedSize           ((1920*2)//3,70)
            self.hiddenManager.setMaximumWidth  ((1920*2)//3)
            self.hiddenLayers.setFixedWidth     ((1920*2)//3)
            self.graphicsView.setFixedWidth     ((1920*2)//3)
            self.settingsWidget.setFixedWidth   ((1920*2)//3)
        else:
            self.manager.setFixedSize           ((self.w*2)//3,70)
            self.hiddenManager.setMaximumWidth  ((self.w*2)//3)
            self.layers.setFixedWidth           ((self.w*2)//3)
            self.graphicsView.setFixedWidth     ((self.w*2)//3)
            self.settingsWidget.setFixedWidth   ((self.w*2)//3)
        
        self.span=1
        self.gridLayout.addWidget(  self.settingsWidget ,0,0,self.span,self.span,Qt.AlignLeft)
        self.gridLayout.addWidget(  self.manager        ,1,0,self.span,self.span,Qt.AlignLeft)
        self.gridLayout.addWidget(  self.layers         ,2,0,self.span,self.span,Qt.AlignLeft)
        self.gridLayout.addWidget(  self.graphicsView   ,3,0,Qt.AlignLeft)
        self.gridLayout.addWidget(  self.dynamicCanvas  ,3,1)
#        self.gridLayout.addWidget(  self.plainTextEdit  ,4,0,2,-1)
################################################################################ 
#
#       Create object name for slot
#
################################################################################

        self.inpLayer.setObjectName                   ('inp')
        self.outpLayer.setObjectName                  ('outp')
#QComboBox        
        self.learningRateComboBox.setObjectName       ('learningRate')
        self.activationComboBox.setObjectName         ('activation')
        self.regularizationComboBox.setObjectName     ('regularization')
        self.regularizationRateComboBox.setObjectName ('regularizationRate')
        self.costComboBox.setObjectName               ('cost')
################################################################################ 
#
#       Connection signal slot
#
################################################################################
        self.hiddenManagerPlus.trigger.connect                      (self.on_managerPlusClicked)
        self.hiddenManagerMinus.trigger.connect                     (self.on_managerMinusClicked)
        self.layerCreated.connect                                   (self.on_layerCreated)
        self.drawNeuron.connect                                     (self.on_drawNeuron)
#QComboxBox
        self.learningRateComboBox.currentIndexChanged.connect       (self.on_currentIndexChanged)
        self.activationComboBox.currentIndexChanged.connect         (self.on_currentIndexChanged)
        self.regularizationComboBox.currentIndexChanged.connect     (self.on_currentIndexChanged)
        self.regularizationRateComboBox.currentIndexChanged.connect (self.on_currentIndexChanged)
        self.costComboBox.currentIndexChanged.connect               (self.on_currentIndexChanged)
################################################################################ 
#
#       Init by emitting signal
#
################################################################################
#create input and output layer
        self.hiddenManagerPlus.trigger.emit()
        self.hiddenManagerPlus.trigger.emit()

        self.learningRateComboBox.currentIndexChanged.emit      (0)
        self.activationComboBox.currentIndexChanged.emit        (0)        
        self.regularizationComboBox.currentIndexChanged.emit    (0)    
        self.regularizationRateComboBox.currentIndexChanged.emit(0)
        self.costComboBox.currentIndexChanged.emit              (0)              

#------------------------------------------------------------------------------- 
#
#       Hidden slots
#
#-------------------------------------------------------------------------------
    @pyqtSlot()
    def on_currentIndexChanged(self):
        s = self.sender()
        if type(s) is QComboBox:
            logging.debug(
                "sender name {} current text:{}"
                .format(s.objectName(),s.currentText())
                )
        else:
            logging.debug(
                    "Error not a comboBox:{}"
                    .format(s.objectName())
                    )

    @pyqtSlot(int)
    def on_layerCreated(self,layer):
        """
        - layer=1 --> Features in layersLayout          (pos=0)
        - layer=2 --> Ouptut in layersLayout            (pos=2)
        - layer>2 --> hidden layers in layersLayout     (pos=1)
                  --> widgets are in hiddenLayersLayout (pos=layer-3)
        """
        #self.plainTextEdit.insertPlainText("{}\n".format(val))
        logging.debug(
                "on_hiddenLayerCreated layer ======={}"
                .format(layer)
                )
        #Features select
        if(layer==1):
            hLL = self.layersLayout
            w   = hLL.itemAt(layer-1).widget()
        #output    
        elif(layer==2):
            hLL = self.layersLayout
            w   = hLL.itemAt(layer).widget()
        else:
            hLL = self.hiddenLayersLayout
            w   = hLL.itemAt(layer-3).widget()
        w.extendLabelPlus.trigger.connect (lambda: self.on_layerPlusClicked(layer))
        w.extendLabelMinus.trigger.connect(lambda: self.on_layerMinusClicked(layer))

    # not @pyqtSlot(int) because of lambda function when trigger is called
    @pyqtSlot()
    def on_layerPlusClicked(self,layer):
        """
        - layer=1 --> Features in layersLayout          (pos=0)
        - layer=2 --> Ouptut in layersLayout            (pos=2)
        - layer>2 --> hidden layers in layersLayout     (pos=1)
                  --> widgets are in hiddenLayersLayout (pos=layer-3)
        """
        logging.debug(
                "Plus ---------------{}"
                .format(layer)
                )
        if(layer == 1):
            hLL = self.layersLayout
            w   = hLL.itemAt(layer-1).widget()
        #output    
        elif(layer == 2):
            hLL = self.layersLayout
            w   = hLL.itemAt(layer).widget()
        else:
            hLL = self.hiddenLayersLayout
            w   = hLL.itemAt(layer-3).widget()
        w.i += 1 
        w.extendLabelTitle.setText("{} Neurones".format(w.i))
        self.drawNeuron.emit(layer,w.i)

    # not @pyqtSlot(int) because of lambda function when trigger is called
    @pyqtSlot()
    def on_layerMinusClicked(self,layer):
        """when minus is clicked from input or hidden or outpu"""
        if(layer == 1):
            hLL = self.layersLayout
            w   = hLL.itemAt(layer-1).widget()
        #output    
        elif(layer == 2):
            hLL = self.layersLayout
            w   = hLL.itemAt(layer).widget()
        else:
            hLL = self.hiddenLayersLayout
            w   = hLL.itemAt(layer-3).widget()

        if w.i > 1:
            w.i -= 1 
            w.extendLabelTitle.setText("{} Neurones".format(w.i))
            self.drawNeuron.emit(layer,w.i)
            
#------------------------------------------------------------------------------- 
#
#       Hidden Manager slots
#
#-------------------------------------------------------------------------------
    @pyqtSlot()
    def on_managerPlusClicked(self):
        """ 
        - First item is the features layer
        - Second is the output layer
        - others are the hidden layers
        Each layer start with 1 neuron
        """
        if self.countl < 10:
            self.countl += 1
            hLL = self.hiddenLayersLayout
            
            if(self.countl == 1):
                self.layersLayout.insertWidget(0,neuronManagerWidget(),Qt.AlignLeft)
            elif(self.countl == 2):
                self.layersLayout.insertWidget(2,neuronManagerWidget(),Qt.AlignRight)
            else:
                self.hiddenLayersLayout.addWidget(neuronManagerWidget(),Qt.AlignCenter)
                self.hiddenManagerTitle.setText("{} HIDDEN LAYER".format(self.countl-2))
            self.layerCreated.emit(self.countl)
            self.drawNeuron.emit(self.countl,1)
    
    @pyqtSlot()
    def on_managerMinusClicked(self):
        """
        Cannot delete features and output layers
        """
        if self.countl > 2:
            self.countl -= 1
            self.hiddenManagerTitle.setText("{} HIDDEN LAYER".format(self.countl-2))
            hLL = self.hiddenLayersLayout
            w   = hLL.itemAt(hLL.count()-1).widget().deleteLater()
            self.drawNeuron.emit(self.countl-1,0)

#------------------------------------------------------------------------------- 
#
#       drawing hidden layer  slot
#
#-------------------------------------------------------------------------------
    @pyqtSlot(int,int)
    def on_drawNeuron(self,layer,neuron):
        """
        Parameters: 
        layer  - the number of the targeted layer
        neuron - the number of neuron to draw
        """
        logging.debug(
            " drawNeuron layer {} -- neuron {}"
            .format(layer,neuron)
        )
#add new layer
        if len(self.hm)<layer:  
            self.hm.append(neuron)
        else:
        ## when removing (manager minus clicked)
            if not neuron:
                del self.hm[layer]
            #input is first    
            elif layer == 1:
                self.hm[0]=neuron
            #output is last    
            elif layer==2:
                self.hm[len(self.hm)-1]=neuron
            # hidden layers
            else:
                self.hm[layer-2] = neuron
        
        logging.debug("hm {}".format(self.hm))
        
        # focus at end of debug 
        self.textCursor = self.plainTextEdit.textCursor()
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
