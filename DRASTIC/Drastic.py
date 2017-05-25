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
from Ui_Drastic import Ui_Drastic
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
import Aquifer_media
from PyQt4 import QtCore, QtGui

class Drastic(QDialog, Ui_Drastic):
    
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)  
    
        QObject.connect(self.selectButton, SIGNAL("clicked()"),self.fillInputFileEdit)
        QObject.connect(self.selectButton2, SIGNAL("clicked()"),self.fillInputFileEdit2)
        QObject.connect(self.selectButton3, SIGNAL("clicked()"),self.fillInputFileEdit3)
        QObject.connect(self.selectButton4, SIGNAL("clicked()"),self.fillInputFileEdit4)
        QObject.connect(self.selectButton5, SIGNAL("clicked()"),self.fillInputFileEdit5)
        QObject.connect(self.selectButton6, SIGNAL("clicked()"),self.fillInputFileEdit6)
        QObject.connect(self.selectButton7, SIGNAL("clicked()"),self.fillInputFileEdit7)
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
            
    def fillInputFileEdit4(self):
        lastUsedFilter = Utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = Utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), Utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo4.addItem(inputFile)
        check = QFile(inputFile) 
            
    def fillInputFileEdit5(self):
        lastUsedFilter = Utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = Utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), Utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo5.addItem(inputFile)
        check = QFile(inputFile) 
        
    def fillInputFileEdit6(self):
        lastUsedFilter = Utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = Utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), Utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo6.addItem(inputFile)
        check = QFile(inputFile)
            
    def fillInputFileEdit7(self):
        lastUsedFilter = Utils.FileFilter.lastUsedRasterFilter()
        inputFile, encoding = Utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), Utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo7.addItem(inputFile)
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
        # read S raster
        inputLayer4 = self.inputLayerCombo4.currentText()
        # read T raster
        inputLayer5 = self.inputLayerCombo5.currentText()
        # read I raster
        inputLayer6 = self.inputLayerCombo6.currentText()
        # read C raster
        inputLayer7 = self.inputLayerCombo7.currentText()       
        # outpath
        outPath = self.outputLayerCombo.text()  

        gdal.AllRegister()
        
        # sum of the raster = DRASTIC
        # D
        gdalRaster = gdal.Open(str(inputLayer))
        # multiply by weight
        depth_weight = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/depth_weight"
        x = gdalRaster.RasterXSize
        y = gdalRaster.RasterYSize
        geo = gdalRaster.GetGeoTransform()
        band = gdalRaster.GetRasterBand(1)
        data = band.ReadAsArray(0,0,x,y)    
        mul = numpy.multiply(data, int(self.lineWeightD.value()))
        # Create an output imagedriver with the reclassified values multiplied by the weight
        driver = gdal.GetDriverByName( "GTiff" ) 
        outData = driver.Create(str(depth_weight), x,y,1, gdal.GDT_Float32)
        outData.GetRasterBand(1).WriteArray(mul)
        outData.SetGeoTransform(geo)  
        outData = None  
        
        geo = gdalRaster.GetGeoTransform()
        # pixel size
        pixelSize = geo[1]
        # extent
        minx = geo[0]
        maxy = geo[3]
        maxx = minx + geo[1]*x
        miny = maxy + geo[5]*y
        extent = str(minx) + "," + str(maxx) + "," + str(miny) + "," + str(maxy)
        band = gdalRaster.GetRasterBand(1)
        #data_d = band.ReadAsArray(0,0,x,y)
      
        
        gdalRaster_d = gdal.Open(str(depth_weight))
        x_d = gdalRaster_d.RasterXSize
        y_d = gdalRaster_d.RasterYSize
        geo_d = gdalRaster_d.GetGeoTransform()
        band_d = gdalRaster_d.GetRasterBand(1)
        data_d = band_d.ReadAsArray(0,0,x_d,y_d)   
      
        
        # R
        # resampling R raster
        gdalRaster2 = gdal.Open(str(inputLayer2))
        # multiply by weight
        recharge_weight = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/recharge_weight"
        x2 = gdalRaster2.RasterXSize
        y2 = gdalRaster2.RasterYSize
        geo2 = gdalRaster2.GetGeoTransform()
        band2 = gdalRaster2.GetRasterBand(1)
        data2 = band2.ReadAsArray(0,0,x2,y2)    
        mul2 = numpy.multiply(data2, int(self.lineWeightR.value()))
        # Create an output imagedriver with the reclassified values multiplied by the weight
        driver2 = gdal.GetDriverByName( "GTiff" ) 
        outData2 = driver2.Create(str(recharge_weight), x2,y2,1, gdal.GDT_Float32)
        outData2.GetRasterBand(1).WriteArray(mul2)
        outData2.SetGeoTransform(geo2)  
        outData2 = None         
        
        Processing.initialize()
        resamp_r = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/resamp_r.sdat" 
        Processing.runAlgorithm("saga:resampling", None, recharge_weight, True, 0, 0, extent, pixelSize, resamp_r)   
        #resamp_r_dir = resamp_r + "." + "tif"
        # R
        gdalRaster_r = gdal.Open(str(resamp_r))
        x_r = gdalRaster_r.RasterXSize
        y_r = gdalRaster_r.RasterYSize
        geo_r = gdalRaster_r.GetGeoTransform()
        band_r = gdalRaster_r.GetRasterBand(1)
        data_r = band_r.ReadAsArray(0,0,x_r,y_r)   
       
        # A
        # resampling A raster
        gdalRaster3 = gdal.Open(str(inputLayer3))
        # multiply by weight
        aquifer_weight = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/aquifer_weight"
        x3 = gdalRaster3.RasterXSize
        y3 = gdalRaster3.RasterYSize
        geo3 = gdalRaster3.GetGeoTransform()
        band3 = gdalRaster3.GetRasterBand(1)
        data3 = band3.ReadAsArray(0,0,x3,y3)    
        mul3 = numpy.multiply(data3, int(self.lineWeightA.value()))
        # Create an output imagedriver with the reclassified values multiplied by the weight
        driver3 = gdal.GetDriverByName( "GTiff" ) 
        outData3 = driver3.Create(str(aquifer_weight), x3,y3,1, gdal.GDT_Float32)
        outData3.GetRasterBand(1).WriteArray(mul3)
        outData3.SetGeoTransform(geo3)  
        outData3 = None          
        resamp_a = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/resamp_a.sdat" 
        Processing.runAlgorithm("saga:resampling", None, aquifer_weight, True, 0, 0, extent, pixelSize, resamp_a)   
       
        # A
        gdalRaster_a = gdal.Open(str(resamp_a))
        x_a = gdalRaster_a.RasterXSize
        y_a = gdalRaster_a.RasterYSize
        geo_a = gdalRaster_a.GetGeoTransform()
        band_a = gdalRaster_a.GetRasterBand(1)
        data_a = band_a.ReadAsArray(0,0,x_a,y_a)
       
        
        # S
        # resampling S raster
        gdalRaster4 = gdal.Open(str(inputLayer4))
        # multiply by weight
        soil_weight = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/soil_weight"
        x4 = gdalRaster4.RasterXSize
        y4 = gdalRaster4.RasterYSize
        geo4 = gdalRaster4.GetGeoTransform()
        band4 = gdalRaster4.GetRasterBand(1)
        data4 = band4.ReadAsArray(0,0,x4,y4)    
        mul4 = numpy.multiply(data4, int(self.lineWeightS.value()))
        # Create an output imagedriver with the reclassified values multiplied by the weight
        driver4 = gdal.GetDriverByName( "GTiff" ) 
        outData4 = driver4.Create(str(soil_weight), x4,y4,1, gdal.GDT_Float32)
        outData4.GetRasterBand(1).WriteArray(mul4)
        outData4.SetGeoTransform(geo4)  
        outData4 = None   
        
        # find nodata values
        if self.lineWeightS.value()==2:
            error = -299997        
        
        soil_weight_correct = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/soil_weight_correct.sdat"
        # reclassify no data values
        Processing.initialize()
        Processing.runAlgorithm("saga:reclassifygridvalues", None, soil_weight, 0, error, 0, 0, 0.0, 1.0, 2.0, 0, "0,0,0,0,0,0,0,0,0", 0, True, 0.0, False, 0.0, soil_weight_correct)    
      
        
        
        resamp_s = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/resamp_s.sdat" 
        Processing.runAlgorithm("saga:resampling", None, soil_weight_correct, True, 0, 0, extent, pixelSize, resamp_s)   
       
        # S
        gdalRaster_s = gdal.Open(str(resamp_s))
        x_s = gdalRaster_s.RasterXSize
        y_s = gdalRaster_s.RasterYSize
        geo_s = gdalRaster_s.GetGeoTransform()
        band_s = gdalRaster_s.GetRasterBand(1)
        data_s = band_s.ReadAsArray(0,0,x_s,y_s)
       
        # T
        # resampling T raster
        gdalRaster5 = gdal.Open(str(inputLayer5))
        # multiply by weight
        topography_weight = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/topography_weight"
        x5 = gdalRaster5.RasterXSize
        y5 = gdalRaster5.RasterYSize
        geo5 = gdalRaster5.GetGeoTransform()
        band5 = gdalRaster5.GetRasterBand(1)
        data5 = band5.ReadAsArray(0,0,x5,y5)    
        mul5 = numpy.multiply(data5, int(self.lineWeightT.value()))
        # Create an output imagedriver with the reclassified values multiplied by the weight
        driver5 = gdal.GetDriverByName( "GTiff" ) 
        outData5 = driver5.Create(str(topography_weight), x5,y5,1, gdal.GDT_Float32)
        outData5.GetRasterBand(1).WriteArray(mul5)
        outData5.SetGeoTransform(geo5)  
        outData5 = None        
        resamp_t = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/resamp_t.sdat" 
        Processing.runAlgorithm("saga:resampling", None, topography_weight, True, 0, 0, extent, pixelSize, resamp_t)   
      
        # T
        gdalRaster_t = gdal.Open(str(resamp_t))
        x_t = gdalRaster_t.RasterXSize
        y_t = gdalRaster_t.RasterYSize
        geo_t = gdalRaster_t.GetGeoTransform()
        band_t = gdalRaster_t.GetRasterBand(1)
        data_t = band_t.ReadAsArray(0,0,x_t,y_t)
        #QMessageBox.about(self, "drastic", str(data_t))
        
        # I
        # resampling I raster
        gdalRaster6 = gdal.Open(str(inputLayer6))
        # multiply by weight
        impact_weight = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/impact_weight"
        x6 = gdalRaster6.RasterXSize
        y6 = gdalRaster6.RasterYSize
        geo6 = gdalRaster6.GetGeoTransform()
        band6 = gdalRaster6.GetRasterBand(1)
        data6 = band6.ReadAsArray(0,0,x6,y6)    
        mul6 = numpy.multiply(data6, int(self.lineWeightI.value()))
        # Create an output imagedriver with the reclassified values multiplied by the weight
        driver6 = gdal.GetDriverByName( "GTiff" ) 
        outData6 = driver6.Create(str(impact_weight), x6,y6,1, gdal.GDT_Float32)
        outData6.GetRasterBand(1).WriteArray(mul6)
        outData6.SetGeoTransform(geo6)  
        outData6 = None          
        resamp_i = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/resamp_i.sdat" 
        Processing.runAlgorithm("saga:resampling", None, impact_weight, True, 0, 0, extent, pixelSize, resamp_i)   
       
        # I
        gdalRaster_i = gdal.Open(str(resamp_i))
        x_i = gdalRaster_i.RasterXSize
        y_i = gdalRaster_i.RasterYSize
        geo_i = gdalRaster_i.GetGeoTransform()
        band_i = gdalRaster_i.GetRasterBand(1)
        data_i = band_i.ReadAsArray(0,0,x_i,y_i)
       
        # C
        # resampling C raster
        gdalRaster7 = gdal.Open(str(inputLayer7))
        # multiply by weight
        hydraulic_weight = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/hydraulic_weight"
        x7 = gdalRaster7.RasterXSize
        y7 = gdalRaster7.RasterYSize
        geo7 = gdalRaster7.GetGeoTransform()
        band7 = gdalRaster7.GetRasterBand(1)
        data7 = band7.ReadAsArray(0,0,x7,y7)    
        mul7 = numpy.multiply(data7, int(self.lineWeightC.value()))
        # Create an output imagedriver with the reclassified values multiplied by the weight
        driver7 = gdal.GetDriverByName( "GTiff" ) 
        outData7 = driver7.Create(str(hydraulic_weight), x7,y7,1, gdal.GDT_Float32)
        outData7.GetRasterBand(1).WriteArray(mul7)
        outData7.SetGeoTransform(geo7)  
        outData7 = None         
        resamp_c = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/resamp_c.sdat" 
        Processing.runAlgorithm("saga:resampling", None, hydraulic_weight, True, 0, 0, extent, pixelSize, resamp_c)   
       
        # C
        gdalRaster_c = gdal.Open(str(resamp_c))
        x_c = gdalRaster_c.RasterXSize
        y_c = gdalRaster_c.RasterYSize
        geo_c = gdalRaster_c.GetGeoTransform()
        band_c = gdalRaster_c.GetRasterBand(1)
        data_c = band_c.ReadAsArray(0,0,x_c,y_c) 
       
        
        # sum
        summ = data_d + data_r + data_a + data_s + data_t + data_i + data_c
        
        sum_nodata = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/sum_nodata"
        sum_nodata_rec = sum_nodata + "." + "tif"
        
        # Create an output imagedriver with the reclassified values multiplied by the weight
        driver_sum = gdal.GetDriverByName( "GTiff" ) 
        outData_sum = driver_sum.Create(str(sum_nodata), x,y,1, gdal.GDT_Float32)
        outData_sum.GetRasterBand(1).WriteArray(summ)
        outData_sum.SetGeoTransform(geo)  
        outData_sum = None    
        
        
        # reclassify no data values
        Processing.runAlgorithm("saga:reclassifygridvalues", None, sum_nodata, 0, -10000100352, 0, 0, 0.0, 1.0, 2.0, 0, "0,0,0,0,0,0,0,0,0", 0, True, 0.0, False, 0.0, outPath)        
        
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
              
        raster2png(outPath, colorfile , outPath_color,1, False)
        
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