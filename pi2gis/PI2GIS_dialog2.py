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

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'PI2GIS_dialog_base2.ui'))
#O FORM_CLASS é no fundo o "Ui_MainWindow", function uic.loadUiType normalmente,
#envia duas variáveis de saída usado __ porque não interessa a segunda. 

class PI2GISDialog2(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(PI2GISDialog2, self).__init__(parent)
               #-----------------------------------------------------------
        self.setupUi(self)

        #if __name__ == "__main__":
        #    app = QtGui.QApplication(sys.argv)
        #    window = MyApp()
        #    window.show()
        #    sys.exit(app.exec_())
