#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2011 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License as follows:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
"""

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

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self.__contentTest1())
        contentLayout.addLayout(self.__contentTest2())
        contentLayout.addStretch(5)

    def __contentTest1(self):
        """ """
        # Active widgets and connections.
        self.__nameedit = QtGui.QLineEdit("<Name>")
        self.__emailedit = QtGui.QLineEdit("<Email>")
        self.__customerlist = QtGui.QListWidget()        
        # Layout widgets.
        layout = QtGui.QFormLayout()
        layout.addRow("&Name:", self.__nameedit)
        layout.addRow("&Email:", self.__emailedit)
        layout.addRow("&Projects:", self.__customerlist)
        #
        return layout

    def __contentTest2(self):
        """ """
        # Active widgets and connections.
        self.__testbutton = QtGui.QPushButton("Write name to log")
        self.connect(self.__testbutton, QtCore.SIGNAL("clicked()"), self.__test)   
        # Active widgets and connections.
        layout = QtGui.QHBoxLayout()
        layout.addStretch(5)
        layout.addWidget(self.__testbutton)
        #
        return layout

    def __test(self):
        """ """
        self._writeToLog("Name: " + unicode(self.__nameedit.text()))
