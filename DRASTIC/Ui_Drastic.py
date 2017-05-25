from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *

class Ui_Drastic(object):
    
    def setupUi(self, Drastic_window):
        
        # create Drastic window
        Drastic_window.setWindowModality(QtCore.Qt.ApplicationModal)
        Drastic_window.resize(450,400)
        
        # input file
        # create gridLayout
        self.gridLayout1 = QtGui.QGridLayout(Drastic_window)
        self.gridLayout1.setObjectName("gridLayout1")
        # group box to input files
        self.groupBox = QtGui.QGroupBox(Drastic_window)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout2.setObjectName("gridLayout2")
        self.gridLayout1.addWidget(self.groupBox,0,0,1,-1)        
        # create label in gridLayout 
        self.label = QtGui.QLabel(Drastic_window)
        self.label.setObjectName("label")  
        self.label2 = QtGui.QLabel(Drastic_window)
        self.label2.setObjectName("label2")  
        self.label3 = QtGui.QLabel(Drastic_window)
        self.label3.setObjectName("label3")  
        self.label4 = QtGui.QLabel(Drastic_window)
        self.label4.setObjectName("label4")  
        self.label5 = QtGui.QLabel(Drastic_window)
        self.label5.setObjectName("label5")   
        self.label6 = QtGui.QLabel(Drastic_window)
        self.label6.setObjectName("label6")   
        self.label7 = QtGui.QLabel(Drastic_window)
        self.label7.setObjectName("label7")         
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout2.addWidget(self.label,0,0,1,1)
        self.gridLayout2.addWidget(self.label2,1,0,1,1)
        self.gridLayout2.addWidget(self.label3,2,0,1,1)
        self.gridLayout2.addWidget(self.label4,3,0,1,1)
        self.gridLayout2.addWidget(self.label5,4,0,1,1)
        self.gridLayout2.addWidget(self.label6,5,0,1,1)
        self.gridLayout2.addWidget(self.label7,6,0,1,1)
        # create select button to input file
        self.selectButton = QtGui.QPushButton(Drastic_window)
        self.selectButton.setObjectName("selectButton")
        self.selectButton2 = QtGui.QPushButton(Drastic_window)
        self.selectButton2.setObjectName("selectButton2")    
        self.selectButton3 = QtGui.QPushButton(Drastic_window)
        self.selectButton3.setObjectName("selectButton3")  
        self.selectButton4 = QtGui.QPushButton(Drastic_window)
        self.selectButton4.setObjectName("selectButton4")  
        self.selectButton5 = QtGui.QPushButton(Drastic_window)
        self.selectButton5.setObjectName("selectButton5")  
        self.selectButton6 = QtGui.QPushButton(Drastic_window)
        self.selectButton6.setObjectName("selectButton6")  
        self.selectButton7 = QtGui.QPushButton(Drastic_window)
        self.selectButton7.setObjectName("selectButton7")    
        
        # button weight Depth to Groundwater
        self.labelWeightD = QtGui.QLabel(Drastic_window)
        self.labelWeightD.setObjectName("labelWeightD")
        self.gridLayout2.addWidget(self.labelWeightD,0,2,1,1)
        self.lineWeightD = QtGui.QSpinBox()
        self.lineWeightD.setValue(4)
        self.lineWeightD.stepBy(1)
        self.lineWeightD.setObjectName("lineWeightD")
        self.gridLayout2.addWidget(self.lineWeightD,0,3,1,1)        
        self.gridLayout2.addWidget(self.selectButton,0,4,1,1)
        
        # button weight Recharge
        self.labelWeightR = QtGui.QLabel(Drastic_window)
        self.labelWeightR.setObjectName("labelWeightR")
        self.gridLayout2.addWidget(self.labelWeightR,1,2,1,1)
        self.lineWeightR = QtGui.QSpinBox()
        self.lineWeightR.setValue(3)
        self.lineWeightR.stepBy(1)
        self.lineWeightR.setObjectName("lineWeightR")
        self.gridLayout2.addWidget(self.lineWeightR,1,3,1,1)        
        self.gridLayout2.addWidget(self.selectButton2,1,4,1,1)
        
        # button weight Aquifer
        self.labelWeightA = QtGui.QLabel(Drastic_window)
        self.labelWeightA.setObjectName("labelWeightA")
        self.gridLayout2.addWidget(self.labelWeightA,2,2,1,1)
        self.lineWeightA = QtGui.QSpinBox()
        self.lineWeightA.setValue(2)
        self.lineWeightA.stepBy(1)
        self.lineWeightA.setObjectName("lineWeightA")
        self.gridLayout2.addWidget(self.lineWeightA,2,3,1,1)        
        self.gridLayout2.addWidget(self.selectButton3,2,4,1,1)
        
        # button weight Soil
        self.labelWeightS = QtGui.QLabel(Drastic_window)
        self.labelWeightS.setObjectName("labelWeightS")
        self.gridLayout2.addWidget(self.labelWeightS,3,2,1,1)
        self.lineWeightS = QtGui.QSpinBox()
        self.lineWeightS.setValue(1)
        self.lineWeightS.stepBy(1)
        self.lineWeightS.setObjectName("lineWeightS")
        self.gridLayout2.addWidget(self.lineWeightS,3,3,1,1)        
        self.gridLayout2.addWidget(self.selectButton4,3,4,1,1)
        
        # button weight Topography
        self.labelWeightT = QtGui.QLabel(Drastic_window)
        self.labelWeightT.setObjectName("labelWeightT")
        self.gridLayout2.addWidget(self.labelWeightT,4,2,1,1)
        self.lineWeightT = QtGui.QSpinBox()
        self.lineWeightT.setValue(0)
        self.lineWeightT.stepBy(1)
        self.lineWeightT.setObjectName("lineWeightT")
        self.gridLayout2.addWidget(self.lineWeightT,4,3,1,1)        
        self.gridLayout2.addWidget(self.selectButton5,4,4,1,1)
        
        # button weight Impact of Vadose Zone
        self.labelWeightI = QtGui.QLabel(Drastic_window)
        self.labelWeightI.setObjectName("labelWeightI")
        self.gridLayout2.addWidget(self.labelWeightI,5,2,1,1)
        self.lineWeightI = QtGui.QSpinBox()
        self.lineWeightI.setValue(4)
        self.lineWeightI.stepBy(1)
        self.lineWeightI.setObjectName("lineWeightI")
        self.gridLayout2.addWidget(self.lineWeightI,5,3,1,1)
        self.gridLayout2.addWidget(self.selectButton6,5,4,1,1)
   
        # button weight Hydraulic
        self.labelWeightC = QtGui.QLabel(Drastic_window)
        self.labelWeightC.setObjectName("labelWeightC")
        self.gridLayout2.addWidget(self.labelWeightC,6,2,1,1)
        self.lineWeightC = QtGui.QSpinBox()
        self.lineWeightC.setValue(2)
        self.lineWeightC.stepBy(1)
        self.lineWeightC.setObjectName("lineWeightC")
        self.gridLayout2.addWidget(self.lineWeightC,6,3,1,1)        
        self.gridLayout2.addWidget(self.selectButton7,6,4,1,1)
        
        
        self.inputLayerCombo = QtGui.QComboBox(Drastic_window)
        self.inputLayerCombo.setObjectName("inputLayerCombo")  
        self.inputLayerCombo2 = QtGui.QComboBox(Drastic_window)
        self.inputLayerCombo2.setObjectName("inputLayerCombo2")  
        self.inputLayerCombo3 = QtGui.QComboBox(Drastic_window)
        self.inputLayerCombo3.setObjectName("inputLayerCombo3")  
        self.inputLayerCombo4 = QtGui.QComboBox(Drastic_window)
        self.inputLayerCombo4.setObjectName("inputLayerCombo4")   
        self.inputLayerCombo5 = QtGui.QComboBox(Drastic_window)
        self.inputLayerCombo5.setObjectName("inputLayerCombo5")  
        self.inputLayerCombo6 = QtGui.QComboBox(Drastic_window)
        self.inputLayerCombo6.setObjectName("inputLayerCombo6")  
        self.inputLayerCombo7 = QtGui.QComboBox(Drastic_window)
        self.inputLayerCombo7.setObjectName("inputLayerCombo7")         
        self.gridLayout2.addWidget(self.inputLayerCombo,0,1,1,1)
        self.gridLayout2.addWidget(self.inputLayerCombo2,1,1,1,1)
        self.gridLayout2.addWidget(self.inputLayerCombo3,2,1,1,1)
        self.gridLayout2.addWidget(self.inputLayerCombo4,3,1,1,1)
        self.gridLayout2.addWidget(self.inputLayerCombo5,4,1,1,1)
        self.gridLayout2.addWidget(self.inputLayerCombo6,5,1,1,1)
        self.gridLayout2.addWidget(self.inputLayerCombo7,6,1,1,1)
        # stretch to extend the widget in column 1
        self.gridLayout2.setColumnStretch(1,1)  
        
        # output file
        # group box to output files
        self.groupBox2 = QtGui.QGroupBox(Drastic_window)
        self.groupBox2.setObjectName("groupBox2")
        self.gridLayout3 = QtGui.QGridLayout(self.groupBox2)
        self.gridLayout3.setObjectName("gridLayout3")
        self.gridLayout1.addWidget(self.groupBox2,1,0,1,-1)        
        # create label in gridLayout
        self.label_out = QtGui.QLabel(Drastic_window)
        self.label_out.setObjectName("label_out")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout3.addWidget(self.label_out,0,0,1,1)
        # create select button to output file
        self.selectButton_out = QtGui.QPushButton(Drastic_window)
        self.selectButton_out.setObjectName("selectButton_out")
        self.gridLayout3.addWidget(self.selectButton_out,0,2,1,1)
        self.outputLayerCombo = QtGui.QLineEdit(Drastic_window)
        self.outputLayerCombo.setObjectName("outputLayerCombo")
        self.gridLayout3.addWidget(self.outputLayerCombo, 0,1,1,1)
        # output color
        # create label in gridLayout
        self.label_color = QtGui.QLabel(Drastic_window)
        self.label_color.setObjectName("label_color")
        # define label (QWidget, row, column, QtAlignement)
        self.gridLayout3.addWidget(self.label_color,2,0,1,1)
        # create select button to output file
        self.selectButton_color = QtGui.QPushButton(Drastic_window)
        self.selectButton_color.setObjectName("selectButton_color")
        self.gridLayout3.addWidget(self.selectButton_color,2,2,1,1)
        self.outputLayerCombo_color = QtGui.QLineEdit(Drastic_window)
        self.outputLayerCombo_color.setObjectName("outputLayerCombo_color")
        self.gridLayout3.addWidget(self.outputLayerCombo_color, 2,1,1,1)
        
        # checkbox to define the output
        self.label_checkdrastic = QtGui.QLabel(Drastic_window)
        self.label_checkdrastic.setObjectName("label_checkdrastic")
        self.gridLayout3.addWidget(self.label_checkdrastic,1,1,1,1)
        self.checkdrastic = QtGui.QCheckBox(Drastic_window)
        self.checkdrastic.setObjectName("checkdrastic")
        self.gridLayout3.addWidget(self.checkdrastic,1,0,1,1)
        
        self.label_checkcolor = QtGui.QLabel(Drastic_window)
        self.label_checkcolor.setObjectName("label_checkcolor")
        self.gridLayout3.addWidget(self.label_checkcolor,3,1,1,1)
        self.checkcolor = QtGui.QCheckBox(Drastic_window)
        self.checkcolor.setObjectName("checkcolor")
        self.gridLayout3.addWidget(self.checkcolor,3,0,1,1)        

    
        # button Ok, Close and Help
        self.buttonBox = QtGui.QDialogButtonBox(Drastic_window)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Help|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout1.addWidget(self.buttonBox, 2, 1, 1, 1)          
        
        self.retranslateUi(Drastic_window)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Drastic_window.close)
    
    def retranslateUi(self, Drastic_window):
        Drastic_window.setWindowTitle(QtGui.QApplication.translate('DRASTIC', 'DRASTIC', None, QtGui.QApplication.UnicodeUTF8))   
        self.label.setText(QtGui.QApplication.translate('DRASTIC', 'D', None, QtGui.QApplication.UnicodeUTF8))
        self.label2.setText(QtGui.QApplication.translate('DRASTIC', 'R', None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setText(QtGui.QApplication.translate('DRASTIC', 'A', None, QtGui.QApplication.UnicodeUTF8))
        self.label4.setText(QtGui.QApplication.translate('DRASTIC', 'S', None, QtGui.QApplication.UnicodeUTF8))
        self.label5.setText(QtGui.QApplication.translate('DRASTIC', 'T', None, QtGui.QApplication.UnicodeUTF8))
        self.label6.setText(QtGui.QApplication.translate('DRASTIC', 'I', None, QtGui.QApplication.UnicodeUTF8))
        self.label7.setText(QtGui.QApplication.translate('DRASTIC', 'C', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton.setText(QtGui.QApplication.translate('DRASTIC', 'Browse', None, QtGui.QApplication.UnicodeUTF8))   
        self.selectButton2.setText(QtGui.QApplication.translate('DRASTIC', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton3.setText(QtGui.QApplication.translate('DRASTIC', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton4.setText(QtGui.QApplication.translate('DRASTIC', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton5.setText(QtGui.QApplication.translate('DRASTIC', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton6.setText(QtGui.QApplication.translate('DRASTIC', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton7.setText(QtGui.QApplication.translate('DRASTIC', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton_out.setText(QtGui.QApplication.translate('DRASTIC', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.label_out.setText(QtGui.QApplication.translate('DRASTIC', 'DRASTIC:', None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("DRASTIC", "Input", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox2.setTitle(QtGui.QApplication.translate("DRASTIC", "Output", None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton_color.setText(QtGui.QApplication.translate('DRASTIC', 'Browse', None, QtGui.QApplication.UnicodeUTF8))
        self.label_color.setText(QtGui.QApplication.translate('DRASTIC', 'DRASTIC COLORED:', None, QtGui.QApplication.UnicodeUTF8))
        self.label_checkdrastic.setText(QtGui.QApplication.translate('DRASTIC', 'Load raster into canvas', None, QtGui.QApplication.UnicodeUTF8))
        self.label_checkcolor.setText(QtGui.QApplication.translate('DRASTIC', 'Load colored raster into canvas', None, QtGui.QApplication.UnicodeUTF8))
        self.labelWeightD.setText(QtGui.QApplication.translate('DRASTIC', 'Weight:', None, QtGui.QApplication.UnicodeUTF8))
        self.labelWeightR.setText(QtGui.QApplication.translate('DRASTIC', 'Weight:', None, QtGui.QApplication.UnicodeUTF8))
        self.labelWeightA.setText(QtGui.QApplication.translate('DRASTIC', 'Weight:', None, QtGui.QApplication.UnicodeUTF8))
        self.labelWeightS.setText(QtGui.QApplication.translate('DRASTIC', 'Weight:', None, QtGui.QApplication.UnicodeUTF8))
        self.labelWeightT.setText(QtGui.QApplication.translate('DRASTIC', 'Weight:', None, QtGui.QApplication.UnicodeUTF8))
        self.labelWeightI.setText(QtGui.QApplication.translate('DRASTIC', 'Weight:', None, QtGui.QApplication.UnicodeUTF8))
        self.labelWeightC.setText(QtGui.QApplication.translate('DRASTIC', 'Weight:', None, QtGui.QApplication.UnicodeUTF8))
        
        
        
        