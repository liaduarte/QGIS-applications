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
#from processing.outputs import OutputRaster
import sys, os
import numpy
from PyQt4 import QtCore, QtGui


class Topography(QDialog, Ui_Topography):
    
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)  
        
        
        QObject.connect(self.selectButton, SIGNAL("clicked()"),self.fillInputFileEdit)
        QObject.connect(self.inputLayerCombo, SIGNAL("currentIndexChanged(QString)"), self.fillInputAttrib) 
        QObject.connect(self.selectButton_dem, SIGNAL("clicked()"),self.fillInputRasterEdit)
        QObject.connect(self.selectButton3, SIGNAL("clicked()"), self.fillOutputFileEdit)
        QObject.connect(self.buttonAdd, SIGNAL("clicked()"), self.actionAdd)
        QObject.connect(self.buttonRemove, SIGNAL("clicked()"), self.actionRemove)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.convert)
        #self.btnCancel = self.buttonBox.button( QDialogButtonBox.Cancel )
        #QObject.connect(self.btnCancel, SIGNAL( "clicked()" ), self.stopProcessing)
       
        # connect help
        QObject.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Help), SIGNAL("clicked()"), self.help)                 
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
             
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
        QMessageBox.about(self, "Topography", """<p><b>Topography factor</b></p> 
        <p><b>Definition:</b>The T factor concerns the terrain surface slope and its influence on the infiltration of polluted water into the soil. 
        The topography section implements two different methods. If a contour shapefile is available with elevation values, the feature creates the DEM, derives from it the slope and reclassifies according to the defined ratings. 
        If the user does not have the contour file but already has the DEM (raster file), he specifies it as input file, and the DEM generation step is skipped. 
        As before, the slope is calculated and reclassified. </p>
        <p><b>First method</b></p> 
        <p>Input file = contour lines. The user must define the attribute and the cell size. </p>
        <p><b>Second method</b></p> 
        <p>Input file = DEM.</p>
        <p><b>Ratings:</b>The ratings are adopted by Aller et al. but the user can modify the values, add or remove lines.</p>
        <p><b>Output file:</b> Topography raster file</p>""")    
          
    # ------------------------------ // ------------------------------------ // ----------------------------
    
    # INPUT RASTER FILE
    def fillInputRasterEdit(self):
        lastUsedFilter = Utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = Utils.FileDialog.getOpenFileName(self, self.tr( "Select the input DEM" ), Utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        #self.loadFields(inputFile)
        self.inputLayerCombo_dem.addItem(inputFile)
        #check = QFile(inputFile)    
            
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
        QMessageBox.about(self,"Topography",str(n))
        self.tableWidget.insertRow(n)
        n = self.tableWidget.rowCount()
        return True
                
    def actionRemove(self):
        n = self.tableWidget.rowCount()
        for i in range(1,n):
            self.tableWidget.removeRow(n-1)
        n = self.tableWidget.rowCount()
        return True
               
    # ------------------------------- // ------------------------------------ // --------------------------------
    
    # CONVERT VECTOR TO GRID
    def convert(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)
        if self.inputLayerCombo.currentText()!="":
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
            # elevation attribute
            Elevation = self.lineAttrib.currentText()
            # cellsize
            cellSize = int(self.linePix.value())
            outPath = self.inputLayerCombo3.text()
          
            Processing.initialize()
            # grid directory (qgis2)
            filedir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/raster" 
           
            
            Processing.runAlgorithm("grass:v.to.rast.attribute", None, inputLayer, 0,Elevation, extent, cellSize, -1.0, 0.0001, filedir)
            out = filedir + "." + "tif"
            userDir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/grid"
            Processing.runAlgorithm("grass:r.surf.contour", None, out, extent, cellSize, userDir)
            # slope
            userSlope = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/slope"
            outGrid = userDir + "." + "tif"
            Processing.runAlgorithm("grass:r.slope.aspect",None, outGrid, 1, 1, 1.0, 0.0, extent, cellSize, userSlope, None, None, None, None, None, None, None, None)
            
            # reclassify slope raster
            outSlope = userSlope + "." + "tif"
            userSlopeRec = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/slopeRec"            

        if self.inputLayerCombo.currentText()=="":
            gdal.AllRegister() 
            inputLayer_dem = self.inputLayerCombo_dem.currentText()
            #QMessageBox.about(self, "recharge", str(inputRaster))
            gdalRaster = gdal.Open(str(inputLayer_dem))
            #QMessageBox.about(self, "recharge", str(gdalRaster))
            x = gdalRaster.RasterXSize
            y = gdalRaster.RasterYSize
            geo = gdalRaster.GetGeoTransform()  
            minx = geo[0]
            maxy = geo[3]
            maxx = minx + geo[1]*x
            miny = maxy + geo[5]*y
            extent_raster = str(minx) + "," + str(maxx) + "," + str(miny) + "," + str(maxy)  
            pixelSize = geo[1]            

            ## layer information
            #layer_raster = QgsRasterLayer(unicode(inputLayer_dem).encode('utf8'), inputLayer_dem , "gdal")         
            #rasterlayer =  layer_raster.dataProvider()
            ## extent
            #extent_rect = rasterlayer.extent()
            #xmin = extent_rect.xMinimum()
            #xmax = extent_rect.xMaximum()
            #ymin = extent_rect.yMinimum()
            #ymax = extent_rect.yMaximum()
            #extent = str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax)
            ##QMessageBox.about(self, "Topography", str(extent))
            ## cellsize
            #cellSize = layer_raster.rasterUnitsPerPixelX()
            ##cellSize = int(self.linePix.value())
            ##QMessageBox.about(self, "Topography", str(cellSize))
            outPath = self.inputLayerCombo3.text()
            
            # pixel size is the same as the dem raster, miss reamostragem
        
            Processing.initialize()
            mdt_interp = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/mdt_interp"
            Processing.runAlgorithm("grass:r.surf.idw", None, inputLayer_dem, 12, False, extent_raster, pixelSize, mdt_interp)
            mdt = mdt_interp + "." + "tif"    
            
            
            #gdalMDT = gdal.Open(str(mdt_interp) + "." + "tif")
            #x_mdt = gdalMDT.RasterXSize
            #y_mdt = gdalMDT.RasterYSize            
            #geo_mdt = gdalMDT.GetGeoTransform() 
            #band_mdt = gdalMDT.GetRasterBand(1)
            #data_mdt = band_mdt.ReadAsArray(0,0,x_mdt,y_mdt)   
            #geo_mdt = gdalMDT.GetGeoTransform()  
            #minx = geo_mdt[0]
            #maxy = geo_mdt[3]
            #maxx = minx + geo_mdt[1]*x_mdt
            #miny = maxy + geo_mdt[5]*y_mdt
            #extent_raster_new = str(minx) + "," + str(maxx) + "," + str(miny) + "," + str(maxy)  
            #pixelSize_new = geo_mdt[1]            
 
            # slope from DEM
            userSlope_dem = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/slope_dem"
            Processing.runAlgorithm("grass:r.slope.aspect",None, mdt, 1, 1, True, 1, 0, extent_raster, pixelSize, userSlope_dem, None, None, None, None, None, None, None, None)            
        
            # reclassify slope raster
            outSlope_dem = userSlope_dem + "." + "tif"
            #userSlopeRec_dem = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/slopeRec_dem"
        
        # indexes for topography
        numberRows = int(self.tableWidget.rowCount())
        numberColumns = int(self.tableWidget.columnCount())
        classes = ''
        lista = []
        for i in range(0,numberRows):
            for j in range(0,numberColumns):
                self.line = self.tableWidget.item(i,j)
                lista = lista + [str(self.line.text())]
                string = ","
                intervalos = string.join(lista)
        
        if self.inputLayerCombo.currentText()!="":
            Processing.runAlgorithm("saga:reclassifygridvalues", None, outSlope, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath)
            outSlopeRec = userSlopeRec + "." + "tif"

            ## multiply by weight
            #fileInfo = QFileInfo(outSlopeRec)
            #baseName = fileInfo.baseName()
            #rlayer = QgsRasterLayer(outSlopeRec, baseName)
            #gdalRaster = gdal.Open(str(outSlopeRec))
            #x = gdalRaster.RasterXSize
            #y = gdalRaster.RasterYSize
            #geo = gdalRaster.GetGeoTransform()
            #band = gdalRaster.GetRasterBand(1)
            #data = band.ReadAsArray(0,0,x,y)    
            #mul = numpy.multiply(data, int(self.lineWeight.value()))
            ## Create an output imagedriver
            #driver = gdal.GetDriverByName( "GTiff" ) 
            #outData = driver.Create(str(outPath), x,y,1, gdal.GDT_Float32)
            #outData.GetRasterBand(1).WriteArray(mul)
            #outData.SetGeoTransform(geo)  
            #outData = None
            
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

        # reclassify slope_dem values
        if self.inputLayerCombo.currentText()=="":
            topo_interp = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/topo_interp.sdat"
            Processing.runAlgorithm("saga:reclassifygridvalues", None, outSlope_dem, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, topo_interp)
            #topo = topo_interp + "." + "tif"
            
            Processing.runAlgorithm("grass:r.surf.idw", None, topo_interp, 12, False, extent_raster, pixelSize, outPath)  

            ## multiply by weight
            #fileInfo_dem = QFileInfo(outSlopeRec_dem)
            #baseName_dem = fileInfo_dem.baseName()
            #rlayer_dem = QgsRasterLayer(outSlopeRec_dem, baseName_dem)
            #gdalRaster_dem = gdal.Open(str(outSlopeRec_dem))
            #x_dem = gdalRaster_dem.RasterXSize
            #y_dem = gdalRaster_dem.RasterYSize
            #geo_dem = gdalRaster_dem.GetGeoTransform()
            #band_dem = gdalRaster_dem.GetRasterBand(1)
            #data_dem = band_dem.ReadAsArray(0,0,x_dem,y_dem)    
            #mul_dem = numpy.multiply(data_dem, int(self.lineWeight.value()))
            ## Create an output imagedriver
            #driver_dem = gdal.GetDriverByName( "GTiff" ) 
            #outData_dem = driver_dem.Create(str(outPath), x_dem,y_dem,1, gdal.GDT_Float32)
            #outData_dem.GetRasterBand(1).WriteArray(mul_dem)
            #outData_dem.SetGeoTransform(geo_dem)  
            #outData_dem = None
        
            # add result into canvas
            file_info_dem = QFileInfo(outPath)
            if file_info_dem.exists():
                layer_name_dem = file_info_dem.baseName()
            else:
                return False
            rlayer_new_dem = QgsRasterLayer(outPath, layer_name_dem)
            if rlayer_new_dem.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_dem)
                layer_dem = QgsMapCanvasLayer(rlayer_new_dem)
                layerList_dem = [layer_dem]
                extent_dem = self.iface.canvas.setExtent(rlayer_new_dem.extent())
                self.iface.canvas.setLayerSet(layerList_dem)
                self.iface.canvas.setVisible(True)        
                return True
            else:
                return False    
        
        QMessageBox.information(self, self.tr( "Finished" ), self.tr( "Topography completed." ) )               
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
          
  # ----------------------------------- // ---------------------------------------- // -----------------------------------
  
  
            
 
  