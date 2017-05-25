from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
#from Ui_Aquifer_media import Ui_Aquifer_media
import GdalTools_utils as Utils
try:
    from PyQt4.QtCore import QString
except ImportError:
    QString = str
import os, sys
from processing.core.Processing import Processing
from osgeo import ogr
import ftools_utils
from osgeo import gdal
import numpy