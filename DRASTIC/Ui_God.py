from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *

class Ui_God(object):
    
    def setupUi(self, God):
        
        # create Drastic window
        God.setWindowModality(QtCore.Qt.ApplicationModal)
        God.resize(450,400)
        
        # input file
        # create gridLayout
        self.gridLayout1 = QtGui.QGridLayout(God)
        self.gridLayout1.setObjectName("gridLayout1")
        # group box to input files
        self.groupBox = QtGui.QGroupBox(God)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox,0,0,1,-1)        
        # create label in gridLayout 
        self.label = QtGui.QLabel(God)
        self.label.setObjectName("label")  
        self.label2 = QtGui.QLabel(God)
        self.label2.setObjectName("label2")  
        self.label3 = QtGui.QLabel(God)
        self.label3.setObjectName("label3")  
               
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout2.addWidget(self.label,0,0,1,1)
        self.gridLayout2.addWidget(self.label2,1,0,1,1)
        self.gridLayout2.addWidget(self.label3,2,0,1,1)
    
        # create select button to input file
        self.selectButton = QtGui.QPushButton(God)
        self.selectButton.setObjectName("selectButton")
        self.selectButton2 = QtGui.QPushButton(God)
        self.selectButton2.setObjectName("selectButton2")    
        self.selectButton3 = QtGui.QPushButton(God)
        self.selectButton3.setObjectName("selectButton3")  
          
        
        # button weight Depth to Groundwater
       
        self.gridLayout2.addWidget(self.selectButton,0,4,1,1)
        
        # button weight Recharge
         
        self.gridLayout2.addWidget(self.selectButton2,1,4,1,1)
        
        # button weight Aquifer
           
        self.gridLayout2.addWidget(self.selectButton3,2,4,1,1)        
        
        
        self.inputLayerCombo = QtGui.QComboBox(God)
        self.inputLayerCombo.setObjectName("inputLayerCombo")  
        self.inputLayerCombo2 = QtGui.QComboBox(God)
        self.inputLayerCombo2.setObjectName("inputLayerCombo2")  
        self.inputLayerCombo3 = QtGui.QComboBox(God)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")  
        
              
        self.gridLayout2.addWidget(self.inputLayerCombo,0,1,1,1)
        self.gridLayout2.addWidget(self.inputLayerCombo2,1,1,1,1)
        self.gridLayout2.addWidget(self.inputLayerCombo3,2,1,1,1)
        #self.gridLayout2.addWidget(self.inputLayerCombo4,3,1,1,1)
      
        # stretch to extend the widget in column 1
        self.gridLayout2.setColumnStretch(1,1)  
        
        # output file
        # group box to output files
        self.groupBox2 = QtGui.QGroupBox(God)
        self.groupBox2.setObjectName("groupBox2")
        self.gridLayout3 = QtGui.QGridLayout(self.groupBox2)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox2,1,0,1,-1)        
        # create label in gridLayout
        self.label_out = QtGui.QLabel(God)
        self.label_out.setObjectName("label_out")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout3.addWidget(self.label_out,0,0,1,1)
        # create select button to output file
        self.selectButton_out = QtGui.QPushButton(God)
        self.selectButton_out.setObjectName("selectButton_out")
        self.gridLayout3.addWidget(self.selectButton_out,0,2,1,1)
        self.outputLayerCombo = QtGui.QLineEdit(God)
        self.outputLayerCombo.setObjectName("outputLayerCombo")
        self.gridLayout3.addWidget(self.outputLayerCombo, 0,1,1,1)
        # output color
        # create label in gridLayout
        self.label_color = QtGui.QLabel(God)
        self.label_color.setObjectName("label_color")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout3.addWidget(self.label_color,2,0,1,1)
        # create select button to output file
        self.selectButton_color = QtGui.QPushButton(God)
        self.selectButton_color.setObjectName("selectButton_color")
        self.gridLayout3.addWidget(self.selectButton_color,2,2,1,1)
        self.outputLayerCombo_color = QtGui.QLineEdit(God)
        self.outputLayerCombo_color.setObjectName("outputLayerCombo_color")
        self.gridLayout3.addWidget(self.outputLayerCombo_color, 2,1,1,1)
        
        # checkbox to define the output
        self.label_checkdrastic = QtGui.QLabel(God)
        self.label_checkdrastic.setObjectName("label_checkdrastic")
        self.gridLayout3.addWidget(self.label_checkdrastic,1,1,1,1)
        self.checkdrastic = QtGui.QCheckBox(God)
        self.checkdrastic.setObjectName("checkdrastic")
        self.gridLayout3.addWidget(self.checkdrastic,1,0,1,1)
        
        self.label_checkcolor = QtGui.QLabel(God)
        self.label_checkcolor.setObjectName("label_checkcolor")
        self.gridLayout3.addWidget(self.label_checkcolor,3,1,1,1)
        self.checkcolor = QtGui.QCheckBox(God)
        self.checkcolor.setObjectName("checkcolor")
        self.gridLayout3.addWidget(self.checkcolor,3,0,1,1)        

    
        # button Ok, Close and Help
        self.buttonBox = QtGui.QDialogButtonBox(God)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Help|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 2, 1, 1, 1)          
        
        self.retranslateUi(God)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), God.close)
    
    def retranslateUi(self, God):
        God.setWindowTitle(QtGui.QApplication.translate('GOD', 'GOD', None, QtGui.QApplication.UnicodeUTF8))   
        self.label.setText(QtGui.QApplication.translate('GOD', 'G', None, QtGui.QApplication.UnicodeUTF8))
        self.label2.setText(QtGui.QApplication.translate('GOD', 'O', None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setText(QtGui.QApplication.translate('GOD', 'D', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton.setText(QtGui.QApplication.translate('GOD', 'Browse', None, QtGui.QApplication.UnicodeUTF8))   
        self.selectButton2.setText(QtGui.QApplication.translate('GOD', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton3.setText(QtGui.QApplication.translate('GOD', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton_out.setText(QtGui.QApplication.translate('GOD', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.label_out.setText(QtGui.QApplication.translate('GOD', 'GOD:', None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("GOD", "Input", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox2.setTitle(QtGui.QApplication.translate("GOD", "Output", None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton_color.setText(QtGui.QApplication.translate('GOD', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.label_color.setText(QtGui.QApplication.translate('GOD', 'GOD COLORED:', None, QtGui.QApplication.UnicodeUTF8))
        self.label_checkdrastic.setText(QtGui.QApplication.translate('GOD', 'Load raster into canvas', None, QtGui.QApplication.UnicodeUTF8))
        self.label_checkcolor.setText(QtGui.QApplication.translate('GOD', 'Load colored raster into canvas', None, QtGui.QApplication.UnicodeUTF8))
       