from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *

class Ui_Hidraulic_conductivity(object):
    
    def setupUi(self, Hidraulic_conductivity_window):
        
        # create Hidraulic conductivity window
        Hidraulic_conductivity_window.setWindowModality(QtCore.Qt.ApplicationModal)
        Hidraulic_conductivity_window.resize(550,450)
        
        # input file
        # create gridLayout
        self.gridLayout1 = QtGui.QGridLayout(Hidraulic_conductivity_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # create label in gridLayout 
        self.label = QtGui.QLabel(Hidraulic_conductivity_window)
        self.label.setObjectName("label")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label,0,0,1,1)
        # create select button to input file
        self.selectButton = QtGui.QPushButton(Hidraulic_conductivity_window)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout1.addWidget(self.selectButton,0,2,1,1)
        self.inputLayerCombo = QtGui.QComboBox(Hidraulic_conductivity_window)
        self.inputLayerCombo.setEditable(True)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout1.addWidget(self.inputLayerCombo, 0,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)       
        
        # define a groupbox to specify the cell size and attribute
        self.groupBox1 = QtGui.QGroupBox(Hidraulic_conductivity_window)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout3 = QtGui.QGridLayout(self.groupBox1)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox1, 1,0,1,-1)
        # define attribute "Elevation"
        self.labelAttrib = QtGui.QLabel(Hidraulic_conductivity_window)
        self.labelAttrib.setObjectName("labelAttrib")
        self.gridLayout3.addWidget(self.labelAttrib,0,0,-1,1)
        self.lineAttrib = QtGui.QComboBox(Hidraulic_conductivity_window)
        self.lineAttrib.setObjectName("lineAttrib")
        self.gridLayout3.addWidget(self.lineAttrib,0,1,-1,1)
        # define pixel size
        self.labelPix = QtGui.QLabel(Hidraulic_conductivity_window)
        self.labelPix.setObjectName("labelPix")
        self.gridLayout3.addWidget(self.labelPix, 0,3,-1,1)
        self.linePix = QtGui.QSpinBox()
        self.linePix.setValue(29)
        self.linePix.stepBy(1)
        self.linePix.setObjectName("linePix")
        self.gridLayout3.addWidget(self.linePix,0,4,-1,1)          
        
        # define the indexs
        # create a group box
        self.groupBox = QtGui.QGroupBox(Hidraulic_conductivity_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 2,0,1,-1)
        # table for classes and indexes
        self.tableWidget = QtGui.QTableWidget(6,3,Hidraulic_conductivity_window)
        self.gridLayout2.addWidget(self.tableWidget,0,0,1,1)
        self.newItem = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0,self.newItem)
        self.newItem = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1,self.newItem)
        self.newItem = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2,self.newItem)        
        # set the values (intervals)
        self.line = QtGui.QLineEdit("0")
        self.tableWidget.setItem(0,0,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("0.114")
        self.tableWidget.setItem(0,1,QtGui.QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(1,0,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("0.339")
        self.tableWidget.setItem(2,0,QtGui.QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(1,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("0.792")
        self.tableWidget.setItem(3,0,QtGui.QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(2,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("1.131")
        self.tableWidget.setItem(4,0,QtGui.QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(3,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("2.264")
        self.tableWidget.setItem(5,0,QtGui.QTableWidgetItem(self.line.text())) 
        self.tableWidget.setItem(4,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("n/d")
        self.tableWidget.setItem(5,1,QtGui.QTableWidgetItem(self.line.text()))
        # set the indexes values
        self.line = QtGui.QLineEdit("1")
        self.tableWidget.setItem(0,2,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("2")
        self.tableWidget.setItem(1,2,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("4")
        self.tableWidget.setItem(2,2,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("6")
        self.tableWidget.setItem(3,2,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("8")
        self.tableWidget.setItem(4,2,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("10")
        self.tableWidget.setItem(5,2,QtGui.QTableWidgetItem(self.line.text()))        
        # create a box layout to insert the buttons Add and Remove
        self.boxLayout = QtGui.QVBoxLayout()
        self.boxLayout.setObjectName("boxLayout")
        # button Add
        self.buttonAdd = QtGui.QPushButton(Hidraulic_conductivity_window)
        self.buttonAdd.setObjectName("buttonAdd")
        self.boxLayout.addWidget(self.buttonAdd)
        # button Remove
        self.buttonRemove = QtGui.QPushButton(Hidraulic_conductivity_window)
        self.buttonRemove.setObjectName("buttonRemove") 
        self.boxLayout.addWidget(self.buttonRemove)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)
        ## button weight
        #self.labelWeight = QtGui.QLabel(Hidraulic_conductivity_window)
        #self.labelWeight.setObjectName("labelWeight")
        #self.boxLayout.addWidget(self.labelWeight)
        #self.lineWeight = QtGui.QSpinBox()
        #self.lineWeight.setValue(2)
        #self.lineWeight.stepBy(1)
        #self.lineWeight.setObjectName("lineWeight")
        #self.boxLayout.addWidget(self.lineWeight)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)        
        
        # output file
        # create label in gridLayout
        self.label3 = QtGui.QLabel(Hidraulic_conductivity_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3,3,0,1,1)
        # create select button to input file
        self.selectButton3 = QtGui.QPushButton(Hidraulic_conductivity_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3,3,2,1,1)
        self.inputLayerCombo3 = QtGui.QLineEdit(Hidraulic_conductivity_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 3,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)    
        
        # button Ok, Close and Help
        self.buttonBox = QtGui.QDialogButtonBox(Hidraulic_conductivity_window)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Help|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 4, 1, 1, 1)            
        
        self.retranslateUi(Hidraulic_conductivity_window)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Hidraulic_conductivity_window.close)
                
    def retranslateUi(self, Hidraulic_conductivity_window):
        Hidraulic_conductivity_window.setWindowTitle(QtGui.QApplication.translate('Hidraulic Conductivity (C)', 'Hidraulic Conductivity (C)', None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate('Hidraulic Conductivity (C)', 'Input file:', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton.setText(QtGui.QApplication.translate('Hidraulic Conductivity (C)', 'Browse', None, QtGui.QApplication.UnicodeUTF8))        
        self.groupBox.setTitle(QtGui.QApplication.translate("Hidraulic Conductivity (C)", "Ratings", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Hidraulic Conductivity (C)","Hidraulic Conductivity (cm/s)", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Hidraulic Conductivity (C)","Hidraulic Conductivity (cm/s)", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Hidraulic Conductivity (C)","Ratings", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonAdd.setText(QtGui.QApplication.translate("Hidraulic Conductivity (C)", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRemove.setText(QtGui.QApplication.translate("Hidraulic Conductivity (C)", "Remove", None, QtGui.QApplication.UnicodeUTF8))   
        #self.labelWeight.setText(QtGui.QApplication.translate('Hidraulic Conductivity (C)', 'Weight:', None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setText(QtGui.QApplication.translate('Hidraulic Conductivity (C)', 'Output file:', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton3.setText(QtGui.QApplication.translate('Hidraulic Conductivity (C)', 'Browse', None, QtGui.QApplication.UnicodeUTF8))  
        self.labelAttrib.setText(QtGui.QApplication.translate('Hidraulic Conductivity (H)', 'Attribute:', None, QtGui.QApplication.UnicodeUTF8)) 
        self.labelPix.setText(QtGui.QApplication.translate('Hidraulic Conductivity (H)', 'Cell size:', None, QtGui.QApplication.UnicodeUTF8))            