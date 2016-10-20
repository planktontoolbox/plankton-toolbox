#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os.path
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.tools.tool_base as tool_base
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
import plankton_toolbox.toolbox.toolbox_sync as toolbox_sync

import toolbox_utils
import plankton_core

class DatasetViewerTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _create_content().
        super(DatasetViewerTool, self).__init__(name, parentwidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.setBaseSize(600,600)
        # Filename used when saving data to file.
        self._lastuseddirectory = '.'

    def _create_content(self):
        """ """
        content = self._create_scrollable_content()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._content_select_dataset())
        contentLayout.addLayout(self._content_result_table())
        contentLayout.addWidget(self._content_save_result())
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
                     QtCore.SIGNAL('datasetListChanged'), 
                     self._update_dataset_list)
        # Allow synch is confusing. Activate again when used in more tools.                       
        # (Currently used in the other way, controlled by a checkbox in load_datasets_activity.)                       
        # Listen for changes in the toolbox sync.
        self.connect(toolbox_sync.ToolboxSync(), 
                     QtCore.SIGNAL('toolboxSyncSelectedRow'), 
                     self._set_selected_dataset)

    def _content_select_dataset(self):
        """ """
        # Active widgets and connections.
        self._selectdataset_list = QtGui.QComboBox()
        self._selectdataset_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._selectdataset_list.addItems(["<select dataset>"])
        self.connect(self._selectdataset_list, QtCore.SIGNAL('currentIndexChanged(int)'), self._view_dataset)
        #
        self._numberofrows_label = QtGui.QLabel('Number of rows: 0')
        
# Allow synch is confusing. Activate again when used in more tools.                       
#         self._allowsync_checkbox = QtGui.QCheckBox('Allow synch')
#         self._allowsync_checkbox.setChecked(False) 
        # Layout widgets.
        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel('Imports:'))
        layout.addWidget(self._selectdataset_list)
#         layout.addWidget(self._allowsync_checkbox)
        layout.addStretch(5)
        layout.addWidget(self._numberofrows_label)
        #
        return layout
        
    def _content_result_table(self):
        """ """
        # Active widgets and connections.
        self._tableview = utils_qt.ToolboxQTableView()
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._tableview)
        #
        return layout
        
    def _content_save_result(self):
        """ """
        saveresultbox = QtGui.QGroupBox('Export dataset', self)
        # Active widgets and connections.
        self._copytoclipboard_button = QtGui.QPushButton('Copy to clipboard')
        self.connect(self._copytoclipboard_button, QtCore.SIGNAL('clicked()'), self._copy_to_clipboard)                
        self._saveformat_list = QtGui.QComboBox()
        self._saveformat_list.addItems(["Tab delimited text file (*.txt)",
                                         "Excel file (*.xlsx)"])
        self._savedataset_button = QtGui.QPushButton('Save...')
        self.connect(self._savedataset_button, QtCore.SIGNAL('clicked()'), self._save_data)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._copytoclipboard_button)
#         hbox1.addStretch(10)
        hbox1.addWidget(QtGui.QLabel('File format:'))
        hbox1.addWidget(self._saveformat_list)
        hbox1.addWidget(self._savedataset_button)
        hbox1.addStretch(10)
        #
        saveresultbox.setLayout(hbox1)
        #
        return saveresultbox
        
    def _update_dataset_list(self):
        """ """
        self._selectdataset_list.clear()
        self._selectdataset_list.addItems(["<select dataset>"])
        
        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().get_datasets()):
            self._selectdataset_list.addItems(['Import-' + unicode(rowindex + 1)])

    def _view_dataset(self, index):
        """ """
        if index <= 0:
            # Clear table.
            self._tableview.clearModel()
            self._refresh_result_table()
        else:
            # envmonlib:
            dataset = toolbox_datasets.ToolboxDatasets().get_dataset_by_index(index - 1)
            if isinstance(dataset, plankton_core.DatasetTable):
                self._tableview.setTableModel(dataset)
                self._refresh_result_table()
            elif isinstance(dataset, plankton_core.DatasetNode):
                # Tree dataset must be converted to table dataset before viewing.
                targetdataset = plankton_core.DatasetTable()
                dataset.convert_to_table_dataset(targetdataset)
                #
                self._tableview.setTableModel(targetdataset)
                self._refresh_result_table()
            #
            # TODO: Remove later. Default alternative used for non toolbox_utils.
            else:
                self._tableview.setTableModel(dataset)
                self._refresh_result_table()
        #
        if self._tableview.getTableModel():
            self._numberofrows_label.setText('Number of rows: ' + unicode(self._tableview.getTableModel().get_row_count()))
        else:
            self._numberofrows_label.setText('Number of rows: 0')
    
    def _save_data(self):
        """ """
#         if self._tableview.getTableModel().getModeldata():
        if self._tableview.getTableModel():
            # Show select file dialog box.
            namefilter = 'All files (*.*)'
            if self._saveformat_list.currentIndex() == 1: # Xlsx file.
                namefilter = 'Excel files (*.xlsx);;All files (*.*)'
            else:
                namefilter = 'Text files (*.txt);;All files (*.*)'
            filename = QtGui.QFileDialog.getSaveFileName(
                            self,
                            'Export dataset',
                            self._lastuseddirectory,
                            namefilter)
            filename = unicode(filename) # QString to unicode.
            # Check if user pressed ok or cancel.
            if filename:
                self._lastuseddirectory = os.path.dirname(filename)
                if self._saveformat_list.currentIndex() == 0: # Text file.
#                     self._tableview.getTableModel().getModeldata().saveAsTextFile(filename)
                    self._tableview.getTableModel().save_as_file(text_file_name = filename)
                elif self._saveformat_list.currentIndex() == 1: # Excel file.
#                     self._tableview.getTableModel().getModeldata().saveAsExcelFile(filename)
                    self._tableview.getTableModel().save_as_file(excel_file_name = filename)
        
    def _copy_to_clipboard(self):
        """ """
        clipboard = QtGui.QApplication.clipboard()
        field_separator = '\t'
        row_separator = '\r\n'
        clipboardstring = ''
        #
#         table_dataset = self._tableview.getTableModel().getModeldata()
        table_dataset = self._tableview.getTableModel()
        if table_dataset:
            # Header.
            clipboardstring = field_separator.join(map(unicode, table_dataset.get_header())).strip() + row_separator
            # Rows.
            for row in table_dataset.get_rows():
                clipboardstring += field_separator.join(map(unicode, row)).strip() + row_separator
        #
        clipboard.setText(clipboardstring)

    def _refresh_result_table(self):
        """ """
        self._tableview.resetModel() # Model data has changed.
        self._tableview.resizeColumnsToContents()

    # Allow synch is confusing. Activate again when used in more tools.
    # (Currently used in the other way, controlled by a checkbox in load_datasets_activity.)                       
    def _set_selected_dataset(self):
        """ """
        index = toolbox_sync.ToolboxSync().get_row_index('dataset')
        self._selectdataset_list.setCurrentIndex(index + 1)
        self._view_dataset(index + 1)
#         if self._allowsync_checkbox.isChecked():
#             index = toolbox_sync.ToolboxSync().get_row_index('dataset')
#             self._selectdataset_list.setCurrentIndex(index + 1)
#             self._view_dataset(index + 1)
        
