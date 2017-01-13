# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CreateCenterline
                                 A QGIS plugin
 Creates a centerline
                             -------------------
        begin                : 2017-01-13
        copyright            : (C) 2017 by Chris Lowrie
        email                : lowriech@msu.edu
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
    """Load CreateCenterline class from file CreateCenterline.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .create_centerline import CreateCenterline
    return CreateCenterline(iface)
