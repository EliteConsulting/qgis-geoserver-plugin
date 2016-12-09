# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import sys
import os
import site

site.addsitedir(os.path.abspath(os.path.dirname(__file__) + '/ext-libs'))

# ABP: TORM import gsconfig from here
# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/ext-src/gsconfig/src'))
#import httplib2
#httplib2.debuglevel = 1

def classFactory(iface):
    from geoserverexplorer.plugin import GeoServerExplorerPlugin
    return GeoServerExplorerPlugin(iface)
