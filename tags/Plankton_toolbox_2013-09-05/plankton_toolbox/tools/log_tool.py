#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2013 SMHI, Swedish Meteorological and Hydrological Institute 
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
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
#        self.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.setBaseSize(600,600)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._contentButtons())
        contentLayout.addLayout(self._contentLogArea())

    def _contentButtons(self):
        """ """
        # Active widgets and connections.
        self._limit_edit = QtGui.QLineEdit("1000")
        self._limit_edit.setMaximumWidth(60)        
        self._clear_button = QtGui.QPushButton("Clear log")
        self.connect(self._clear_button, QtCore.SIGNAL("clicked()"), self._clearLog)      
#        self._openlogfile_button = QtGui.QPushButton("Open log file")
#        self.connect(self._openlogfile_button, QtCore.SIGNAL("clicked()"), self._openLogFile)      
        # Layout.
        layout = QtGui.QHBoxLayout()
        limit_label = QtGui.QLabel("Row limit: ")
        layout.addStretch(5)
        layout.addWidget(limit_label)
        layout.addWidget(self._limit_edit)
        layout.addWidget(self._clear_button)
#        layout.addWidget(self._openlogfile_button)
        #
        return layout

    def _contentLogArea(self):
        """ """
        # Active widgets and connections.
        self._logarea = QtGui.QListWidget(self)
##        self._logarea = QtGui.QTextEdit(self)
        self._logarea.setMinimumHeight(20)
        self._logarea.setMinimumWidth(100)
        # Layout.
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self._logarea)
        #
        return layout

    def writeToLog(self, message):
        """ """
        self._logarea.addItem(message)
##        self._logarea.append(message)
        self._logarea.scrollToBottom()
##        self._logarea.ensureCursorVisible()
        # Remove oldest lines if max exceeded.
        try:
            maxrows = int(unicode(self._limit_edit.text())) 
            if maxrows > 0:
                while self._logarea.count() > maxrows:
                    self._logarea.takeItem(0)
        except:
            pass # Don't remove rows if max is not a valid integer.    
        
    def _clearLog(self):
        """ """
        self._logarea.clear()

#    def _openLogFile(self):
#        """ """
#        import sys
#        import subprocess
#        if sys.platform.startswith('win'):           
#            subprocess.Popen('plankton_toolbox_log.txt')
#            subprocess.call(u'plankton_toolbox_log.txt')

