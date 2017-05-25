from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *

class Ui_Drastic_window(object):
    def setupUi(self, Window):
        
        # create main window
        Window.setWindowModality(QtCore.Qt.ApplicationModal)
        Window.resize(1000,600)        
       
        
        # create menubar with File, DRASTIC and Help sections
        Window.menuBar = QtGui.QMenuBar()
        Window.menuFile = QtGui.QMenu("File", self)
        Window.menuDrastic = QtGui.QMenu("DRASTIC", self)
        Window.menuGod = QtGui.QMenu("GOD", self)
        Window.menuHelp = QtGui.QMenu("Help", self)      
        Window.setMenuBar(Window.menuBar)
                
    
        self.retranslateUi(Window)
        #QtCore.QMetaObject.connectSlotsByName(Window)
        
        Window.show()
    
    def retranslateUi(self, Window):
        Window.setWindowTitle(QtGui.QApplication.translate("Window", "DRASTIC", None, QtGui.QApplication.UnicodeUTF8))
        
    