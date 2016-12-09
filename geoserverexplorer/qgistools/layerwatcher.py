# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from qgis.core import QgsMapLayerRegistry

from geoserverexplorer.qgistools import uri as uri_utils
from geoserverexplorer.qgistools.utils import tempFilename
from geoserverexplorer.qgistools.sldadapter import adaptGsToQgs

_explorer = None

def layerAdded(qgislayer):
    try:
        if qgislayer.providerType().lower() != "wfs":
            return
    except:
        pass #Not all layers have a providerType method
    catalogs = list(_explorer.explorerTree.gsItem._catalogs.values())
    for cat in catalogs:
        if cat.gs_base_url in qgislayer.source():
            for layer in cat.get_layers():
                uri = uri_utils.layerUri(layer)
                if uri == qgislayer.source():
                    try:
                        sld = layer.default_style.sld_body
                        sld = adaptGsToQgs(sld)
                        sldfile = tempFilename("sld")
                        with open(sldfile, 'w') as f:
                            f.write(sld)
                        msg, ok = qgislayer.loadSldStyle(sldfile)
                        if not ok:
                            raise Exception("Could not load style for layer <b>%s</b>" % qgislayer.name())
                    except Exception as e:
                        _explorer.setWarning("Could not set style for layer <b>%s</b>" % qgislayer.name())
                    break

def connectLayerWasAdded(explorer):
    global _explorer
    _explorer = explorer
    QgsMapLayerRegistry.instance().layerWasAdded.connect(layerAdded)

def disconnectLayerWasAdded():
    QgsMapLayerRegistry.instance().layerWasAdded.disconnect(layerAdded)
