#!/usr/bin/env python3.4

from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')

from hiddenLayer import neuralNetworkWidget
from PyQt5 import QtCore,QtWidgets,QtSvg,QtGui
from PyQt5.QtGui import QTextCursor,QColor,QBrush,QPen,QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow ,QWidget, \
                QGridLayout,QHBoxLayout, \
                QGraphicsView,QGraphicsScene,QGraphicsRectItem, \
                QPushButton,QLabel,QPlainTextEdit,QComboBox, \
                QSpacerItem,QSizePolicy

from PyQt5.QtCore import QRect,QRectF,pyqtSignal,pyqtSlot

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


progname = os.path.basename(sys.argv[0])
progversion = "0.1"

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]

        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()



class hiddenLayer(QWidget):
    """ creating a hidden layer interface"""
    def __init__(self):
        super(hiddenLayer,self).__init__()
        self.layout=QGridLayout(self)
        
        self.i=1
        self.extendLabelPlus=ExtendedQLabel()
        self.extendLabelPlus.setPixmap(QtGui.QPixmap(os.getcwd() + "/ressource/icons/pluss.png"))
        
        self.extendLabelMinus=ExtendedQLabel()
        self.extendLabelMinus.setPixmap(QtGui.QPixmap(os.getcwd() + "/ressource/icons/minuss.png"))
        
        self.extendLabelTitle=QLabel("{} Neurones".format(self.i))
        self.layout.addWidget(self.extendLabelPlus,0,0)
        self.layout.addWidget(self.extendLabelMinus,0,1)
        self.layout.addWidget(self.extendLabelTitle,1,0)
        #self.setFixedSize(100,100)


class ExtendedQLabel(QLabel):
    """Re implemented QLabel: clickable QLabel"""
    trigger=pyqtSignal()
    def __init__(self):
        super(ExtendedQLabel,self).__init__()
 
    def mouseReleaseEvent(self, ev):
        self.trigger.emit()



class centralWidget(QWidget):
    """ main widget"""

    hiddenLayerCreated=pyqtSignal(int)
    drawHiddenLayerNeurone=pyqtSignal(int,int)


    def __init__(self):
        super(centralWidget, self).__init__()
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
        self.settingsLayout=QGridLayout(self.settingsWidget)
        
        self.reloadLabel=ExtendedQLabel()
        self.reloadLabel.setPixmap(QtGui.QPixmap(os.getcwd() + "/ressource/icons/reload.png"))
        self.settingsLayout.addWidget(self.reloadLabel,0,0,0,1)
        
        self.pauseLabel=ExtendedQLabel()
        self.pauseLabel.setPixmap(QtGui.QPixmap(os.getcwd() + "/ressource/icons/pause.png"))
        self.settingsLayout.addWidget(self.pauseLabel,0,1,0,1)
        
        self.playLabel=ExtendedQLabel()
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
        self.layerManagerLayout=QHBoxLayout(self.layerManager)
        #Features
        self.featuresManager =QLabel("Features")
        
        #Number hidden layout
        self.hiddenManagerLayer=QWidget()
        self.hiddenManagerLayerLayout=QHBoxLayout(self.hiddenManagerLayer)
        
        self.i=0
        self.extendLabelHiddenManagerTitle=QLabel("{} HIDDEN LAYER".format(self.i))
        
        self.extendLabelHiddenManagerPlus=ExtendedQLabel()
        self.extendLabelHiddenManagerPlus.setPixmap(QtGui.QPixmap(os.getcwd() + "/ressource/icons/pluss.png"))
        
        self.extendLabelHiddenManagerMinus=ExtendedQLabel()
        self.extendLabelHiddenManagerMinus.setPixmap(QtGui.QPixmap(os.getcwd() + "/ressource/icons/minuss.png"))
        
        self.hiddenManagerLayerLayout.addWidget(self.extendLabelHiddenManagerPlus)
        self.hiddenManagerLayerLayout.addWidget(self.extendLabelHiddenManagerMinus)
        self.hiddenManagerLayerLayout.addWidget(self.extendLabelHiddenManagerTitle)
        
        #Output
        self.outputManager =QLabel("Output")
        #Setup layer manager layout
        self.layerManagerLayout.addWidget(self.featuresManager)
        self.layerManagerLayout.addWidget(self.hiddenManagerLayer)
        self.layerManagerLayout.addWidget(self.outputManager)

################################################################################ 
#
#       Hidden Layers widget 2,0
#
################################################################################ 
        self.hiddenLayers=QWidget()       
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

################################################################################ 
#
#       Main Layout 
#
################################################################################ 
        self.spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding,QSizePolicy.Minimum)
        
        self.gridLayout.addItem(self.spacerItem,0,0)
        self.gridLayout.addWidget(self.settingsWidget,0,1)
        self.gridLayout.addItem(self.spacerItem,0,2)

        self.gridLayout.addItem(self.spacerItem,1,0)
        self.gridLayout.addWidget(self.layerManager,1,1)
        self.gridLayout.addItem(self.spacerItem,1,2)
        
        self.gridLayout.addItem(self.spacerItem,2,0)
        self.gridLayout.addWidget(self.hiddenLayers,2,1)
        self.gridLayout.addItem(self.spacerItem,2,2)

        self.gridLayout.addWidget(self.graphicsView,3,0,1,-1)
        self.gridLayout.addWidget(self.plainTextEdit,4,0,1,-1)

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
        self.plainTextEdit.insertPlainText("{}\n".format(val))
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
        self.i+=1
        self.extendLabelHiddenManagerTitle.setText("{} HIDDEN LAYER".format(self.i))
        hLL=self.hiddenLayersLayout
        hLL.addWidget(hiddenLayer())
        
        self.plainTextEdit.insertPlainText("Add -- layer number:{}\n".format(hLL.count()))
        self.hiddenLayerCreated.emit(self.i)
        self.drawHiddenLayerNeurone.emit(self.i,1)
    
    @pyqtSlot()
    def on_extendLabelHiddenManagerMinusClicked(self):
        if self.i > 0:
            self.i-=1
            self.extendLabelHiddenManagerTitle.setText("{} HIDDEN LAYER".format(self.i))
            hLL=self.hiddenLayersLayout
            w=hLL.itemAt(hLL.count()-1).widget().deleteLater()
            self.plainTextEdit.insertPlainText("Remove -- layer number{}\n".format(self.hiddenLayersLayout.count()))
        self.drawHiddenLayerNeurone.emit(self.i,0)

#------------------------------------------------------------------------------- 
#
#       Test slot
#
#-------------------------------------------------------------------------------
    @pyqtSlot(int,int)
    def on_drawHiddenLayerNeurone(self,layer,neurone):
        self.plainTextEdit.clear()
        self.plainTextEdit.insertPlainText("layer {},neurone{}\n".format(layer,neurone))
        if len(self.hm)<=layer:
            self.hm.append(neurone)
            self.plainTextEdit.insertPlainText("++len {}\n".format(len(self.hm)))
        else:
            self.hm[layer-1]=neurone
            self.plainTextEdit.insertPlainText("==len {}\n".format(len(self.hm)))
        
        self.plainTextEdit.insertPlainText("len {}\n".format(self.hm))
        
        hl=neuralNetworkWidget(20,120,self.hm)        
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
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
