#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os.path
import glob

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.activity_base as activity_base
#import plankton_toolbox.core.monitoring.monitoring_files as monitoring_files
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
import plankton_toolbox.toolbox.toolbox_sync as toolbox_sync
# import plankton_toolbox.toolbox.help_texts as help_texts

import envmonlib
import toolbox_utils
import toolbox_core

class CounterActivity(activity_base.ActivityBase):
    """
    Template class for new activities.
    """
    
    def __init__(self, name, parentwidget):
        """ """
#         self._datasettabledata = DatasetTableData()
#         self._last_used_textfile_name = ''
#         self._last_used_excelfile_name = ''
        # Load available dataset parsers.
#         self._parser_list = []
#         self._load_available_parsers()
        # Initialize parent (self._create_content will be called).
        super(CounterActivity, self).__init__(name, parentwidget)
        # Log available parsers when GUI setup has finished.
#         QtCore.QTimer.singleShot(10, self._log_available_parsers)

#     def _load_available_parsers(self):
#         """ """
#         self._parser_path = 'toolbox_data/parsers/'
#         self._parser_list = []
#         for parserpath in glob.glob(self._parser_path + '*.xlsx'):
#             self._parser_list.append(os.path.basename(parserpath))
# 
#     def _log_available_parsers(self):
#         """ """
#         if len(self._parser_list) > 0:
#             toolbox_utils.Logging().log('') # Empty line.
#             toolbox_utils.Logging().log('Available dataset parsers (located in "toolbox_data/parsers"):')
#             for parserpath in self._parser_list:
#                 toolbox_utils.Logging().log('- ' + os.path.basename(parserpath))
#         else:
#             toolbox_utils.Logging().log('No dataset parsers are found in "/toolbox_data/parsers". ')

    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = QtGui.QLabel('<h2>' + self.objectName() + '</h2>', self)
        self._activityheader.setTextFormat(QtCore.Qt.RichText)
        self._activityheader.setAlignment(QtCore.Qt.AlignHCenter)
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self._content_plankton_counter(), 10)
#        contentLayout.addStretch(5)
        # Style.
        self._activityheader.setStyleSheet(""" 
            * { color: white; background-color: #00677f; }
            """)
    
    def _content_load_dataset(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox('Import dataset', self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._content_textfile(), 'Text files (*.txt)')
        tabWidget.addTab(self._content_xlsx(), 'Excel files (*.xlsx)')
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    # ===== COUNTER DATASETS =====    
    def _content_plankton_counter(self):
        """ """
        widget = QtGui.QWidget()
        #
        loaded_datasets_listview = QtGui.QListView()
        self._loaded_datasets_model = QtGui.QStandardItemModel()
        loaded_datasets_listview.setModel(self._loaded_datasets_model)
        #
        
#         loaded_datasets_listview.
        
        #
        self._clearall_button = QtGui.QPushButton('Clear all')
        self.connect(self._clearall_button, QtCore.SIGNAL('clicked()'), self._uncheck_all_datasets)                
        self._markall_button = QtGui.QPushButton('Mark all')
        self.connect(self._markall_button, QtCore.SIGNAL('clicked()'), self._check_all_datasets)                
        self._importcounterdataset_button = QtGui.QPushButton('Import marked dataset(s)')
        self.connect(self._importcounterdataset_button, QtCore.SIGNAL('clicked()'), self._import_counter_datasets)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._clearall_button)
        hbox1.addWidget(self._markall_button)
        hbox1.addStretch(10)
        hbox1.addWidget(self._importcounterdataset_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(loaded_datasets_listview, 10)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget

    def _check_all_datasets(self):
        """ """
        for rowindex in range(self._loaded_datasets_model.rowCount()):
            item = self._loaded_datasets_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Checked)
            
    def _uncheck_all_datasets(self):
        """ """
        for rowindex in range(self._loaded_datasets_model.rowCount()):
            item = self._loaded_datasets_model.item(rowindex, 0)
            item.setCheckState(QtCore.Qt.Unchecked)

    def _import_counter_datasets(self):
        """ """
        QtGui.QMessageBox.information(self, "Information", 'Not implemented yet.')
    
# class DatasetTableData(object):
#     """ """
#     def __init__(self):
#         """ """
#         self._header = []
#         self._rows = []
#         
#     def clear(self):
#         """ """
#         self._header = []
#         self._rows = []
# 
#     def clearRows(self):
#         """ """
#         self._rows = []
# 
#     def setHeader(self, header):
#         """ """
#         self._header = header
# 
#     def addRow(self, row):
#         """ """
#         self._rows.append(row)
# 
#     def getHeaderItem(self, column):
#         """ Used for calls from QAbstractTableModel. """
#         try:
#             return self._header[column]
#         except Exception:
#             return ''
# 
#     def getDataItem(self, row, column):
#         """ Used for calls from QAbstractTableModel. """
#         try:
#             return self._rows[row][column]
#         except Exception:
#             return ''
# 
#     def getColumnCount(self):
#         """ Used for calls from QAbstractTableModel. """
#         try:
#             return len(self._header)
#         except Exception:
#             return ''
# 
#     def getRowCount(self):
#         """ Used for calls from QAbstractTableModel. """
#         try:
#             return len(self._rows)
#         except Exception:
#             return ''

        