#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

# from PyQt6 import QtWidgets
# from PyQt6 import QtCore
# import plankton_toolbox.tools.tool_base as tool_base
#
# class MetadataEditorTool(tool_base.ToolBase):
#     """
#     """
#
#     def __init__(self, name, parentwidget):
#         """ """
#         # Initialize parent. Should be called after other
#         # initialization since the base class calls _create_content().
#         super(MetadataEditorTool, self).__init__(name, parentwidget)
#         #
#         # Where is the tool allowed to dock in the main window.
#         self.setAllowedAreas(QtCore.Qt.DockWidgetArea.RightDockWidgetArea)
#         self.setBaseSize(600,600)
#
#     def _create_content(self):
#         """ """
#         content = self._create_scrollable_content()
#         contentLayout = QtWidgets.QVBoxLayout()
#         content.setLayout(contentLayout)
#         contentLayout.addLayout(self._content_test_1())
#         contentLayout.addLayout(self._content_test_2())
#         contentLayout.addStretch(5)
#
#     def _content_test_1(self):
#         """ """
#         # Active widgets and connections.
#         self._nameedit = QtWidgets.QLineEdit('<Name>')
#         self._emailedit = QtWidgets.QLineEdit('<Email>')
#         self._customerlist = QtWidgets.QListWidget()
#         # Layout widgets.
#         layout = QtWidgets.QFormLayout()
#         layout.addRow('&Name:', self._nameedit)
#         layout.addRow('&Email:', self._emailedit)
#         layout.addRow('&Projects:', self._customerlist)
#         #
#         return layout
#
#     def _content_test_2(self):
#         """ """
#         # Active widgets and connections.
#         self._testbutton = QtWidgets.QPushButton('Write name to log')
#         self._testbutton.clicked.connect(self._test)
#         # Active widgets and connections.
#         layout = QtWidgets.QHBoxLayout()
#         layout.addStretch(5)
#         layout.addWidget(self._testbutton)
#         #
#         return layout
#
#     def _test(self):
#         """ """
#         self._write_to_log('Name: ' + str(self._nameedit.text()))
