# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
import webbrowser
import config

from PyQt4.QtCore import Qt, QSettings
from PyQt4.QtGui import QIcon, QAction

from geoserverexplorer.geoserver import pem
from geoserverexplorer.gui.explorer import GeoServerExplorer
from geoserverexplorer.gui.dialogs.configdialog import ConfigDialog
from geoserverexplorer.qgis.sldadapter import adaptGsToQgs
from geoserverexplorer.qgis import layerwatcher

try:
    from processing.core.Processing import Processing
    from geoserverexplorer.processingprovider.geoserverprovider import GeoServerProvider
    processingOk = True
except:
    processingOk = False


class GeoServerExplorerPlugin:

    def __init__(self, iface):
        self.iface = iface
        config.iface = iface
        if processingOk:
            self.provider = GeoServerProvider()

        try:
            from qgistester.tests import addTestModule
            from geoserverexplorer.test import testplugin
            from geoserverexplorer.test import testpkiplugin
            addTestModule(testplugin, "GeoServer")
            addTestModule(testpkiplugin, "PKI GeoServer")
        except Exception as ex:
            pass

    def unload(self):
        pem.removePkiTempFiles(self.explorer.catalogs())
        self.explorer.deleteLater()
        self.iface.removePluginWebMenu(u"GeoServer", self.explorerAction)
        self.iface.removePluginWebMenu(u"GeoServer", self.configAction)
        self.iface.removePluginWebMenu(u"GeoServer", self.helpAction)
        if processingOk:
            Processing.removeProvider(self.provider)
        layerwatcher.disconnectLayerWasAdded()
        try:
            from qgistester.tests import removeTestModule
            from geoserverexplorer.test import testplugin
            from geoserverexplorer.test import testpkiplugin
            removeTestModule(testplugin, "GeoServer")
            removeTestModule(testpkiplugin, "PKI GeoServer")
        except Exception as ex:
            pass

    def initGui(self):
        icon = QIcon(os.path.dirname(__file__) + "/images/geoserver.png")
        self.explorerAction = QAction(icon, "GeoServer Explorer", self.iface.mainWindow())
        self.explorerAction.triggered.connect(self.openExplorer)
        self.iface.addPluginToWebMenu(u"GeoServer", self.explorerAction)

        settings = QSettings()
        self.explorer = GeoServerExplorer()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.explorer)
        if not settings.value("/GeoServer/Settings/General/ExplorerVisible", False, bool):
            self.explorer.hide()
        self.explorer.visibilityChanged.connect(self._explorerVisibilityChanged)

        icon = QIcon(os.path.dirname(__file__) + "/images/config.png")
        self.configAction = QAction(icon, "GeoServer Explorer settings", self.iface.mainWindow())
        self.configAction.triggered.connect(self.openSettings)
        self.iface.addPluginToWebMenu(u"GeoServer", self.configAction)

        icon = QIcon(os.path.dirname(__file__) + "/images/help.png")
        self.helpAction = QAction(icon, "GeoServer Explorer help", self.iface.mainWindow())
        self.helpAction.triggered.connect(self.showHelp)
        self.iface.addPluginToWebMenu(u"GeoServer", self.helpAction)

        if processingOk:
            Processing.addProvider(self.provider)

        layerwatcher.connectLayerWasAdded(self.explorer)

    def _explorerVisibilityChanged(self, visible):
        settings = QSettings()
        settings.setValue("/GeoServer/Settings/General/ExplorerVisible", visible)

    def showHelp(self):
        webbrowser.open_new(
                        "file://" + os.path.join(os.path.dirname(__file__), "docs", "html", "index.html"))

    def openExplorer(self):
        self.explorer.show()

    def openSettings(self):
        dlg = ConfigDialog(self.explorer)
        dlg.exec_()
