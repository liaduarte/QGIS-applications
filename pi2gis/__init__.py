# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PI2GIS
                                 A QGIS plugin
 Processing Image to Geographical Information Systems – a learning tool for QGIS
                             -------------------
        begin                : 2017-03-23
        copyright            : (C) 2017 by Rui Correia
        email                : rui_correia11@hotmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PI2GIS class from file PI2GIS.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .PI2GIS import PI2GIS
    return PI2GIS(iface)
