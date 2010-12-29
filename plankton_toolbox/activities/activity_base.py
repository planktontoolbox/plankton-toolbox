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
from abc import abstractmethod

class ActivityBase(QtGui.QWidget):
    """
    Abstract base class for activities in Plankton toolbox.
    """
    
    def __init__(self, name, parentwidget):
        """ """
        super(ActivityBase, self).__init__(parentwidget)
        self._parent = parentwidget
        
        self._writeToStatusBar("Loading " + name + "...")
#        self._writeToLog("Loading " + name + "...")
        
        self.setObjectName(name)

        self._createContent() # Adds specific content. Abstract.
        
        self._writeToStatusBar("")
#        self._writeToLog(name + " loaded.")

    @abstractmethod
    def _createContent(self):
        """ 
        Used to create the content of the activity window.
        Note: Abstract. Should be implemented by subclasses. 
        """
        pass

    def showInMainWindow(self):
        """ """
        self._parent.showActivity(self)
    
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