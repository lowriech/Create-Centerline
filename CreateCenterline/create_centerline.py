# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CreateCenterline
                                 A QGIS plugin
 Creates a centerline from parallel lines
                              -------------------
        begin                : 2016-10-12
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Chris Lowrie
        email                : lowriech@msu.edu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from create_centerline_dialog import CreateCenterlineDialog
import os.path
from shapely.geometry import LineString, Point
from osgeo import ogr
from qgis.core import *


class CreateCenterline:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CreateCenterline_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Create Centerline')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'CreateCenterline')
        self.toolbar.setObjectName(u'CreateCenterline')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CreateCenterline', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = CreateCenterlineDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)
        
        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/CreateCenterline/Icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Create Centerline'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Create Centerline'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

		
    def run(self):

        layers = self.iface.legendInterface().layers()
        self.dlg.selectLayer.clear()
        layer_list = []
        for layer in layers:
            layer_list.append(layer.name())
        self.dlg.selectLayer.addItems(layer_list)
        self.dlg.show()
        result = self.dlg.exec_()

        if result:
            selectedLayerIndex = self.dlg.selectLayer.currentIndex()
            layer = layers[selectedLayerIndex]
            selection = layer.selectedFeatures()
            if len(selection) ==2:
                geom1 = (selection[0].geometry()).asPolyline()
                line = LineString((selection[1].geometry()).asPolyline())
                new_line_array = []
                #print('Hello World')
                for i in geom1:
                    p = Point(i)
                    np = line.interpolate(line.project(p))
                    #print(p)
                    #print(np)
                    p = QgsPoint(p.x, p.y)
                    np = QgsPoint(np.x, np.y)
                    new_pt = (p[0]+np[0])/2, (p[1]+np[1])/2
                    new_pt = QgsPoint(new_pt[0], new_pt[1])
                    new_line_array.append(new_pt)

                print(new_line_array)        
                new_line = QgsGeometry.fromPolyline(new_line_array)
                feat = QgsFeature()
                feat.setGeometry(new_line)
                layer.dataProvider().addFeatures([feat])
                QgsMapLayerRegistry.instance().addMapLayer(layer)
                layer.triggerRepaint()
            else:
                mw = self.iface.mainWindow()
                QMessageBox.warning(mw, "Create Centerline", "Select two and only two lines")
