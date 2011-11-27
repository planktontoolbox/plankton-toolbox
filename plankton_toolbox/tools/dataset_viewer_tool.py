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

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_base as tool_base
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets

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
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.setBaseSize(600,600)
        #
        self.__lastusedfilename = '.'

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        contentLayout.addLayout(self.__contentSelectDataset())
        contentLayout.addLayout(self.__contentResultTable())
        contentLayout.addWidget(self.__contentSaveResult())
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
                     QtCore.SIGNAL("datasetListChanged"), 
                     self.__updateDatasetList)
#
#        self.__updateDatasetList()

    def __contentSelectDataset(self):
        """ """
        # Active widgets and connections.
        self.__selectdataset_list = QtGui.QComboBox()
        self.__selectdataset_list.addItems(["<select dataset>"])
        self.connect(self.__selectdataset_list, QtCore.SIGNAL("currentIndexChanged(int)"), self.__viewDataset)                
        # Layout widgets.
        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel("Loaded datasets:"))
        layout.addWidget(self.__selectdataset_list)
        layout.addStretch(5)
        #
        return layout
        
    def __contentResultTable(self):
        """ """
        # Active widgets and connections.
        self.__tableview = QtGui.QTableView()
        self.__tableview.setAlternatingRowColors(True)
        self.__tableview.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        #self.__tableview.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.__tableview.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
        self.__tableview.verticalHeader().setDefaultSectionSize(18)
        # Model, data and selection        
        self.__model = ResultTableModel(None)
        self.__tableview.setModel(self.__model)        
        selectionModel = QtGui.QItemSelectionModel(self.__model)
        self.__tableview.setSelectionModel(selectionModel)
        self.__tableview.resizeColumnsToContents()
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.__tableview)
        #
        return layout
        
    def __contentSaveResult(self):
        """ """
        saveresultbox = QtGui.QGroupBox("Save dataset", self)
        # Active widgets and connections.
        self.__saveformat_list = QtGui.QComboBox()
        #
        self.__saveformat_list.addItems(["Tab delimited text file (.txt)",
                                         "Excel files (.xlsx)"])
        self.__savedataset_button = QtGui.QPushButton("Save as...")
        self.connect(self.__savedataset_button, QtCore.SIGNAL("clicked()"), self.__saveData)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(QtGui.QLabel("Format:"))
        hbox1.addWidget(self.__saveformat_list)
        hbox1.addWidget(self.__savedataset_button)
        #
        saveresultbox.setLayout(hbox1)
        #
        return saveresultbox
        
    def __updateDatasetList(self):
        """ """
        self.__selectdataset_list.clear()
        self.__selectdataset_list.addItems(["<select dataset>"])
        
        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().getDatasets()):
            self.__selectdataset_list.addItems([u'Dataset - ' + unicode(rowindex)])

    def __viewDataset(self, index):
        """ """
        if index <= 0:
            # Clear table.
            self.__model.setDataset(None)
            self.__refreshResultTable()
        else:
            self.__model.setDataset(toolbox_datasets.ToolboxDatasets().getDatasetByIndex(index - 1))
            self.__refreshResultTable()
    
    def __saveData(self):
        """ """
        # Show select file dialog box.
        namefilter = 'All files (*.*)'
        if self.__saveformat_list.currentIndex() == 1: # Xlsx file.
            namefilter = 'Excel files (*.xlsx);;All files (*.*)'
        else:
            namefilter = 'Text files (*.txt);;All files (*.*)'
#        filename = QtGui.QFileDialog.getOpenFileNames(
        filename = QtGui.QFileDialog.getSaveFileName(
                            self,
                            'Save dataset',
                            self.__lastusedfilename,
                            namefilter)
        # Check if user pressed ok or cancel.
        if self.__model.getDataset():
            if filename:
                self.__lastusedfilename = filename
                if self.__saveformat_list.currentIndex() == 0: # Text file.
                    self.__model.getDataset().SaveAsTextFile(unicode(filename))
                elif self.__saveformat_list.currentIndex() == 1: # Xlsx file.
                    self.__model.getDataset().SaveExcelXlsxFile(unicode(filename))

        
    def __refreshResultTable(self):
        """ """
        self.__model.reset() # Model data has changed.
        self.__tableview.resizeColumnsToContents()


class ResultTableModel(QtCore.QAbstractTableModel):
    """
    """
    def __init__(self, dataset):
        """ """
        self.__dataset = dataset
        # Initialize parent.
        super(ResultTableModel, self).__init__()
        
    def setDataset(self, dataset):
        """ """
        self.__dataset = dataset

    def getDataset(self):
        """ """
        return self.__dataset

    def rowCount(self, parent=QtCore.QModelIndex()):
        """ """
        if self.__dataset == None:
            return 0
        return self.__dataset.getRowCount()

    def columnCount(self, parent=QtCore.QModelIndex()):
        """ """
        if self.__dataset == None:
            return 0
        return self.__dataset.getColumnCount()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """ """
        if self.__dataset == None:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.__dataset.getHeaderItem(section))
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(section + 1)
        return QtCore.QVariant()

    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
        """ """
        if self.__dataset == None:
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole:
            if index.isValid():
                return QtCore.QVariant(self.__dataset.getDataItem(index.row(), index.column()))
        return QtCore.QVariant()

