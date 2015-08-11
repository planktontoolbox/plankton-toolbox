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
        self._datasettabledata = DatasetTableData()
        self._last_used_textfile_name = ''
        self._last_used_excelfile_name = ''
        # Load available dataset parsers.
        self._parser_list = []
        self._load_available_parsers()
        # Initialize parent (self._create_content will be called).
        super(CounterActivity, self).__init__(name, parentwidget)
        # Log available parsers when GUI setup has finished.
        QtCore.QTimer.singleShot(10, self._log_available_parsers)

    def _load_available_parsers(self):
        """ """
        self._parser_path = 'toolbox_data/parsers/'
        self._parser_list = []
        for parserpath in glob.glob(self._parser_path + '*.xlsx'):
            self._parser_list.append(os.path.basename(parserpath))

    def _log_available_parsers(self):
        """ """
        if len(self._parser_list) > 0:
            toolbox_utils.Logging().log('') # Empty line.
            toolbox_utils.Logging().log('Available dataset parsers (located in "toolbox_data/parsers"):')
            for parserpath in self._parser_list:
                toolbox_utils.Logging().log('- ' + os.path.basename(parserpath))
        else:
            toolbox_utils.Logging().log('No dataset parsers are found in "/toolbox_data/parsers". ')

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
        contentLayout.addWidget(self._content_loaded_datasets(), 10)
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

    # ===== LOADED DATASETS =====    
    def _content_loaded_datasets(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox('Loaded datasets', self)
        #
        self._datasets_table = utils_qt.ToolboxQTableView()
        self._datasets_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        
        self._datasettabledata.clear()
        self._datasettabledata.setHeader(['Dataset      ', 
#                                           'Type         ', 
                                          'Content      ', 
                                          'File         ', 
                                          'File path    ',
                                          'Parser       ',
                                          'Import column',
                                          'Export column'])
        self._datasets_table.tablemodel.setModeldata(self._datasettabledata)
        self._datasets_table.resizeColumnsToContents()
        
        self._datasets_table.selectionModel.Rows
        
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
             QtCore.SIGNAL('datasetListChanged'), 
             self._update_dataset_list)
        # Connection for selected row.
        self._datasets_table.clicked.connect(self._selection_changed)
                        
        # Buttons.
        self._unloadalldatasets_button = QtGui.QPushButton('Remove all datasets')
        self._unloadmarkeddatasets_button = QtGui.QPushButton('Remove marked dataset(s)')
        # If checked the selected dataset content should be viewed in the dataset viewer tool.
        self._viewdataset_checkbox = QtGui.QCheckBox('View marked dataset')
        self._viewdataset_checkbox.setChecked(False)
        # Button connections.
        self.connect(self._unloadalldatasets_button, QtCore.SIGNAL('clicked()'), self._unload_all_datasets)                
        self.connect(self._unloadmarkeddatasets_button, QtCore.SIGNAL('clicked()'), self._unload_marked_datasets)                
        self._viewdataset_checkbox.clicked.connect(self._selection_changed)
        # Layout widgets.
        buttonlayout = QtGui.QHBoxLayout()
        buttonlayout.addWidget(self._unloadalldatasets_button)
        buttonlayout.addWidget(self._unloadmarkeddatasets_button)
        buttonlayout.addWidget(self._viewdataset_checkbox)
        buttonlayout.addStretch(5)
        #
        widget = QtGui.QWidget()        
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(self._datasets_table)
        layout.addLayout(buttonlayout)
        selectdatabox.setLayout(layout) 
        #       
        return selectdatabox

    def _unload_all_datasets(self):
        """ """
        toolbox_datasets.ToolboxDatasets().clear()

    def _unload_marked_datasets(self):
        # Remove datasets, start with the last one. 
        rowcount = self._datasets_table.tablemodel.rowCount()
        for rowindex in range(rowcount):
            index = rowcount - rowindex - 1
            if self._datasets_table.selectionModel.isSelected(self._datasets_table.tablemodel.createIndex(index, 0)): # Check if selected by user.
                toolbox_datasets.ToolboxDatasets().remove_dataset_by_index(index)

    def _update_dataset_list(self):
        """ """
        self._datasettabledata.clearRows()
        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().get_datasets()):
            # Get content info depending on dataset type.
#             datasettype = '',
            contentinfo = ''
            if isinstance(dataset, toolbox_core.DatasetTable):
#                 datasettype = 'Table dataset'
                contentinfo = 'Rows: ' + unicode(len(dataset.getRows())) + '. '
            elif isinstance(dataset, toolbox_core.DatasetNode):
#                 datasettype = 'Tree dataset'
                visitcount, samplecound, variablecount = dataset.getCounters()
                contentinfo = 'Visits: ' + unicode(visitcount) + ', ' + \
                              'samples: ' + unicode(samplecound) + ', ' + \
                              'variables: ' + unicode(variablecount) + '. '
#             else:
#                 datasettype = 'Unspecified'

            # Add row 
            self._datasettabledata.addRow(
                ['Dataset-' + unicode(rowindex + 1),
#                  datasettype,
                 contentinfo,
                 dataset.getMetadata('file_name'),
                 dataset.getMetadata('file_path'),
                 dataset.getMetadata('parser'),
                 dataset.getMetadata('import_column'),
                 dataset.getMetadata('export_column')])
            #
        self._datasets_table.tablemodel.reset()
        self._datasets_table.resizeColumnsToContents()

    
    def _selection_changed(self):
        """ """
        if self._viewdataset_checkbox.isChecked():
            modelIndex = self._datasets_table.selectionModel.currentIndex()
            if modelIndex.isValid():
                # View tool.
                tool_manager.ToolManager().show_tool_by_name('Dataset viewer') # Show tool if hidden.
                # graphtool = tool_manager.ToolManager().getToolByName('Dataset viewer')
                toolbox_sync.ToolboxSync().set_row_index('dataset', modelIndex.row())

    
class DatasetTableData(object):
    """ """
    def __init__(self):
        """ """
        self._header = []
        self._rows = []
        
    def clear(self):
        """ """
        self._header = []
        self._rows = []

    def clearRows(self):
        """ """
        self._rows = []

    def setHeader(self, header):
        """ """
        self._header = header

    def addRow(self, row):
        """ """
        self._rows.append(row)

    def getHeaderItem(self, column):
        """ Used for calls from QAbstractTableModel. """
        try:
            return self._header[column]
        except Exception:
            return ''

    def getDataItem(self, row, column):
        """ Used for calls from QAbstractTableModel. """
        try:
            return self._rows[row][column]
        except Exception:
            return ''

    def getColumnCount(self):
        """ Used for calls from QAbstractTableModel. """
        try:
            return len(self._header)
        except Exception:
            return ''

    def getRowCount(self):
        """ Used for calls from QAbstractTableModel. """
        try:
            return len(self._rows)
        except Exception:
            return ''

        