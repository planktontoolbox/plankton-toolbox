#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from PyQt6 import QtWidgets
from PyQt6 import QtCore
import app_framework

class LogTool(app_framework.ToolBase):
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
        self.setAllowedAreas(QtCore.Qt.DockWidgetArea.RightDockWidgetArea | 
                             QtCore.Qt.DockWidgetArea.BottomDockWidgetArea)
        self.setBaseSize(600,600)        
        # Default position. Hide as default.
        self._parent.addDockWidget(QtCore.Qt.DockWidgetArea.BottomDockWidgetArea, self)
        self.hide()

    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtWidgets.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._content_buttons())
        contentLayout.addLayout(self._content_log_area())

    def _content_buttons(self):
        """ """
        # Active widgets and connections.
        self._limit_edit = QtWidgets.QLineEdit('1000')
        self._limit_edit.setMaximumWidth(60)        
        self._clear_button = QtWidgets.QPushButton('Clear log')
        self._clear_button.clicked.connect(self._clear_log)              
#        self._openlogfile_button = QtWidgets.QPushButton('Open log file')
#        self._openlogfile_button.clicked.connect(self._openLogFile)      
        # Layout.
        layout = QtWidgets.QHBoxLayout()
        limit_label = QtWidgets.QLabel('Number of displayed rows: ')
        layout.addWidget(limit_label)
        layout.addWidget(self._limit_edit)
        layout.addWidget(self._clear_button)
#        layout.addWidget(self._openlogfile_button)
        layout.addStretch(10)
        #
        return layout

    def _content_log_area(self):
        """ """
        # Active widgets and connections.
        self._logarea = QtWidgets.QListWidget(self)
##        self._logarea = QtWidgets.QTextEdit(self)
        self._logarea.setMinimumHeight(20)
        self._logarea.setMinimumWidth(100)
        # Layout.
        layout = QtWidgets.QHBoxLayout()
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
            maxrows = int(str(self._limit_edit.text())) 
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

