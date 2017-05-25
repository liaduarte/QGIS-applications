from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from Ui_Depth import Ui_Depth
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

class Depth(QDialog, Ui_Depth):
    
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        QObject.connect(self.selectButton, SIGNAL("clicked()"),self.fillInputFileEdit)
        QObject.connect(self.selectMask, SIGNAL("clicked()"),self.fillInputMask)
        QObject.connect(self.selectButton_mdt, SIGNAL("clicked()"),self.fillInputMDT)
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
        
    # INPUT MASK SHAPEFILE
    def fillInputMask(self):
        lastUsedFilter = Utils.FileFilter.lastUsedVectorFilter()
        inputFile, encoding = Utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), Utils.FileFilter.allVectorsFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputMaskCombo.addItem(inputFile)
        check = QFile(inputFile)    
        
    # INPUT MDT
    def fillInputMDT(self):
        lastUsedFilter = Utils.FileFilter.lastUsedRasterFilter()
        inputRaster, encoding = Utils.FileDialog.getOpenFileName(self, self.tr( "Select the input file" ), Utils.FileFilter.allRastersFilter(), lastUsedFilter, True)
        self.lastEncoding = encoding
        self.inputLayerCombo_mdt.addItem(inputRaster)
        check = QFile(inputRaster)     

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
   
   # POINTS INTERPOLATION
    def convert(self):    
        
        gdal.AllRegister()
    # ------------------------ FIRST METHOD -------------------------------------------------
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)
        if self.inputLayerCombo.currentText()!="":
            inputLayer = self.inputLayerCombo.currentText()
            inputMask = self.inputMaskCombo.currentText()
            # layer information
            layer = QgsVectorLayer(unicode(inputLayer).encode('utf8'), inputLayer , "ogr")  
            vectorlayer_vector =  layer.dataProvider()
            layer_mask = QgsVectorLayer(unicode(inputMask).encode('utf8'), inputMask , "ogr")  
            vectorlayer_mask =  layer_mask.dataProvider()        
            # mask extent
            extent_rect = vectorlayer_mask.extent()
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
            # size of atributte table == number of points
            count = layer.featureCount()
            
            # points interpolation idw
            if self.comboBoxMethod.currentText()=="Inverse Distance Weighting":
                Processing.initialize()
                # grid directory (qgis2)
                idw_interpolation = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/idw_interpolation"        
                Processing.runAlgorithm("grass:v.surf.idw", None, inputLayer, count, 2.0, Elevation, False, extent, cellSize, -1.0, 0.0001, idw_interpolation)
                idw_int = idw_interpolation + "." + "tif"
                
                int_mask = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/int_mask"
                # clip grid(interpolation) with polygon (mask)
                Processing.runAlgorithm("saga:clipgridwithpolygon", None, idw_int, inputMask, int_mask)
                int_mask_zone = int_mask + "." + "tif"
            
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
            
            
            # reclassify idw interpolation
            if self.comboBoxMethod.currentText()=="Inverse Distance Weighting":
                idw_reclassify = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/idw_reclassify"
                Processing.runAlgorithm("saga:reclassifygridvalues", None, int_mask_zone, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath)
                  
                
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
            
            # points interpolation kriging
            if self.comboBoxMethod.currentText()=="Kriging":
                Processing.initialize()
                # grid directory (qgis2)
                kriging_interpolation = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/kriging_interpolation"        
                Processing.runAlgorithm("saga:ordinarykrigingglobal", None, inputLayer, Elevation, True, 0, 1, False, 100, False, 0.0, 10, 1000, 1.0, 0.1, 1.0, 0.5, cellSize, True, extent, kriging_interpolation, None)
                kriging_int = kriging_interpolation + "." + "tif"
                
                int_mask_kriging = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/int_mask_kriging"
                # clip grid(interpolation) with polygon (mask)
                Processing.runAlgorithm("saga:clipgridwithpolygon", None, kriging_int, inputMask, int_mask_kriging)
                int_mask_zone_k = int_mask_kriging + "." + "tif"    
                
                kriging_reclassify = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/kriging_reclassify"
                Processing.runAlgorithm("saga:reclassifygridvalues", None, int_mask_zone_k, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath)
                
                
                
                # add result into canvas
                file_info_k = QFileInfo(outPath)
                if file_info_k.exists():
                    layer_name_k = file_info_k.baseName()
                else:
                    return False
                rlayer_new_k = QgsRasterLayer(outPath, layer_name_k)
                if rlayer_new_k.isValid():
                    QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_k)
                    layer_k = QgsMapCanvasLayer(rlayer_new_k)
                    layerList_k = [layer_k]
                    extent_k = self.iface.canvas.setExtent(rlayer_new_k.extent())
                    self.iface.canvas.setLayerSet(layerList_k)
                    self.iface.canvas.setVisible(True)         
                    return True
                else:
                    return False             
        
                # points interpolation cubic spline
            if self.comboBoxMethod.currentText()=="Cubic spline approximation (SAGA)":
                Processing.initialize()
                # grid directory (qgis2)
                cubicSpline_interpolation = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/cubicSpline_interpolation"        
                Processing.runAlgorithm("saga:cubicsplineapproximation", None, inputLayer, Elevation, 0, 3, count, 5, 140.0, extent, cellSize, cubicSpline_interpolation)
                cubicSpline_int = cubicSpline_interpolation + "." + "tif"
                
                int_mask_cubicSpline = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/int_mask_cubicSpline"
                # clip grid(interpolation) with polygon (mask)
                Processing.runAlgorithm("saga:clipgridwithpolygon", None, cubicSpline_int, inputMask, int_mask_cubicSpline)
                int_mask_zone_cs = int_mask_cubicSpline + "." + "tif"    
                
                cubicSpline_reclassify = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/cubicSpline_reclassify"
                Processing.runAlgorithm("saga:reclassifygridvalues", None, int_mask_zone_cs, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath)
                
               
                # add result into canvas
                file_info_cs = QFileInfo(outPath)
                if file_info_cs.exists():
                    layer_name_cs = file_info_cs.baseName()
                else:
                    return False
                rlayer_new_cs = QgsRasterLayer(outPath, layer_name_cs)
                if rlayer_new_cs.isValid():
                    QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_cs)
                    layer_cs = QgsMapCanvasLayer(rlayer_new_cs)
                    layerList_cs = [layer_cs]
                    extent_cs = self.iface.canvas.setExtent(rlayer_new_cs.extent())
                    self.iface.canvas.setLayerSet(layerList_cs)
                    self.iface.canvas.setVisible(True)         
                    return True
                else:
                    return False   
        
            if self.comboBoxMethod.currentText()=="Spatial approximation using spline with tension (GRASS)":
                Processing.initialize()
                # grid directory (qgis2)
                rst_interpolation = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/rst_interpolation"        
                Processing.runAlgorithm("grass:v.surf.rst", None, inputLayer, "", None, Elevation, 40, 40, 300, 0.001, 2.5, 1, 0, 0, False, False, extent, cellSize, -1, 0.0001, rst_interpolation, None, None, None, None, None)
                rst_int = rst_interpolation + "." + "tif"
                
                int_mask_rst = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/int_mask_rst"
                # clip grid(interpolation) with polygon (mask)
                Processing.runAlgorithm("saga:clipgridwithpolygon", None, rst_int, inputMask, int_mask_rst)
                int_mask_zone_rst = int_mask_rst + "." + "tif"    
                
                rst_reclassify = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/rst_reclassify"
                Processing.runAlgorithm("saga:reclassifygridvalues", None, int_mask_zone_rst, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath)
                
               
                # add result into canvas
                file_info_rst = QFileInfo(outPath)
                if file_info_rst.exists():
                    layer_name_rst = file_info_rst.baseName()
                else:
                    return False
                rlayer_new_rst = QgsRasterLayer(outPath, layer_name_rst)
                if rlayer_new_rst.isValid():
                    QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_rst)
                    layer_rst = QgsMapCanvasLayer(rlayer_new_rst)
                    layerList_rst = [layer_rst]
                    extent_rst = self.iface.canvas.setExtent(rlayer_new_rst.extent())
                    self.iface.canvas.setLayerSet(layerList_rst)
                    self.iface.canvas.setVisible(True)         
                    return True
                else:
                    return False       
        
    # ----------------------- SECOND RASTER ----------------------------------------------------------------------------------------
        if self.inputLayerCombo_mdt!="":
            outPath2 = self.inputLayerCombo3.text() 
            # read raster
            inputRaster = self.inputLayerCombo_mdt.currentText()
            layer_raster = QgsRasterLayer(unicode(inputRaster).encode('utf8'), inputRaster , "gdal")      
            data_mdt = layer_raster.dataProvider()
            extent_raster = data_mdt.extent()
            xmin_raster = extent_raster.xMinimum()
            xmax_raster = extent_raster.xMaximum()
            ymin_raster = extent_raster.yMinimum()
            ymax_raster = extent_raster.yMaximum()
            extent_raster_str = str(xmin_raster) + "," + str(xmax_raster) + "," + str(ymin_raster) + "," + str(ymax_raster)     
            cellSize = layer_raster.rasterUnitsPerPixelX()
           
            
            # read maximum depth
            max_depth = self.line_max.value()
            # read distance
            distance = self.line_distance.value()   
            # minimum size
            size = self.line_size.value()
            
            Processing.initialize()
            # grid directory (qgis2)
            # generate stream segments
            stream = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/stream" 
            Processing.runAlgorithm("grass:r.watershed",None, inputRaster, None, None, None, None, size, 0,5,300,False, True, False, False, extent_raster_str, cellSize, None, None, None, stream, None, None, None, None)
            stream_tif = stream + "." + "tif"
            
            # condition stream > 1 to have the lines with value 1
            stream_ones = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/stream_ones" 
           
            Processing.runAlgorithm("gdalogr:rastercalculator", None, stream_tif, "1",None,"1",None,"1",None,"1",None,"1",None,"1","A>1","-9999",5,"", stream_ones)
            stream_ones_str = stream_ones + "." + "tif"
            
            # raster distance
            raster_distance = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/raster_distance.sdat" 
            
            Processing.runAlgorithm("saga:proximitygrid", None, stream_ones_str, raster_distance, None, None)
           
            # condition distance >=  200, always maximum depth meters
            dist_major_200 = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/dist_major_200"
           
            Processing.runAlgorithm("gdalogr:rastercalculator", None, raster_distance, "1",None,"1",None,"1",None,"1",None,"1",None,"1","A>="+str(distance),"-9999",5,"", dist_major_200)
            dist_major_200_str = dist_major_200 + "." + "tif"  
            
            dist_multiplication = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/dist_multiplication"
            Processing.runAlgorithm("gdalogr:rastercalculator", None, dist_major_200_str, "1",None,"1",None,"1",None,"1",None,"1",None,"1","A*"+str(max_depth),"-9999",5,"", dist_multiplication)
            dist_multiplication_str = dist_multiplication + "." + "tif"   
            
            # condition distance < 200, inteprolation between 0 and maximum depth
            dist_minor_200 = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/dist_minor_200"

            Processing.runAlgorithm("gdalogr:rastercalculator", None, raster_distance, "1",None,"1",None,"1",None,"1",None,"1",None,"1","A<"+str(distance),"-9999",5,"", dist_minor_200)
            dist_minor_200_str = dist_minor_200 + "." + "tif"  
            
            # multiplication by the raster distance
            dist_multiplication_dist = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/dist_multiplication_dist"
        
            Processing.runAlgorithm("gdalogr:rastercalculator", None, dist_minor_200_str, "1",raster_distance,"1",None,"1",None,"1",None,"1",None,"1","A*B","-9999",5,"", dist_multiplication_dist)
            dist_multiplication_dist_str = dist_multiplication_dist + "." + "tif"   
            
            # interpolation between 0 and distance
            interpolation_dist = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/interpolation_dist"
         
            Processing.runAlgorithm("gdalogr:rastercalculator", None,dist_multiplication_dist_str , "1",None,"1",None,"1",None,"1",None,"1",None,"1","A*"+str(max_depth)+"/"+str(distance),"-9999",5,"", interpolation_dist)
            interpolation_dist_str = interpolation_dist + "." + "tif"   
            
            # depth surface = sum of two conditions
            depth_surface = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/depth_surface"
          
            Processing.runAlgorithm("gdalogr:rastercalculator", None,dist_multiplication_str , "1",interpolation_dist_str,"1",None,"1",None,"1",None,"1",None,"1","A+B","-9999",5,"", depth_surface)
            depth_surface_tif = depth_surface + "." + "tif"        
            
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
            
            depth_reclassify = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/depth_reclassify.sdat"
            Processing.runAlgorithm("saga:reclassifygridvalues", None, depth_surface_tif, 2, 0.0, 1.0, 0, 0.0, 1.0, 2.0, 0, intervalos, 0, True, 0.0, True, 0.0, outPath2)
           
            
            # add result into canvas
            file_info_norm = QFileInfo(outPath2)
            if file_info_norm.exists():
                layer_name_norm = file_info_norm.baseName()
            else:
                return False
            rlayer_new_norm = QgsRasterLayer(outPath2, layer_name_norm)
            if rlayer_new_norm.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(rlayer_new_norm)
                layer_norm = QgsMapCanvasLayer(rlayer_new_norm)
                layerList_norm = [layer_norm]
                extent_norm = self.iface.canvas.setExtent(rlayer_new_norm.extent())
                self.iface.canvas.setLayerSet(layerList_norm)
                self.iface.canvas.setVisible(True)         
                return True
            else:
                return False                 

        QMessageBox.information(self, self.tr( "Finished" ), self.tr( "Depth completed." ) ) 
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        
        
    def help(self):
        QMessageBox.about(self, "Depth Groundwater", """<p><b>Depth to Groundwater factor</b></p> 
        <p><b>Definition:</b>The D factor contributes to control the distance that pollutants must travel before reaching the aquifer and allows creating a surface map according to depth values measured in the wells. It can be created by two methods: the base method, which allows interpolating data point with the depth to groundwater values into a raster file, and an improvement method, which allows to create a depth to groundwater surface from DEM (Digital Elevation Model).</p>
        <p><b>Base method</b></p> 
        <p>Input files = points file with the depth values and a mask file with the study area extension. The user must to choose the attribute field with the depth values and the cell size. The user must to choose between different <b>interpolation methods</p> to estimate the depth to groundwater map.  </p>
        <p><b>Improved method</b></p> 
        <p>Input file = DEM. The method intends to create a surface through drainage network segments (rivers or streams). A new surface is generated with values ranging from 0 m to a maximum depth value which can be modified by the user (<b>Maximum depth</b> field). A distance raster is created from drainage network segments data and a condition is imposed. The user defines a distance (<b>Distance</b> field) to streams or rivers value, and if the distance is smaller than this threshold, the depth values are interpolated between 0 m (at river or stream segments) and the maximum depth (in places located at the defined maximum distance). </p>
        <p><b>Ratings:</b>The ratings are adopted by Aller et al. but the user can modify the values, add or remove lines. </p>
        <p><b>Output file:</b> Depth to Groundwater raster file</p>""")            

    