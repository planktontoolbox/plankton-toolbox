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
from abc import abstractmethod

class ToolBase(QtGui.QDockWidget):
    """
    Abstract base class for tools in Plankton Toolbox.
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent.
        super(ToolBase, self).__init__(name, parentwidget)
        self._parent = parentwidget
        #
        self._writeToStatusBar("Loading " + name + "...")
        #        
        self.setObjectName(name)
        #
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | 
                             QtCore.Qt.BottomDockWidgetArea)
        self.setBaseSize(600,600)
        # Add specific content. Abstract, implemented by subclasses.
        self._createContent() 
        # Default position to the right. Hide as default.
        self._parent.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
        self.hide()
        #  Toggles show/hide from the Tools menu in the main window.
        self._parent.toolsmenu.addAction(self.toggleViewAction())
        #
        self._writeToStatusBar("")

    @abstractmethod
    def _createContent(self):
        """ 
        Used to create the content of the tool window.
        Note: Abstract. Should be implemented by subclasses. 
        """
        pass

    def _createScrollableContent(self):
        """ 
        Creates the scrollable part of the tool content. 
        Used by subclasses, if needed.
        """
        content = QtGui.QWidget()
        widget = QtGui.QWidget()
        self.setWidget(widget)        
        # Add scroll.
        mainscroll = QtGui.QScrollArea()
        mainscroll.setFrameShape(QtGui.QFrame.NoFrame)
#        mainscroll.setBackgroundRole(QtGui.QPalette.Light)     
        mainscroll.setBackgroundRole(QtGui.QPalette.Midlight)     
#        mainscroll.setBackgroundRole(QtGui.QPalette.Dark)     
#        mainscroll.setBackgroundRole(QtGui.QPalette.Mid)     
#        mainscroll.setBackgroundRole(QtGui.QPalette.Shadow)     
        mainscroll.setWidget(content)
        mainscroll.setWidgetResizable(True)
        mainlayout = QtGui.QVBoxLayout()
        mainlayout.setMargin(0)
        mainlayout.setSpacing(0)
        mainlayout.addWidget(mainscroll)
        widget.setLayout(mainlayout)
        return content 

    def _writeToStatusBar(self, message):
        """ Used to write short messages to the main window status bar. """
        self._parent.statusBar().showMessage(message)

    def _writeToLog(self, message):
        """ 
        Used to write log messages. Depending on the main window
        settings they will appear on different locations, for example
        in log file and/or in the log tool window. 
        """
        self._parent.writeToLog(message)
