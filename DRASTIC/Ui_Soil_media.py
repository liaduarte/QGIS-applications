from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *

class Ui_Soil_media(object):
    
    def setupUi(self, Soil_window):
        
        # create Soil window
        Soil_window.setWindowModality(QtCore.Qt.ApplicationModal)
        Soil_window.resize(450,500)
        
        # input file
        # create gridLayout
        self.gridLayout1 = QtGui.QGridLayout(Soil_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # create label in gridLayout 
        self.label = QtGui.QLabel(Soil_window)
        self.label.setObjectName("label")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label,0,0,1,1)
        # create select button to input file
        self.selectButton = QtGui.QPushButton(Soil_window)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout1.addWidget(self.selectButton,0,2,1,1)
        self.inputLayerCombo = QtGui.QComboBox(Soil_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout1.addWidget(self.inputLayerCombo, 0,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)       
        
        # define a groupbox to specify the cell size and attribute
        self.groupBox1 = QtGui.QGroupBox(Soil_window)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout3 = QtGui.QGridLayout(self.groupBox1)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox1, 1,0,1,-1)
        # define attribute "Elevation"
        self.labelAttrib = QtGui.QLabel(Soil_window)
        self.labelAttrib.setObjectName("labelAttrib")
        self.gridLayout3.addWidget(self.labelAttrib,0,0,-1,1)
        self.lineAttrib = QtGui.QComboBox(Soil_window)
        self.lineAttrib.setObjectName("lineAttrib")
        self.gridLayout3.addWidget(self.lineAttrib,0,1,-1,1)
        # define pixel size
        self.labelPix = QtGui.QLabel(Soil_window)
        self.labelPix.setObjectName("labelPix")
        self.gridLayout3.addWidget(self.labelPix, 0,3,-1,1)
        self.linePix = QtGui.QSpinBox()
        self.linePix.setValue(29)
        self.linePix.stepBy(1)
        self.linePix.setObjectName("linePix")
        self.gridLayout3.addWidget(self.linePix,0,4,-1,1)            
        
        
        # define the indexs
        # create a group box
        self.groupBox = QtGui.QGroupBox(Soil_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 2,0,1,-1)
        # table for classes and indexes
        self.tableWidget = QtGui.QTableWidget(11,2,Soil_window)
        self.gridLayout2.addWidget(self.tableWidget,0,0,1,1)
        self.newItem = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0,self.newItem)
        self.newItem = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1,self.newItem)
        # set the description
        self.line = QtGui.QLineEdit("Fino ou ausente")
        self.tableWidget.setItem(0,0,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("Balastro")
        self.tableWidget.setItem(1,0,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("Areia")
        self.tableWidget.setItem(2,0,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("Turfa")
        self.tableWidget.setItem(3,0,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("Argila agregada e/ou expansivel")
        self.tableWidget.setItem(4,0,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("Franco arenoso")
        self.tableWidget.setItem(5,0,QtGui.QTableWidgetItem(self.line.text())) 
        self.line = QtGui.QLineEdit("Franco")
        self.tableWidget.setItem(6,0,QtGui.QTableWidgetItem(self.line.text())) 
        self.line = QtGui.QLineEdit("Franco siltoso")
        self.tableWidget.setItem(7,0,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("Franco argiloso")
        self.tableWidget.setItem(8,0,QtGui.QTableWidgetItem(self.line.text())) 
        self.line = QtGui.QLineEdit("Muck")
        self.tableWidget.setItem(9,0,QtGui.QTableWidgetItem(self.line.text()))  
        self.line = QtGui.QLineEdit("Argila nao agregada e nao expansivel")
        self.tableWidget.setItem(10,0,QtGui.QTableWidgetItem(self.line.text()))        
        # set the indexes values
        self.line = QtGui.QLineEdit("10")
        self.tableWidget.setItem(0,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("10")
        self.tableWidget.setItem(1,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("9")
        self.tableWidget.setItem(2,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("8")
        self.tableWidget.setItem(3,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("7")
        self.tableWidget.setItem(4,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("6")
        self.tableWidget.setItem(5,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("5")
        self.tableWidget.setItem(6,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("4")
        self.tableWidget.setItem(7,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("3")
        self.tableWidget.setItem(8,1,QtGui.QTableWidgetItem(self.line.text())) 
        self.line = QtGui.QLineEdit("2")
        self.tableWidget.setItem(9,1,QtGui.QTableWidgetItem(self.line.text())) 
        self.line = QtGui.QLineEdit("1")
        self.tableWidget.setItem(10,1,QtGui.QTableWidgetItem(self.line.text()))        
        # create a box layout to insert the buttons Add and Remove
        self.boxLayout = QtGui.QVBoxLayout()
        self.boxLayout.setObjectName("boxLayout")
        # button Add
        self.buttonAdd = QtGui.QPushButton(Soil_window)
        self.buttonAdd.setObjectName("buttonAdd")
        self.boxLayout.addWidget(self.buttonAdd)
        # button Remove
        self.buttonRemove = QtGui.QPushButton(Soil_window)
        self.buttonRemove.setObjectName("buttonRemove") 
        self.boxLayout.addWidget(self.buttonRemove)
        # attribute table button
        self.buttonAttribute = QtGui.QPushButton(Soil_window)
        self.buttonAttribute.setObjectName("buttonAttribute")
        self.boxLayout.addWidget(self.buttonAttribute)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)        
        ## button weight
        #self.labelWeight = QtGui.QLabel(Soil_window)
        #self.labelWeight.setObjectName("labelWeight")
        #self.boxLayout.addWidget(self.labelWeight)
        #self.lineWeight = QtGui.QSpinBox()
        #self.lineWeight.setValue(1)
        #self.lineWeight.stepBy(1)
        #self.lineWeight.setObjectName("lineWeight")
        #self.boxLayout.addWidget(self.lineWeight)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)        
        
        # output file
        # create label in gridLayout
        self.label3 = QtGui.QLabel(Soil_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3,3,0,1,1)
        # create select button to input file
        self.selectButton3 = QtGui.QPushButton(Soil_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3,3,2,1,1)
        self.inputLayerCombo3 = QtGui.QLineEdit(Soil_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 3,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)     
        
        # button Ok, Close and Help
        self.buttonBox = QtGui.QDialogButtonBox(Soil_window)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Help|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 4, 1, 1, 1)                   
        
        self.retranslateUi(Soil_window)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Soil_window.close)
                
    def retranslateUi(self, Soil_window):
        Soil_window.setWindowTitle(QtGui.QApplication.translate('Soil Media (S)', 'Soil Media (S)', None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate('Soil Media (S)', 'Input file:', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton.setText(QtGui.QApplication.translate('Soil Media (S)', 'Browse', None, QtGui.QApplication.UnicodeUTF8))        
        self.groupBox.setTitle(QtGui.QApplication.translate("Soil Media (S)", "Ratings", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Soil Media (S)","Soil Media", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Soil Media (S)","Ratings", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonAdd.setText(QtGui.QApplication.translate("Soil Media (S)", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRemove.setText(QtGui.QApplication.translate("Soil Media (S)", "Remove", None, QtGui.QApplication.UnicodeUTF8))        
        self.buttonAttribute.setText(QtGui.QApplication.translate("Soil Media (S)", "Attribute Table", None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setText(QtGui.QApplication.translate('Soil Media (S)', 'Output file:', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton3.setText(QtGui.QApplication.translate('Soil Media (S)', 'Browse', None, QtGui.QApplication.UnicodeUTF8))    
        self.labelAttrib.setText(QtGui.QApplication.translate('Soil Media (S)', 'Attribute:', None, QtGui.QApplication.UnicodeUTF8)) 
        self.labelPix.setText(QtGui.QApplication.translate('Soil Media (S)', 'Cell size:', None, QtGui.QApplication.UnicodeUTF8))        
        #self.labelWeight.setText(QtGui.QApplication.translate('Soil Media (S)', 'Weight:', None, QtGui.QApplication.UnicodeUTF8))