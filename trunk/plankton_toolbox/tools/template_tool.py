#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010 SMHI, Swedish Meteorological and Hydrological Institute 
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

class TemplateTool(tool_base.ToolBase):
    """
    This is a simple tool to be used as a template when creating new tools.
    """
    
    def __init__(self, name, parentwidget):
        """ """
        super(TemplateTool, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        mainwidget = QtGui.QWidget(self._parent)
        self.setWidget(mainwidget)
        # Active widgets and connections.
        self.__nameedit = QtGui.QLineEdit("<Name>")
        self.__emailedit = QtGui.QLineEdit("<Email>")
        self.__customerlist = QtGui.QListWidget()
        self.__testbutton = QtGui.QPushButton("Write name to log")
        self.connect(self.__testbutton, QtCore.SIGNAL("clicked()"), self.__test)                
        # Layout widgets.
        form1 = QtGui.QFormLayout()
        form1.addRow("&Name:", self.__nameedit);
        form1.addRow("&Email:", self.__emailedit);
        form1.addRow("&Projects:", self.__customerlist);
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch()
        hbox1.addWidget(self.__testbutton)
        # Top level layout.
        toplayout = QtGui.QVBoxLayout()
        toplayout.addLayout(form1)
        toplayout.addLayout(hbox1)
        toplayout.addStretch()
        mainwidget.setLayout(toplayout)
        # Test data.
        self.__customerlist.addItems(QtCore.QStringList()
            << "First project."
            << "Second project.")
        # 
        self._writeToLog("The template tool was successfully created.")

    def __test(self):
        """ """
        self._writeToLog("Name: " + self.__nameedit.text())
