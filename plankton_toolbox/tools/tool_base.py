#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

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
        self._writeToStatusBar('Loading ' + name + '...')
        #        
        self.setObjectName(name)
        #
#        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | 
#                             QtCore.Qt.BottomDockWidgetArea)
#        self.setBaseSize(600,600)
        # Add specific content. Abstract, implemented by subclasses.
        self._createContent() 
        # Default position to the right. Hide as default.
        self._parent.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
        self.hide()
        #  Toggles show/hide from the Tools menu in the main window.
        self._parent.toolsmenu.addAction(self.toggleViewAction())
        #
        self._writeToStatusBar('')

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
        ### mainscroll.setFrameShape(QtGui.QFrame.NoFrame)
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
