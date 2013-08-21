#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2012 SMHI, Swedish Meteorological and Hydrological Institute 
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
import envmonlib

import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
#import plankton_toolbox.toolbox.toolbox_main_window as toolbox_main_window


class DevTestTool(tool_base.ToolBase):
    """
    For development and test only. Deactivate in public releases.
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(DevTestTool, self).__init__(name, parentwidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setBaseSize(600,600)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._contentButtons())
        contentLayout.addStretch(5)

    def _contentButtons(self):
        """ """
        # Active widgets and connections.
        self._testbutton_1 = QtGui.QPushButton("Select TEST_Sharkweb_PP_en.txt")
        self.connect(self._testbutton_1, QtCore.SIGNAL("clicked()"), self._test_1)                
        self._testbutton_2 = QtGui.QPushButton("Select TEST_Sharkweb_PP_sv.txt")
        self.connect(self._testbutton_2, QtCore.SIGNAL("clicked()"), self._test_2)                
        self._testbutton_3 = QtGui.QPushButton("Select TEST_Sharkweb_ZP_en.txt")
        self.connect(self._testbutton_3, QtCore.SIGNAL("clicked()"), self._test_3)                
        self._testbutton_4 = QtGui.QPushButton("Select TEST_Sharkweb_ZP_sv.txt")
        self.connect(self._testbutton_4, QtCore.SIGNAL("clicked()"), self._test_4)                
#         self._testbutton_5 = QtGui.QPushButton("Test 5")
#         self.connect(self._testbutton_5, QtCore.SIGNAL("clicked()"), self._test_5)                
        # Layout.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._testbutton_1)
        layout.addWidget(self._testbutton_2)
        layout.addWidget(self._testbutton_3)
        layout.addWidget(self._testbutton_4)
#         layout.addWidget(self._testbutton_5)
        layout.addStretch(5)
        #
        return layout

    def _test_1(self):
        """ """
        try:
            envmonlib.Logging().log("Select TEST_Sharkweb_PP_en.txt")
            
    #         import_parser_path = u'C:/Users/arnold/Desktop/python/w_plankton_toolbox/p_plankton_toolbox/src/toolbox_data/parsers/'
            import_parser_path = u'toolbox_data/parsers/'
            import_parser = u'sharkweb_phytoplankton_parser.xlsx'
            import_column = u'Sharkweb english'
            export_column = u'Export english'
    #         data_file_path = u'C:/Users/arnold/Desktop/python/w_plankton_toolbox/p_plankton_toolbox/src/'
            data_file_path = u''
            data_file_name = u'TEST_Sharkweb_PP_en.txt'
            data_file_encoding = 'windows-1252'
            
            self._parent.showActivityByName(u'Load datasets')
            
            # Set up for import file parsing.
            impMgr = envmonlib.ImportManager(import_parser_path + import_parser,
                                             import_column,
                                             export_column)
            # Import and parse file.
            dataset = impMgr.importTextFile(data_file_path + data_file_name,
                                            data_file_encoding)
            # Add metadata related to imported file.
            dataset.addMetadata(u'parser', import_parser)
            dataset.addMetadata(u'file_name', data_file_name)
            dataset.addMetadata(u'file_path', data_file_path)
            dataset.addMetadata(u'import_column', import_column)
            dataset.addMetadata(u'export_column', export_column)
            toolbox_datasets.ToolboxDatasets().addDataset(dataset)
            
            self._parent.showActivityByName(u'Analyse datasets')
        except Exception as e:
            envmonlib.Logging().warning(u"Failed to run script: %s" % (e.args[0]))
            raise
        
    def _test_2(self):
        """ """
        try:
            envmonlib.Logging().log("Select TEST_Sharkweb_PP_sv.txt")
            
    #         import_parser_path = u'C:/Users/arnold/Desktop/python/w_plankton_toolbox/p_plankton_toolbox/src/toolbox_data/parsers/'
            import_parser_path = u'toolbox_data/parsers/'
            import_parser = u'sharkweb_phytoplankton_parser.xlsx'
            import_column = u'Sharkweb swedish'
            export_column = u'Export swedish'
    #         data_file_path = u'C:/Users/arnold/Desktop/python/w_plankton_toolbox/p_plankton_toolbox/src/'
            data_file_path = u''
            data_file_name = u'TEST_Sharkweb_PP_sv.txt'
            data_file_encoding = 'windows-1252'
            
            self._parent.showActivityByName(u'Load datasets')
            
            # Set up for import file parsing.
            impMgr = envmonlib.ImportManager(import_parser_path + import_parser,
                                             import_column,
                                             export_column)
            # Import and parse file.
            dataset = impMgr.importTextFile(data_file_path + data_file_name,
                                            data_file_encoding)
            # Add metadata related to imported file.
            dataset.addMetadata(u'parser', import_parser)
            dataset.addMetadata(u'file_name', data_file_name)
            dataset.addMetadata(u'file_path', data_file_path)
            dataset.addMetadata(u'import_column', import_column)
            dataset.addMetadata(u'export_column', export_column)
            toolbox_datasets.ToolboxDatasets().addDataset(dataset)
            
            self._parent.showActivityByName(u'Analyse datasets')
        except Exception as e:
            envmonlib.Logging().warning(u"Failed to run script: %s" % (e.args[0]))
            raise

    def _test_3(self):
        """ """
        try:
            envmonlib.Logging().log("Select TEST_Sharkweb_ZP_en.txt")
            
    #         import_parser_path = u'C:/Users/arnold/Desktop/python/w_plankton_toolbox/p_plankton_toolbox/src/toolbox_data/parsers/'
            import_parser_path = u'toolbox_data/parsers/'
            import_parser = u'sharkweb_zooplankton_parser.xlsx'
            import_column = u'Sharkweb english'
            export_column = u'Export english'
    #         data_file_path = u'C:/Users/arnold/Desktop/python/w_plankton_toolbox/p_plankton_toolbox/src/'
            data_file_path = u''
            data_file_name = u'TEST_Sharkweb_ZP_en.txt'
            data_file_encoding = 'windows-1252'
            
            self._parent.showActivityByName(u'Load datasets')
            
            # Set up for import file parsing.
            impMgr = envmonlib.ImportManager(import_parser_path + import_parser,
                                             import_column,
                                             export_column)
            # Import and parse file.
            dataset = impMgr.importTextFile(data_file_path + data_file_name,
                                            data_file_encoding)
            # Add metadata related to imported file.
            dataset.addMetadata(u'parser', import_parser)
            dataset.addMetadata(u'file_name', data_file_name)
            dataset.addMetadata(u'file_path', data_file_path)
            dataset.addMetadata(u'import_column', import_column)
            dataset.addMetadata(u'export_column', export_column)
            toolbox_datasets.ToolboxDatasets().addDataset(dataset)
            
            self._parent.showActivityByName(u'Analyse datasets')
        except Exception as e:
            envmonlib.Logging().warning(u"Failed to run script: %s" % (e.args[0]))
            raise

    def _test_4(self):
        """ """
        try:
            envmonlib.Logging().log("Select TEST_Sharkweb_ZP_sv.txt")
            
    #         import_parser_path = u'C:/Users/arnold/Desktop/python/w_plankton_toolbox/p_plankton_toolbox/src/toolbox_data/parsers/'
            import_parser_path = u'toolbox_data/parsers/'
            import_parser = u'sharkweb_zooplankton_parser.xlsx'
            import_column = u'Sharkweb swedish'
            export_column = u'Export swedish'
    #         data_file_path = u'C:/Users/arnold/Desktop/python/w_plankton_toolbox/p_plankton_toolbox/src/'
            data_file_path = u''
            data_file_name = u'TEST_Sharkweb_ZP_sv.txt'
            data_file_encoding = 'windows-1252'
            
            self._parent.showActivityByName(u'Load datasets')
            
            # Set up for import file parsing.
            impMgr = envmonlib.ImportManager(import_parser_path + import_parser,
                                             import_column,
                                             export_column)
            # Import and parse file.
            dataset = impMgr.importTextFile(data_file_path + data_file_name,
                                            data_file_encoding)
            # Add metadata related to imported file.
            dataset.addMetadata(u'parser', import_parser)
            dataset.addMetadata(u'file_name', data_file_name)
            dataset.addMetadata(u'file_path', data_file_path)
            dataset.addMetadata(u'import_column', import_column)
            dataset.addMetadata(u'export_column', export_column)
            toolbox_datasets.ToolboxDatasets().addDataset(dataset)
            
            self._parent.showActivityByName(u'Analyse datasets')
        except Exception as e:
            envmonlib.Logging().warning(u"Failed to run script: %s" % (e.args[0]))
            raise

#     def _test_5(self):
#         """ """
#         envmonlib.Logging().log("Button Test 5")
