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
import plankton_toolbox.toolbox.toolbox_settings as toolbox_settings

class ToolboxSettingsTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(ToolboxSettingsTool, self).__init__(name, parentwidget)
        
    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self.__contentGeneral())
        contentLayout.addLayout(self.__contentResources())
        contentLayout.addLayout(self.__contentButtons())
        contentLayout.addStretch(5)
        # Used when toolbox settings has changed.        
        self.connect(toolbox_settings.ToolboxSettings(), QtCore.SIGNAL("settingsChanged"), self.__update)
        #
        self.__update()

    def __contentGeneral(self):
        """ """
        # Active widgets and connections.
        self.__delimiter_edit = QtGui.QLineEdit('')
        # Layout.
        box = QtGui.QGroupBox("General", self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(box)
        layout2 = QtGui.QFormLayout()
        box.setLayout(layout2)
        layout2.addRow("Decimal delimiter:", self.__delimiter_edit)
        #
        return layout
    
    def __contentResources(self):
        """ """
        # Active widgets and connections.
        self.__dyntaxafilepath_edit = QtGui.QLineEdit('')
        self.__pegfilepath_edit = QtGui.QLineEdit('')
        self.__iocfilepath_edit = QtGui.QLineEdit('')
        self.__loadresources_checkbox = QtGui.QCheckBox('Load resources at startup.')
#        self.connect(self.__loadresources_checkbox, QtCore.SIGNAL("stateChanged(int)"), self.__toogleLoadResources)                
        # Layout.
        box = QtGui.QGroupBox("Resources", self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(box)
        layout2 = QtGui.QFormLayout()
        box.setLayout(layout2)
        layout2.addRow("<b>Dyntaxa</b>", None)
        layout2.addRow("Filepath (.json):", self.__dyntaxafilepath_edit)
        layout2.addRow("<b>PEG</b>", None)
        layout2.addRow("Filepath (.json):", self.__pegfilepath_edit)
        layout2.addRow("<b>Harmful plankton</b>", None)
        layout2.addRow("Filepath (.json):", self.__iocfilepath_edit)
        layout2.addRow(None, self.__loadresources_checkbox)
        #
        return layout
    
    def __contentButtons(self):
        """ """
        # Active widgets and connections.
        self.__restoredefault_button = QtGui.QPushButton("Restore defaults")
        self.__restore_button = QtGui.QPushButton("Restore")
        self.__save_button = QtGui.QPushButton("Save")
        self.connect(self.__restoredefault_button, QtCore.SIGNAL("clicked()"), self.__restoreDefault)                
        self.connect(self.__restore_button, QtCore.SIGNAL("clicked()"), self.__cancel)                
        self.connect(self.__save_button, QtCore.SIGNAL("clicked()"), self.__save)                
        # Layout widgets.
        layout = QtGui.QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.__restoredefault_button)
        layout.addWidget(self.__restore_button)
        layout.addWidget(self.__save_button)
        #
        return layout
    
#    def __toogleLoadResources(self, checkStatus):
#        """ """
#        if checkStatus == QtCore.Qt.Checked:
#            toolbox_settings.ToolboxSettings().setValue('Resources:Load at startup', True)
#        else:
#            toolbox_settings.ToolboxSettings().setValue('Resources:Load at startup', False)
    
    def __update(self):
        """ """
        self.__delimiter_edit.setText(toolbox_settings.ToolboxSettings().getValue('General:Decimal delimiter'))
        self.__dyntaxafilepath_edit.setText(toolbox_settings.ToolboxSettings().getValue('Resources:Dyntaxa:Filepath'))
        self.__pegfilepath_edit.setText(toolbox_settings.ToolboxSettings().getValue('Resources:PEG:Filepath'))
        self.__iocfilepath_edit.setText(toolbox_settings.ToolboxSettings().getValue('Resources:Harmful plankton:Filepath'))
        #
        loadresources = toolbox_settings.ToolboxSettings().getValue('Resources:Load at startup')
        if loadresources:
            self.__loadresources_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.__loadresources_checkbox.setCheckState(QtCore.Qt.Unchecked)
            
    
    def __restoreDefault(self):
        """ """
        toolbox_settings.ToolboxSettings().restoreDefault()
        self.__update()
    
    def __cancel(self):
        """ """
        self.__update()
    
    def __save(self):
        """ """
        toolbox_settings.ToolboxSettings().setValue('General:Decimal delimiter', unicode(self.__delimiter_edit.text()))
        toolbox_settings.ToolboxSettings().setValue('Resources:Dyntaxa:Filepath', unicode(self.__dyntaxafilepath_edit.text()))
        toolbox_settings.ToolboxSettings().setValue('Resources:PEG:Filepath', unicode(self.__pegfilepath_edit.text()))
        toolbox_settings.ToolboxSettings().setValue('Resources:Harmful plankton:Filepath', unicode(self.__iocfilepath_edit.text()))
        if self.__loadresources_checkbox.checkState() == QtCore.Qt.Checked:
            toolbox_settings.ToolboxSettings().setValue('Resources:Load at startup', True)
        else:
            toolbox_settings.ToolboxSettings().setValue('Resources:Load at startup', False)
        # Save by use of QSettings.
        toolbox_settings.ToolboxSettings().saveSettings(QtCore.QSettings())

