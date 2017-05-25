from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from Ui_Overall import Ui_Overall
import GdalTools_utils as Utils
from PyQt4 import QtCore, QtGui
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

class Overall(QDialog, Ui_Overall):
    
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
        QObject.connect(self.buttonAttribute, SIGNAL("clicked()"), self.attributeTable)
        
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
    
    # ------------------------------ // ------------------------------------ // ----------------------------    
    
    def help(self):
        QMessageBox.about(self, "Overall lithology of aquifer or aquitard", """<p><b>Overall lithology of aquifer or aquitard</b></p> 
        <p><b>Definition:</b>The O factor corresponds to the overall lithology of the aquifer. 
        The required information is obtained in geological maps and other bibliographical sources. </p>
        <p><b>Method</b></p> 
        <p>Input file = geological map. The user must to define the attribute and the cell size. </p>
        <p><b>Ratings:</b>The ratings are adopted by Foster et al. but the user can modify the values, add or remove lines. 
        Additionally, the users can modify the provided descriptions or introduce their own descriptions. A third option is available through a button (<b>Attribute Table</b>), created to import the input attribute table. 
        This option is faster than the others. </p>
        <p><b>Output file:</b> Overall lithology of aquifer or aquitard raster file</p>""")    
    
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
        # read fields and add a new column with the indexes
        fields = layer.pendingFields() 
        new_field = QgsField("Indexes", QVariant.Double)
        layer_new = vectorlayer_vector.addAttributes([new_field])
        layer.updateFields()
        newFieldIndex = vectorlayer_vector.fieldNameIndex(new_field.name())
        allAttrs = vectorlayer_vector.attributeIndexes()
        # editing the new column
        numberRows = int(self.tableWidget.rowCount())
        numberColumns = int(self.tableWidget.columnCount())
        classes = ''
        lista = []
        for i in range(0,numberRows):
            for j in range(0,numberColumns):
                self.line = self.tableWidget.item(i,j)
                lista = lista + [str(self.line.text())]
               
        # list of description on tool table
        lista_table = lista
       
        field_names = [field.name() for field in fields]
        n = len(field_names)
        lista_attrib = []
        for i in range(0,n):
            f = field_names[i]
            if f==str(Elevation):
                number = i
                for feat in layer.getFeatures():
                    attrb = feat.attributes()
                    attribute_read = attrb[number]
                    lista_attrib = lista_attrib + [str(attribute_read)]
        # list of description on attribute table of shapefile
        lista_attributes = lista_attrib   
       
        # obtain the indexes of the description of shapefile attribute table
        description_common = set(lista_attributes).intersection(lista_table)
        listDescription = list(description_common)
       
        listElem = []
        listElements = []
        for j in range(0,len(listDescription)):
            elem = lista_table.index(listDescription[j])
            listElements = listElements + [elem]
           
            elem_index = lista_table[int(elem+1)]
            listElem = listElem + [float(elem_index)]
    
            
        for l in range(0, len(listElem)):
            layer.startEditing()
            exp = QgsExpression(str(listElem[l]))
            exp.prepare(fields)   
            elemDescription = lista_table[listElements[l]]
            for f in layer.getFeatures():
                # get attributes of column defined by the user
                attrb_elem = f[number]
                if attrb_elem==elemDescription: 
                    f[newFieldIndex] = exp.evaluate(f)
                    layer.updateFeature(f)  
            layer.commitChanges()   
        list_attrb_newField = []
        for features in layer.getFeatures():
            attrb_newField = features.attributes()
            attrb_newField_read = attrb_newField[number+1]
          
        # update and read the new field
        fieldsNew = layer.pendingFields()
        field_names_new = [newField.name() for newField in fieldsNew]          
        parameter_indexes = field_names_new[newFieldIndex]        
        
        Processing.initialize()
        soil = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/soil.sdat"
        Processing.runAlgorithm("grass7:v.to.rast.attribute", None, inputLayer, 0, parameter_indexes, extent, cellSize, -1, 0.0001, outPath)
       
        
              
       
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
        QMessageBox.information(self, self.tr( "Finished" ), self.tr( "Aquifer media completed." ) )                  
    
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)           
    
    def attributeTable(self):
        inputLayer = self.inputLayerCombo.currentText()
        # layer information
        layer = QgsVectorLayer(unicode(inputLayer).encode('utf8'), inputLayer , "ogr")     
        # attribute
        Elevation = self.lineAttrib.currentText()        
        fields = layer.pendingFields() 
        field_names = [field.name() for field in fields]
        n = len(field_names)
        lista_attrib = []
        for i in range(0,n):
            f = field_names[i]
            if f==str(Elevation):
                number = i
                for feat in layer.getFeatures():
                    attrb = feat.attributes()
                    attribute_read = attrb[number] #reads the attribute one by one
                    lista_attrib = lista_attrib + [str(attribute_read)]
        # list of description on attribute table of shapefile
        lista_attributes = lista_attrib  
        len_attb = len(lista_attributes)
        
        # delete duplicate names
        lista_att_dupl = []
        [lista_att_dupl.append(i) for i in lista_attributes if not i in lista_att_dupl]        
        
        # save the description of shapefile in tool table and delete all the other information, such as indexes and other descriptions
        numberRows = int(self.tableWidget.rowCount())
        self.tableWidget.clearContents()
        lista_i = []

        for i in range(0,numberRows):     
            lista_i = lista_i + [i]
        
        for j in range(0,len(lista_att_dupl)):
            self.tableWidget.setItem(j, 0, QtGui.QTableWidgetItem(lista_att_dupl[j]))
            
        # remove the lines with no values
        for a in range(0, numberRows):
            if self.tableWidget.item(a,0)== None:
                self.actionRemove()    