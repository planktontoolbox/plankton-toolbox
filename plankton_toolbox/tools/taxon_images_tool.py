#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_base as tool_base

class TaxonImagesTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(TaxonImagesTool, self).__init__(name, parentwidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setBaseSize(600,600)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._contentImage())
        contentLayout.addStretch(5)

    def _contentImage(self):
        """ """
        layout = QtGui.QVBoxLayout()
        label = QtGui.QLabel('<b><i>Incertae sedis</i></b>')
        label.setAlignment(QtCore.Qt.AlignHCenter)
        imagelabel = QtGui.QLabel()
        imagelabel.setAlignment(QtCore.Qt.AlignHCenter)
        image = QtGui.QImage('../planktondata/cache/images/Incertae_sedis.jpg')
        imagelabel.setPixmap(QtGui.QPixmap.fromImage(image))
        layout.addWidget(label)
        layout.addWidget(imagelabel)
        #
        return layout
    
    def _test(self):
        """ """
        self._writeToLog("Name: " + unicode(self._nameedit.text()))
