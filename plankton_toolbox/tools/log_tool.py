#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

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
        # initialization since the base class calls _create_content().
        super(LogTool, self).__init__(name, parentwidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
#        self.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.setBaseSize(600,600)

    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._content_buttons())
        contentLayout.addLayout(self._content_log_area())

    def _content_buttons(self):
        """ """
        # Active widgets and connections.
        self._limit_edit = QtGui.QLineEdit('1000')
        self._limit_edit.setMaximumWidth(60)        
        self._clear_button = QtGui.QPushButton('Clear log')
        ###self.connect(self._clear_button, QtCore.SIGNAL('clicked()'), self._clear_log) 
        self._clear_button.clicked.connect(self._clear_log) 
             
#        self._openlogfile_button = QtGui.QPushButton('Open log file')
#        self.connect(self._openlogfile_button, QtCore.SIGNAL('clicked()'), self._openLogFile)      
        # Layout.
        layout = QtGui.QHBoxLayout()
        limit_label = QtGui.QLabel('View last number of rows: ')
        layout.addStretch(5)
        layout.addWidget(limit_label)
        layout.addWidget(self._limit_edit)
        layout.addWidget(self._clear_button)
#        layout.addWidget(self._openlogfile_button)
        #
        return layout

    def _content_log_area(self):
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

    def write_to_log(self, message):
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
        
    def _clear_log(self):
        """ """
        self._logarea.clear()

#    def _openLogFile(self):
#        """ """
#        import sys
#        import subprocess
#        if sys.platform.startswith('win'):           
#            subprocess.Popen('plankton_toolbox_log.txt')
#            subprocess.call('plankton_toolbox_log.txt')

