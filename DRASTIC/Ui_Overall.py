from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *

class Ui_Overall(object):
    
    def setupUi(self, Overall_window):
        
        # create Depth window
        Overall_window.setWindowModality(QtCore.Qt.ApplicationModal)
        Overall_window.resize(400,400)
        
         # input file
        # create gridLayout
        self.gridLayout1 = QtGui.QGridLayout(Overall_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # create label in gridLayout 
        self.label = QtGui.QLabel(Overall_window)
        self.label.setObjectName("label")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label,0,0,1,1)
        # create select button to input file
        self.selectButton = QtGui.QPushButton(Overall_window)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout1.addWidget(self.selectButton,0,2,1,1)
        self.inputLayerCombo = QtGui.QComboBox(Overall_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout1.addWidget(self.inputLayerCombo, 0,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)       
        
        # define a groupbox to specify the cell size and attribute
        self.groupBox1 = QtGui.QGroupBox(Overall_window)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout3 = QtGui.QGridLayout(self.groupBox1)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox1, 1,0,1,-1)
        # define attribute "Elevation"
        self.labelAttrib = QtGui.QLabel(Overall_window)
        self.labelAttrib.setObjectName("labelAttrib")
        self.gridLayout3.addWidget(self.labelAttrib,0,0,-1,1)
        self.lineAttrib = QtGui.QComboBox(Overall_window)
        self.lineAttrib.setObjectName("lineAttrib")
        self.gridLayout3.addWidget(self.lineAttrib,0,1,-1,1)
        # define pixel size
        self.labelPix = QtGui.QLabel(Overall_window)
        self.labelPix.setObjectName("labelPix")
        self.gridLayout3.addWidget(self.labelPix, 0,3,-1,1)
        self.linePix = QtGui.QSpinBox()
        self.linePix.setValue(29)
        self.linePix.stepBy(1)
        self.linePix.setObjectName("linePix")
        self.gridLayout3.addWidget(self.linePix,0,4,-1,1)            
        
        
        # define the indexs
        # create a group box
        self.groupBox = QtGui.QGroupBox(Overall_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 2,0,1,-1)
        # table for classes and indexes
        self.tableWidget = QtGui.QTableWidget(7,2,Overall_window)
        self.gridLayout2.addWidget(self.tableWidget,0,0,1,1)
        self.newItem = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0,self.newItem)
        self.newItem = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1,self.newItem)
        #self.newItem = QtGui.QTableWidgetItem()
        #self.tableWidget.setHorizontalHeaderItem(2,self.newItem)  
        #self.newItem = QtGui.QTableWidgetItem()
        #self.tableWidget.setHorizontalHeaderItem(3,self.newItem)   
         
        # set the description unconsolidated     
        #self.line = QtGui.QLineEdit("Residual soils")
        #self.tableWidget.setItem(0,0,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("Alluvial silts, loess, glacial till")
        #self.tableWidget.setItem(1,0,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("Aeolian sands")
        #self.tableWidget.setItem(2,0,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("Alluvial and fluvial-glacial sands")
        #self.tableWidget.setItem(3,0,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("Alluvial-fan gravels")
        #self.tableWidget.setItem(4,0,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("-")
        #self.tableWidget.setItem(5,0,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("-")
        #self.tableWidget.setItem(6,0,QtGui.QTableWidgetItem(self.line.text()))        
        
        # set the description consolidated (porous rocks)
        #self.line = QtGui.QLineEdit("-")
        #self.tableWidget.setItem(0,1,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("Mudstones, shales")
        #self.tableWidget.setItem(1,1,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("Sillstones")
        #self.tableWidget.setItem(2,1,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("Volcanic tuffs")
        #self.tableWidget.setItem(3,1,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("Sandstones")
        #self.tableWidget.setItem(4,1,QtGui.QTableWidgetItem(self.line.text())) 
        #self.line = QtGui.QLineEdit("Chalky limestones calcarenites")
        #self.tableWidget.setItem(5,1,QtGui.QTableWidgetItem(self.line.text()))   
        #self.line = QtGui.QLineEdit("-")
        #self.tableWidget.setItem(6,1,QtGui.QTableWidgetItem(self.line.text()))           
        
        ## set the description consolidated (dense rocks)
        #self.line = QtGui.QLineEdit("-")
        #self.tableWidget.setItem(0,2,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("-")
        #self.tableWidget.setItem(1,2,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("Igneous")
        #self.tableWidget.setItem(2,2,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("Metamorphic formations and older volcanics")
        #self.tableWidget.setItem(3,2,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("Recent volcanic lavas")
        #self.tableWidget.setItem(4,2,QtGui.QTableWidgetItem(self.line.text()))   
        #self.line = QtGui.QLineEdit("Calcretes")
        #self.tableWidget.setItem(5,2,QtGui.QTableWidgetItem(self.line.text()))  
        #self.line = QtGui.QLineEdit("Karst limestones")
        #self.tableWidget.setItem(6,2,QtGui.QTableWidgetItem(self.line.text()))           
               
        ## set the indexes values
        #self.line = QtGui.QLineEdit("0.4")
        #self.tableWidget.setItem(0,3,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("0.5")
        #self.tableWidget.setItem(1,3,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("0.6")
        #self.tableWidget.setItem(2,3,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("0.7")
        #self.tableWidget.setItem(3,3,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("0.8")
        #self.tableWidget.setItem(4,3,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("0.9")
        #self.tableWidget.setItem(5,3,QtGui.QTableWidgetItem(self.line.text()))
        #self.line = QtGui.QLineEdit("1.0")
        #self.tableWidget.setItem(6,3,QtGui.QTableWidgetItem(self.line.text()))
             
        # create a box layout to insert the buttons Add and Remove
        self.boxLayout = QtGui.QVBoxLayout()
        self.boxLayout.setObjectName("boxLayout")
        # button Add
        self.buttonAdd = QtGui.QPushButton(Overall_window)
        self.buttonAdd.setObjectName("buttonAdd")
        self.boxLayout.addWidget(self.buttonAdd)
        # button Remove
        self.buttonRemove = QtGui.QPushButton(Overall_window)
        self.buttonRemove.setObjectName("buttonRemove") 
        self.boxLayout.addWidget(self.buttonRemove)
        # attribute table button
        self.buttonAttribute = QtGui.QPushButton(Overall_window)
        self.buttonAttribute.setObjectName("buttonAttribute")
        self.boxLayout.addWidget(self.buttonAttribute)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)        
        ## button weight
        #self.labelWeight = QtGui.QLabel(Overall_window)
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
        self.label3 = QtGui.QLabel(Overall_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3,3,0,1,1)
        # create select button to input file
        self.selectButton3 = QtGui.QPushButton(Overall_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3,3,2,1,1)
        self.inputLayerCombo3 = QtGui.QLineEdit(Overall_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 3,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)     
        
        # button Ok, Close and Help
        self.buttonBox = QtGui.QDialogButtonBox(Overall_window)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Help|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 4, 1, 1, 1)                   
        
        self.retranslateUi(Overall_window)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Overall_window.close)
                
    def retranslateUi(self, Overall_window):
        Overall_window.setWindowTitle(QtGui.QApplication.translate('Overall Occurrence (O)', 'Overall Occurrence (O)', None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate('Overall Occurrence (O)', 'Input file:', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton.setText(QtGui.QApplication.translate('Overall Occurrence (O)', 'Browse', None, QtGui.QApplication.UnicodeUTF8))        
        self.groupBox.setTitle(QtGui.QApplication.translate("Overall Occurrence (O)", "Ratings", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Overall Occurrence (O)","Overall Occurrence (Unconsolidated (sediments))", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Overall Occurrence (O)","Overall Occurrence (Consolidated (porous rocks))", None, QtGui.QApplication.UnicodeUTF8))
        #self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Overall Occurrence (O)","Overall Occurrence (Consolidated (dense rocks))", None, QtGui.QApplication.UnicodeUTF8))
        #self.tableWidget.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("Overall Occurrence (O)","Ratings", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonAdd.setText(QtGui.QApplication.translate("Overall Occurrence (O)", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRemove.setText(QtGui.QApplication.translate("Overall Occurrence (O)", "Remove", None, QtGui.QApplication.UnicodeUTF8))        
        self.buttonAttribute.setText(QtGui.QApplication.translate("Overall Occurrence (O)", "Attribute Table", None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setText(QtGui.QApplication.translate('Overall Occurrence (O)', 'Output file:', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton3.setText(QtGui.QApplication.translate('Overall Occurrence (O)', 'Browse', None, QtGui.QApplication.UnicodeUTF8))    
        self.labelAttrib.setText(QtGui.QApplication.translate('Overall Occurrence (O)', 'Attribute:', None, QtGui.QApplication.UnicodeUTF8)) 
        self.labelPix.setText(QtGui.QApplication.translate('Overall Occurrence (O)', 'Cell size:', None, QtGui.QApplication.UnicodeUTF8))        
        #self.labelWeight.setText(QtGui.QApplication.translate('Overall Occurrence (S)', 'Weight:', None, QtGui.QApplication.UnicodeUTF8))