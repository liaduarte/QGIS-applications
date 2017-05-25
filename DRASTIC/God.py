from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from Ui_Topography import Ui_Topography
import GdalTools_utils as Utils
try:
    from PyQt4.QtCore import QString
except ImportError:
    QString = str
from processing.core.Processing import Processing
#from processing.core.ProcessingUtils import ProcessingUtils
import ftools_utils
from osgeo import ogr
from processing import *
#from processing.core.QGisLayers import QGisLayers
from processing.core.GeoAlgorithm import GeoAlgorithm
from osgeo.gdalconst import GA_ReadOnly
from osgeo import gdal
from processing import ProcessingPlugin
from processing.core.Processing import Processing
#from processing.outputs import OutputRaster
import sys, os
import numpy
from Ui_God import Ui_God
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
import Aquifer_media
from PyQt4 import QtCore, QtGui

class God(QDialog, Ui_God):
    
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)  
    
        QObject.connect(self.selectButton, SIGNAL("clicked()"),self.fillInputFileEdit)
        QObject.connect(self.selectButton2, SIGNAL("clicked()"),self.fillInputFileEdit2)
        QObject.connect(self.selectButton3, SIGNAL("clicked()"),self.fillInputFileEdit3)
       
        QObject.connect(self.selectButton_out, SIGNAL("clicked()"), self.fillOutputFileEdit)
        QObject.connect(self.selectButton_color, SIGNAL("clicked()"), self.fillOutputFileEdit_color)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.convert)
        
        # connect help
        QObject.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Help), SIGNAL("clicked()"), self.help)        
        
    def help(self):
        QMessageBox.about(self, "DRASTIC", """<p><b>DRASTIC Index</b></p> 
        <p><b>Definition:</b>The last feature, the DRASTIC index, corresponds to the final map, which results from the sum of the seven factor
        maps created before multiplied by the corresponding weights as defined in equation 1, according to Aller et al. (1987).  </p>
        <p><b>DRASTIC</b> = DR x DW + RR x RW + AR x AW + SR x SW + TR x TW + IR x IW + CR x CW	(1)</p>
        <p>R and W (in subscript) correspond to the rating and weight for each factor, respectively. 
        The DRASTIC interface is composed by seven input files corresponding to D, R, A, S, T, I and C raster files, and an output file corresponding to DRASTIC index map. </p>
        <p><b>Method</b></p> 
        <p>Input files = seven raster created before. The user must to define the weight values which are defined according Aller et al (1987) by default.  </p>
        <p><b>Output file:</b> DRASTIC raster file without color or DRASTIC COLORED with the colors and intervals defined according to Aller et al. (1987)</p>""")  
      
 # INPUT RASTER FILE
    def fillInputFileEdit(self):
        lastUsedFilter = Utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = Utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), Utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo.addItem(inputFile)
        check = QFile(inputFile)     
        
    def fillInputFileEdit2(self):
        lastUsedFilter = Utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = Utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), Utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo2.addItem(inputFile)
        check = QFile(inputFile)    
        
    def fillInputFileEdit3(self):
        lastUsedFilter = Utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = Utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), Utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo3.addItem(inputFile)
        check = QFile(inputFile) 
            
   
            
# --------------------------------------- // ----------------------------------------------------- // ------------------------------------------------------------------------------

# OUTPUT RASTER FILE
    def fillOutputFileEdit(self):
        lastUsedFilter = Utils.FileFilter.lastUsedRasterFilter()
        outputFile = Utils.FileDialog.getSaveFileName(self, self.tr( "Select the raster file to save the results to" ), Utils.FileFilter.allRastersFilter(), lastUsedFilter )
        if outputFile==None:
            return
        Utils.FileFilter.setLastUsedRasterFilter(lastUsedFilter)
        self.outputFormat = Utils.fillRasterOutputFormat( lastUsedFilter, outputFile )
        self.outputLayerCombo.setText(outputFile) 
        

    def fillOutputFileEdit_color(self):
        lastUsedFilter = Utils.FileFilter.lastUsedRasterFilter()
        outputFile = Utils.FileDialog.getSaveFileName(self, self.tr( "Select the raster file to save the results to" ), Utils.FileFilter.allRastersFilter(), lastUsedFilter )
        if outputFile==None:
            return
        Utils.FileFilter.setLastUsedRasterFilter(lastUsedFilter)
        self.outputFormat = Utils.fillRasterOutputFormat( lastUsedFilter, outputFile )
        self.outputLayerCombo_color.setText(outputFile) 

# DRASTIC CALCULATION
    def convert(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)
        # read D raster
        inputLayer = self.inputLayerCombo.currentText()
        # read R raster
        inputLayer2 = self.inputLayerCombo2.currentText()
        # read A raster
        inputLayer3 = self.inputLayerCombo3.currentText()
        
        # outpath
        outPath = self.outputLayerCombo.text()  
        lista = []
        lista.append(inputLayer2)
        lista.append(inputLayer3)

        gdal.AllRegister()
        Processing.initialize()
        Processing.runAlgorithm("saga:rastercalculator", None,inputLayer, ';'.join(lista),"a*b*c",False, 7, outPath)
     
       
        
        if self.checkdrastic.isChecked():
            # add result into canvas
            file_info = QFileInfo(outPath)
            if file_info.exists():
                layer_name = file_info.baseName()
            else:
                return False
            rlayer_new = QgsRasterLayer(outPath, layer_name)
            if rlayer_new.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(rlayer_new)
                layer = QgsMapCanvasLayer(rlayer_new)
                layerList = [layer]
                extent = self.iface.canvas.setExtent(rlayer_new.extent())
                self.iface.canvas.setLayerSet(layerList)
                self.iface.canvas.setVisible(True)         
                return True
            else:
                return False    
            QMessageBox.information(self, self.tr( "Finished" ), self.tr( "DRASTIC completed." ) )                    
    
        colorfile = 'C:/OSGeo4W64/apps/qgis/python/plugins/DRASTIC/colorfile.clr'
        outPath_color = self.outputLayerCombo_color.text()
        from colorize import raster2png
              
       
        
        if self.checkcolor.isChecked():
            # add result into canvas
            file_info = QFileInfo(outPath_color)
            if file_info.exists():
                layer_name = file_info.baseName()
            else:
                return False
            rlayer_new = QgsRasterLayer(outPath_color, layer_name)
            if rlayer_new.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(rlayer_new)
                layer = QgsMapCanvasLayer(rlayer_new)
                layerList = [layer]
                extent = self.iface.canvas.setExtent(rlayer_new.extent())
                self.iface.canvas.setLayerSet(layerList)
                self.iface.canvas.setVisible(True)         
                return True
            else:
                return False    
            QMessageBox.information(self, self.tr( "Finished" ), self.tr( "DRASTIC completed." ) )   
        
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True) 