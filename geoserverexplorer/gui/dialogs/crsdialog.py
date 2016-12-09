# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from PyQt4.QtGui import (QDialog,
                         QVBoxLayout,
                         QDialogButtonBox
                        )
from qgis.gui import QgsProjectionSelector

class CrsSelectionDialog(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.authid = None
        layout = QVBoxLayout()
        self.selector = QgsProjectionSelector(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        layout.addWidget(self.selector)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)

    def okPressed(self):
        self.authid = self.selector.selectedAuthId()
        self.close()

    def cancelPressed(self):
        self.authid = None
        self.close()
