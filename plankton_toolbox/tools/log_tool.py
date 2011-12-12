#!/usr/bin/env python
# -*- coding:utf-8 -*-
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

class LogTool(tool_base.ToolBase):
    """
    Log window tool.
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(LogTool, self).__init__(name, parentwidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
#        self.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.setBaseSize(600,600)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self.__contentButtons())
        contentLayout.addLayout(self.__contentLogArea())

    def __contentButtons(self):
        """ """
        # Active widgets and connections.
        self.__clearbutton = QtGui.QPushButton("Clear log")
        self.__limitedit = QtGui.QLineEdit("1000")
        self.__limitedit.setMaximumWidth(60)        
        self.connect(self.__clearbutton, QtCore.SIGNAL("clicked()"), self.__clearLog)      
        # Layout.
        layout = QtGui.QHBoxLayout()
        limitlabel = QtGui.QLabel("Row limit: ")
        layout.addStretch(5)
        layout.addWidget(limitlabel)
        layout.addWidget(self.__limitedit)
        layout.addWidget(self.__clearbutton)
        #
        return layout

    def __contentLogArea(self):
        """ """
        # Active widgets and connections.
        self.__logarea = QtGui.QListWidget(self)
        self.__logarea.setMinimumHeight(20)
        self.__logarea.setMinimumWidth(100)
        self.connect(self.__clearbutton, QtCore.SIGNAL("clicked()"), self.__clearLog)      
        # Layout.
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.__logarea)
        #
        return layout

    def writeToLog(self, message):
        """ """
        self.__logarea.addItem(message)
        self.__logarea.scrollToBottom()
        # Remove oldest lines if max exceeded.
        try:
            max = int(unicode(self.__limitedit.text())) 
            if max > 1:
                while self.__logarea.count() > max:
                    self.__logarea.takeItem(0)
        except:
            pass # Don't remove rows if max is not a valid integer.    
        

    def __clearLog(self):
        """ """
        self.__logarea.clear()

