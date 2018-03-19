# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PI2GIS
                                 A QGIS plugin
 Processing Image to Geographical Information Systems – a learning tool for QGIS
                              -------------------
        begin                : 2017-03-23
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Rui Correia
        email                : rui_correia11@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import QgsRasterLayer, QgsApplication, QgsBrightnessContrastFilter,QgsRasterPipe,QgsMapLayerRegistry

from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QObject, SIGNAL,QDir, QSettings, QFileInfo
from PyQt4.QtGui import QColor, QFont, QMessageBox, QTreeWidget,QAction, QIcon, QFileDialog

#from qgis.core import *

# Initialize Qt resources from file resources.py
import resources

# Import the code for the dialog
from PI2GIS_dialog import PI2GISDialog
from PI2GIS_dialog2 import PI2GISDialog2
from PI2GIS_dialog3 import PI2GISDialog3

from processing import *

import os, sys
import traceback
import optparse
import time

from osgeo import gdal, gdalnumeric, ogr, osr
import os.path
#import glob

#Math
import math

from sys import argv

#Importing Orfeo
import otbApplication

import subprocess
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pylab as plt

from PIL import Image

#SciPY
from scipy import ndimage

#Bilioteca numpy
import numpy as np

try:
    from PyQt4.QtCore import QString
except ImportError:
    QString=str

class PI2GIS:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PI2GIS_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&PI2GIS')

        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PI2GIS')
        self.toolbar.setObjectName(u'PI2GIS')


        # Create the dialog (after translation) and keep reference
        self.dlg = PI2GISDialog()
        self.dlg2 = PI2GISDialog2()
        self.dlg3 = PI2GISDialog3()

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PI2GIS', message)
    
    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        #C:\OSGeo4W64\apps\qgis\python\plugins\PI2GIS\icons

        icon_path = ':/plugins/PI2GIS/icons/icon.png'
        icon_path_2 = ':/plugins/PI2GIS/icons/icon2.png'
        icon_path_3 = ':/plugins/PI2GIS/icons/icon3.png'
        
        #----------------------------Activation of Push Buttons "Run1"-------------------------------------------------
        #self.dlg.pushButton.clicked.connect(self.inputDir)#Caso tente ler todas as imagens de uma vez

        #First Tab
        self.dlg.pushButton.clicked.connect(self.inputDir)
        self.dlg.pushButton_2.clicked.connect(self.outputDir)
        self.dlg.pushButton_3.clicked.connect(self.inputshapefile)
        self.dlg.pushButton_4.clicked.connect(self.outputfiles_2)
        self.dlg.pushButton_10.clicked.connect(self.outrescale)
        self.dlg.pushButton_12.clicked.connect(self.outputPreview)

        #Second Tab
        self.dlg.pushButton_5.clicked.connect(self.inputDir2)
        self.dlg.pushButton_6.clicked.connect(self.inputMTL)
        self.dlg.pushButton_8.clicked.connect(self.inputshapefile_2)
        self.dlg.pushButton_11.clicked.connect(self.OUT_16bits_clip)
        self.dlg.pushButton_9.clicked.connect(self.outputRefl)
        self.dlg.pushButton_13.clicked.connect(self.out_src_t)
        self.dlg.pushButton_14.clicked.connect(self.out_Refle_clip)


        # ----------------------------Activation of Push Buttons "Run2"-------------------------------------------------

        self.dlg2.pushButton.clicked.connect(self.inputabc)
        self.dlg2.pushButton_2.clicked.connect(self.super)
        self.dlg2.pushButton_4.clicked.connect(self.Multi_input)
        self.dlg2.pushButton_5.clicked.connect(self.OUTPUT)
        self.dlg2.pushButton_6.clicked.connect(self.B8_Input)
        self.dlg2.pushButton_7.clicked.connect(self.Out_Pan)
        self.dlg2.pushButton_8.clicked.connect(self.inputshapefile8)
        self.dlg2.pushButton_3.clicked.connect(self.multi_clip)


        #-----------------------------------------------Activation of Push Buttons "Run 3"------------------------------

        #Unsupervised Classification

        self.dlg3.pushButton.clicked.connect(self.inshape3)
        self.dlg3.pushButton_2.clicked.connect(self.un_cl)
        self.dlg3.pushButton_3.clicked.connect(self.InputRGB)
        self.dlg3.pushButton_4.clicked.connect(self.Out_Un_Class)

        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.add_action(
            icon_path_2,
            text=self.tr(u''),
            callback=self.run2,
            parent=self.iface.mainWindow())

        self.add_action(
            icon_path_3,
            text=self.tr(u''),
            callback=self.run3,
            parent=self.iface.mainWindow())

        #------------------------------------------------ComboBOX-------------------------------------------------------
        #-------------------------------------------------RUN1---------------------------------------------------------

        #Filters Methods------------------------------------------------
        FM=[" ","Median","Low Pass","High Pass"]
        self.dlg.comboBox_2.addItems(FM)
        #DN converton
        convertion_type=["","Radiance","Reflectance"]
        self.dlg.comboBox_5.addItems(convertion_type)
        #Convertion From DN to Reflectance----------------------------
        Atmos=[" ","Radiance with DOS1","Reflectance with DOS1"]
        self.dlg.comboBox_3.addItems(Atmos)

        # -------------------------------------------------RUN2---------------------------------------------------------
        #Options Processing
        Options=[" ","Colour Composite ","NDVI (A=B4,B=B5)","NDWI (A=B5,B=B3)","EVI (A=B4,B=B5,C=B2)"]#
        # ,"SMI (A=NDVI Mtlfile=MTL)"]
        self.dlg2.comboBox.addItems(Options)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&PI2GIS'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
	
    #-----------------------------------------------------------Functions INITGUI RUN1 ----------------------------

    # ---------------------------------------------Functions INITGUI RUN1-------------------------------------------------------
    #First Tab
    def inputDir( self ):
        settings = QSettings()#Importar definições do PYQY
        #lastDir = settings.value( "/fTools/lastRasterDir", "." )
        inDir = QFileDialog.getExistingDirectory()#Consegui obter o nome do diretório
        self.dlg.lineEdit.setText(inDir)#Escrito o nome do dir

        self.workDir = QDir( inDir )
        
        #Filtrar imagens
        self.workDir.setFilter( QDir.Files | QDir.NoSymLinks | QDir.NoDotAndDotDot )
        nameFilter = [ "*.tif", "*.TIF", "*.hdf" ]
        fil = self.workDir.setNameFilters( nameFilter )

        self.inputFiles = self.workDir.entryList()#Lista Ligada

        rasters=self.inputFiles

        l = [" "] + ["All Bands"] + rasters

        self.dlg.comboBox_4.clear()

        self.dlg.comboBox_4.addItems(l)

        if len( self.inputFiles ) == 0:
            QMessageBox.warning( self.dlg, self.tr( "No raster files found" ), self.tr( "There are no raster in this directory. Please select another one." ) )
            self.inputFiles = None
            return


        return self.inputFiles#ficheiros filtrados da pasta numa lista ligada


    def inputshapefile(self):
        inputFile = self.dlg.lineEdit_3.setText(
            QFileDialog.getOpenFileName(None, self.tr("Select the input file"), '',
                                        self.tr("ESRI Shapefile (*.shp)")))
        self.layer = QgsVectorLayer(unicode(self.dlg.lineEdit_3.text()).encode('utf8'),
                                    self.dlg.lineEdit_3.text(), "ogr")

    # Output Histogram
    def outputDir(self):
        #self.dlg.lineEdit_2.setText(QFileDialog.getSaveFileName())
        settings = QSettings()#Importar definições do PYQY
        inDir = QFileDialog.getExistingDirectory()#Consegui obter o nome do diretório
        self.dlg.lineEdit_2.setText(inDir)#Escrito o nome do dir


    def outputfiles_2(self):
        settings = QSettings()  # Importar definições do PYQY
        inDir = QFileDialog.getExistingDirectory()  # Consegui obter o nome do diretório
        self.dlg.lineEdit_4.setText(inDir)  # Escrito o nome do dir


    def outrescale(self):
        settings = QSettings()  # Importar definições do PYQY
        inDir = QFileDialog.getExistingDirectory()  # Consegui obter o nome do diretório
        self.dlg.lineEdit_10.setText(inDir)  # Escrito o nome do dir

    #Second Tab
    def inputDir2(self):

        inDir = QFileDialog.getExistingDirectory()  # Consegui obter o nome do diretório
        self.dlg.lineEdit_5.setText(inDir)  # Escrito o nome do dir

        self.workDir = QDir(inDir)

        # Filtrar imagens
        self.workDir.setFilter(QDir.Files | QDir.NoSymLinks | QDir.NoDotAndDotDot)
        nameFilter = ["*.tif", "*.TIF", "*.hdf"]
        fil = self.workDir.setNameFilters(nameFilter)
        # selg.workDir esta filtrado e chama se fil
        self.inputFiles_2 = self.workDir.entryList()  # Lista Ligada

        if len(self.inputFiles_2) == 0:
            QMessageBox.warning(self.dlg, self.tr("No raster files found"),
                                self.tr("There are no raster in this directory. Please select another one."))
            self.inputFiles_2 = None
            return


        return self.inputFiles_2  # ficheiros filtrados da pasta numa lista ligada


    def inputMTL(self):
        self.dlg.lineEdit_6.setText(QFileDialog.getOpenFileName())


    def inputshapefile_2(self):
        inputFile = self.dlg.lineEdit_7.setText(
            QFileDialog.getOpenFileName(None, self.tr("Select the input file"), '',
                                        self.tr("ESRI Shapefile (*.shp)")))
        self.layer = QgsVectorLayer(unicode(self.dlg.lineEdit_7.text()).encode('utf8'),
                                    self.dlg.lineEdit_7.text(), "ogr")

    def OUT_16bits_clip(self):
        settings = QSettings()  # Importar definições do PYQY
        inDir = QFileDialog.getExistingDirectory()  # Consegui obter o nome do diretório
        self.dlg.lineEdit_8.setText(inDir)  # Escrito o nome do dir


    def outputRefl(self):
        settings = QSettings()  # Importar definições do PYQY
        inDir = QFileDialog.getExistingDirectory()  # Consegui obter o nome do diretório
        self.dlg.lineEdit_9.setText(inDir)  # Escrito o nome do dir

    def out_src_t(self):
        settings = QSettings()  # Importar definições do PYQY
        inDir = QFileDialog.getExistingDirectory()  # Consegui obter o nome do diretório
        self.dlg.lineEdit_11.setText(inDir)  # Escrito o nome do dir

    def out_Refle_clip(self):
        settings = QSettings()  # Importar definições do PYQY
        inDir = QFileDialog.getExistingDirectory()  # Consegui obter o nome do diretório
        self.dlg.lineEdit_14.setText(inDir)  # Escrito o nome do dir

    #---------------------------------------------Functions INITGUI RUN2-------------------------------------------------------

    def inputabc(self):
        settings = QSettings()  # Importar definições do PYQY
        # lastDir = settings.value( "/fTools/lastRasterDir", "." )
        inDir = QFileDialog.getExistingDirectory()  # Consegui obter o nome do diretório
        self.dlg2.lineEdit.setText(inDir)  # Escrito o nome do dir

        self.workDir = QDir(inDir)

        # Filtrar imagens
        self.workDir.setFilter(QDir.Files | QDir.NoSymLinks | QDir.NoDotAndDotDot)
        nameFilter = ["*.tif", "*.TIF", "*.hdf"]
        fil = self.workDir.setNameFilters(nameFilter)

        self.inputFiles = self.workDir.entryList()  # Lista Ligada

        RASTERS = self.inputFiles
        l = [" "] + RASTERS

        self.dlg2.comboBox_3.clear()
        self.dlg2.comboBox_4.clear()
        self.dlg2.comboBox_5.clear()

        self.dlg2.comboBox_3.addItems(l)
        self.dlg2.comboBox_4.addItems(l)
        self.dlg2.comboBox_5.addItems(l)

        if len(self.inputFiles) == 0:
            QMessageBox.warning(self.dlg, self.tr("No raster files found"),
                                self.tr("There are no raster in this directory. Please select another one."))
            self.inputFiles = None
            return


        return self.inputFiles  # ficheiros filtrados da pasta numa lista ligada

    def inputshapefile8(self):
        inputFile = self.dlg2.lineEdit_8.setText(
            QFileDialog.getOpenFileName(None, self.tr("Select the input file"), '',
                                        self.tr("ESRI Shapefile (*.shp)")))
        self.layer = QgsVectorLayer(unicode(self.dlg2.lineEdit_8.text()).encode('utf8'),
                                    self.dlg2.lineEdit_8.text(), "ogr")

    def OUTPUT(self):    
        self.dlg2.lineEdit_5.setText(QFileDialog.getSaveFileName())

    def multi_clip(self):
        self.dlg2.lineEdit_3.setText(QFileDialog.getSaveFileName())

    def Multi_input(self):
        self.dlg2.lineEdit_4.setText(QFileDialog.getOpenFileName())

    def B8_Input(self):
        self.dlg2.lineEdit_6.setText(QFileDialog.getOpenFileName())

    def super(self):
        self.dlg2.lineEdit_2.setText(QFileDialog.getSaveFileName())

    def Out_Pan(self):
        self.dlg2.lineEdit_7.setText(QFileDialog.getSaveFileName())


    #----------------------------------------------Functions INITGUI RUN3-------------------------------------------

    def inshape3(self):
        inputFile = self.dlg3.lineEdit.setText(
            QFileDialog.getOpenFileName(None, self.tr("Select the input file"), '',
                                        self.tr("ESRI Shapefile (*.shp)")))
        self.layer = QgsVectorLayer(unicode(self.dlg3.lineEdit.text()).encode('utf8'),
                                    self.dlg3.lineEdit.text(), "ogr")

    def un_cl(self):
        self.dlg3.lineEdit_2.setText(QFileDialog.getSaveFileName())

    def InputRGB(self):
        self.dlg3.lineEdit_3.setText(QFileDialog.getOpenFileName())

    def Out_Un_Class(self):
        self.dlg3.lineEdit_4.setText(QFileDialog.getSaveFileName())

    #------------------------------------------------RUN1---------------------------------------------------------------
    def run(self):
        self.dlg.show()
        QObject.connect(self.dlg.button_box, SIGNAL("accepted()"), self.preprocessing)
        QObject.connect(self.dlg.button_box, SIGNAL("rejected()"), self.exit)
        QObject.connect(self.dlg.button_box_2, SIGNAL("accepted()"), self.convertionDN)
        QObject.connect(self.dlg.button_box_2, SIGNAL("rejected()"), self.exit)

    def exit(self):
        # Close the widnow
        self.dlg.close()


    def preprocessing(self):#Pre Processing Image

        inputLayer = self.dlg.lineEdit.text()#Name until directory thanks to inDir
        out_tx_hist = self.dlg.lineEdit_2.text()  # In this case it is directory where I want to put histogram images
        # Obtain with outputDir only strings
        out_rescale = self.dlg.lineEdit_10.text()
        #mask
        inshape=self.dlg.lineEdit_3.text()
        rasters = self.inputFiles
        Pre_Processed_tx = self.dlg.lineEdit_4.text()
        
        # histogram for all raster
        if self.dlg.comboBox_4.currentText()=='All Bands':
            #histograms creation
            if len(out_rescale) > 0:
                for i in range(len(rasters)):
                    #The list rasters only has images (less 2 elements than, combobox_4
                    image_in =os.path.join(str(inputLayer), str(rasters[i])) #"path_input_image"
                    #QMessageBox.about(self.dlg, 'raster', rasters[i])
                    out=QFileInfo(QgsApplication.qgisUserDbFilePath()).path()+"out.tif"
                    #QMessageBox.about(self.dlg, 'raster', str(out))


                    subprocess.check_call(["gdal_translate.exe","-of","GTiff","-ot","Float32","-scale","-co", "TFW=YES",image_in,out])

                    subprocess.check_call(["gdalwarp.exe","-srcnodata", "255", "-dstnodata", "nan","-crop_to_cutline","-cutline",inshape,out,
                                     os.path.join(str(out_rescale),"8bits_"+str(rasters[i]))])


            if len(out_tx_hist)>0 or len(Pre_Processed_tx)>0:
                for i in range(len(rasters)):
                    # The list rasters only has images (less 2 elements than, combobox_4
                    image_in = os.path.join(str(inputLayer), str(rasters[i]))  # "path_input_image"
                    # QMessageBox.about(self.dlg, 'raster', rasters[i])

                    im = gdal.Open(os.path.join(str(inputLayer), str(str(rasters[i]))))
                    #image_in = os.path.join(str(inputLayer), str(rasters[selected_raster_index]))
                    im_array = np.array(im.GetRasterBand(1).ReadAsArray())
                    x = im.RasterXSize
                    y = im.RasterYSize
                    geo = im.GetGeoTransform()
                    srs = im.GetProjectionRef()  # Projection
                    # QMessageBox.about(self.dlg,'raster',str(im))
                    image = im_array.flatten()  # copy of the array collapsed into one dimension.
                    QMessageBox.about(self.dlg,'raster',str(image))

                    #Histogram

                    plt.figure()#show image
                    plt.title(str(str(rasters[i]))+"_Histogram")
                    plt.ylabel("Number of pixels")
                    plt.xlabel("Pixels Values")
                    #,bins=256 I culd use bins=None
                    plt.hist(image,bins=256,range=[0,255])#,255])
                    plt.show()

                    H="Hist_"
                    plt.savefig(os.path.join(str(out_tx_hist),H+"8bits_"+str(rasters[i]))) # Guardar de ficheiro de texto
                
            #histogram equalization
            if  self.dlg.checkBox.isChecked()or len(Pre_Processed_tx):
                im = gdal.Open(os.path.join(str(inputLayer), str(str(rasters[i]))))
                # image_in = os.path.join(str(inputLayer), str(rasters[selected_raster_index]))
                im_array = np.array(im.GetRasterBand(1).ReadAsArray())
                x = im.RasterXSize
                y = im.RasterYSize
                geo = im.GetGeoTransform()
                srs = im.GetProjectionRef()  # Projection
                # QMessageBox.about(self.dlg,'raster',str(im))
                image = im_array.flatten()  # copy of the array collapsed into one dimension.
                # QMessageBox.about(self.dlg,'raster',str(im))
                nbr_bins = 256
                imhist,bins =np.histogram(image,256,[0,256])
                cdf = imhist.cumsum()# cumulative distribution function
                cdf = 255 * cdf / cdf[-1]#normalize
                data2 = np.interp(image, bins[:-1], cdf)
                data2 = data2.reshape(im_array.shape)
                H = "Equalization_"
                driver = gdal.GetDriverByName("GTiff")
                outData = driver.Create(os.path.join(str(Pre_Processed_tx),H + str("8bits_"+str(rasters[i]))), x, y, 1,
                                        gdal.GDT_Float32)
                outData.SetProjection(srs)
                outData.SetGeoTransform(geo)
                outData.GetRasterBand(1).WriteArray(im_array)
                outData = None


                # ------------------------FILTERS-------------------------------------
                # Call FM function according to selection in ComboBox-----------------------
                selectedFMindex = self.dlg.comboBox_2.currentIndex()
                sigma = self.dlg.spinBox_2.value()
                if selectedFMindex == 0:
                    pass  # No FM function selected
                if selectedFMindex == 1:# Median
                    data = ndimage.filters.median_filter(im_array, size=(sigma, sigma))
                    H="Median_"
                if selectedFMindex == 2:# Low Pass
                    H="Low Pass_"
                    data = ndimage.gaussian_filter(im_array, sigma)
                if selectedFMindex == 3:# High Pass countor detection
                    H = "High Pass_"
                    lowpass = ndimage.gaussian_filter(im_array, sigma)
                    data = im_array - lowpass

                if selectedFMindex != 0:
                    driver = gdal.GetDriverByName("GTiff")
                    outData = driver.Create(os.path.join(str(Pre_Processed_tx),H + str(str(rasters[i]))), x, y, 1,
                                            gdal.GDT_Float32)
                    outData.SetProjection(srs)
                    outData.SetGeoTransform(geo)
                    outData.GetRasterBand(1).WriteArray(im_array)
                    outData = None

        #one selected band
        if self.dlg.comboBox_4.currentText()!='All Bands':
            # histogram creation
            selected_raster_index = self.dlg.comboBox_4.currentIndex()-2
            # List rasters has less 2 elements. combobox_4 has +2 " " and "All Bands"
            #QMessageBox.about(self.dlg,'selected_raster_index',str(selected_raster_index))
            #QMessageBox.about(self.dlg, 'selected_raster_text', str(self.dlg.comboBox_4.currentText()))

            #Image
            image_in =os.path.join(str(inputLayer), str(rasters[selected_raster_index])) #"path_input_image"
            out=QFileInfo(QgsApplication.qgisUserDbFilePath()).path()+"/out"

            if len(out_rescale) > 0:

                subprocess.call(["gdal_translate.exe","-of","GTiff","-ot","Float32","-scale","-co", "TFW=YES",image_in,out])

                subprocess.call(["gdalwarp.exe","-srcnodata", "255", "-dstnodata", "nan","-crop_to_cutline","-cutline",inshape,out,
                                 os.path.join(str(out_rescale),"8bits_"+str(rasters[selected_raster_index]))])

            # im = gdal.Open(os.path.join(str(inputLayer),str("8bits_"+str(rasters[selected_raster_index-2]))))
            # Teacher wanted to connect with the rescalled images recently created.
            # The idea is to separete rescale from histograms production
            # im = gdal.Open(os.path.join(str(inputLayer), str("8bits_" + str(rasters[selected_raster_index]))))


            if len(out_tx_hist) > 0 or self.dlg.checkBox.isChecked() or len(Pre_Processed_tx)>0:

                #Open and reading image in different ways
                im = gdal.Open(image_in)
                im_array = np.array(im.GetRasterBand(1).ReadAsArray())#im_array is values of pixeis in an array
                x = im.RasterXSize
                y = im.RasterYSize
                geo = im.GetGeoTransform()
                srs = im.GetProjectionRef()  # Projection
                # QMessageBox.about(self.dlg,'raster',str(im))
                image = im_array.flatten()  # copy of the array collapsed into one dimension.
                # QMessageBox.about(self.dlg,'raster',str(im))

            #Histogram
            if len(out_tx_hist) > 0:
                plt.figure()#show image
                plt.title(str(str(rasters[selected_raster_index]))+"_Histogram")
                plt.ylabel("Number of pixels")
                plt.xlabel("Pixels Values")
                #,bins=256 I culd use bins=None
                plt.hist(image,bins=256,range=[0,255])#,255])
                plt.show()

                H="Hist_"
                plt.savefig(os.path.join(str(out_tx_hist),H+str(rasters[selected_raster_index]))) # Guardar de ficheiro de texto

            #Histogram equalization
            if  self.dlg.checkBox.isChecked():
                nbr_bins = 256
                imhist,bins =np.histogram(image,256,[0,256])
                cdf = imhist.cumsum()# cumulative distribution function
                cdf = 255 * cdf / cdf[-1]#normalize
                data2 = np.interp(image, bins[:-1], cdf)#image is data in one dimension
                data2=data2.reshape(im_array.shape)
                H = "Equalization_"
                driver = gdal.GetDriverByName("GTiff")
                outData = driver.Create(os.path.join(str(Pre_Processed_tx),H + str(str(rasters[selected_raster_index]))), x, y, 1,
                                        gdal.GDT_Float32)
                outData.SetProjection(srs)
                outData.SetGeoTransform(geo)
                outData.GetRasterBand(1).WriteArray(data2)
                outData = None

            # ------------------------FILTERS-------------------------------------
            # Call FM function according to selection in ComboBox-----------------------
            #Filters
            selectedFMindex = self.dlg.comboBox_2.currentIndex()
            sigma = self.dlg.spinBox_2.value()
            if selectedFMindex == 0:
                    pass  # No FM function selected
            if selectedFMindex == 1:# Median
                data = ndimage.filters.median_filter(im_array, size=(sigma, sigma))
                H="Median_sg"+str(sigma)+"_"
            if selectedFMindex == 2:# Low Pass
                H="Low Pass_sg"+str(sigma)+"_"
                data = ndimage.gaussian_filter(im_array, sigma)
            if selectedFMindex == 3:# High Pass countor detection
                H = "High Pass_sg"+str(sigma)+"_"
                lowpass = ndimage.gaussian_filter(im_array, sigma)
                data = im_array - lowpass

            if selectedFMindex != 0:

                driver = gdal.GetDriverByName("GTiff")
                outData = driver.Create(os.path.join(str(Pre_Processed_tx),H + str(str(rasters[selected_raster_index]))), x, y, 1,
                                        gdal.GDT_Float32)
                outData.SetProjection(srs)
                outData.SetGeoTransform(geo)
                outData.GetRasterBand(1).WriteArray(data)
                outData = None

        QMessageBox.about(self.dlg, 'pre operations', 'Finished')

    def outputPreview(self):
        # Temporary directory
        light_preview = os.path.join(QFileInfo(QgsApplication.qgisUserDbFilePath()).path(), 'light_preview')
        inputLayer = self.dlg.lineEdit.text()  # Name until directory thanks to inDir
        rasters = self.inputFiles

        if self.dlg.comboBox_4.currentText()=='All Bands':
            QMessageWarning(self.dlg, 'raster', 'Choose one band')
        if self.dlg.comboBox_4.currentText()!='All Bands':
            selected_raster_index = self.dlg.comboBox_4.currentIndex()
            # 3. Light Correction.........................................................................
            light_value = self.dlg.horizontalSlider.value()
            #if light_value != 0:
                #data = data + light_value
            file_Info = QFileInfo(str(os.path.join(str(inputLayer), str(rasters[selected_raster_index ]))))
            layer_name = file_Info.baseName()
            layer = QgsRasterLayer(str(os.path.join(str(inputLayer), str(rasters[selected_raster_index ]))), layer_name)
            # define the filter
            brightnessFilter = QgsBrightnessContrastFilter()
            brightnessFilter.setBrightness(light_value)
            pipe = QgsRasterPipe()
            # assign filter to raster pipe
            layer.pipe().set(brightnessFilter)
            # apply changes
            layer.triggerRepaint()
            QgsMapLayerRegistry.instance().addMapLayer(layer)

    ####Convertion DN
    def convertionDN(self):
        #-----------LANDSAT 8 (OLI)-----------------
        #Source

        #Convertion to radiance with git hub

        #https://gist.github.com/jgomezdans/5488682

        #Author:  J Gomez-Dans <j.gomez-dans@ucl.ac.uk>

        #Directory of LandBands in DN

        #From UI file
        InputLayer2 = self.dlg.lineEdit_5.text()

        # Read MTL file
        MTL = self.dlg.lineEdit_6.text()

        inshape2=self.dlg.lineEdit_7.text()
        out_16_clip=self.dlg.lineEdit_8.text()

        Out_Refle = self.dlg.lineEdit_9.text()

        out_T = self.dlg.lineEdit_11.text()

        out_Refle_clip=self.dlg.lineEdit_14.text()

        #Extract Data from MTL file
        if not (len(InputLayer2) and len(MTL)) == 0:
            fp = open(str(MTL), 'r')
            #Creation of dictionaries for Reflectance multi and add
            multi = {}
            add = {}
            se = {}
            d = {}
            multi_rad = {}
            add_rad = {}
            rad_max = {}
            refle_max = {}
            #rad_min= {}

            for line in fp:
                if (line.find("REFLECTANCE_MULT_BAND") >= 0):
                    s = line.split("=")  # Split by equal sign
                    the_band = int(s[0].split("_")[3])  # Band number as integer
                    if the_band in [1,2, 3, 4, 5, 6, 7,8,9,10,11,12]: # Is this one of the bands we want?
                        multi[the_band] = float(s[-1])  # Attribui um valor a uma chave como float
                if (line.find("REFLECTANCE_ADD_BAND") >= 0):
                    s = line.split("=")  # Split by equal sign
                    the_band = int(s[0].split("_")[3])  # Band number as integer
                    if the_band in [1,2, 3, 4, 5, 6, 7,8,9,10,11,12]: # Is this one of the bands we want?
                        add[the_band] = float(s[-1])  # Get constant as float
                if (line.find("REFLECTANCE_MAXIMUM_BAND")>=0):
                    s = line.split("=")  # Split by equal sign
                    the_band = int(s[0].split("_")[3])  # Band number as integer
                    if the_band in [1,2, 3, 4, 5, 6, 7,8,9,10,11,12]: # Is this one of the bands we want?
                        refle_max[the_band] = float(s[-1])
                if (line.find("RADIANCE_MULT_BAND") >= 0):
                    s = line.split("=")  # Split by equal sign
                    the_band = int(s[0].split("_")[3])  # Band number as integer
                    if the_band in [1,2, 3, 4, 5, 6, 7,8,9,10,11,12]: # Is this one of the bands we want?
                        multi_rad[the_band] = float(s[-1])
                if (line.find("RADIANCE_ADD_BAND") >= 0):
                    s = line.split("=")  # Split by equal sign
                    the_band = int(s[0].split("_")[3])  # Band number as integer
                    if the_band in [1,2, 3, 4, 5, 6, 7,8,9,10,11,12]: # Is this one of the bands we want?
                        add_rad[the_band] = float(s[-1])
                if (line.find("RADIANCE_MAXIMUM_BAND")>=0):
                    s = line.split("=")  # Split by equal sign
                    the_band = int(s[0].split("_")[3])  # Band number as integer
                    if the_band in [1,2, 3, 4, 5, 6, 7,8,9,10,11,12]: # Is this one of the bands we want?
                        rad_max[the_band] = float(s[-1])
                if (line.find("SUN_ELEVATION")>= 0):
                    s = line.split("=")  # Split by equal sign
                    #QMessageBox.about(self.dlg, 's', str(s))
                    se=float(s[1])
                    #QMessageBox.about(self.dlg, 'se', str(se))
                    # Solar zenith angle θs  = 90° - θe
                    ss = 90 - se
                if (line.find("EARTH_SUN_DISTANCE")>=0):
                    s = line.split("=")  # Split by equal sign
                    d=float(s[-1])

        RastersDN = self.inputFiles_2

        #Clip Raster 16 bits
        if len(out_16_clip)>0:
            for i in range(len(RastersDN)):
                im_in = os.path.join(str(InputLayer2), str(RastersDN[i]))
                im_out = os.path.join(str(out_16_clip),"16bits_" + str(RastersDN[i]))
                #QMessageBox.about(self.dlg, 'Raster', str(RastersDN[i]))
                #QMessageBox.about(self.dlg, 'Dir', str(out_Refle_clip))
                value_0 = self.dlg.spinBox.value()
                subprocess.call(["gdalwarp.exe","-srcnodata", str(value_0), "-dstnodata", "nan","-of","GTiff","-crop_to_cutline",
                                 "-cutline",inshape2,im_in,im_out])
                if len(inshape2)==0:
                    subprocess.call(["gdalwarp.exe", "-srcnodata", str(value_0), "-dstnodata", "nan",
                                     "-of", "GTiff",im_in, im_out])

        if not (len(InputLayer2) and len(Out_Refle) and len(MTL)) == 0:
            #Has to have landbands in
            for i in range(len(RastersDN)):
                #Temporary
                band=i+2#Works for 2,3,4,5,6,7 and 8
                image_in=os.path.join(str(InputLayer2),str(RastersDN[i]))
                s = str(RastersDN[i])
                g=gdal.Open(image_in)
                #QMessageBox.about(self.dlg, 'Raster', str(RastersDN[i]))
                ## find DNmin in raster for DOS1
                x_size, y_size = g.RasterXSize, g.RasterYSize
                data = np.array(g.GetRasterBand(1).ReadAsArray())  # ,dtype=float)#arriscar o float
                DNmin=np.amin(data)
                geo = g.GetGeoTransform()

                #-----------DOS 1 Landsat_8_OLI------------

                #This was done for the band 2 until 8
                selectedCTindex = self.dlg.comboBox_5.currentIndex()
                if selectedCTindex==0:
                    pass
                if selectedCTindex==1:
                    im=self.convertionRad(data,multi_rad[band],add_rad[band])
                    H = "Rad_"
                if selectedCTindex==2:
                    im=self.convertionRefle(data,multi[band],add[band],se)
                    im[im>1]=np.nan
                    H = "Rfl_"
                selectedDOSindex=self.dlg.comboBox_3.currentIndex()
                if selectedDOSindex==0:
                    pass
                if selectedDOSindex==1:#Radiance
                    Ldos=(0.01*self.ESUN(d,refle_max[band],rad_max[band])*(math.cos(math.radians(ss))))/math.pi*d**2
                    Lmin=multi_rad[band]*DNmin+add_rad[band]
                    im=Lmin-Ldos
                if selectedDOSindex==2:
                    E=self.ESUN(d, refle_max[band], rad_max[band])
                    Lp = multi_rad[band] * DNmin + add_rad[band]-0.01 * E * (math.cos(math.radians(ss))) / (math.pi * math.pow(d,2))
                    Ll=self.convertionRad(data,multi_rad[band],add_rad[band])
                    im=(math.pi*(Ll-Lp)*math.pow(d,2))/(E*math.cos(math.radians(ss)))
                    im[im > 1] = np.nan
                    H="DOS1_"

                # QMessageBox.about(self.dlg, 'teste', str(im))
                gdal.AllRegister()
                # Output GDAL way
                # Create an output imagedriver
                driver = gdal.GetDriverByName("GTiff")
                outDN = os.path.join(str(Out_Refle), H + str(RastersDN[i]))
                #s is the name of the file like Landsat_B*
                #outData = driver.Create(os.path.join(str(Out_Refle), H + s), x_size, y_size, 1,gdal.GDT_Float32)
                outData = driver.Create(outDN,x_size, y_size, 1, gdal.GDT_Float32)
                outData.GetRasterBand(1).WriteArray(im)
                outData.SetGeoTransform(geo)
                outData = None
            QMessageBox.about(self.dlg, 'Convertion ', "complete")

        # Correct Rasters Resulted from Reflactance
        if len(InputLayer2) > 0 and len(out_T)>0:
            #out = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/out"
            for i in range(len(RastersDN)):
                im_in2 = os.path.join(str(InputLayer2), str(RastersDN[i]))
                im_out2 = os.path.join(str(out_T),"T_" + str(RastersDN[i]))
                # Change coordinate system
                epsg = self.dlg.spinBox_3.value()
                subprocess.call(["gdalwarp.exe", "-of", "GTiff", "-t_srs", "EPSG:"+str(epsg), im_in2, im_out2])
                if len(out_Refle_clip) > 0:
                    im_out3 = os.path.join(str(out_Refle_clip), "Cl_" + str(RastersDN[i]))
                    replace_ndata = self.dlg.doubleSpinBox.value()
                    subprocess.call(["gdalwarp.exe","-ot","Float32","-srcnodata", str(replace_ndata), "-dstnodata", "nan",
                                     "-crop_to_cutline","-cutline",inshape2,im_out2,im_out3])
                    if len(inshape2)==0:#No clip
                        subprocess.call(["gdalwarp.exe", "-ot", "Float32", "-srcnodata", str(replace_ndata),
                                         "-dstnodata", "nan",im_out2, im_out3])

            QMessageBox.about(self.dlg, 'CLIP Convertion ', "complete")


    def convertionRad(self,dat, mr, ar):
        radi = mr * dat + ar
        return radi

    # Application of formula of convertion

    def convertionRefle(self,dat, mp, ap, solar):
        # img is an array
        # Band=np.array(img,dtype=float)
        refle = mp * dat + ap
        # Sun elevation
        # x=59.18937092
        Refle = refle / (math.sin(math.radians(solar)))
        return Refle  # .reshape(img.shape)

        # DOS1 -------------------------------------------------------------------

    # (π∗d2)∗RADIANCE_MAXIMUM/REFLECTANCE_MAXIMUM
    def ESUN(self,dis, pmax, rmax):  # ban is the index of band
        # pmax is REFLECTANCE_MAXIMUM_BAND
        # rmax is RADIANCE_MAXIMUM_BAND
        return (math.pi * math.pow(dis,2)) * (rmax / pmax)


    # ------------------------------------------------RUN2-------------------------------------------------------------
    def run2(self):
        self.dlg2.show()
        QObject.connect(self.dlg2.buttonBox, SIGNAL("accepted()"), self.processing)

    def processing(self):
        # Run the dialog event loop

        gdal.AllRegister()
        INPUT = self.dlg2.lineEdit.text()
        inshape8 = self.dlg2.lineEdit_8.text()#Used in Colour composite, (VI) and Pansharping
        out_cl = self.dlg2.lineEdit_3.text()

        if not(len(INPUT)==0):

            RASTERS = self.inputFiles
            selectedAindex = self.dlg2.comboBox_3.currentIndex()
            selectedBindex = self.dlg2.comboBox_4.currentIndex()
            selectedCindex = self.dlg2.comboBox_5.currentIndex()

            #A= Image.open(str(A)).convert('L')
            lista = []

            gdalRaster = gdal.Open(os.path.join(str(INPUT), str(RASTERS[selectedAindex-1])))
            #Try put A instead of gdal raster
            #QMessageBox.about(self.dlg, 'A', str(A))

            x = gdalRaster.RasterXSize
            y = gdalRaster.RasterYSize
            geo = gdalRaster.GetGeoTransform()
            minx = geo[0]
            maxy = geo[3]
            maxx = minx + geo[1] * x
            miny = maxy + geo[5] * y
            extent_raster = str(minx) + "," + str(maxx) + "," + str(miny) + "," + str(maxy)
            pixelSize = geo[1]

            A=os.path.join(str(INPUT), str(RASTERS[selectedAindex-1]))
            B=os.path.join(str(INPUT), str(RASTERS[selectedBindex-1]))
            C=os.path.join(str(INPUT), str(RASTERS[selectedCindex-1]))
            #-1 happens because of the sapace " " index

            lista = lista + [str(A)] + [str(B)]+ [str(C)]
            dirs = ';'.join(lista)
            #QMessageBox.about(self.dlg2, 'teste', str(dirs))

            OUT=self.dlg2.lineEdit_5.text()


            Processing.initialize()
            selected_index=self.dlg2.comboBox.currentIndex()
            #srcdata= self.dlg2.doubleSpinBox.value()

            if selected_index==0:
                pass
            # -------------------------------Color composite---------------------------------------
            if selected_index==1:

                Processing.runAlgorithm("gdalogr:merge", None, str(dirs), False, True, -9999, 5, str(OUT) + ".tif")

            # ----------------------NDVI-----------------------------------------------------------
            if selected_index==2:
                #1 - Red B4 e 2 - NIR B5
                #Processing.runAlgorithm("saga:rastercalculator",None,str(A),str(B),"(b-a)/(b+a)",False,7,str(OUT)+".tif")
                Processing.runAlgorithm("gdalogr:rastercalculator",None,str(A),"1",str(B),"1",None,"1",None,"1",None,"1",None,"1","(B-A)/(B+A)","",5,"",str(OUT)+".tif")
            # ---------------------------------NDWI------------------------------------------------
            if selected_index==3:
                Processing.runAlgorithm("gdalogr:rastercalculator", None, str(A), "1", str(B), "1", None, "1", None, "1",None, "1",None, "1", "(B-A)/(B+A)", "", 5, "", str(OUT) + ".tif")

            # -----------------------------EVI-----------------------------------------------------
            if selected_index==4:
                #Use GDAL raster calculator
                Processing.runAlgorithm("gdalogr:rastercalculator", None, str(A), "1", str(B), "1", str(C), "1", None,"1", None, "1",None, "1", "(2.5*(B-A))/(B+6*A-7.5*C+1)", "", 5, "", str(OUT) + ".tif")

            if self.dlg2.checkBox.isChecked():
                subprocess.call(["gdalwarp.exe", "-srcnodata", str(self.dlg2.spinBox.value()), "-dstnodata", "nan",
                                 "-crop_to_cutline", "-cutline", inshape8, str(OUT) + ".tif", str(out_cl) + ".tif"])


        #Pan sharpenning--------------------------------------------------------------------------------------------
        Multi = self.dlg2.lineEdit_4.text()#RGB
        Pan = self.dlg2.lineEdit_6.text()#B8
        super= self.dlg2.lineEdit_2.text()#superimpose
        Out_pan = self.dlg2.lineEdit_7.text()#pan_sharpeed
        #out_cl specified before is the clipping result

        if not(len(Multi)==0 and len(Pan)==0):
            Processing.initialize()
            Processing.runAlgorithm("otb:superimposesensor",None,str(Pan),str(Multi),0, 4, 0, 0, 2, 128,super)

            if len(super)==0:
                #Apply the RCS pansharpening algorithm Multi==Super
                Processing.runAlgorithm("otb:pansharpeningrcs", None, str(Pan), str(Multi), 0, 128, str(Out_pan) + ".tif")
            else:#Use the output from superimpose algorithm
                Processing.runAlgorithm("otb:pansharpeningrcs", None, str(Pan), str(super), 0, 128, str(Out_pan) + ".tif")

        #Clipping process
        if self.dlg2.checkBox_2.isChecked():
            subprocess.call(["gdalwarp.exe", "-srcnodata", str(self.dlg.spinBox.value()), "-dstnodata", "nan",
                             "-crop_to_cutline", "-cutline", inshape8, str(Out_pan)+".tif",str(out_cl) + ".tif"])


    # ------------------------------------------------RUN3--------------------------------------------------------------
    def run3(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg3.show()

        QObject.connect(self.dlg3.buttonBox, SIGNAL("accepted()"), self.classification)

    def classification(self):

        inshapefile3 = self.dlg3.lineEdit.text()

        #INPUT Read RGB file
        RGB = self.dlg3.lineEdit_3.text()


        Out_Un = self.dlg3.lineEdit_4.text()

        Un_Cl=self.dlg3.lineEdit_2.text()

        ts_value = self.dlg3.spinBox.value()
        nc_value = self.dlg3.spinBox_2.value()
        maxit_value = self.dlg3.spinBox_3.value()
        ct_value = self.dlg3.doubleSpinBox.value()
        nan_value = self.dlg3.spinBox_4.value()

        Processing.runAlgorithm("otb:unsupervisedkmeansimageclassification",None,str(RGB), 128, None, ts_value, nc_value,
                                maxit_value,ct_value,str(Out_Un)+".tif", None)

        subprocess.call(["gdalwarp.exe", "-srcnodata", str(nan_value), "-dstnodata", "nan", "-crop_to_cutline", "-cutline",
                         inshapefile3,str(Out_Un)+".tif",str(Un_Cl)+".tif"])

        QMessageBox.about(self.dlg3, 'Classification', "complete")

        
