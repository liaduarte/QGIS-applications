# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PI2GISDialog
                                 A QGIS plugin
 Processing Image to Geographical Information Systems – a learning tool for QGIS
                             -------------------
        begin                : 2017-03-23
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Rui Correia
        email                : rui_correia11@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                             *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import sys

import os

from PyQt4 import QtGui,QtCore , uic
from PyQt4.QtCore import pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'PI2GIS_dialog_base.ui'))
#O FORM_CLASS é no fundo o "Ui_MainWindow", function uic.loadUiType normalmente,
#envia duas variáveis de saída usado __ porque não interessa a segunda. 

class PI2GISDialog(QtGui.QTabWidget, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(PI2GISDialog, self).__init__(parent)
        #Parece ser uma alternativa to the function super
        #QtGui.QDialog.__init__(self)
        #FORM_CLASS.__init__(self)
        #QtGui.QWidget.__init__(self, parent)
        
        #tabs	= QtGui.QTabWidget()
        # Create tabs
        #tab1	= QtGui.QWidget()	
        #tab2	= QtGui.QWidget()
        #tab3	= QtGui.QWidget()
        #tab4	= QtGui.QWidget()
        # Add tabs
        #tabs.addTab(tab1,"Tab 1")
        #tabs.addTab(tab2,"Tab 2")
        #tabs.addTab(tab3,"Tab 3")
        #tabs.addTab(tab4,"Tab 4")

        #Mensagem Inicial-----------------------------------------
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        #-----------------------------------------------------------
        self.setupUi(self)

    #def closeEvent(self, event):
    #    self.closingPlugin.emit()
    #    event.accept()
