from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from Ui_Hidraulic_conductivity import Ui_Hidraulic_conductivity
import GdalTools_utils as Utils
try:
    from PyQt4.QtCore import QString
except ImportError:
    QString = str
import os, sys
from processing.core.Processing import Processing
from osgeo import ogr
import ftools_utils
from osgeo import gdal
import numpy
from PyQt4 import QtCore, QtGui


class Hidraulic_conductivity(QDialog, Ui_Hidraulic_conductivity):
    
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        
        QObject.connect(self.selectButton, SIGNAL("clicked()"),self.fillInputFileEdit)
        QObject.connect(self.inputLayerCombo, SIGNAL("currentIndexChanged(QString)"), self.fillInputAttrib)
        QObject.connect(self.selectButton3, SIGNAL("clicked()"), self.fillOutputFileEdit)
        QObject.connect(self.buttonAdd, SIGNAL("clicked()"), self.actionAdd)
        QObject.connect(self.buttonRemove, SIGNAL("clicked()"), self.actionRemove)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.convert)   
        
        # connect help
        QObject.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Help), SIGNAL("clicked()"), self.help)               

    # INPUT VECTOR FILE
    def fillInputFileEdit(self):
        lastUsedFilter = Utils.FileFilter.lastUsedVectorFilter()
        inputFile, encoding = Utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), Utils.FileFilter.allVectorsFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.loadFields(inputFile)
        self.inputLayerCombo.addItem(inputFile)
        check = QFile(inputFile)    
        
    def fillInputAttrib(self, inputFile):
        self.layer = QgsVectorLayer(unicode(self.inputLayerCombo.currentText()).encode('utf8'), inputFile  , "ogr")
        self.lineAttrib.clear()    
        changedField = ftools_utils.getFieldList(self.layer)
        for f in changedField:
            if f.type() == QVariant.Int or f.type() == QVariant.String or f.type()==QVariant.Double:
                self.lineAttrib.addItem(unicode(f.name()))   
                
    def loadFields(self, vectorFile = QString()):
        if vectorFile == None:
            return
        try:
            (fields, names) = Utils.getVectorFields(vectorFile)
        except Exception, e:
            QErrorMessage(self).showMessage( str(e) )          
        self.inputLayerCombo.clearEditText()
        ncodec = QTextCodec.codecForName(self.lastEncoding)  
        
    def help(self):
        QMessageBox.about(self, "Hydraulic Conductivity", """<p><b>Hydraulic Conductivity factor</b></p> 
        <p><b>Definition:</b>The C factor relies on the fact that the higher the hydraulic conductivity of the aquifer material, the higher the groundwater vulnerability to pollution. 
        Hydraulic conductivity values are usually obtained from pumping tests and may be introduced by the user in the attribute table of the geological vector file. 
        If the user does not have access to specific hydraulic conductivity values for the region under study, typical values for the prevailing hydrogeological conditions may be adopted.  </p>
        <p><b>Method</b></p> 
        <p>Input file = geological map or a map with hydraulic conductivity values. The user must to define the attribute and the cell size. </p>
        <p><b>Ratings:</b>The ratings are adopted by Aller et al. but the user can modify the values, add or remove lines. </p>
        <p><b>Output file:</b> Hydraulic Conductivity raster file</p>""")  
    
    # ------------------------------ // ------------------------------------ // ----------------------------   
    
    # OUTPUT RASTER FILE
    def fillOutputFileEdit(self):
        lastUsedFilter = Utils.FileFilter.lastUsedRasterFilter()
        outputFile = Utils.FileDialog.getSaveFileName(self, self.tr( "Select the raster file to save the results to" ), Utils.FileFilter.allRastersFilter(), lastUsedFilter )
        if outputFile==None:
            return
        Utils.FileFilter.setLastUsedRasterFilter(lastUsedFilter)
        self.outputFormat = Utils.fillRasterOutputFormat( lastUsedFilter, outputFile )
        self.inputLayerCombo3.setText(outputFile) 
    
    # -------------------------------- // --------------------------------- // -------------------------------     
    
    # BUTTON ADD AND REMOVE CLASSES
    def actionAdd(self):
        n = self.tableWidget.rowCount()
        self.tableWidget.insertRow(n)
        n = self.tableWidget.rowCount()
        return True
                   
    def actionRemove(self):
        n = self.tableWidget.rowCount()
        for i in range(1,n):
            self.tableWidget.removeRow(n-1)
        n = self.tableWidget.rowCount()
        return True
    
   # ---------------------------------- // ----------------------------- // ------------------------------------       
   
   # CONVERT SHAPEFILE TO RASTER
    def convert(self):    
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)
        inputLayer = self.inputLayerCombo.currentText()
        # layer information
        layer = QgsVectorLayer(unicode(inputLayer).encode('utf8'), inputLayer , "ogr")  
        vectorlayer_vector =  layer.dataProvider()
        # extent
        extent_rect = vectorlayer_vector.extent()
        xmin = extent_rect.xMinimum()
        xmax = extent_rect.xMaximum()
        ymin = extent_rect.yMinimum()
        ymax = extent_rect.yMaximum()
        extent = str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax)
        # attribute
        Elevation = self.lineAttrib.currentText()
        # cellsize
        cellSize = int(self.linePix.value())
        outPath = self.inputLayerCombo3.text() 
        
        # indexes for hidraulic conductivity
        numberRows = int(self.tableWidget.rowCount())
        numberColumns = int(self.tableWidget.columnCount())
        classes = ''
        lista = []
        for i in range(0,numberRows):
            for j in range(0,numberColumns):
                self.line = self.tableWidget.item(i,j)
                lista = lista + [str(self.line.text())]
                string = ","
                intervals = string.join(lista)        
        QMessageBox.about(self, 'teste', str(intervals))  
        
        Processing.initialize()
        conductivity = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/conductivity"  
       
        Processing.runAlgorithm("grass7:v.to.rast.attribute", None, inputLayer, 0, Elevation, extent, cellSize, -1.0, 0.0001, conductivity)
        conductivity_raster = conductivity + "." + "tif"
        
        cond_reclassify = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/cond_reclassify.sdat"
        Processing.runAlgorithm("saga:reclassifygridvalues", None, conductivity_raster, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervals, 0, True, 0.0, True, 0.0, cond_reclassify)
       
        
        Processing.runAlgorithm("grass:r.surf.idw", None, cond_reclassify, 12, False, extent, cellSize, outPath)
        
        
        
        
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
        QMessageBox.information(self, self.tr( "Finished" ), self.tr( "Hidraulic conductivity completed." ) )                  
    
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)              