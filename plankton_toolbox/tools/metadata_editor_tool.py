#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_base as tool_base

class MetadataEditorTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(MetadataEditorTool, self).__init__(name, parentwidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setBaseSize(600,600)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._contentTest1())
        contentLayout.addLayout(self._contentTest2())
        contentLayout.addStretch(5)

    def _contentTest1(self):
        """ """
        # Active widgets and connections.
        self._nameedit = QtGui.QLineEdit("<Name>")
        self._emailedit = QtGui.QLineEdit("<Email>")
        self._customerlist = QtGui.QListWidget()        
        # Layout widgets.
        layout = QtGui.QFormLayout()
        layout.addRow("&Name:", self._nameedit)
        layout.addRow("&Email:", self._emailedit)
        layout.addRow("&Projects:", self._customerlist)
        #
        return layout

    def _contentTest2(self):
        """ """
        # Active widgets and connections.
        self._testbutton = QtGui.QPushButton("Write name to log")
        self.connect(self._testbutton, QtCore.SIGNAL("clicked()"), self._test)   
        # Active widgets and connections.
        layout = QtGui.QHBoxLayout()
        layout.addStretch(5)
        layout.addWidget(self._testbutton)
        #
        return layout

    def _test(self):
        """ """
        self._writeToLog("Name: " + unicode(self._nameedit.text()))
