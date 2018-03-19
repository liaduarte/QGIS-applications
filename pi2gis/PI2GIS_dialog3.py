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
 *                                                                         *
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
    os.path.dirname(__file__), 'PI2GIS_dialog_base3.ui'))

class PI2GISDialog3(QtGui.QDialog, FORM_CLASS):


    #Tentativa de corrigi o erro com  base no Hospital Data
    #No sei o que faz
    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(PI2GISDialog3, self).__init__(parent)
        self.setupUi(self)
 
    #def closeEvent(self, event):
    #    self.closingPlugin.emit()
    #    event.accept()


            
