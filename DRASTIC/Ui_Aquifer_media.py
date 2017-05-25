from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *

class Ui_Aquifer_media(object):
    
    def setupUi(self, Aquifer_window):
        
        # create Aquifer window
        Aquifer_window.setWindowModality(QtCore.Qt.ApplicationModal)
        Aquifer_window.resize(450,500)
        
        # input file
        # create gridLayout
        self.gridLayout1 = QtGui.QGridLayout(Aquifer_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # create label in gridLayout 
        self.label = QtGui.QLabel(Aquifer_window)
        self.label.setObjectName("label")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label,0,0,1,1)
        # create select button to input file
        self.selectButton = QtGui.QPushButton(Aquifer_window)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout1.addWidget(self.selectButton,0,2,1,1)
        self.inputLayerCombo = QtGui.QComboBox(Aquifer_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout1.addWidget(self.inputLayerCombo, 0,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)       
        
        # define a groupbox to specify the cell size and attribute
        self.groupBox1 = QtGui.QGroupBox(Aquifer_window)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout3 = QtGui.QGridLayout(self.groupBox1)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox1, 1,0,1,-1)
        # define attribute "Elevation"
        self.labelAttrib = QtGui.QLabel(Aquifer_window)
        self.labelAttrib.setObjectName("labelAttrib")
        self.gridLayout3.addWidget(self.labelAttrib,0,0,-1,1)
        self.lineAttrib = QtGui.QComboBox(Aquifer_window)
        self.lineAttrib.setObjectName("lineAttrib")
        self.gridLayout3.addWidget(self.lineAttrib,0,1,-1,1)
        # define pixel size
        self.labelPix = QtGui.QLabel(Aquifer_window)
        self.labelPix.setObjectName("labelPix")
        self.gridLayout3.addWidget(self.labelPix, 0,3,-1,1)
        self.linePix = QtGui.QSpinBox()
        self.linePix.setValue(29)
        self.linePix.stepBy(1)
        self.linePix.setObjectName("linePix")
        self.gridLayout3.addWidget(self.linePix,0,4,-1,1)            
        
        # define the indexs
        # create a group box
        self.groupBox = QtGui.QGroupBox(Aquifer_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 2,0,1,-1)
        # table for classes and indexes
        self.tableWidget = QtGui.QTableWidget(10,2,Aquifer_window)
        self.gridLayout2.addWidget(self.tableWidget,0,0,1,1)
        self.newItem = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0,self.newItem)
        self.newItem = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1,self.newItem)      
        # set the description
        self.line = QtGui.QLineEdit("Xisto argiloso, argilito")
        self.tableWidget.setItem(0,0,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("Rocha metamorfica/ ignea")
        self.tableWidget.setItem(1,0,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("Rocha metamorfica/ ignea alterada")
        self.tableWidget.setItem(2,0,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("Till glaciar")
        self.tableWidget.setItem(3,0,QtGui.QTableWidgetItem(self.line.text()))        
        self.line = QtGui.QLineEdit("Arenito, calcario e argilito estratificados")
        self.tableWidget.setItem(4,0,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("Arenito macico")
        self.tableWidget.setItem(5,0,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("Calcario macico")
        self.tableWidget.setItem(6,0,QtGui.QTableWidgetItem(self.line.text())) 
        self.line = QtGui.QLineEdit("Areia e balastro")
        self.tableWidget.setItem(7,0,QtGui.QTableWidgetItem(self.line.text())) 
        self.line = QtGui.QLineEdit("Basalto")
        self.tableWidget.setItem(8,0,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("Calcario carsificado")
        self.tableWidget.setItem(9,0,QtGui.QTableWidgetItem(self.line.text()))        
        # set the indexes values
        self.line = QtGui.QLineEdit("2")
        self.tableWidget.setItem(0,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("3")
        self.tableWidget.setItem(1,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("4")
        self.tableWidget.setItem(2,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("5")        
        self.tableWidget.setItem(3,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("6")
        self.tableWidget.setItem(4,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("6")
        self.tableWidget.setItem(5,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("6")
        self.tableWidget.setItem(6,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("8")
        self.tableWidget.setItem(7,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("9")
        self.tableWidget.setItem(8,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("10")
        self.tableWidget.setItem(9,1,QtGui.QTableWidgetItem(self.line.text()))        
        # create a box layout to insert the buttons Add and Remove
        self.boxLayout = QtGui.QVBoxLayout()
        self.boxLayout.setObjectName("boxLayout")
        # button Add
        self.buttonAdd = QtGui.QPushButton(Aquifer_window)
        self.buttonAdd.setObjectName("buttonAdd")
        self.boxLayout.addWidget(self.buttonAdd)
        # button Remove
        self.buttonRemove = QtGui.QPushButton(Aquifer_window)
        self.buttonRemove.setObjectName("buttonRemove") 
        self.boxLayout.addWidget(self.buttonRemove)
        # attribute table button
        self.buttonAttribute = QtGui.QPushButton(Aquifer_window)
        self.buttonAttribute.setObjectName("buttonAttribute")
        self.boxLayout.addWidget(self.buttonAttribute)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)
        ## button weight
        #self.labelWeight = QtGui.QLabel(Aquifer_window)
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
        self.label3 = QtGui.QLabel(Aquifer_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3,3,0,1,1)
        # create select button to input file
        self.selectButton3 = QtGui.QPushButton(Aquifer_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3,3,2,1,1)
        self.inputLayerCombo3 = QtGui.QLineEdit(Aquifer_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 3,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)     
        
        # button Ok, Close and Help
        self.buttonBox = QtGui.QDialogButtonBox(Aquifer_window)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Help|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 4, 1, 1, 1)           

        self.retranslateUi(Aquifer_window)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Aquifer_window.close)
                
    def retranslateUi(self, Aquifer_window):
        Aquifer_window.setWindowTitle(QtGui.QApplication.translate('Aquifer Media (A)', 'Aquifer Media (A)', None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate('Aquifer Media (A)', 'Input file:', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton.setText(QtGui.QApplication.translate('Aquifer Media (A)', 'Browse', None, QtGui.QApplication.UnicodeUTF8))        
        self.groupBox.setTitle(QtGui.QApplication.translate("Aquifer Media (A)", "Ratings", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Aquifer Media (A)","Aquifer Media", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Aquifer Media (A)","Ratings", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonAdd.setText(QtGui.QApplication.translate("Aquifer Media (A)", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRemove.setText(QtGui.QApplication.translate("Aquifer Media (A)", "Remove", None, QtGui.QApplication.UnicodeUTF8)) 
        self.buttonAttribute.setText(QtGui.QApplication.translate("Aquifer Media (A)", "Attribute Table", None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setText(QtGui.QApplication.translate('Aquifer Media (A)', 'Output file:', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton3.setText(QtGui.QApplication.translate('Aquifer Media (A)', 'Browse', None, QtGui.QApplication.UnicodeUTF8))  
        self.labelAttrib.setText(QtGui.QApplication.translate('Aquifer Media (A)', 'Attribute:', None, QtGui.QApplication.UnicodeUTF8)) 
        self.labelPix.setText(QtGui.QApplication.translate('Aquifer Media (A)', 'Cell size:', None, QtGui.QApplication.UnicodeUTF8))  
        #self.labelWeight.setText(QtGui.QApplication.translate('Aquifer Media (A)', 'Weight:', None, QtGui.QApplication.UnicodeUTF8))