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
import envmonlib

import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
#import plankton_toolbox.toolbox.toolbox_main_window as toolbox_main_window


class DevTestTool(tool_base.ToolBase):
    """
    For development and test only. Deactivate in public releases.
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Settings for the DevTestTool. NOTE: Max 4 is supported.
        self._dev_settings = [
            {   'button_text': 'SHARKweb_ZP_2010-2012_en_SHORT',
                'import_parser_path': 'toolbox_data/parsers/',
                'import_parser': 'SHARKweb_Zooplankton_parser.xlsx',
                'import_column': 'SHARKweb english',
                'export_column': 'Export english',
                'data_file_path': '',
                'data_file_name': 'SHARKweb_ZP_2010-2012_en_SHORT.txt',
                'data_file_encoding': 'windows-1252',
#                 'show_activity_after': 'Import datasets'
                'show_activity_after': 'Analyse data'

            },
            {   'button_text': 'SHARKweb_ZP_2010-2012_sv_SHORT',
                'import_parser_path': 'toolbox_data/parsers/',
                'import_parser': 'SHARKweb_Zooplankton_parser.xlsx',
                'import_column': 'SHARKweb swedish',
                'export_column': 'Export swedish',
                'data_file_path': '',
                'data_file_name': 'SHARKweb_ZP_2010-2012_sv_SHORT.txt',
                'data_file_encoding': 'windows-1252',
#                 'show_activity_after': 'Import datasets'
                'show_activity_after': 'Analyse data'

            },
            {   'button_text': 'PTBX_testdata',
                'import_parser_path': 'toolbox_data/parsers/',
                'import_parser': 'PTBX_testdata_parser.xlsx',
                'import_column': 'Import format',
                'export_column': 'Export format',
                'data_file_path': '',
                'data_file_name': 'PTBX_testdata.txt',
                'data_file_encoding': 'windows-1252',
#                 'show_activity_after': 'Import datasets'
                'show_activity_after': 'Screening'

            },
        ]

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
        layout = QtGui.QVBoxLayout()
        for index, settings_item in enumerate(self._dev_settings):
            self._testbutton = QtGui.QPushButton(settings_item['button_text'])
            if index == 0:
                self.connect(self._testbutton, QtCore.SIGNAL('clicked()'), self._test_0)   
            if index == 1:
                self.connect(self._testbutton, QtCore.SIGNAL('clicked()'), self._test_1)   
            if index == 2:
                self.connect(self._testbutton, QtCore.SIGNAL('clicked()'), self._test_2)   
            if index == 3:
                self.connect(self._testbutton, QtCore.SIGNAL('clicked()'), self._test_3)   
            layout.addWidget(self._testbutton)
        #
        layout.addStretch(5)
        #
        return layout

    def _test_0(self):
        """ """
        self._test(self._dev_settings[0])
        
    def _test_1(self):
        """ """
        self._test(self._dev_settings[1])
        
    def _test_2(self):
        """ """
        self._test(self._dev_settings[2])
        
    def _test_3(self):
        """ """
        self._test(self._dev_settings[3])
        
    def _test(self, settings):
        """ """
        try:
            envmonlib.Logging().log('Dev. tool: ' + settings['button_text'])
            #
            import_parser_path = settings['import_parser_path']
            import_parser = settings['import_parser']
            import_column = settings['import_column']
            export_column = settings['export_column']
            #
            self._parent.showActivityByName(settings['show_activity_after'])
            #
            # Set up for import file parsing.
            impMgr = envmonlib.ImportManager(import_parser_path + import_parser,
                                             import_column,
                                             export_column)
            # Import and parse file.
            data_file_path = settings['data_file_path']
            data_file_name = settings['data_file_name']
            data_file_encoding = settings['data_file_encoding']
            #
            dataset = impMgr.importTextFile(data_file_path + data_file_name,
                                            data_file_encoding)
            # Add metadata related to imported file.
            dataset.addMetadata('parser', import_parser)
            dataset.addMetadata('file_name', data_file_name)
            dataset.addMetadata('file_path', data_file_path)
            dataset.addMetadata('import_column', import_column)
            dataset.addMetadata('export_column', export_column)
            toolbox_datasets.ToolboxDatasets().addDataset(dataset)
            
            self._parent.showActivityByName(settings['show_activity_after'])
        except Exception as e:
            envmonlib.Logging().warning('Failed to run script: %s' % (e))
            raise
        
