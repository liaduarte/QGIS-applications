# -*- coding: utf-8 -*-

from PyQt4.QtCore import*
from PyQt4.QtGui import*
from qgis.core import*
from qgis.gui import*

# initialize Qt resources from file resources.py
import resources

# import DRASTIC window
from Drastic_window import Drastic_window

class DrasticToolbar:
    
    def __init__(self,  iface):
        # save reference to the QGIS interface
        self.iface = iface   
       
    def initGui(self):
        # create action that will start plugin configuration
        self.Drastic_window = QAction(QIcon(":/plugins/DRASTIC/tin.png"), "DrasticToolbar", self.iface.mainWindow())
        
        # connect new action to plugin function - when action is triggered
        QObject.connect(self.Drastic_window, SIGNAL("triggered()"), self.doDrastic_window)
        
        # create toolbar
        self.toolbar = self.iface.addToolBar("DrasticToolbar")
        self.toolbar.setObjectName("DrasticToolbar")
        self.toolbar.addAction(self.Drastic_window)        
        
        # add toolbar button and menu item
        self.iface.addToolBarIcon(self.Drastic_window)
        self.iface.addPluginToMenu("&DrasticToolbar",  self.Drastic_window)
        
        # connect to signal renderComplete which is emitted when canvas rendering is done
        QObject.connect(self.iface.mapCanvas(), SIGNAL("renderComplete(QPainter *)"), self.renderTest)
        
    def unload(self):
        # remove the plugin menu item and icon
        self.iface.removePluginMenu("&DrasticToolbar", self.Drastic_window)
        self.iface.removeToolBarIcon(self.Drastic_window)
        
        # remove toolbar icon
        del self.toolbar
                        
    def run(self):
        #create and show a configuration dialog or something similar
        print "DrasticToolbar: run called!"
        
    def renderTest(self, painter):
        #use painter for drawing to map canvas
        print "DrasticToolbar: renderTest called!"
        
    def doDrastic_window(self):
        self.dlgwindow = Drastic_window(self)
        if Drastic_window ==0:
            return
        self.dlgwindow.show()
        
   
        
        
