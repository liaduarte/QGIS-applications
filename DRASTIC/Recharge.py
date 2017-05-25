from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from Ui_Recharge import Ui_Recharge
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
from gdalconst import *
from processing import ProcessingPlugin
#from processing.outputs import OutputRaster
import sys, os
import numpy
from PyQt4 import QtCore, QtGui

class Recharge(QDialog, Ui_Recharge):
    
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        
        QObject.connect(self.selectButton, SIGNAL("clicked()"),self.fillInputFileEdit)
        QObject.connect(self.selectButton1, SIGNAL("clicked()"),self.fillInputFileEdit1)
        QObject.connect(self.selectButton2, SIGNAL("clicked()"),self.fillInputFileEdit2)
        QObject.connect(self.selectButton4, SIGNAL("clicked()"),self.fillInputFileEdit4)
        QObject.connect(self.inputLayerCombo, SIGNAL("currentIndexChanged(QString)"), self.fillInputAttrib)     
        QObject.connect(self.inputLayerCombo1, SIGNAL("currentIndexChanged(QString)"), self.fillInputAttrib1) 
        QObject.connect(self.inputLayerCombo2, SIGNAL("currentIndexChanged(QString)"), self.fillInputAttrib2) 
        QObject.connect(self.selectButton3, SIGNAL("clicked()"), self.fillOutputFileEdit)
        QObject.connect(self.buttonAdd, SIGNAL("clicked()"), self.actionAdd)
        QObject.connect(self.buttonRemove, SIGNAL("clicked()"), self.actionRemove)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.convert)    
        
        # connect help
        QObject.connect(self.buttonBox.button(QtGui.QDialogButtonBox.Help), SIGNAL("clicked()"), self.help)             
      
# METHOD I
# INPUT VECTOR FILE PRECIPITATION
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
        QMessageBox.about(self, "Net Recharge", """<p><b>Net Recharge factor</b></p> 
        <p><b>Definition:</b>The R factor assumes that the greater the aquifer recharge the greater the groundwater vulnerability to pollution. 
        The feature is composed by three methods to determine the recharge map. The user can choose the best method depending on the available information. 
        The first method estimates net recharge according to a simplified water budget (e.g., Charles et al. 1993; Custodio and Llamas 1996): Recharge = Precipitation - Overland Flow-Evapotranspiration. </p>
        <p><b>First method</b></p> 
        <p>Input files = precipitation, overland flow and evapotranspiration data (mm/year). The user must to define the attributes and the cell size. </p>
        <p><b>Second method</b></p> 
        <p>Input file = precipitation data. The second method requires the availability of recharge rates expressed as a percentage of mean annual precipitation data (mm/year). 
        In this case the user assumes that the spatial variability of precipitation and other factors that control aquifer recharge is not significant and therefore a constant 
        recharge value may be accepted for the entire study region. This type of data may be found in regional hydrogeological studies. The user must define the input precipitation data as well as the respective attribute.  </p>
        <p><b>Third method</b></p> 
        <p>Input file = DEM. If the spatial variability of precipitation is significant and is essentially controlled by altitude, a third method may be applied. 
        In this case, the spatial distribution of precipitation is calculated through a DEM coupled with a regression model expressing precipitation as a function of altitude. 
        Finally, a regional recharge rate expressed as percentage of annual precipitation is applied.  </p>
        <p><b>Ratings:</b>The ratings are adopted by Aller et al. but the user can modify the values, add or remove lines. </p>
        <p><b>Output file:</b> Net Recharge raster file</p>""")            

        
# INPUT VECTOR FILE SURFACE RUNNOFF
    def fillInputFileEdit1(self):
        lastUsedFilter = Utils.FileFilter.lastUsedVectorFilter()
        inputFile, encoding = Utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), Utils.FileFilter.allVectorsFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.loadFields1(inputFile)
        self.inputLayerCombo1.addItem(inputFile)
        check = QFile(inputFile)      

    def fillInputAttrib1(self, inputFile):
        self.layer = QgsVectorLayer(unicode(self.inputLayerCombo1.currentText()).encode('utf8'), inputFile  , "ogr")
        self.lineAttribRunoff.clear()    
        changedField = ftools_utils.getFieldList(self.layer)
        for f in changedField:
            if f.type() == QVariant.Int or f.type() == QVariant.String or f.type()==QVariant.Double:
                self.lineAttribRunoff.addItem(unicode(f.name()))  
                
    def loadFields1(self, vectorFile = QString()):
        if vectorFile == None:
            return
        try:
            (fields, names) = Utils.getVectorFields(vectorFile)
        except Exception, e:
            QErrorMessage(self).showMessage( str(e) )          
        self.inputLayerCombo1.clearEditText()
        ncodec = QTextCodec.codecForName(self.lastEncoding)    
        
# INPUT VECTOR FILE EVAPOTRANSPIRATION
    def fillInputFileEdit2(self):
        lastUsedFilter = Utils.FileFilter.lastUsedVectorFilter()
        inputFile, encoding = Utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), Utils.FileFilter.allVectorsFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.loadFields2(inputFile)
        self.inputLayerCombo2.addItem(inputFile)
        check = QFile(inputFile)    
        
    def fillInputAttrib2(self, inputFile):
        self.layer = QgsVectorLayer(unicode(self.inputLayerCombo1.currentText()).encode('utf8'), inputFile  , "ogr")
        self.lineAttribEvap.clear()    
        changedField = ftools_utils.getFieldList(self.layer)
        for f in changedField:
            if f.type() == QVariant.Int or f.type() == QVariant.String or f.type()==QVariant.Double:
                self.lineAttribEvap.addItem(unicode(f.name()))  
                
    def loadFields2(self, vectorFile = QString()):
        if vectorFile == None:
            return
        try:
            (fields, names) = Utils.getVectorFields(vectorFile)
        except Exception, e:
            QErrorMessage(self).showMessage( str(e) )          
        self.inputLayerCombo2.clearEditText()
        ncodec = QTextCodec.codecForName(self.lastEncoding) 
                    
# INPUT MDT (METHOD II)
    def fillInputFileEdit4(self):
        lastUsedFilter = Utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = Utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), Utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo4.addItem(inputFile)
        check = QFile(inputFile) 

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
        
# ------------------------------ // ---------------------------------- // -----------------------------------                  

# CONVERT VECTOR TO GRID
    def convert(self):    
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)
        if self.inputLayerCombo.currentText()!="":
            inputLayer = self.inputLayerCombo.currentText()
            inputLayer1 = self.inputLayerCombo1.currentText()
            inputLayer2 = self.inputLayerCombo2.currentText()
            # layer information
            layer = QgsVectorLayer(unicode(inputLayer).encode('utf8'), inputLayer , "ogr")  
            layer1 = QgsVectorLayer(unicode(inputLayer1).encode('utf8'), inputLayer1 , "ogr")
            layer2 = QgsVectorLayer(unicode(inputLayer2).encode('utf8'), inputLayer2 , "ogr")
            vectorlayer_vector =  layer.dataProvider()
            vectorlayer_vector1 =  layer1.dataProvider()
            vectorlayer_vector2 =  layer2.dataProvider()
            # extent
            extent_rect = vectorlayer_vector.extent()
            xmin = extent_rect.xMinimum()
            xmax = extent_rect.xMaximum()
            ymin = extent_rect.yMinimum()
            ymax = extent_rect.yMaximum()
            extent = str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax)
            # attribute
            Elevation = self.lineAttrib.currentText()
            Attrib1 = self.lineAttribRunoff.currentText()
            Attrib2 = self.lineAttribEvap.currentText()
            # cellsize
            cellSize = int(self.linePix.value())
            outPath = self.inputLayerCombo3.text()
        
            Processing.initialize()
            # grid directory (qgis2)
            filedir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/pret" 
            filedir1 = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/runoff"
            filedir2 = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/evapo"
            Processing.runAlgorithm("grass:v.to.rast.attribute", None, inputLayer, 0,Elevation, extent, cellSize, -1.0, 0.0001, filedir)
            out = filedir + "." + "tif" 
             
            
            # map subtraction in case of having the three shapefiles
            if self.inputLayerCombo1.currentText()!="":
                Processing.runAlgorithm("grass:v.to.rast.attribute", None, inputLayer1, 0,Attrib1, extent, cellSize, -1.0, 0.0001, filedir1)
                outRunoff = filedir1 + "." + "tif"    
                Processing.runAlgorithm("grass:v.to.rast.attribute", None, inputLayer2, 0,Attrib2, extent, cellSize, -1.0, 0.0001, filedir2)
                outEvap = filedir2 + "." + "tif"         
                recharge = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/recharge"
                gdalRaster_prec = gdal.Open(str(out))
                x_prec = gdalRaster_prec.RasterXSize
                y_prec = gdalRaster_prec.RasterYSize
                geo_prec = gdalRaster_prec.GetGeoTransform()
                band_prec = gdalRaster_prec.GetRasterBand(1)
                data_prec = band_prec.ReadAsArray(0,0,x_prec,y_prec)
                gdalRaster_runoff = gdal.Open(str(outRunoff))
                x_runoff = gdalRaster_runoff.RasterXSize
                y_runoff = gdalRaster_runoff.RasterYSize
                geo_runoff = gdalRaster_runoff.GetGeoTransform()
                band_runoff = gdalRaster_runoff.GetRasterBand(1)
                data_runoff = band_runoff.ReadAsArray(0,0,x_runoff,y_runoff)   
                gdalRaster_evapo = gdal.Open(str(outEvap))
                x_evapo = gdalRaster_evapo.RasterXSize
                y_evapo = gdalRaster_evapo.RasterYSize
                geo_evapo = gdalRaster_evapo.GetGeoTransform()
                band_evapo = gdalRaster_evapo.GetRasterBand(1)
                data_evapo = band_evapo.ReadAsArray(0,0,x_evapo,y_evapo)   
                sub1 = numpy.subtract(data_prec, data_runoff)
                sub2 = numpy.subtract(sub1, data_evapo)
                # Create an output imagedriver with the substraction result
                driver_out = gdal.GetDriverByName( "GTiff" ) 
                outData_recharge = driver_out.Create(str(recharge), x_prec,y_prec,1, gdal.GDT_Float32)
                outData_recharge.GetRasterBand(1).WriteArray(sub2)
                outData_recharge.SetGeoTransform(geo_prec)  
                outData_recharge = None   
            
            # multiplication of precipitation by 0.1, in case of having only the precipitation shapefile
            if self.inputLayerCombo1.currentText()=="":
                userReclassify = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/reclassify"
                # recharge = precipitation * 0.1 (10% of precipitation)
                gdalRaster = gdal.Open(str(out))
                x = gdalRaster.RasterXSize
                y = gdalRaster.RasterYSize
                geo = gdalRaster.GetGeoTransform()
                band = gdalRaster.GetRasterBand(1)
                data = band.ReadAsArray(0,0,x,y)    
                mul = numpy.multiply(data, 0.1)
                # Create an output imagedriver with the multiplication result
                driver = gdal.GetDriverByName( "GTiff" ) 
                outData = driver.Create(str(userReclassify), x,y,1, gdal.GDT_Float32)
                outData.GetRasterBand(1).WriteArray(mul)
                outData.SetGeoTransform(geo)  
                outData = None 
            
            # indexes for topography for the two methods
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
            
            # reclassification of recharge values in case of having only the precipitation shapefile
            if self.inputLayerCombo1.currentText()=="":
                recharge_prec = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/recharge_prec"
                Processing.runAlgorithm("saga:reclassifygridvalues", None, userReclassify, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath)
                
                
                # add result into canvas
                file_info_prec = QFileInfo(outPath)
                if file_info_prec.exists():
                    layer_name_prec = file_info_prec.baseName()
                else:
                    return False
                rlayer_new_prec = QgsRasterLayer(outPath, layer_name_prec)
                if rlayer_new_prec.isValid():
                    QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_prec)
                    layer_prec = QgsMapCanvasLayer(rlayer_new_prec)
                    layerList_prec = [layer_prec]
                    extent_prec = self.iface.canvas.setExtent(rlayer_new_prec.extent())
                    self.iface.canvas.setLayerSet(layerList_prec)
                    self.iface.canvas.setVisible(True)         
                    return True
                else:
                    return False    
                QMessageBox.information(self, self.tr( "Finished" ), self.tr( "Net Recharge completed." ) )           
            
            # reclassification of recharge values in case of having the three shapefiles
            if self.inputLayerCombo1.currentText()!="":
                recharge_prec_run_evap = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/recharge_prec_run_evap"
                Processing.runAlgorithm("saga:reclassifygridvalues", None, recharge, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath)
    
                
                # add result into canvas
                file_info_prec_runoff_evapo = QFileInfo(outPath)
                if file_info_prec_runoff_evapo.exists():
                    layer_name_prec_runoff_evapo = file_info_prec_runoff_evapo.baseName()
                else:
                    return False
                rlayer_new_prec_runoff_evapo = QgsRasterLayer(outPath, layer_name_prec_runoff_evapo)
                if rlayer_new_prec_runoff_evapo.isValid():
                    QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_prec_runoff_evapo)
                    layer_prec_runoff_evapo = QgsMapCanvasLayer(rlayer_new_prec_runoff_evapo)
                    layerList_prec_runoff_evapo = [layer_prec_runoff_evapo]
                    extent_prec_runoff_evapo = self.iface.canvas.setExtent(rlayer_new_prec_runoff_evapo.extent())
                    self.iface.canvas.setLayerSet(layerList_prec_runoff_evapo)
                    self.iface.canvas.setVisible(True)         
                    return True
                else:
                    return False    
                QMessageBox.information(self, self.tr( "Finished" ), self.tr( "Net Recharge completed." ) )            
            
        if self.inputLayerCombo4.currentText()!="":
            gdal.AllRegister()
            # read mdt data
            outPath2 = self.inputLayerCombo3.text()
            inputRaster = self.inputLayerCombo4.currentText()
          
            gdalRaster = gdal.Open(str(inputRaster))

            x = gdalRaster.RasterXSize
            y = gdalRaster.RasterYSize
            geo = gdalRaster.GetGeoTransform()  
            minx = geo[0]
            maxy = geo[3]
            maxx = minx + geo[1]*x
            miny = maxy + geo[5]*y
            extent_raster = str(minx) + "," + str(maxx) + "," + str(miny) + "," + str(maxy)  
            pixelSize = geo[1]
            
            Processing.initialize()
            mdt_interp = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/mdt_interp"
            Processing.runAlgorithm("grass:r.surf.idw", None, inputRaster, 12, False, extent_raster, pixelSize, mdt_interp)
            mdt = mdt_interp + "." + "tif"
            
            gdalMDT = gdal.Open(str(mdt_interp) + "." + "tif")
            x_mdt = gdalMDT.RasterXSize
            y_mdt = gdalMDT.RasterYSize            
            geo_mdt = gdalMDT.GetGeoTransform() 
            band_mdt = gdalMDT.GetRasterBand(1)
            data_mdt = band_mdt.ReadAsArray(0,0,x_mdt,y_mdt) 
            # coeficients a and b of the regression lines, y = ax + b, used for mean monthly precipitation, y(mm), as a function of altitude, x(m)
            a = 0.99
            b = 542.22
            precip_mul = numpy.multiply(data_mdt,a)  
            precipitat = precip_mul + b
            precipitation = numpy.array(precipitat)
            recharge = numpy.multiply(precipitation, 0.15)
            recharge_without_rec = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/recharge_without_rec"
            # Create an output imagedriver with the multiplication result
            driver2 = gdal.GetDriverByName( "GTiff" ) 
            outData2 = driver2.Create(str(recharge_without_rec+'.'+'tif'), x_mdt,y_mdt,1, gdal.GDT_Float32)
            outData2.GetRasterBand(1).WriteArray(recharge)
            outData2.SetGeoTransform(geo_mdt)  
            outData2 = None       

            # indexes for topography for the two methods
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
            
          
            Processing.initialize()

            Processing.runAlgorithm("saga:reclassifygridvalues", None, str(recharge_without_rec) + '.tif' , 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath2)
              
      
            
            # add result into canvas
            file_info_recharge = QFileInfo(outPath2)
            if file_info_recharge.exists():
                layer_name_recharge = file_info_recharge.baseName()
            else:
                return False
            rlayer_new_recharge = QgsRasterLayer(outPath2, layer_name_recharge)
            if rlayer_new_recharge.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_recharge)
                layer_prec_recharge = QgsMapCanvasLayer(rlayer_new_recharge)
                layerList_recharge = [layer_prec_recharge]
                extent_recharge = self.iface.canvas.setExtent(rlayer_new_recharge.extent())
                self.iface.canvas.setLayerSet(layerList_recharge)
                self.iface.canvas.setVisible(True)         
                return True
            else:
                return False               
            QMessageBox.information(self, self.tr( "Finished" ), self.tr( "Net Recharge completed." ) )

 
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)