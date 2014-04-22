#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import os.path
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.tools.tool_base as tool_base
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
import plankton_toolbox.toolbox.toolbox_sync as toolbox_sync

import envmonlib

class DatasetViewerTool(tool_base.ToolBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(DatasetViewerTool, self).__init__(name, parentwidget)
        #
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.setBaseSize(600,600)
        # Filename used when saving data to file.
        self._lastuseddirectory = '.'

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self._contentSelectDataset())
        contentLayout.addLayout(self._contentResultTable())
        contentLayout.addWidget(self._contentSaveResult())
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
                     QtCore.SIGNAL("datasetListChanged"), 
                     self._updateDatasetList)
        # Allow synch is confusing. Activate again when used in more tools.                       
        # (Currently used in the other way, controlled by a checkbox in load_datasets_activity.)                       
        # Listen for changes in the toolbox sync.
        self.connect(toolbox_sync.ToolboxSync(), 
                     QtCore.SIGNAL("toolboxSyncSelectedRow"), 
                     self._setSelectedDataset)

    def _contentSelectDataset(self):
        """ """
        # Active widgets and connections.
        self._selectdataset_list = QtGui.QComboBox()
        self._selectdataset_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._selectdataset_list.addItems(["<select dataset>"])
        self.connect(self._selectdataset_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._viewDataset)
        #
        self._numberofrows_label = QtGui.QLabel("Number of rows: 0")
        
# Allow synch is confusing. Activate again when used in more tools.                       
#         self._allowsync_checkbox = QtGui.QCheckBox("Allow synch")
#         self._allowsync_checkbox.setChecked(False) 
        # Layout widgets.
        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel("Datasets:"))
        layout.addWidget(self._selectdataset_list)
#         layout.addWidget(self._allowsync_checkbox)
        layout.addStretch(5)
        layout.addWidget(self._numberofrows_label)
        #
        return layout
        
    def _contentResultTable(self):
        """ """
        # Active widgets and connections.
        self._tableview = utils_qt.ToolboxQTableView()
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._tableview)
        #
        return layout
        
    def _contentSaveResult(self):
        """ """
        saveresultbox = QtGui.QGroupBox("Export dataset", self)
        # Active widgets and connections.
        self._copytoclipboard_button = QtGui.QPushButton("Copy to clipboard")
        self.connect(self._copytoclipboard_button, QtCore.SIGNAL("clicked()"), self._copyToClipboard)                
        self._saveformat_list = QtGui.QComboBox()
        self._saveformat_list.addItems(["Tab delimited text file (*.txt)",
                                         "Excel file (*.xlsx)"])
        self._savedataset_button = QtGui.QPushButton("Save...")
        self.connect(self._savedataset_button, QtCore.SIGNAL("clicked()"), self._saveData)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._copytoclipboard_button)
        hbox1.addStretch(5)
        hbox1.addWidget(QtGui.QLabel("File format:"))
        hbox1.addWidget(self._saveformat_list)
        hbox1.addWidget(self._savedataset_button)
        #
        saveresultbox.setLayout(hbox1)
        #
        return saveresultbox
        
    def _updateDatasetList(self):
        """ """
        self._selectdataset_list.clear()
        self._selectdataset_list.addItems(["<select dataset>"])
        
        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().getDatasets()):
            self._selectdataset_list.addItems([u'Dataset-' + unicode(rowindex + 1)])

    def _viewDataset(self, index):
        """ """
        if index <= 0:
            # Clear table.
            self._tableview.tablemodel.setModeldata(None)
            self._refreshResultTable()
        else:
            # envmonlib:
            dataset = toolbox_datasets.ToolboxDatasets().getDatasetByIndex(index - 1)
            if isinstance(dataset, envmonlib.DatasetTable):
                self._tableview.tablemodel.setModeldata(dataset)
                self._refreshResultTable()
            elif isinstance(dataset, envmonlib.DatasetNode):
                # Tree dataset must be converted to table dataset before viewing.
                targetdataset = envmonlib.DatasetTable()
                dataset.convertToTableDataset(targetdataset)
                #
                self._tableview.tablemodel.setModeldata(targetdataset)
                self._refreshResultTable()
            #
            # TODO: Remove later. Default alternative used for non envmonlib.
            else:
                self._tableview.tablemodel.setModeldata(dataset)
                self._refreshResultTable()
        #
        self._numberofrows_label.setText("Number of rows: " + unicode(self._tableview.tablemodel.rowCount()))
    
    def _saveData(self):
        """ """
        if self._tableview.tablemodel.getModeldata():
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
                    self._tableview.tablemodel.getModeldata().saveAsTextFile(filename)
                elif self._saveformat_list.currentIndex() == 1: # Excel file.
                    self._tableview.tablemodel.getModeldata().saveAsExcelFile(filename)
        
    def _copyToClipboard(self):
        """ """
        clipboard = QtGui.QApplication.clipboard()
        field_separator = u'\t'
        row_separator = u'\r\n'
        clipboardstring = ''
        #
        table_dataset = self._tableview.tablemodel.getModeldata()
        if table_dataset:
            # Header.
            clipboardstring = field_separator.join(map(unicode, table_dataset.getHeader())) + row_separator
            # Rows.
            for row in table_dataset.getRows():
                clipboardstring += field_separator.join(map(unicode, row)) + row_separator
        #
        clipboard.setText(clipboardstring)

    def _refreshResultTable(self):
        """ """
        self._tableview.tablemodel.reset() # Model data has changed.
        self._tableview.resizeColumnsToContents()

    # Allow synch is confusing. Activate again when used in more tools.
    # (Currently used in the other way, controlled by a checkbox in load_datasets_activity.)                       
    def _setSelectedDataset(self):
        """ """
        index = toolbox_sync.ToolboxSync().getRow()
        self._selectdataset_list.setCurrentIndex(index + 1)
        self._viewDataset(index + 1)
#         if self._allowsync_checkbox.isChecked():
#             index = toolbox_sync.ToolboxSync().getRow()
#             self._selectdataset_list.setCurrentIndex(index + 1)
#             self._viewDataset(index + 1)
        
