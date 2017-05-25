from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *

class Ui_Depth_groundwater(object):
    
    def setupUi(self, Depth_window):
        
        # create Depth window
        Depth_window.setWindowModality(QtCore.Qt.ApplicationModal)
        Depth_window.resize(400,400)
        
        # input file points
        # create gridLayout
        self.gridLayout1 = QtGui.QGridLayout(Depth_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # create groupBox method I
        self.groupBox_m1 = QtGui.QGroupBox(Depth_window)
        self.groupBox_m1.setObjectName("groupBox_m1")
        self.groupBox_m1.setTitle("Base")
        self.gridLayout_m1 = QtGui.QGridLayout(self.groupBox_m1) 
        self.gridLayout_m1.setObjectName("gridLayout_m1")
        self.gridLayout1.addWidget(self.groupBox_m1, 0,0,1,-1)        
        # create label in gridLayout 
        self.label = QtGui.QLabel(Depth_window)
        self.label.setObjectName("label")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout_m1.addWidget(self.label,0,0,1,1)
        # create select button to input file
        self.selectButton = QtGui.QPushButton(Depth_window)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout_m1.addWidget(self.selectButton,0,2,1,1)
        self.inputLayerCombo = QtGui.QComboBox(Depth_window)
        self.inputLayerCombo.setEditable(True)
        self.inputLayerCombo.setObjectName("inputLayerCombo")
        self.gridLayout_m1.addWidget(self.inputLayerCombo, 0,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout_m1.setColumnStretch(1,1)
        
        # field to mask shapefile input
        self.maskLabel = QtGui.QLabel(Depth_window)
        self.maskLabel.setObjectName("maskLabel")
        self.gridLayout_m1.addWidget(self.maskLabel, 1,0,1,1)
        # create select button to input mask
        self.selectMask = QtGui.QPushButton(Depth_window)
        self.selectMask.setObjectName("selectMask")
        self.gridLayout_m1.addWidget(self.selectMask, 1,2,1,1)
        self.inputMaskCombo = QtGui.QComboBox(Depth_window)
        self.inputMaskCombo.setEditable(True)
        self.inputMaskCombo.setObjectName("inputMaskCombo")
        self.gridLayout_m1.addWidget(self.inputMaskCombo, 1,1,1,1)
        # stretch to extend the widget in column1
        self.gridLayout_m1.setColumnStretch(1,1)
        
        # field to interpolation method (the user must to choose)
        self.methodLabel = QtGui.QLabel(Depth_window)
        self.methodLabel.setObjectName("methodLabel")
        self.gridLayout1.addWidget(self.methodLabel, 2,0,1,1)
        # combobox to choose the method
        self.comboBoxMethod = QtGui.QComboBox(Depth_window)
        self.comboBoxMethod.setObjectName("comboBoxMethod")
        self.gridLayout1.addWidget(self.comboBoxMethod,2,1,1,-1)
        self.styles = ['Inverse Distance Weighting', 'Kriging', 'Cubic spline approximation (SAGA)', 'Spatial approximation using spline with tension (GRASS)']
        self.comboBoxMethod.addItems(self.styles)
        
        # define a groupbox to specify the cell size and attribute
        self.groupBox1 = QtGui.QGroupBox(Depth_window)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout3 = QtGui.QGridLayout(self.groupBox1)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox1, 1,0,1,-1)
        # define attribute "Elevation"
        self.labelAttrib = QtGui.QLabel(Depth_window)
        self.labelAttrib.setObjectName("labelAttrib")
        self.gridLayout3.addWidget(self.labelAttrib,0,0,-1,1)
        self.lineAttrib = QtGui.QComboBox(Depth_window)
        self.lineAttrib.setObjectName("lineAttrib")
        self.gridLayout3.addWidget(self.lineAttrib,0,1,-1,1)
        # define pixel size
        self.labelPix = QtGui.QLabel(Depth_window)
        self.labelPix.setObjectName("labelPix")
        self.gridLayout3.addWidget(self.labelPix, 0,3,-1,1)
        self.linePix = QtGui.QSpinBox()
        self.linePix.setValue(29)
        self.linePix.stepBy(1)
        self.linePix.setObjectName("linePix")
        self.gridLayout3.addWidget(self.linePix,0,4,-1,1)     
        
        
        # input file mdt
        # create groupBox method II
        self.groupBox_m2 = QtGui.QGroupBox(Depth_window)
        self.groupBox_m2.setObjectName("groupBox_m2")
        self.groupBox_m2.setTitle("Improvement")
        self.gridLayout_m2 = QtGui.QGridLayout(self.groupBox_m2) 
        self.gridLayout_m2.setObjectName("gridLayout_m2")
        self.gridLayout1.addWidget(self.groupBox_m2, 3,0,1,-1)            
        # create label 
        self.label_mdt = QtGui.QLabel(Depth_window)
        self.label_mdt.setObjectName("label_mdt")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout_m2.addWidget(self.label_mdt,0,0,1,1)
        # create select button to input file
        self.selectButton_mdt = QtGui.QPushButton(Depth_window)
        self.selectButton_mdt.setObjectName("selectButton_mdt")
        self.gridLayout_m2.addWidget(self.selectButton_mdt,0,2,1,1)
        self.inputLayerCombo_mdt = QtGui.QComboBox(Depth_window)
        self.inputLayerCombo_mdt.setEditable(True)
        self.inputLayerCombo_mdt.setObjectName("inputLayerCombo_mdt")
        self.gridLayout_m2.addWidget(self.inputLayerCombo_mdt, 0,1,1,1)
        self.gridLayout_m2.setColumnStretch(1,1)     
        
        # define a groupbox to specify the maximum depth and distance
        self.groupBox_max = QtGui.QGroupBox(Depth_window)
        self.groupBox_max.setObjectName("groupBox_max")
        self.gridLayout5 = QtGui.QGridLayout(self.groupBox_max)
        self.gridLayout5.setObjectName("gridLayout5")
        self.gridLayout1.addWidget(self.groupBox_max, 4,0,1,-1)
        # field to maximum depth
        self.label_max_depth = QtGui.QLabel(Depth_window)
        self.label_max_depth.setObjectName("label_max_depth")    
        self.gridLayout5.addWidget(self.label_max_depth,0,0,1,1)
        self.line_max = QtGui.QSpinBox()
        self.line_max.setValue(19)
        self.line_max.stepBy(1)
        self.line_max.setObjectName("line_max")
        self.gridLayout5.addWidget(self.line_max,0,1,1,1)
        # field to distance
        self.label_distance = QtGui.QLabel(Depth_window)
        self.label_distance.setObjectName("label_distance")    
        self.gridLayout5.addWidget(self.label_distance,0,2,1,1)
        self.line_distance = QtGui.QSpinBox()
        self.line_distance.setMinimum(100)
        self.line_distance.setMaximum(1000)
        self.line_distance.setValue(199)
        self.line_distance.stepBy(1)
        self.line_distance.setObjectName("line_distance")
        self.gridLayout5.addWidget(self.line_distance,0,3,1,1)    
        # field to define the minimum size of basin
        self.label_size = QtGui.QLabel(Depth_window)
        self.label_size.setObjectName("label_size")    
        self.gridLayout5.addWidget(self.label_size,0,4,1,1)
        self.line_size = QtGui.QSpinBox()
        self.line_size.setMinimum(49)
        self.line_size.setMaximum(1000)
        self.line_size.setValue(49)
        self.line_size.stepBy(1)
        self.line_size.setObjectName("line_size")
        self.gridLayout5.addWidget(self.line_size,0,5,1,1)           
        # stretch to extend the widget in column 1
        self.gridLayout5.setColumnStretch(1,1)        
        
        # define the indexs
        # create a group box
        self.groupBox = QtGui.QGroupBox(Depth_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox, 5,0,1,-1)
        # table for classes and indexes
        self.tableWidget = QtGui.QTableWidget(7,3,Depth_window)
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
        self.line = QtGui.QLineEdit("1.5")
        self.tableWidget.setItem(1,0,QtGui.QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(0,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("4.6")
        self.tableWidget.setItem(2,0,QtGui.QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(1,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("9.1")
        self.tableWidget.setItem(3,0,QtGui.QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(2,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("15.2")
        self.tableWidget.setItem(4,0,QtGui.QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(3,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("22.9")
        self.tableWidget.setItem(5,0,QtGui.QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(4,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("30.5")
        self.tableWidget.setItem(6,0,QtGui.QTableWidgetItem(self.line.text()))
        self.tableWidget.setItem(5,1,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("200")
        self.tableWidget.setItem(6,1,QtGui.QTableWidgetItem(self.line.text()))
        # set the indexes values
        self.line = QtGui.QLineEdit("10")
        self.tableWidget.setItem(0,2,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("9")
        self.tableWidget.setItem(1,2,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("7")
        self.tableWidget.setItem(2,2,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("5")
        self.tableWidget.setItem(3,2,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("3")
        self.tableWidget.setItem(4,2,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("2")
        self.tableWidget.setItem(5,2,QtGui.QTableWidgetItem(self.line.text()))
        self.line = QtGui.QLineEdit("1")
        self.tableWidget.setItem(6,2,QtGui.QTableWidgetItem(self.line.text())) 
        # create a box layout to insert the buttons Add and Remove
        self.boxLayout = QtGui.QVBoxLayout()
        self.boxLayout.setObjectName("boxLayout")
        # button Add
        self.buttonAdd = QtGui.QPushButton(Depth_window)
        self.buttonAdd.setObjectName("buttonAdd")
        self.boxLayout.addWidget(self.buttonAdd)
        # button Remove
        self.buttonRemove = QtGui.QPushButton(Depth_window)
        self.buttonRemove.setObjectName("buttonRemove") 
        self.boxLayout.addWidget(self.buttonRemove)
        ## button weight
        #self.labelWeight = QtGui.QLabel(Depth_window)
        #self.labelWeight.setObjectName("labelWeight")
        #self.boxLayout.addWidget(self.labelWeight)
        #self.lineWeight = QtGui.QSpinBox()
        #self.lineWeight.setValue(4)
        #self.lineWeight.stepBy(1)
        #self.lineWeight.setObjectName("lineWeight")
        #self.boxLayout.addWidget(self.lineWeight)
        self.gridLayout2.addLayout(self.boxLayout,0,1,-1,1)
        
        # output file
        # create label in gridLayout
        self.label3 = QtGui.QLabel(Depth_window)
        self.label3.setObjectName("label3")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout1.addWidget(self.label3,6,0,1,1)
        # create select button to input file
        self.selectButton3 = QtGui.QPushButton(Depth_window)
        self.selectButton3.setObjectName("selectButton3")
        self.gridLayout1.addWidget(self.selectButton3,6,2,1,1)
        self.inputLayerCombo3 = QtGui.QLineEdit(Depth_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")
        self.gridLayout1.addWidget(self.inputLayerCombo3, 6,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout1.setColumnStretch(1,1)   
        
        # button Ok, Close and Help
        self.buttonBox = QtGui.QDialogButtonBox(Depth_window)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Help|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 7, 1, 1, 1)        
        
        self.retranslateUi(Depth_window)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Depth_window.close)
        
    def retranslateUi(self, Depth_window):
        Depth_window.setWindowTitle(QtGui.QApplication.translate('Depth Groundwater (D)', 'Depth Groundwater (D)', None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Input file points:', None, QtGui.QApplication.UnicodeUTF8))
        self.label_mdt.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Input file MDT:', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton_mdt.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.selectMask.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.methodLabel.setText(QtGui.QApplication.translate("Depth Groundwater (D)", "Interpolation Method", None, QtGui.QApplication.UnicodeUTF8))
        self.maskLabel.setText(QtGui.QApplication.translate("Depth Groundwater (D)", "Mask:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Depth Groundwater (D)", "Ratings", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Depth Groundwater (D)","Depth(m)", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Depth Groundwater (D)","Depth(m)", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Depth Groundwater (D)","Ratings", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonAdd.setText(QtGui.QApplication.translate("Depth Groundwater (D)", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRemove.setText(QtGui.QApplication.translate("Depth Groundwater (D)", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Output file:', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton3.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Browse', None, QtGui.QApplication.UnicodeUTF8))  
        #self.labelWeight.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Weight:', None, QtGui.QApplication.UnicodeUTF8))
        self.labelAttrib.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Attribute:', None, QtGui.QApplication.UnicodeUTF8)) 
        self.labelPix.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Cell size:', None, QtGui.QApplication.UnicodeUTF8))
        self.label_max_depth.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Maximum depth:', None, QtGui.QApplication.UnicodeUTF8))
        self.label_distance.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Distance:', None, QtGui.QApplication.UnicodeUTF8))
        self.label_size.setText(QtGui.QApplication.translate('Depth Groundwater (D)', 'Minimum size of watershed basin:', None, QtGui.QApplication.UnicodeUTF8))