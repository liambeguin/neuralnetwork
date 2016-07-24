#!/usr/bin/python

from __future__ import unicode_literals
import sys
import os
import time


import logging
LOG_FILENAME = 'example.log'
logging.basicConfig( filename=LOG_FILENAME, level=logging.DEBUG )

from lib.gui.neuralNetworkGraphicsView import drawNeuralNetworkWidget
from lib.gui.neuronManager import neuronManagerWidget
from lib.gui.extendedQLabel import clickableLabel
from lib.gui.mplCanvas import DynamicMplCanvas
from lib.gui.mplCanvas import StaticMplCanvas

import network

from lib import utils

from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtGui import QTextCursor, QColor,QPixmap,QPainter,QPainterPath,QRegion
from PyQt5.QtWidgets import QApplication,  QMainWindow ,QWidget, QDesktopWidget, \
                QGridLayout,  QHBoxLayout, QVBoxLayout, \
                QGraphicsView,  QGraphicsScene, QGraphicsRectItem, \
                QPushButton,  QLabel, QPlainTextEdit, QComboBox, QMessageBox,QCheckBox, \
                QSpacerItem,  QSizePolicy, QGraphicsPixmapItem, \
                QMenu,QFileDialog,QAction,QLineEdit, \
                QTabWidget,\
                qApp

from PyQt5.QtCore import QObject,QThread, Qt,pyqtSignal,pyqtSlot,QTimer


class centralWidget( QWidget ):
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
    threadId         = pyqtSignal(str)
    layerCreated     = pyqtSignal( int )
    drawNeuron       = pyqtSignal( int, int )
    textChanged      = pyqtSignal()
    updateParameters = pyqtSignal( dict )
    clicked          = pyqtSignal()
    stopped           = pyqtSignal()

    def __init__( self ):
        super( centralWidget,  self ).__init__()
        scr         = QDesktopWidget()
        self.w      = scr.width()
        self.h      = scr.height()
        self.debug  = 0
        self.initUi()

    def initUi( self ):

        self.gridLayout=QGridLayout( self )

        self.spacerItem = QSpacerItem( 500,  20, QSizePolicy.Expanding,QSizePolicy.Minimum )
        self.buttonName = ""
################################################################################ 
#
#       Settings top widget 0, 0
#
################################################################################ 
        self.settingsWidget = QWidget()
        self.settingsWidget.setObjectName("settings")
        self.settingsLayout = QGridLayout( self.settingsWidget )
        
        if self.debug:
            self.settingsWidget.setStyleSheet( 
                    "border-style: outset; "+
                    "border-width: 1px;    "+
                    "border-color: red;  "
                     )
        else:
            self.settingsWidget.setStyleSheet( 
                    "QWidget#settings "
                    "{border-style: outset;"+
                    "border-radius: 8px;   "+
                    "border-width: 2px;    "+
                    "border-color: black;}   "
                     )
# 0-----------------------------------------------------------------------------
        self.trainLabel = clickableLabel( pixmap="/ressource/icons/train.png",toolTip="train" )
        self.settingsLayout.addWidget( self.trainLabel                  , 0,0,0,1 )
# 1-----------------------------------------------------------------------------
        self.loadLabel = clickableLabel( pixmap="/ressource/icons/download.png",toolTip="load dataset" )
        self.settingsLayout.addWidget( self.loadLabel                   , 0,1,0,1 )
# 2-----------------------------------------------------------------------------
        self.playLabel=clickableLabel( pixmap="/ressource/icons/play.png",toolTip="init" )
        self.settingsLayout.addWidget( self.playLabel                    , 0,2,0,1 )
# 4-----------------------------------------------------------------------------
        self.iterationsInitValue = 0
        self.iterations          = QLabel( "{}".format(self.iterationsInitValue ))
        iterationsLabel          = QLabel( "Iterations" )
        
        self.settingsLayout.addWidget( iterationsLabel                   , 0,3 )
        self.settingsLayout.addWidget( self.iterations                   , 1,3 )
# 5-----------------------------------------------------------------------------
        self.learningRateLineEdit = QLineEdit()
        learningRateLabel         = QLabel( "Leanrning rate" )
        
        self.learningRateLineEdit.setFixedWidth(100)
        
        self.settingsLayout.addWidget( learningRateLabel                 , 0,4 )
        self.settingsLayout.addWidget( self.learningRateLineEdit         , 1,4 )
# 6-----------------------------------------------------------------------------
        self.activationComboBox=QComboBox()
        activationLabel=QLabel( "Activation" )
        activationStrList=[]
        
        self.activationComboBox.addItems( network.Network.options["activation"] )
        self.settingsLayout.addWidget( activationLabel                   , 0,5 )
        self.settingsLayout.addWidget( self.activationComboBox           , 1,5 )
# 7-----------------------------------------------------------------------------
        self.regularizationComboBox = QComboBox()
        regularizationLabel         = QLabel( "Regularization" )
        regularizationStrList       = []
        

        self.regularizationComboBox.addItems( network.Network.options["regularization"] )
        
        self.settingsLayout.addWidget( regularizationLabel               , 0,6 )
        self.settingsLayout.addWidget( self.regularizationComboBox       , 1,6 )
# 8-----------------------------------------------------------------------------
        self.regularizationRateLineEdit = QLineEdit()
        regularizationRateLabel         = QLabel( "Regularization rate" )
        self.regularizationRateLineEdit.setFixedWidth( 100 )
        
        self.settingsLayout.addWidget( regularizationRateLabel           , 0,7 )
        self.settingsLayout.addWidget( self.regularizationRateLineEdit   , 1,7 )
# 9-----------------------------------------------------------------------------
        self.costComboBox = QComboBox()
        costLabel         = QLabel( "Cost function" )
        costStrList       = []
        
        self.costComboBox.addItems( network.Network.options["cost"] )

        self.settingsLayout.addWidget( costLabel                         , 0,8 )
        self.settingsLayout.addWidget( self.costComboBox                 , 1,8 )
        

################################################################################ 
#
#       Layers Mangaer  widget 1, 0
#
#    +-----------+--------------------------------+--------+
#    | Features  |     +  -    X hidden layers    |  out   |
#    +-----------+--------------------------------+--------+
################################################################################
        self.manager = QWidget()
        self.manager.setObjectName("manager")
        
        if self.debug:
            self.manager.setStyleSheet( 
                    "border-style: outset; "+
                    "border-width: 1px;    "+
                    "border-color: red;  "
                     )
        else:
            self.manager.setStyleSheet( 
                    "QWidget#manager "
                    "{border-style: outset;"+
                    "border-radius: 8px;   "+
                    "border-width: 2px;    "+
                    "border-color: black;}   "
                     )

        self.managerLayout = QHBoxLayout( self.manager )
        #Features
        self.featuresManager         = QWidget()
        self.featuresManagerLabel    = QLabel( "Features" )
        self.featuresManagerList     = ["40","50","60"] 
        self.featuresManagerComboBox = QComboBox()
        self.featuresManagerComboBox.addItems( self.featuresManagerList )

        self.featuresManagerLabelNeuronFactor   = QLabel("Neuron factor")
        self.featuresManagerLineEdit            = QLineEdit()
        self.neuronFactor = 1



        self.featuresManagerLayout              = QGridLayout(self.featuresManager)
        self.featuresManagerLayout.addWidget( self.featuresManagerLabel             , 0, 0 )
        self.featuresManagerLayout.addWidget( self.featuresManagerComboBox          , 1, 0 )
        self.featuresManagerLayout.addWidget( self.featuresManagerLabelNeuronFactor , 0, 1 )
        self.featuresManagerLayout.addWidget( self.featuresManagerLineEdit          , 1, 1 )
        self.featuresManagerLayout.setSpacing( 0 )
        self.featuresManagerLayout.setContentsMargins( 0, 0, 0, 0 )
        #Number hidden layout
        self.hiddenManager = QWidget()
        #self.hiddenManager.setFixedSize( 500, 50 )
        self.hiddenManagerLayout = QHBoxLayout( self.hiddenManager )
        
        self.countl = 0
        #label
        self.hiddenManagerTitle = QLabel( "{} HIDDEN LAYER".format(self.countl ))
        #Buttons
        self.hiddenManagerPlus = clickableLabel( pixmap="/ressource/icons/add.png" )
        #self.hiddenManagerPlus.scaleRegion( 48, 8,36,34,QRegion.Ellipse )

        self.hiddenManagerMinus = clickableLabel( "/ressource/icons/remove.png" )
        #self.hiddenManagerMinus.scaleRegion( 48, 8,36,34,QRegion.Ellipse )
        
        self.hiddenManagerLayout.setSpacing( 0 )
        self.hiddenManagerLayout.setContentsMargins( 0, 0, 0, 0 )

        self.hiddenManagerLayout.addItem   ( self.spacerItem )
        self.hiddenManagerLayout.addWidget ( self.hiddenManagerPlus )
        self.hiddenManagerLayout.addWidget ( self.hiddenManagerMinus )
        self.hiddenManagerLayout.addWidget ( self.hiddenManagerTitle )
        self.hiddenManagerLayout.addItem   ( self.spacerItem )
        #Output
        self.outputManager         = QWidget()
        self.outputManagerLayout   = QGridLayout( self.outputManager )
        self.outputManagerLabel    = QLabel( "Output" )
        self.outputManagerValue    = 9
        self.outputManagerLabel    = QLabel("{}".format(self.outputManagerValue))
        self.sexCheckBox           = QCheckBox("man/woman")
        
        self.outputManagerLayout.addWidget( self.sexCheckBox       , 0, 0 )
        self.outputManagerLayout.addWidget( self.outputManagerLabel, 0, 1 )
        self.outputManagerLayout.addWidget( self.outputManagerLabel, 1, 1 )
        self.outputManagerLayout.setSpacing( 0 )
        self.outputManagerLayout.setContentsMargins( 0, 0, 0, 0 )
        #self.outputManager.setAlignment( QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter )
        #Setup layer manager layout
        self.managerLayout.addWidget( self.featuresManager )
        self.managerLayout.addWidget( self.hiddenManager )
        self.managerLayout.addWidget( self.outputManager, Qt.AlignRight )

################################################################################ 
#
#       Layers widget 2, 0
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
        self.hiddenLayersLayout = QHBoxLayout( self.hiddenLayers )       
        
        #self.hiddenLayersLayout.addItem( self.spacerItem )
        self.hiddenLayersLayout.setSpacing( 0 )
        self.hiddenLayersLayout.setContentsMargins( 0, 0, 0, 0 )
       

        self.layers         = QWidget()
        self.layersLayout   = QHBoxLayout( self.layers )
        self.inpLayer       = neuronManagerWidget()
        self.outpLayer      = neuronManagerWidget()

        self.layersLayout.addWidget( self.hiddenLayers, QSizePolicy.Expanding )

        self.layersLayout.setSpacing( 0 )
        self.layersLayout.setContentsMargins( 0, 0, 0, 0 )
        
        if self.debug:
            self.layers.setStyleSheet( 
                    "border-style: outset; "+
                    "border-width: 1px;    "+
                    "border-color: red;  "
                     )
################################################################################ 
#
#       NeuralNetwork itabWidget 3, 0
#
################################################################################ 
        
        self.err          = DynamicMplCanvas(pos=111,title='Error')
        self.cost         = DynamicMplCanvas(pos=111,title='Cost')
        self.canvas       = QWidget()
        self.canvasLayout = QGridLayout(self.canvas)
        self.canvasLayout.addWidget(self.err ,0,0)
        self.canvasLayout.addWidget(self.cost,0,1)



        self.graphicsView = QGraphicsView()
        #hidden manager: list layer's neurons
        self.hm = []
        self.tabWidget = QTabWidget()
        self.tabNetwork = QWidget()
        self.tabNetworkLayout = QVBoxLayout(self.tabNetwork)
        self.tabNetworkLayout.addWidget(self.layers)
        self.tabNetworkLayout.addWidget(self.graphicsView)

        self.tabWidget.insertTab(0,self.tabNetwork,"Network")
        self.tabWidget.insertTab(1,self.canvas,"Graphics")
################################################################################ 
#
#       Debug 4, 0
#
################################################################################ 
        self.plainTextEdit = QPlainTextEdit()
        self.textCursor    = QTextCursor()
        self.plainTextEdit.setReadOnly( True )

        self.plainTextEdit.insertPlainText( "w={} h={}\n".format(self.w, self.h ))
################################################################################ 
#
#       Main Layout 
#
################################################################################ 
        # screen resolution
        if self.w>1920:
            self.manager.setFixedSize           ( (1920*2 )//3, 70)
            self.hiddenManager.setMaximumWidth  ( (1920*2 )//3)
            self.hiddenLayers.setFixedWidth     ( (1920*2 )//3)
            self.graphicsView.setFixedWidth     ( (1920*2 )//3)
            self.settingsWidget.setFixedWidth   ( (1920*2 )//3)
            self.canvas.setFixedWidth           ( ((1920 *2)//3)-50)
            self.tabWidget.setFixedWidth        ( (1920 *2)//3)
        else:
            self.manager.setFixedSize           ( (self.w * 2 )//3, 70)
            self.hiddenManager.setMaximumWidth  ( (self.w * 2 )//3)
            self.layers.setFixedWidth           ( (self.w * 2 )//3)
            self.graphicsView.setFixedWidth     ( (self.w * 2 )//3)
            self.settingsWidget.setFixedWidth   ( (self.w * 2 )//3)
            self.canvas.setFixedWidth           ( ((self.w * 2 )//3) -50)
            self.tabWidget.setFixedWidth        ( (self.w *2  )//3)
        
        self.span=1
        self.gridLayout.addWidget(  self.settingsWidget , 0,0,self.span,self.span,Qt.AlignLeft )
        self.gridLayout.addWidget(  self.manager        , 1,0,self.span,self.span,Qt.AlignLeft )
        self.gridLayout.addWidget(  self.tabWidget      , 2,0,self.span,self.span,Qt.AlignLeft )
        #self.gridLayout.addWidget(  self.graphicsView   , 3,0,Qt.AlignLeft                     )
        #self.gridLayout.addWidget(  self.dynamicCanvas  , 3,1                                  )
#        self.gridLayout.addWidget(  self.plainTextEdit  , 4,0,2,-1 )
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotateImage)
        self.radius = 45

################################################################################ 
#
#       Create object name for slot
#
################################################################################
        self.sexCheckBox.setObjectName                ( 'sex'     )
        self.inpLayer.setObjectName                   ( 'inp'     )
        self.outpLayer.setObjectName                  ( 'outp'    )
#QComboBox        
        self.featuresManagerComboBox.setObjectName    ( 'datasetSize'         )
        self.learningRateLineEdit.setObjectName       ( 'learningRate'        )
        self.activationComboBox.setObjectName         ( 'activation'          )
        self.regularizationComboBox.setObjectName     ( 'regularization'      )
        self.regularizationRateLineEdit.setObjectName ( 'regularizationRate'  )
        self.costComboBox.setObjectName               ( 'cost'                )
#clickableLabel        
        self.trainLabel.setObjectName ( "train" )
        self.playLabel.setObjectName  ( "play"  )
        self.loadLabel.setObjectName  ( "load"  )
#QLineEdit        
        self.featuresManagerLineEdit.setObjectName("factor")


        self.parameters = {
                'learningRate'      :'', 
                'activation'        :'', 
                'regularization'    :'', 
                'regularizationRate':'', 
                'cost'              :'',
                'button'            :'',
                'datasetSize'       :'',
                'output'            :'',
                'sex'               :'',
                'layers'            :'',
                }
#        logging.debug( "parameters {}".format( self.parameters ) )
################################################################################ 
#
#       Connection signal slot
#
################################################################################
        self.hiddenManagerPlus.trigger.connect                      ( self.on_managerPlusClicked  )
        self.hiddenManagerMinus.trigger.connect                     ( self.on_managerMinusClicked )
        self.layerCreated.connect                                   ( self.on_layerCreated        )
        self.drawNeuron.connect                                     ( self.on_drawNeuron          )
#QComboxBox
        self.activationComboBox.currentIndexChanged.connect         ( self.on_currentIndexChanged )
        self.regularizationComboBox.currentIndexChanged.connect     ( self.on_currentIndexChanged )
        self.costComboBox.currentIndexChanged.connect               ( self.on_currentIndexChanged )
        self.featuresManagerComboBox.currentIndexChanged.connect    ( self.on_currentIndexChanged )
#QLineEdit
        self.learningRateLineEdit.textChanged.connect               ( self.on_textChanged         )
        self.regularizationRateLineEdit.textChanged.connect         ( self.on_textChanged         )
        self.featuresManagerLineEdit.textChanged.connect            ( self.on_textChanged         )
#clickableLabel
        self.trainLabel.trigger.connect                             ( self.on_labelClicked        )
        self.playLabel.trigger.connect                              ( self.on_labelClicked        )
        self.loadLabel.trigger.connect                              ( self.on_labelClicked        )
#QRadioButton
        self.sexCheckBox.stateChanged.connect                       ( self.on_stateChanged        )
################################################################################ 
#
#       Init by emitting signal
#
################################################################################

        self.activationComboBox.currentIndexChanged.emit        ( 0 )        
        self.regularizationComboBox.currentIndexChanged.emit    ( 0 )    
        self.costComboBox.currentIndexChanged.emit              ( 0 )              
        self.featuresManagerComboBox.currentIndexChanged.emit   ( 0 )
        self.sexCheckBox.stateChanged.emit                      ( 0 )
        
        self.learningRateLineEdit.setText( "0.5" )
        self.regularizationRateLineEdit.setText( "0.01" )
        self.featuresManagerLineEdit.setText("{}".format(self.neuronFactor))

#create input and output layer
        self.hiddenManagerPlus.trigger.emit()
        self.hiddenManagerPlus.trigger.emit()

#------------------------------------------------------------------------------- 
#
#       Hidden slots
#
#-------------------------------------------------------------------------------
    
    @pyqtSlot()
    def on_stopRotate(self):
        self.timer.stop()
        self.loadLabel.set_pixmap(pixmap="/ressource/icons/download.png")
        self.manager.setEnabled(True)
        self.layers.setEnabled(True)

    @pyqtSlot()
    def rotateImage(self):
        self.manager.setEnabled(False)
        self.layers.setEnabled(False)
        self.loadLabel.rotate_pixmap(self.radius)
        self.radius += 45

    @pyqtSlot(int)
    def on_stateChanged(self,state):
        """QCheckBox label """
        s=self.sender()
        n = s.objectName()
        self.parameters[n]=state
        if not state:
            self.outputManagerValue = 9
            self.outputManagerLabel.setText("{}".format(self.outputManagerValue ))
            self.drawNeuron.emit( 2, 9 )
            hLL = self.layersLayout
            w   = hLL.itemAt( 2 ).widget()
            w.setEnabled(False)
            w.extendLabelTitle.setText( "{} Neurones".format(self.outputManagerValue ))
        else:
            self.outputManagerValue = 18
            self.outputManagerLabel.setText("{}".format(self.outputManagerValue  ))
            self.drawNeuron.emit( 2, 18 )
            #Remove later
            hLL = self.layersLayout
            w   = hLL.itemAt( 2 ).widget()
            w.setEnabled(False)
            w.extendLabelTitle.setText( "{} Neurones".format(self.outputManagerValue ))

    @pyqtSlot()
    def on_labelClicked(self):
        """clickable label """
        s = self.sender()
        print(s.get_pixmap())
        if "play" in s.get_pixmap():
            s.set_pixmap(pixmap="/ressource/icons/stop.png")
            s.setObjectName("play")
            self.manager.setEnabled(False)
            self.layers.setEnabled(False)
        elif "stop" in s.get_pixmap():
            s.set_pixmap(pixmap="/ressource/icons/play.png")
            s.setObjectName("stop")
            self.manager.setEnabled(True)
            self.layers.setEnabled(True)
            self.stopped.emit()
            print("emit stopped")
            return
        elif "load" in s.get_pixmap():
            s.set_pixmap(pixmap="/ressource/icons/wait.png")
            self.timer.start(500)


        n = s.objectName()

        #if n == "play":
        self.parameters['button']=str(n)
        self.updateParameters.emit(self.parameters)
        self.clicked.emit()
        
    @pyqtSlot(str)
    def on_textChanged( self, text ):
        """ QLineEdit """
        s = self.sender()
        
        o = s.objectName()
        if o == "factor" and not text :
            print("neuron Factor{}".format(self.neuronFactor))
            self.neuronFactor = 1
        elif o == "factor" :
            self.neuronFactor = int(text)


        if type( s ) is QLineEdit:

            self.parameters[o]=text
            self.updateParameters.emit(self.parameters)
            logging.debug( "parameters {}: {} text{}"
                    .format( o, self.parameters[o],text))

        else:
            logging.debug( 
                    "Error not a lineEdit:{}"
                    .format( s.objectName())
                    )
    @pyqtSlot()
    def on_currentIndexChanged( self ):
        """QComboBox"""
        s = self.sender()
        if type( s ) is QComboBox:
            self.parameters[str( s.objectName())]=s.currentText()
            self.updateParameters.emit(self.parameters)
            logging.debug( "parameters {}: {}" 
                    .format( s.objectName(), self.parameters[str(s.objectName())]))
        else:
            logging.debug( "Error not a comboBox:{}" .format( s.objectName()))


    @pyqtSlot( int )                 
    def on_updateIterations(self,i):
        self.iterations.setText("{}".format(i))
    
    @pyqtSlot( int )
    def on_layerCreated( self, layer ):
        """
        - layer=1 --> Features in layersLayout          ( pos=0 )
        - layer=2 --> Ouptut in layersLayout            ( pos=2 )
        - layer>2 --> hidden layers in layersLayout     ( pos=1 )
                  --> widgets are in hiddenLayersLayout ( pos=layer-3 )
        """
        #logging.debug( 
        #        "on_hiddenLayerCreated layer ======={}"
        #        .format( layer )
        #         )
        #Features select
        if( layer==1 ):
            hLL = self.layersLayout
            w   = hLL.itemAt( layer-1 ).widget()
        #output    
        elif( layer==2 ):
            hLL = self.layersLayout
            w   = hLL.itemAt( layer ).widget()
        else:
            hLL = self.hiddenLayersLayout
            w   = hLL.itemAt( layer-3 ).widget()
        w.extendLabelPlus.trigger.connect ( lambda: self.on_layerPlusClicked(layer ))
        w.extendLabelMinus.trigger.connect( lambda: self.on_layerMinusClicked(layer ))

    # not @pyqtSlot( int ) because of lambda function when trigger is called
    @pyqtSlot()
    def on_layerPlusClicked( self, layer ):
        """
        - layer=1 --> Features in layersLayout          ( pos=0 )
        - layer=2 --> Ouptut in layersLayout            ( pos=2 )
        - layer>2 --> hidden layers in layersLayout     ( pos=1 )
                  --> widgets are in hiddenLayersLayout ( pos=layer-3 )
        """
        #logging.debug( 
        #        "Plus layer{}"
        #        .format( layer )
        #         )
        if( layer == 1 ):
            hLL = self.layersLayout
            w   = hLL.itemAt( layer-1 ).widget()
        #output    
        elif( layer == 2 ):
            hLL = self.layersLayout
            w   = hLL.itemAt( layer ).widget()
        else:
            hLL = self.hiddenLayersLayout
            w   = hLL.itemAt( layer-3 ).widget()
        w.i += self.neuronFactor 
        w.extendLabelTitle.setText( "{} Neurones".format(w.i ))
        self.drawNeuron.emit( layer, w.i )

    # not @pyqtSlot( int ) because of lambda function when trigger is called
    @pyqtSlot()
    def on_layerMinusClicked( self, layer ):
        """when minus is clicked from input or hidden or outpu"""
        if( layer == 1 ):
            hLL = self.layersLayout
            w   = hLL.itemAt( layer-1 ).widget()
        #output    
        elif( layer == 2 ):
            hLL = self.layersLayout
            w   = hLL.itemAt( layer ).widget()
        else:
            hLL = self.hiddenLayersLayout
            w   = hLL.itemAt( layer-3 ).widget()

        if w.i > 1:
            w.i -=  self.neuronFactor
            w.extendLabelTitle.setText( "{} Neurones".format(w.i ))
            self.drawNeuron.emit( layer, w.i )
            
#------------------------------------------------------------------------------- 
#
#       Hidden Manager slots
#
#-------------------------------------------------------------------------------
    @pyqtSlot()
    def on_managerPlusClicked( self ):
        """ 
        - First item is the features layer
        - Second is the output layer
        - others are the hidden layers
        Each layer start with 1 neuron
        """
        if self.countl < 10:
            self.countl += 1
            hLL = self.hiddenLayersLayout
            
            if( self.countl == 1 ):
                self.layersLayout.insertWidget( 0, neuronManagerWidget(),Qt.AlignLeft)
                size = int(self.parameters['datasetSize']) * 11 

                #Remove later
                hLL = self.layersLayout
                w   = hLL.itemAt( 0 ).widget()
                w.setEnabled(False)
                w.extendLabelTitle.setText( "{} Neurones".format(size ))
                self.drawNeuron.emit( self.countl, size )

            elif( self.countl == 2 ):
                self.layersLayout.insertWidget( 2, neuronManagerWidget(),Qt.AlignRight)
                size = self.outputManagerValue
                #Remove later
                hLL = self.layersLayout
                w   = hLL.itemAt( 2 ).widget()
                w.setEnabled(False)
                w.extendLabelTitle.setText( "{} Neurones".format(size ))
                self.drawNeuron.emit( self.countl, size )
            else:
                self.hiddenLayersLayout.addWidget( neuronManagerWidget(), Qt.AlignCenter)
                self.hiddenManagerTitle.setText( "{} HIDDEN LAYER".format(self.countl-2 ))
                self.drawNeuron.emit( self.countl, 1 )
            self.layerCreated.emit( self.countl )
    
    @pyqtSlot()
    def on_managerMinusClicked( self ):
        """delete hidden layers """
        if self.countl > 2:
            self.countl -= 1
            self.hiddenManagerTitle.setText( "{} HIDDEN LAYER".format(self.countl-2 ))
            hLL = self.hiddenLayersLayout
            w   = hLL.itemAt( hLL.count()-1).widget().deleteLater()
            self.drawNeuron.emit( self.countl-1, 0 )

#------------------------------------------------------------------------------- 
#
#       drawing hidden layer  slot
#
#-------------------------------------------------------------------------------
    @pyqtSlot( int,  int )
    def on_drawNeuron( self,  layer, neuron ):
        """
        Parameters: 
        layer  - the number of the targeted layer
        neuron - the number of neuron to draw
        """
        logging.debug( 
            " drawNeuron layer {} -- neuron {}"
            .format( layer,  neuron  )
         )
        #add new layer
        if len( self.hm  ) < layer:  
            self.hm.append( neuron * self.neuronFactor  )
            self.parameters['layers']=self.hm[1:-1]
        else:
        # when removing ( manager minus clicked )
            if not neuron:
                del self.hm[ layer ]
                self.parameters['layers']=self.hm[1:-1]
            #input is first    
            elif layer == 1:
                self.hm[ 0 ] = neuron //11
            #output is last    
            elif layer == 2:
                self.hm[len( self.hm ) - 1 ] = neuron
            # hidden layers
            else:
                self.hm[layer-2] = neuron*self.neuronFactor        
                self.parameters['layers']=self.hm[1:-1]
        
        logging.debug( 
            " hm {} "
            .format( self.hm  )
         )
        # focus at end of debug 
        #self.textCursor = self.plainTextEdit.textCursor()
        #self.textCursor.movePosition( QTextCursor.End )
        #self.plainTextEdit.setTextCursor( self.textCursor )

        hl=drawNeuralNetworkWidget( 20,( (self.w *2  )//3)//len(self.hm),self.hm )
        
        #draw if 2 layers
        if len( self.hm )>1:
            hl.drawNeurones()
            hl.drawLines()
        self.graphicsView.setScene( hl.getScene() )
        
#------------------------------------------------------------------------------- 
#
#       Test slot
#
#-------------------------------------------------------------------------------
    @pyqtSlot( int )
    def on_test( self, val ):
        self.plainTextEdit.insertPlainText( "on_test slot -- item num: {}\n".format(val ))

    def buttonClicked( self ):

        QtCore.QCoreApplication.instance().quit()




class MainWindow( QMainWindow ): #,  Ui_MainWindow):
    loadfile = pyqtSignal(str)
    
    def __init__( self ):
        super( MainWindow, self ).__init__()
        self.initUi()
        # Set up the user interface from Designer.
    def initUi( self ):

        bar = self.menuBar()
        self.f = bar.addMenu("&File")
        
        self.loadAction = QAction( '&Load', self) 
        self.loadAction.setShortcut('Ctrl+L')
        self.loadAction.triggered.connect(self.load_file)

        self.saveAction = QAction( '&Save', self) 
        self.saveAction.setShortcut('Ctrl+S')
        
        self.saveAction.triggered.connect(self.save_file)
        
        self.resetAction = QAction( '&Reset Netwotk', self) 
        self.resetAction.setShortcut('Ctrl+R')

        self.exitAction = QAction( '&Exit', self)               
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qApp.quit)

        self.f.addAction(self.exitAction)
        self.f.addAction(self.loadAction)
        self.f.addAction(self.resetAction)
        self.f.addAction(self.saveAction)
    
        self.msg = QMessageBox()
        self.msg.setObjectName("message")

        self.filename=''

    @pyqtSlot(str)
    def get_save_filename(self,filename):
        self.filename = filname

    @pyqtSlot()
    def save_file(self):
        self.msg.setIcon(QMessageBox.Information)
        filename = "aaa"
        self.msg.setInformativeText("Save file{}".format(filename))
        self.msg.setWindowTitle("Save")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()
        if retval == QMessageBox.Ok:
            logging.debug("retval {}".format(retval))
    
    @pyqtSlot()
    def load_file(self):
        filename =  QFileDialog.getOpenFileName(self, 'Open file', 
            os.path.dirname(os.path.abspath(__file__)))
        logging.debug("filename {}".format(str(filename)))

class backend( QObject ):

    updateErr        = pyqtSignal( list )
    updateCost       = pyqtSignal( list )
    updateIterations = pyqtSignal( int )
    finished         = pyqtSignal()
    stop             = pyqtSignal()

    def __init__( self,  parent = None ):
        QObject.__init__( self,  parent )
        self.size   = 50
        self.parameters = {
                'learningRate'      :'', 
                'activation'        :'', 
                'regularization'    :'', 
                'regularizationRate':'', 
                'cost'              :'',
                }
        self.input_size  = None
        self.output_size = None

        self.layers = 150 
        self.net    = None
        self.training_data, self.validation_data, self.test_data = [],[],[]
    

    @pyqtSlot()
    def run( self):
        """ run network """ 
        print("backend param == {}".format(self.parameters))
        
        try: 
            if self.parameters['button'] == "load":
                self.training_data,self.validation_data, self.test_data = utils.extract_datasets(
                        size=int(self.parameters['datasetSize']))
                self.input_size  = len(self.training_data[0][0])
                self.output_size = len(self.training_data[0][1])
                print("load finished")
                self.stop.emit()
                self.finished.emit()
            
            elif self.parameters['button'] == "play":
             #instance 
                if None in self.parameters['layers']:
                    self.parameters['layers']=[]
                    self.parameters['layers'].append(self.input_size)
                    self.parameters['layers'].append(self.output_size)
                else:
                    self.parameters['layers'].insert(0,self.input_size)
                    self.parameters['layers'].append(self.output_size)
                
                
                print("layers {}".format(self.parameters['layers']))
                self.net = network.Network(
                self.parameters['layers'],
                activation     = self.parameters['activation'],
                cost           = self.parameters['cost'],
                regularization = self.parameters['regularization'],
                learning_rate  = float(self.parameters['learningRate']),
                lambda_        = float(self.parameters['regularizationRate'])
                )
               # print(self.net)
                print("in {} out {} lR {} lambda_ {} ".format(self.input_size,
                    self.output_size,
                    float(self.parameters['learningRate']),
                    float(self.parameters['regularizationRate']),
                    ))
                if os.path.exists('autoload.save.gz'):
                #    print(" *** Found autoload, loading config...")
                    self.net.load('autoload.save.gz')
                
                print("play finished")
                self.finished.emit()
            
            elif self.parameters['button'] == "train":

                self.net.qnet.costValueChange  = self.updateCost
                self.net.qnet.errValueChange   = self.updateErr
                self.net.qnet.epochValueChange = self.updateIterations

                tr_err, tr_cost, va_err, va_cost = self.net.train(
                        self.training_data,
                        epochs       = 1000,
                        batch_size   = 10,
                        va_d         = self.validation_data,
                        early_stop_n = 20,
                        monitoring   = {'error':True, 'cost':True}
                        )
                print("tain finished")
                self.finished.emit()
                

            else:
                self.finished.emit()
        except Exception as e :
            print(e)
            self.finished.emit()


def main():
    app = QApplication( sys.argv )

    dw = QDesktopWidget()
    x  = dw.width()
    y  = dw.height()
    
    thread = QThread()
################################################################################
#
#                           GUI frontend
#
################################################################################
    window  = MainWindow()
    central = centralWidget()
    window.setCentralWidget(central)
    window.show()
    

################################################################################
#
#                            backend
#
################################################################################

    b            = backend()
    b.parameters = central.parameters
    

    b.updateErr.connect       ( central.err.update_figure2  )
    b.updateCost.connect      ( central.cost.update_figure2 )
    b.updateIterations.connect( central.on_updateIterations )
    b.stop.connect            ( central.on_stopRotate       )
    b.moveToThread(thread)


    central.stopped.connect(thread.terminate)
    central.stopped.connect(thread.quit)
    b.finished.connect(thread.quit)
    thread.started.connect(b.run)
    central.clicked.connect(thread.start)

    app.exec_()
    app.deleteLater()
    sys.exit()

#    sys.exit( app.exec_() )
    


if __name__ == "__main__":
    try: 
        main()
    except Exception as e :
        print(e)

