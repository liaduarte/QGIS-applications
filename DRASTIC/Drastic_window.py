from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from UI_Drastic_window import Ui_Drastic_window
from Depth_groundwater import Depth_groundwater
from Recharge import Recharge
from Aquifer_media import Aquifer_media
from Soil_media import Soil_media
from Topography import Topography
from Impact_zone import Impact_zone
from Hidraulic_conductivity import Hidraulic_conductivity
from Drastic import Drastic
from Groundwater import Groundwater
from Overall import Overall
from Depth import Depth
from God import God
try:
    from PyQt4.QtCore import QString
except ImportError:
    QString = str

class Drastic_window(QMainWindow, Ui_Drastic_window):
    
    def __init__(self, iface):
        QMainWindow.__init__(self)  
        self.iface = iface
        self.setupUi(self)
        self.setWindowTitle("DRASTIC")
        #self.process = QProcess(self) 
        
        self.canvas = QgsMapCanvas()
        self.canvas.setCanvasColor(QColor(255,255,255))
        self.setCentralWidget(self.canvas)
       
       
        actionMenuFile = self.menuBar.addMenu(self.menuFile)
        actionMenuDrastic = self.menuBar.addMenu(self.menuDrastic)
        actionMenuGod = self.menuBar.addMenu(self.menuGod)
        actionMenuHelp = self.menuBar.addMenu(self.menuHelp)
       
        
        # connect help to help window
        QObject.connect(actionMenuHelp, SIGNAL("triggered()"), self.helpRequested)
        
        
        # actions for DRASTIC menu
        self.actionDepth_groundwater = self.menuDrastic.addAction(QIcon(":/plugins/DRASTIC/calc.png"), self.tr("Depth to Groundwater (D)"), self.doDepth_groundwater, QKeySequence("F1"))
        self.actionRecharge = self.menuDrastic.addAction(QIcon(":/plugins/DRASTIC/raster.png"), self.tr("Net Recharge (R)"), self.doRecharge, QKeySequence("F2"))
        self.actionAquifer = self.menuDrastic.addAction(QIcon(":/plugins/DRASTIC/rasterize.png"), self.tr("Aquifer Media (A)"), self.doAquifer_media, QKeySequence("F3"))
        self.actionSoil = self.menuDrastic.addAction(QIcon(":/plugins/DRASTIC/risc.png"), self.tr("Soil Media (S)"), self.doSoil_media, QKeySequence("F4"))
        self.actionTopography = self.menuDrastic.addAction(QIcon(":/plugins/DRASTIC/slope.png"), self.tr("Topography (T)"), self.doTopography, QKeySequence("F5"))
        self.actionImpact = self.menuDrastic.addAction(QIcon(":/plugins/DRASTIC/mapa.png"), self.tr("Impact of the Vadose Zone (I)"), self.doImpact_zone, QKeySequence("F6"))
        self.actionHidraConduc = self.menuDrastic.addAction(QIcon(":/plugins/DRASTIC/calc.png"), self.tr("Hydraulic Conductivity (C)"), self.doHidraulic_conductivity, QKeySequence("F7"))
        self.actionDrastic = self.menuDrastic.addAction(QIcon(":/plugins/DRASTIC/calc.png"), self.tr("DRASTIC"), self.doDrastic, QKeySequence("F8"))
        
        # actions for GOD menu
        self.actionGroundwater = self.menuGod.addAction(QIcon(":/plugins/DRASTIC/calc.png"), self.tr("Groundwater Occurrence (G)"), self.doGroundwater, QKeySequence("F1"))
        self.actionOverall = self.menuGod.addAction(QIcon(":/plugins/DRASTIC/raster.png"), self.tr("Overall lithology of aquifer or aquitard (O)"), self.doOverall, QKeySequence("F2"))
        self.actionDepth = self.menuGod.addAction(QIcon(":/plugins/DRASTIC/rasterize.png"), self.tr("Depth to Groundwater (D)"), self.doDepth, QKeySequence("F3"))        
        self.actionGOD = self.menuGod.addAction(QIcon(":/plugins/DRASTIC/calc.png"), self.tr("GOD"), self.doGod, QKeySequence("F3"))        
        
        # actions for File menu
        self.actionAddRasterLayer = self.menuFile.addAction(QIcon(":/plugins/DRASTIC/calc.png"), self.tr("Add Raster Layer"), self.AddRaster, QKeySequence("F1"))
        self.actionAddVectorLayer = self.menuFile.addAction(QIcon(":/plugins/DRASTIC/raster.png"), self.tr("Add Vector Layer"), self.AddVector, QKeySequence("F2"))
              
    def unload(self):
        self.menu.removeAction(self.Drastic_menu.menuAction())  
        
    def doGroundwater(self):
        self.dlgGroundwater = Groundwater(self)
        if Groundwater ==0:
            return
        self.dlgGroundwater.show()
        self.dlgGroundwater.exec_()   
        
    def doGod(self):
        self.dlgGod = God(self)
        if God ==0:
            return
        self.dlgGod.show()
        self.dlgGod.exec_()      
        
    def doOverall(self):
        self.dlgOverall = Overall(self)
        if Overall ==0:
            return
        self.dlgOverall.show()
        self.dlgOverall.exec_()      
        
    def doDepth(self):
        self.dlgDepthG = Depth(self)
        if Depth ==0:
            return
        self.dlgDepthG.show()
        self.dlgDepthG.exec_()    
        
    def doDepth_groundwater(self):
        self.dlgDepth = Depth_groundwater(self)
        if Depth_groundwater ==0:
            return
        self.dlgDepth.show()
        self.dlgDepth.exec_()
        
        
    def doRecharge(self):
        self.dlgRecharge = Recharge(self)
        if Recharge ==0:
            return
        self.dlgRecharge.show()
        self.dlgRecharge.exec_()    
    
    def doAquifer_media(self):
        self.dlgAquifer = Aquifer_media(self)
        if Aquifer_media ==0:
            return
        self.dlgAquifer.show()
        self.dlgAquifer.exec_()   
        
    def doSoil_media(self):
        self.dlgSoil = Soil_media(self)
        if Soil_media ==0:
            return
        self.dlgSoil.show()
        self.dlgSoil.exec_()
        
    def doTopography(self):
        self.dlgTopography = Topography(self)
        if Topography ==0:
            return
        self.dlgTopography.show()
        self.dlgTopography.exec_()    
        
    def doImpact_zone(self):
        self.dlgImpact = Impact_zone(self)
        if Impact_zone ==0:
            return
        self.dlgImpact.show()
        self.dlgImpact.exec_()
    
    def doHidraulic_conductivity(self):
        self.dlgHidraulic = Hidraulic_conductivity(self)
        if Hidraulic_conductivity==0:
            return
        self.dlgHidraulic.show()
        self.dlgHidraulic.exec_()    
        
    def doDrastic(self):
        self.dlgDrastic = Drastic(self)
        if Drastic==0:
            return
        self.dlgDrastic.show()
        self.dlgDrastic.exec_()
        
    def AddVector(self):
        file = QFileDialog.getOpenFileName(self, "Open shapefile", ".", "Shp (*.shp)")   
        fileInfo = QFileInfo(file)
        
        # add the shapefile
        layer = QgsVectorLayer(file, fileInfo.fileName(), "ogr")
        
        if not layer.isValid():
            return
        
        # add layer to the registry
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        
        # set extent to the extent of our layer
        self.canvas.setExtent(layer.extent())
        
        # set the map canvas layer set
        self.canvas.setLayerSet([QgsMapCanvasLayer(layer)])
        
    def AddRaster(self):
        file = QFileDialog.getOpenFileName(self, "Open raster", ".", "Images(*.tif *.png *.jpg *.jpeg *.img)")
        fileInfo = QFileInfo(file)
        
        # add the raster
        layer = QgsRasterLayer(file, fileInfo.fileName(), "gdal")
        
        if not layer.isValid():
            return
        
        # add layer to the registry
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        
        # set extent to the extent of our layer
        self.canvas.setExtent(layer.extent())
        
        # set the map canvas layer set
        self.canvas.setLayerSet([QgsMapCanvasLayer(layer)])
        
    def helpRequested(self):
        QMessageBox.about(self, "Help", """<p>The tool determines the spatial distribution of the DRASTIC index and incorporates some procedures under a plugin. <p>
        <p>The DRASTIC method comprises several factors and the corresponding maps: <p>
        <p><b>Depth to groundwater (D)<b><p>
        <p><b>Net Recharge (R)<b><p>
        <p><b>Aquifer media (A)<b><p>
        <p><b>Soil media (S)<b><p>
        <p><b>Topography (T)<b><p>
        <p><b>Impact of the Vadose Zone (I) <b><p>
        <p><b>Hydraulic Conductivity (C)<b><p>
        
        <p>The application consists of a window where the spatial objects can be presented. <p>
        <p>This window allows the user to analyze the result and modify the input parameters. <p>
        <p>The DRASTIC window is composed by a map canvas, a menu bar containing a <b>File<b> menu, the <b>DRASTIC<b> menu and the <b>Help<b> menu.<p>
        <p>The first one is composed by two buttons that allow the user to add a vector or a raster file (<b>Add Vector File<b> and <b>Add Raster File<b>). <p>
        <p>The DRASTIC menu is composed by eight buttons, one for each factor.<p> """)
        
        
    def ident(self):
        QMessageBox.about(self, "Help", """abc""")
    
