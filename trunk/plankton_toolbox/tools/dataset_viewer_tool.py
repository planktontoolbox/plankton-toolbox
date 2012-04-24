#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2011 SMHI, Swedish Meteorological and Hydrological Institute 
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

"""
"""

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
        # Listen for changes in the toolbox sync.
        self.connect(toolbox_sync.ToolboxSync(), 
                     QtCore.SIGNAL("syncSelectedRowTEST"), 
                     self._setSelectedDataset)

    def _contentSelectDataset(self):
        """ """
        # Active widgets and connections.
        self._selectdataset_list = QtGui.QComboBox()
        self._selectdataset_list.addItems(["<select dataset>"])
        self.connect(self._selectdataset_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._viewDataset)                
        self._allowsync_checkbox = QtGui.QCheckBox("Allow synch" )
        self._allowsync_checkbox.setChecked(False) 
        # Layout widgets.
        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel("Loaded datasets:"))
        layout.addWidget(self._selectdataset_list)
        layout.addWidget(self._allowsync_checkbox)
        layout.addStretch(5)
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
        saveresultbox = QtGui.QGroupBox("Save dataset", self)
        # Active widgets and connections.
        self._saveformat_list = QtGui.QComboBox()
        #
        self._saveformat_list.addItems(["Tab delimited text file (*.txt)",
                                         "Excel file (*.xlsx)"])
        self._savedataset_button = QtGui.QPushButton("Save...")
        self.connect(self._savedataset_button, QtCore.SIGNAL("clicked()"), self._saveData)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
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
            self._selectdataset_list.addItems([u'Dataset-' + unicode(rowindex)])

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
                            'Save dataset',
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
        
    def _refreshResultTable(self):
        """ """
        self._tableview.tablemodel.reset() # Model data has changed.
        self._tableview.resizeColumnsToContents()

    def _setSelectedDataset(self):
        """ """
        if self._allowsync_checkbox.isChecked():
            index = toolbox_sync.ToolboxSync().getRowTest()
            self._selectdataset_list.setCurrentIndex(index + 1)
            self._viewDataset(index + 1)
        
