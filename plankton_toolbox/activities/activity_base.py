#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import PyQt4.QtGui as QtGui
#import PyQt4.QtCore as QtCore
from abc import abstractmethod

class ActivityBase(QtGui.QWidget):
    """
    Abstract base class for activities in Plankton Toolbox.
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent.
        super(ActivityBase, self).__init__(parentwidget)
        self._parent = parentwidget
        self._mainmenubutton = None
        #
        self._writeToStatusBar('Loading ' + name + '...')
        #
        self.setObjectName(name)
        # Add specific content. Abstract, implemented by subclasses.
        self._createContent()
        #
        self._writeToStatusBar('')

    def setMainMenuButton(self, button):
        """ """
        self._mainmenubutton = button
    
    def getMainMenuButton(self):
        """ """
        return self._mainmenubutton
    
    def showInMainWindow(self):
        """ """
        self._parent.showActivity(self)
    
    @abstractmethod
    def _createContent(self):
        """ 
        Used to create the content of the activity window.
        Note: Abstract. Should be implemented by subclasses.
        """
        pass

    def _createScrollableContent(self):
        """ 
        Creates the scrollable part of the activity content.
        Used by subclasses, if needed.
        """
        content = QtGui.QWidget()
        # Add scroll.
        mainscroll = QtGui.QScrollArea()
        ### mainscroll.setFrameShape(QtGui.QFrame.NoFrame)
        mainscroll.setWidget(content)
        mainscroll.setWidgetResizable(True)
        mainlayout = QtGui.QVBoxLayout()
        mainlayout.setMargin(0)
        mainlayout.setSpacing(0)
        mainlayout.addWidget(mainscroll)
        self.setLayout(mainlayout)
        return content 

    def _writeToStatusBar(self, message):
        """ Used to write short messages to the main window status bar. """
        self._parent.statusBar().showMessage(message)

    def _writeToLog(self, message):
        """ 
        Used to write log messages. Depending on the main window
        settings they will appear on different locations, for example
        in log file and/or in the Log tool window. 
        """
        self._parent.writeToLog(message)
