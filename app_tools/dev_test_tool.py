#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

# from PyQt5 import QtWidgets
# from PyQt5 import QtCore
# import plankton_toolbox.tools.tool_base as tool_base
# 
# import toolbox_utils
# import plankton_core
# 
# import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
# #import plankton_toolbox.toolbox.toolbox_main_window as toolbox_main_window
# 
# 
# class DevTestTool(tool_base.ToolBase):
#     """
#     For development and test only. Deactivate in public releases.
#     """
#     
#     def __init__(self, name, parentwidget):
#         """ """
#         # Settings for the DevTestTool. NOTE: Max 4 is supported.
#         self._dev_settings = [
#             {   'button_text': 'Phytoplankton',
#                 'import_parser_path': 'plankton_toolbox_data/parsers/',
#                 'import_parser': 'sharkweb_phytoplankton_parser.xlsx',
#                 'import_column': 'Sharkweb english',
#                 'export_column': 'Export english',
#                 'data_file_path': '',
#                 'data_file_name': 'demodata_Phytoplankton.txt',
#                 'data_file_encoding': 'windows-1252',
# #                 'show_activity_after': 'Import datasets'
#                 'show_activity_after': 'Dataset analysis'
# 
#             },
#             {   'button_text': 'Zooplankton',
#                 'import_parser_path': 'plankton_toolbox_data/parsers/',
#                 'import_parser': 'sharkweb_zooplankton_parser.xlsx',
#                 'import_column': 'SHARKweb english',
#                 'export_column': 'Export english',
#                 'data_file_path': '',
#                 'data_file_name': 'demodata_Zooplankton.txt',
#                 'data_file_encoding': 'windows-1252',
# #                 'show_activity_after': 'Import datasets'
#                 'show_activity_after': 'Dataset screening'
# 
#             },
# #             {   'button_text': 'SHARKweb_ZP_2010-2012_en_SHORT',
# #                 'import_parser_path': 'plankton_toolbox_data/parsers/',
# #                 'import_parser': 'SHARKweb_Zooplankton_parser.xlsx',
# #                 'import_column': 'SHARKweb english',
# #                 'export_column': 'Export english',
# #                 'data_file_path': '',
# #                 'data_file_name': 'SHARKweb_ZP_2010-2012_en_SHORT.txt',
# #                 'data_file_encoding': 'windows-1252',
# # #                 'show_activity_after': 'Import datasets'
# #                 'show_activity_after': 'Analyse data'
# # 
# #             },
# #             {   'button_text': 'SHARKweb_ZP_2010-2012_sv_SHORT',
# #                 'import_parser_path': 'plankton_toolbox_data/parsers/',
# #                 'import_parser': 'SHARKweb_Zooplankton_parser.xlsx',
# #                 'import_column': 'SHARKweb swedish',
# #                 'export_column': 'Export swedish',
# #                 'data_file_path': '',
# #                 'data_file_name': 'SHARKweb_ZP_2010-2012_sv_SHORT.txt',
# #                 'data_file_encoding': 'windows-1252',
# # #                 'show_activity_after': 'Import datasets'
# #                 'show_activity_after': 'Analyse data'
# # 
# #             },
# #             {   'button_text': 'PTBX_testdata',
# #                 'import_parser_path': 'plankton_toolbox_data/parsers/',
# #                 'import_parser': 'PTBX_testdata_parser.xlsx',
# #                 'import_column': 'Import format',
# #                 'export_column': 'Export format',
# #                 'data_file_path': '',
# #                 'data_file_name': 'PTBX_testdata.txt',
# #                 'data_file_encoding': 'windows-1252',
# # #                 'show_activity_after': 'Import datasets'
# #                 'show_activity_after': 'Screening'
# # 
# #             },
#         ]
# 
#         # Initialize parent. Should be called after other 
#         # initialization since the base class calls _create_content().
#         super(DevTestTool, self).__init__(name, parentwidget)
#         #
#         # Where is the tool allowed to dock in the main window.
#         self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
#         self.setBaseSize(600,600)
# 
#     def _create_content(self):
#         """ """
#         content = self._create_scrollable_content()
#         contentLayout = QtWidgets.QVBoxLayout()
#         content.setLayout(contentLayout)
#         contentLayout.addLayout(self._content_buttons())
#         contentLayout.addStretch(5)
# 
#     def _content_buttons(self):
#         """ """
#         # Active widgets and connections.
#         layout = QtWidgets.QVBoxLayout()
#         for index, settings_item in enumerate(self._dev_settings):
#             self._testbutton = QtWidgets.QPushButton(settings_item['button_text'])
#             if index == 0:
#                 self._testbutton.clicked.connect(self._test_0)   
#             if index == 1:
#                 self._testbutton.clicked.connect(self._test_1)   
#             if index == 2:
#                 self._testbutton.clicked.connect(self._test_2)   
#             if index == 3:
#                 self._testbutton.clicked.connect(self._test_3)   
#             layout.addWidget(self._testbutton)
#         #
#         layout.addStretch(5)
#         #
#         return layout
# 
#     def _test_0(self):
#         """ """
#         self._test(self._dev_settings[0])
#         
#     def _test_1(self):
#         """ """
#         self._test(self._dev_settings[1])
#         
#     def _test_2(self):
#         """ """
#         self._test(self._dev_settings[2])
#         
#     def _test_3(self):
#         """ """
#         self._test(self._dev_settings[3])
#         
#     def _test(self, settings):
#         """ """
#         try:
#             toolbox_utils.Logging().log('Dev. tool: ' + settings['button_text'])
#             #
#             import_parser_path = settings['import_parser_path']
#             import_parser = settings['import_parser']
#             import_column = settings['import_column']
#             export_column = settings['export_column']
#             #
#             self._parent.show_activity_by_name(settings['show_activity_after'])
#             #
#             # Set up for import file parsing.
#             impMgr = plankton_core.ImportManager(import_parser_path + import_parser,
#                                              import_column,
#                                              export_column)
#             # Import and parse file.
#             data_file_path = settings['data_file_path']
#             data_file_name = settings['data_file_name']
#             data_file_encoding = settings['data_file_encoding']
#             #
#             dataset = impMgr.import_text_file(data_file_path + data_file_name,
#                                             data_file_encoding)
#             # Add metadata related to imported file.
#             dataset.add_metadata('parser', import_parser)
#             dataset.add_metadata('file_name', data_file_name)
#             dataset.add_metadata('file_path', data_file_path)
#             dataset.add_metadata('import_column', import_column)
#             dataset.add_metadata('export_column', export_column)
#             app_framework.ToolboxDatasets().add_dataset(dataset)
#             
#             self._parent.show_activity_by_name(settings['show_activity_after'])
#         except Exception as e:
#             toolbox_utils.Logging().warning('Failed to run script: %s' % (e))
#             raise
#         