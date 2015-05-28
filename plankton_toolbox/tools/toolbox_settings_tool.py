#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

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
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setBaseSize(600,600)
        
    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._contentGeneral())
        contentLayout.addLayout(self._contentResources())
        contentLayout.addLayout(self._contentButtons())
        contentLayout.addStretch(5)
        # Used when toolbox settings has changed.        
        self.connect(toolbox_settings.ToolboxSettings(), QtCore.SIGNAL("settingsChanged"), self._update)
        #
        self._update()

    def _contentGeneral(self):
        """ """
        # Active widgets and connections.
        self._delimiter_edit = QtGui.QLineEdit('')
        # Layout.
        box = QtGui.QGroupBox("General", self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(box)
        layout2 = QtGui.QFormLayout()
        box.setLayout(layout2)
        layout2.addRow("Decimal delimiter:", self._delimiter_edit)
        #
        return layout
    
    def _contentResources(self):
        """ """
        # Active widgets and connections.
        self._dyntaxafilepath_edit = QtGui.QLineEdit('')
        self._pegfilepath_edit = QtGui.QLineEdit('')
        self._iocfilepath_edit = QtGui.QLineEdit('')
        self._loadresources_checkbox = QtGui.QCheckBox('Load resources at startup.')
#        self.connect(self._loadresources_checkbox, QtCore.SIGNAL("stateChanged(int)"), self._toogleLoadResources)                
        # Layout.
        box = QtGui.QGroupBox("Resources", self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(box)
        layout2 = QtGui.QFormLayout()
        box.setLayout(layout2)
        layout2.addRow("<b>Dyntaxa</b>", None)
        layout2.addRow("Filepath (.json):", self._dyntaxafilepath_edit)
        layout2.addRow("<b>PEG</b>", None)
        layout2.addRow("Filepath (.json):", self._pegfilepath_edit)
        layout2.addRow("<b>Harmful plankton</b>", None)
        layout2.addRow("Filepath (.json):", self._iocfilepath_edit)
        layout2.addRow(None, self._loadresources_checkbox)
        #
        return layout
    
    def _contentButtons(self):
        """ """
        # Active widgets and connections.
        self._restoredefault_button = QtGui.QPushButton("Restore defaults")
        self._restore_button = QtGui.QPushButton("Restore")
        self._save_button = QtGui.QPushButton("Save")
        self.connect(self._restoredefault_button, QtCore.SIGNAL("clicked()"), self._restoreDefault)                
        self.connect(self._restore_button, QtCore.SIGNAL("clicked()"), self._cancel)                
        self.connect(self._save_button, QtCore.SIGNAL("clicked()"), self._save)                
        # Layout widgets.
        layout = QtGui.QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self._restoredefault_button)
        layout.addWidget(self._restore_button)
        layout.addWidget(self._save_button)
        #
        return layout
    
#    def _toogleLoadResources(self, checkStatus):
#        """ """
#        if checkStatus == QtCore.Qt.Checked:
#            toolbox_settings.ToolboxSettings().setValue('Resources:Load at startup', True)
#        else:
#            toolbox_settings.ToolboxSettings().setValue('Resources:Load at startup', False)
    
    def _update(self):
        """ """
        self._delimiter_edit.setText(toolbox_settings.ToolboxSettings().getValue('General:Decimal delimiter'))
        self._dyntaxafilepath_edit.setText(toolbox_settings.ToolboxSettings().getValue('Resources:Dyntaxa:Filepath'))
        self._pegfilepath_edit.setText(toolbox_settings.ToolboxSettings().getValue('Resources:PEG:Filepath'))
        self._iocfilepath_edit.setText(toolbox_settings.ToolboxSettings().getValue('Resources:Harmful plankton:Filepath'))
        #
        loadresources = toolbox_settings.ToolboxSettings().getValue('Resources:Load at startup')
        if loadresources:
            self._loadresources_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self._loadresources_checkbox.setCheckState(QtCore.Qt.Unchecked)
            
    
    def _restoreDefault(self):
        """ """
        toolbox_settings.ToolboxSettings().restoreDefault()
        self._update()
    
    def _cancel(self):
        """ """
        self._update()
    
    def _save(self):
        """ """
        toolbox_settings.ToolboxSettings().setValue('General:Decimal delimiter', unicode(self._delimiter_edit.text()))
        toolbox_settings.ToolboxSettings().setValue('Resources:Dyntaxa:Filepath', unicode(self._dyntaxafilepath_edit.text()))
        toolbox_settings.ToolboxSettings().setValue('Resources:PEG:Filepath', unicode(self._pegfilepath_edit.text()))
        toolbox_settings.ToolboxSettings().setValue('Resources:Harmful plankton:Filepath', unicode(self._iocfilepath_edit.text()))
        if self._loadresources_checkbox.checkState() == QtCore.Qt.Checked:
            toolbox_settings.ToolboxSettings().setValue('Resources:Load at startup', True)
        else:
            toolbox_settings.ToolboxSettings().setValue('Resources:Load at startup', False)
        # Save by use of QSettings.
        toolbox_settings.ToolboxSettings().saveSettings(QtCore.QSettings())

