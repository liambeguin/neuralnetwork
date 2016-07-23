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
                QPushButton,  QLabel, QPlainTextEdit, QComboBox, QMessageBox, \
                QSpacerItem,  QSizePolicy, QGraphicsPixmapItem, \
                QMenu,QFileDialog,QAction,QLineEdit, \
                QTabWidget,\
                qApp

from PyQt5.QtCore import QObject,QThread, Qt,pyqtSignal,pyqtSlot


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

    layerCreated     = pyqtSignal( int )
    drawNeuron       = pyqtSignal( int, int )
    textChanged      = pyqtSignal()
    updateParameters = pyqtSignal( dict )

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
################################################################################ 
#
#       Settings top widget 0, 0
#
################################################################################ 
        self.settingsWidget=QWidget()
        if self.debug:
            self.settingsWidget.setStyleSheet( 
                    "border-style: outset; "+
                    "border-width: 1px;    "+
                    "border-color: red;  "
                     )
        #else:
        #    self.settingsWidget.setStyleSheet( 
        #            "background-color:white")
        
        self.settingsLayout = QGridLayout( self.settingsWidget )
        
# 0-----------------------------------------------------------------------------
        self.reloadLabel = clickableLabel( pixmap="/ressource/icons/reload.png" )
        self.settingsLayout.addWidget( self.reloadLabel                  , 0,0,0,1 )
# 1-----------------------------------------------------------------------------
        self.pauseLabel = clickableLabel( pixmap="/ressource/icons/pause.png" )
        self.settingsLayout.addWidget( self.pauseLabel                   , 0,1,0,1 )
# 2-----------------------------------------------------------------------------
        self.playLabel=clickableLabel( pixmap="/ressource/icons/play.png" )
        self.settingsLayout.addWidget( self.playLabel                    , 0,2,0,1 )
# 4-----------------------------------------------------------------------------
        self.iterationsInitValue = 0
        self.iterations          = QLabel( "{}".format(self.iterationsInitValue ))
        iterationsLabel          = QLabel( "Iterations" )
        
        self.settingsLayout.addWidget( iterationsLabel                   , 0,4 )
        self.settingsLayout.addWidget( self.iterations                   , 1,4 )
# 5-----------------------------------------------------------------------------
        self.learningRateLineEdit = QLineEdit()
        learningRateLabel         = QLabel( "Leanrning rate" )
        
        self.learningRateLineEdit.setFixedWidth(100)
        
        self.settingsLayout.addWidget( learningRateLabel                 , 0,5 )
        self.settingsLayout.addWidget( self.learningRateLineEdit         , 1,5 )
# 6-----------------------------------------------------------------------------
        self.activationComboBox=QComboBox()
        activationLabel=QLabel( "Activation" )
        activationStrList=[]
        
        self.activationComboBox.addItems( network.Network.options["activation"] )
        self.settingsLayout.addWidget( activationLabel                   , 0,6 )
        self.settingsLayout.addWidget( self.activationComboBox           , 1,6 )
# 7-----------------------------------------------------------------------------
        self.regularizationComboBox = QComboBox()
        regularizationLabel         = QLabel( "Regularization" )
        regularizationStrList       = []
        

        self.regularizationComboBox.addItems( network.Network.options["regularization"] )
        
        self.settingsLayout.addWidget( regularizationLabel               , 0,7 )
        self.settingsLayout.addWidget( self.regularizationComboBox       , 1,7 )
# 8-----------------------------------------------------------------------------
        self.regularizationRateLineEdit = QLineEdit()
        regularizationRateLabel         = QLabel( "Regularization rate" )
        self.regularizationRateLineEdit.setFixedWidth(100)
        
        self.settingsLayout.addWidget( regularizationRateLabel           , 0,8 )
        self.settingsLayout.addWidget( self.regularizationRateLineEdit   , 1,8 )
# 9-----------------------------------------------------------------------------
        self.costComboBox = QComboBox()
        costLabel         = QLabel( "Cost function" )
        costStrList       = []
        
        self.costComboBox.addItems( network.Network.options["cost"] )

        self.settingsLayout.addWidget( costLabel                         , 0,9 )
        self.settingsLayout.addWidget( self.costComboBox                 , 1,9 )
################################################################################ 
#
#       Layers Mangaer  widget 1, 0
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
        #else:
        #    self.manager.setStyleSheet( 
        #            "background-color:grey")

        self.managerLayout = QHBoxLayout( self.manager )
        #Features
        self.featuresManager         = QWidget()
        self.featuresManagerLabel    = QLabel( "Features" )
        self.featuresManagerList     = ["40","50","60"] 
        6
        self.featuresManagerComboBox = QComboBox()
        self.featuresManagerComboBox.addItems( self.featuresManagerList )

        self.featuresManagerLayout   = QVBoxLayout(self.featuresManager)
        self.featuresManagerLayout.addWidget( self.featuresManagerLabel )
        self.featuresManagerLayout.addWidget( self.featuresManagerComboBox )
        self.featuresManagerLayout.setSpacing(0)
        self.featuresManagerLayout.setContentsMargins( 0, 0,0,0 )
        #Number hidden layout
        self.hiddenManager = QWidget()
        #self.hiddenManager.setFixedSize( 500, 50 )
        self.hiddenManagerLayout = QHBoxLayout( self.hiddenManager )
        
        self.countl = 0
        #label
        self.hiddenManagerTitle = QLabel( "{} HIDDEN LAYER".format(self.countl ))
        #Buttons
        self.hiddenManagerPlus = clickableLabel( pixmap="/ressource/icons/pluss.png" )
        self.hiddenManagerPlus.scaleRegion( 48, 8,36,34,QRegion.Ellipse )

        self.hiddenManagerMinus = clickableLabel( "/ressource/icons/minuss.png" )
        self.hiddenManagerMinus.scaleRegion( 48, 8,36,34,QRegion.Ellipse )
        
        self.hiddenManagerLayout.setSpacing( 0 )
        self.hiddenManagerLayout.setContentsMargins( 0, 0,0,0 )

        self.hiddenManagerLayout.addItem   ( self.spacerItem )
        self.hiddenManagerLayout.addWidget ( self.hiddenManagerPlus )
        self.hiddenManagerLayout.addWidget ( self.hiddenManagerMinus )
        self.hiddenManagerLayout.addWidget ( self.hiddenManagerTitle )
        self.hiddenManagerLayout.addItem   ( self.spacerItem )
        #Output
        self.outputManager         = QWidget()
        self.outputManagerLayout   = QVBoxLayout( self.outputManager )
        self.outputManagerLabel    = QLabel( "Output" )
        self.outputManagerComboBox = QComboBox()
        self.outputManagerList     = [ "9" ]

        self.outputManagerComboBox.addItems( self.outputManagerList )
        self.outputManagerLayout.addWidget( self.outputManagerLabel )
        self.outputManagerLayout.addWidget( self.outputManagerComboBox )
        self.outputManagerLayout.setSpacing( 0 )
        self.outputManagerLayout.setContentsMargins( 0, 0,0,0 )
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
        self.hiddenLayersLayout.setContentsMargins( 0, 0,0,0 )
       

        self.layers         = QWidget()
        self.layersLayout   = QHBoxLayout( self.layers )
        self.inpLayer       = neuronManagerWidget()
        self.outpLayer      = neuronManagerWidget()

        self.layersLayout.addWidget( self.hiddenLayers, QSizePolicy.Expanding )

        self.layersLayout.setSpacing( 0 )
        self.layersLayout.setContentsMargins( 0, 0,0,0 )
        
        if self.debug:
            self.layers.setStyleSheet( 
                    "border-style: outset; "+
                    "border-width: 1px;    "+
                    "border-color: red;  "
                     )
################################################################################ 
#
#       NeuralNetwork Widget 3, 0
#
################################################################################ 
        
        self.tr_err       = DynamicMplCanvas(pos=111)
        self.tr_cost      = DynamicMplCanvas(pos=111)
        self.va_err       = DynamicMplCanvas(pos=111)
        self.va_cost      = DynamicMplCanvas(pos=111)
        self.canvas       = QWidget()
        self.canvasLayout = QGridLayout(self.canvas)
        self.canvasLayout.addWidget(self.tr_err ,0,0)
        self.canvasLayout.addWidget(self.tr_cost,0,1)
        self.canvasLayout.addWidget(self.va_err ,1,0)
        self.canvasLayout.addWidget(self.va_cost,1,1)



        self.graphicsView = QGraphicsView()
        #hidden manager: list layer's neurons
        self.hm = []
        self.tabWidget = QTabWidget()
        self.tabWidget.insertTab(0,self.graphicsView,"Network")
        self.tabWidget.insertTab(1,self.canvas,"Graphics")
################################################################################ 
#
#        Matplotlib canvas 3, 1
#
################################################################################
        
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
        else:
            self.manager.setFixedSize           ( (self.w * 2 )//3, 70)
            self.hiddenManager.setMaximumWidth  ( (self.w * 2 )//3)
            self.layers.setFixedWidth           ( (self.w * 2 )//3)
            self.graphicsView.setFixedWidth     ( (self.w * 2 )//3)
            self.settingsWidget.setFixedWidth   ( (self.w * 2 )//3)
            self.dynamicCanvas.setFixedWidth    ( (self.w * 2 )//3)
        
        self.span=1
        self.gridLayout.addWidget(  self.settingsWidget , 0,0,self.span,self.span,Qt.AlignLeft )
        self.gridLayout.addWidget(  self.manager        , 1,0,self.span,self.span,Qt.AlignLeft )
        self.gridLayout.addWidget(  self.layers         , 2,0,self.span,self.span,Qt.AlignLeft )
        self.gridLayout.addWidget(  self.tabWidget      , 3,0,self.span,self.span,Qt.AlignLeft )
        #self.gridLayout.addWidget(  self.graphicsView   , 3,0,Qt.AlignLeft                     )
        #self.gridLayout.addWidget(  self.dynamicCanvas  , 3,1                                  )
#        self.gridLayout.addWidget(  self.plainTextEdit  , 4,0,2,-1 )
################################################################################ 
#
#       Create object name for slot
#
################################################################################

        self.inpLayer.setObjectName                   ( 'inp'     )
        self.outpLayer.setObjectName                  ( 'outp'    )
#QComboBox        
        self.learningRateLineEdit.setObjectName       ( 'learningRate'        )
        self.activationComboBox.setObjectName         ( 'activation'          )
        self.regularizationComboBox.setObjectName     ( 'regularization'      )
        self.regularizationRateLineEdit.setObjectName ( 'regularizationRate'  )
        self.costComboBox.setObjectName               ( 'cost'                )
        self.parameters = {
                'learningRate'      :'', 
                'activation'        :'', 
                'regularization'    :'', 
                'regularizationRate':'', 
                'cost'              :''
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
#QLineEdit
        self.learningRateLineEdit.textChanged.connect               ( self.on_textChanged )
        self.regularizationRateLineEdit.textChanged.connect         ( self.on_textChanged )
################################################################################ 
#
#       Init by emitting signal
#
################################################################################
#create input and output layer
        self.hiddenManagerPlus.trigger.emit()
        self.hiddenManagerPlus.trigger.emit()

        self.activationComboBox.currentIndexChanged.emit        ( 0 )        
        self.regularizationComboBox.currentIndexChanged.emit    ( 0 )    
        self.costComboBox.currentIndexChanged.emit              ( 0 )              
        
        self.learningRateLineEdit.setText( "0.5" )
        self.regularizationRateLineEdit.setText( "0.01" )


#------------------------------------------------------------------------------- 
#
#       Hidden slots
#
#-------------------------------------------------------------------------------

    @pyqtSlot(str)
    def on_textChanged( self, text ):
        s = self.sender()
        if type( s ) is QLineEdit:

            self.parameters[str( s.objectName())]=text
            self.updateParameters.emit(self.parameters)
            logging.debug( 
                    "parameters {}: {} text{}"
                    .format( s.objectName(), self.parameters[str(s.objectName())],text)
                     )

        else:
            logging.debug( 
                    "Error not a lineEdit:{}"
                    .format( s.objectName())
                    )
    @pyqtSlot()
    def on_currentIndexChanged( self ):
        s = self.sender()
        if type( s ) is QComboBox:
            self.parameters[str( s.objectName())]=s.currentText()
            self.updateParameters.emit(self.parameters)
            logging.debug( 
                    "parameters {}: {}"
                    .format( s.objectName(), self.parameters[str(s.objectName())])
                     )

        else:
            logging.debug( 
                    "Error not a comboBox:{}"
                    .format( s.objectName())
                    )
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
        w.i += 1 
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
            w.i -= 1 
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
            elif( self.countl == 2 ):
                self.layersLayout.insertWidget( 2, neuronManagerWidget(),Qt.AlignRight)
            else:
                self.hiddenLayersLayout.addWidget( neuronManagerWidget(), Qt.AlignCenter)
                self.hiddenManagerTitle.setText( "{} HIDDEN LAYER".format(self.countl-2 ))
            self.layerCreated.emit( self.countl )
            self.drawNeuron.emit( self.countl, 1 )
    
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
            self.hm.append( neuron  )
        else:
        # when removing ( manager minus clicked )
            if not neuron:
                del self.hm[ layer ]
            #input is first    
            elif layer == 1:
                self.hm[ 0 ] = neuron
            #output is last    
            elif layer == 2:
                self.hm[len( self.hm ) - 1 ] = neuron
            # hidden layers
            else:
                self.hm[layer-2] = neuron
        
        # focus at end of debug 
        #self.textCursor = self.plainTextEdit.textCursor()
        #self.textCursor.movePosition( QTextCursor.End )
        #self.plainTextEdit.setTextCursor( self.textCursor )
        
        hl=drawNeuralNetworkWidget( 20, 120,self.hm )
        
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



class backend( QObject ):

    updateVa_err     = pyqtSignal( list )
    updateVa_cost    = pyqtSignal( list )
    updateTr_err     = pyqtSignal( list )
    updateTr_cost    = pyqtSignal( list )
    updateIterations = pyqtSignal( int )
    finished         = pyqtSignal()


    def __init__( self,  parent = None ):
        QObject.__init__( self,  parent )
        self.parameters = {
                'learningRate'      :'', 
                'activation'        :'', 
                'regularization'    :'', 
                'regularizationRate':'', 
                'cost'              :''
                }
        self.size   = 50
        self.layers = 150 



    @pyqtSlot()
    def run( self ):
        
        logging.debug("backend param == {}".format(self.parameters))
        logging.debug("size = {}".format(self.size))
        training_data, validation_data, test_data = utils.extract_datasets(size=self.size)

        input_size  = len(training_data[0][0])
        output_size = len(training_data[0][1])
        #try:
        #except Exception as e:
        #    pass
        #    #msg =QMesssageBox()
        #    #msg.setInformativeText("{}".format(e))
        #    #msg.exec_()
        #    #msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        net = network.Network(
                (input_size, 150, output_size),
                activation     = self.parameters['activation'],
                cost           = self.parameters['cost'],
                regularization = self.parameters['regularization'],
                learning_rate  = float(self.parameters['learningRate']),
                lambda_        = float(self.parameters['regularizationRate'])
                )
        if os.path.exists('autoload.save.gz'):
        #    print(" *** Found autoload, loading config...")
            net.load('autoload.save.gz')

#        print(net)
        net.qnet.validationErrorValueChange = self.updateVa_err
        net.qnet.validationCostValueChange  = self.updateVa_cost
        net.qnet.trainingCostValueChange    = self.updateTr_cost
        net.qnet.trainingErrorValueChange   = self.updateTr_err
        net.qnet.epochValueChange           = self.updateIterations


        tr_err, tr_cost, va_err, va_cost = net.train(
                training_data,
                epochs       = 20,
                batch_size   = 10,
                va_d         = validation_data,
                early_stop_n = None,
                monitoring   = {'error':True, 'cost':True}
                )

        self.finished.emit()


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

        self.exitAction = QAction( '&Exit', self)               
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qApp.quit)

        self.f.addAction(self.exitAction)
        self.f.addAction(self.loadAction)
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



    


def main():
    app = QApplication( sys.argv )

    dw = QDesktopWidget()
    x  = dw.width()
    y  = dw.height()
    
    thread = QThread()
    #thread2=QThread()

    window  = MainWindow()
    central = centralWidget()
    window.setCentralWidget(central)
    window.show()


    b            = backend()
    b.parameters = central.parameters
    b.size       = int(central.featuresManagerComboBox.currentText())
    
    central.drawNeuron.emit(1,int(b.size))
    central.drawNeuron.emit(2,150)
    central.drawNeuron.emit(3,9)

    b.updateTr_err.connect(  central.tr_err.update_figure)
    b.updateVa_err.connect(  central.va_err.update_figure)
    b.updateTr_cost.connect( central.tr_cost.update_figure)
    b.updateVa_cost.connect( central.va_cost.update_figure)

    b.updateIterations.connect( central.on_updateIterations )
    b.moveToThread(thread)

    b.finished.connect(thread.quit)
    thread.started.connect(b.run)
    central.playLabel.trigger.connect(thread.start)
    sys.exit( app.exec_() )


if __name__ == "__main__":
    main()
