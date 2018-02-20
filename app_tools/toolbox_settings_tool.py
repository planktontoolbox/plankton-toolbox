#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from PyQt5 import QtWidgets
from PyQt5 import QtCore

# class ToolboxSettingsTool(tool_base.ToolBase):
#     """
#     """
#     
#     def __init__(self, name, parentwidget):
#         """ """
#         # Initialize parent. Should be called after other 
#         # initialization since the base class calls _create_content().
#         super(ToolboxSettingsTool, self).__init__(name, parentwidget)
#         #
#         # Where is the tool allowed to dock in the main window.
#         self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
#         self.setBaseSize(600,600)
#         
#     def _create_content(self):
#         """ """
#         content = self._create_scrollable_content()
#         contentLayout = QtWidgets.QVBoxLayout()
#         content.setLayout(contentLayout)
#         contentLayout.addLayout(self._content_general())
#         contentLayout.addLayout(self._content_resources())
#         contentLayout.addLayout(self._content_buttons())
#         contentLayout.addStretch(5)
#         # Used when toolbox settings has changed.        
#         toolbox_settings.ToolboxSettings().settingsChanged.connect(self._update)
#         #
#         self._update()
# 
#     def _content_general(self):
#         """ """
#         # Active widgets and connections.
#         self._delimiter_edit = QtWidgets.QLineEdit('')
#         # Layout.
#         box = QtWidgets.QGroupBox('General', self)
#         layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(box)
#         layout2 = QtWidgets.QFormLayout()
#         box.setLayout(layout2)
#         layout2.addRow('Decimal delimiter:', self._delimiter_edit)
#         #
#         return layout
#     
#     def _content_resources(self):
#         """ """
#         # Active widgets and connections.
#         self._dyntaxafilepath_edit = QtWidgets.QLineEdit('')
#         self._pegfilepath_edit = QtWidgets.QLineEdit('')
#         self._iocfilepath_edit = QtWidgets.QLineEdit('')
#         self._loadresources_checkbox = QtWidgets.QCheckBox('Load resources at startup.')
# #        self._loadresources_checkbox.stateChanged(int)'), self._toogleLoadResources)                
#         # Layout.
#         box = QtWidgets.QGroupBox('Resources', self)
#         layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(box)
#         layout2 = QtWidgets.QFormLayout()
#         box.setLayout(layout2)
#         layout2.addRow('<b>Dyntaxa</b>', None)
#         layout2.addRow('Filepath (.json):', self._dyntaxafilepath_edit)
#         layout2.addRow('<b>PEG</b>', None)
#         layout2.addRow('Filepath (.json):', self._pegfilepath_edit)
#         layout2.addRow('<b>Harmful plankton</b>', None)
#         layout2.addRow('Filepath (.json):', self._iocfilepath_edit)
#         layout2.addRow(None, self._loadresources_checkbox)
#         #
#         return layout
#     
#     def _content_buttons(self):
#         """ """
#         # Active widgets and connections.
#         self._restoredefault_button = QtWidgets.QPushButton('Restore defaults')
#         self._restore_button = QtWidgets.QPushButton('Restore')
#         self._save_button = QtWidgets.QPushButton('Save')
#         self._restoredefault_button.clicked.connect(self._restore_default)                
#         self._restore_button.clicked.connect(self._cancel)                
#         self._save_button.clicked.connect(self._save)                
#         # Layout widgets.
#         layout = QtWidgets.QHBoxLayout()
#         layout.addStretch()
#         layout.addWidget(self._restoredefault_button)
#         layout.addWidget(self._restore_button)
#         layout.addWidget(self._save_button)
#         #
#         return layout
#     
# #    def _toogleLoadResources(self, checkStatus):
# #        """ """
# #        if checkStatus == QtCore.Qt.Checked:
# #            toolbox_settings.ToolboxSettings().set_value('Resources:Load at startup', True)
# #        else:
# #            toolbox_settings.ToolboxSettings().set_value('Resources:Load at startup', False)
#     
#     def _update(self):
#         """ """
#         self._delimiter_edit.setText(toolbox_settings.ToolboxSettings().get_value('General:Decimal delimiter'))
#         self._dyntaxafilepath_edit.setText(toolbox_settings.ToolboxSettings().get_value('Resources:Dyntaxa:Filepath'))
#         self._pegfilepath_edit.setText(toolbox_settings.ToolboxSettings().get_value('Resources:PEG:Filepath'))
#         self._iocfilepath_edit.setText(toolbox_settings.ToolboxSettings().get_value('Resources:Harmful plankton:Filepath'))
#         #
#         loadresources = toolbox_settings.ToolboxSettings().get_value('Resources:Load at startup')
#         if loadresources:
#             self._loadresources_checkbox.setCheckState(QtCore.Qt.Checked)
#         else:
#             self._loadresources_checkbox.setCheckState(QtCore.Qt.Unchecked)
#             
#     
#     def _restore_default(self):
#         """ """
#         toolbox_settings.ToolboxSettings().restore_default()
#         self._update()
#     
#     def _cancel(self):
#         """ """
#         self._update()
#     
#     def _save(self):
#         """ """
#         toolbox_settings.ToolboxSettings().set_value('General:Decimal delimiter', str(self._delimiter_edit.text()))
#         toolbox_settings.ToolboxSettings().set_value('Resources:Dyntaxa:Filepath', str(self._dyntaxafilepath_edit.text()))
#         toolbox_settings.ToolboxSettings().set_value('Resources:PEG:Filepath', str(self._pegfilepath_edit.text()))
#         toolbox_settings.ToolboxSettings().set_value('Resources:Harmful plankton:Filepath', str(self._iocfilepath_edit.text()))
#         if self._loadresources_checkbox.checkState() == QtCore.Qt.Checked:
#             toolbox_settings.ToolboxSettings().set_value('Resources:Load at startup', True)
#         else:
#             toolbox_settings.ToolboxSettings().set_value('Resources:Load at startup', False)
#         # Save by use of QSettings.
#         toolbox_settings.ToolboxSettings().save_settings(QtCore.QSettings())

