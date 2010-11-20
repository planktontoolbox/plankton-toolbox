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

class LogTool(tool_base.ToolBase):
    """
    Log window tool.
    """
    
    def __init__(self, name, parentwidget):
        """ """
        super(LogTool, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        mainwidget = QtGui.QWidget(self._parent)
        self.setWidget(mainwidget)
        # Active widgets and connections.
        self.__clearbutton = QtGui.QPushButton("Clear", mainwidget)
        self.__limitedit = QtGui.QLineEdit("1000", mainwidget)
        self.__limitedit.setMaximumWidth(60)        
        self.__logarea = QtGui.QListWidget(self)
        self.connect(self.__clearbutton, QtCore.SIGNAL("clicked()"), self.__clearLog)      
        # Layout widgets.
        limitlabel = QtGui.QLabel("Row limit: ", mainwidget)
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch()
        hbox1.addWidget(limitlabel)
        hbox1.addWidget(self.__limitedit)
        hbox1.addWidget(self.__clearbutton)
        # Top level layout.
        toplayout = QtGui.QVBoxLayout()
        toplayout.addLayout(hbox1)
        toplayout.addWidget(self.__logarea)
        mainwidget.setLayout(toplayout)
        
    def writeToLog(self, message):
        """ """
        self.__logarea.addItem(message)
        # Remove oldest lines if max exceeded.
        try:
            max = int(self.__limitedit.text()) 
            if max > 1:
                while self.__logarea.count() > max:
                    self.__logarea.takeItem(0)
        except:
            pass # Don't remove rows if max is not a valid integer.    
        

    def __clearLog(self):
        """ """
        self.__logarea.clear()

