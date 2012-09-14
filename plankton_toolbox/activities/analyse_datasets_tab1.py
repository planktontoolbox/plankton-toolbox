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
#import datetime
import copy
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
import envmonlib

class AnalyseDatasetsTab1(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """
        super(AnalyseDatasetsTab1, self).__init__()

    def setMainActivity(self, main_activity):
        """ """
        self._main_activity = main_activity
                
    def clear(self):
        """ """
        
    def update(self):
        """ """        

    # ===== TAB: Select dataset(s) ===== 
    def contentSelectDatasets(self):
        """ """
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.
        """)
        #
        loaded_datasets_listview = QtGui.QListView()
        loaded_datasets_listview.setMaximumHeight(80)
#        view.setMinimumWidth(500)
        self._loaded_datasets_model = QtGui.QStandardItemModel()
        loaded_datasets_listview.setModel(self._loaded_datasets_model)
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
                     QtCore.SIGNAL("datasetListChanged"), 
                     self._updateLoadedDatasetList)
        #
        self._clearcurrentdata_button = QtGui.QPushButton("Clear current data")
        self.connect(self._clearcurrentdata_button, QtCore.SIGNAL("clicked()"), self._clearCurrentData)                
        self._useselecteddatasets_button = QtGui.QPushButton("Use selected dataset(s)")
        self.connect(self._useselecteddatasets_button, QtCore.SIGNAL("clicked()"), self._useSelectedDatasets)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(self._clearcurrentdata_button)
        hbox1.addWidget(self._useselecteddatasets_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addWidget(loaded_datasets_listview)
#        layout.addStretch(1)
        layout.addLayout(hbox1)
        self.setLayout(layout)                
        #
        return self

    def _updateLoadedDatasetList(self):
        """ """
        self._loaded_datasets_model.clear()        
        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().getDatasets()):
            item = QtGui.QStandardItem(u"Dataset-" + unicode(rowindex) + 
                                       u".   Source: " + dataset.getMetadata(u'File name'))
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            self._loaded_datasets_model.appendRow(item)

    def _clearCurrentData(self):
        """ """
        self._main_activity.setCurrentData(None)    

    def _useSelectedDatasets(self):
        """ """
        try:
            # Clear current data.
            self._clearCurrentData()    
            # Check if all selected datasets contains the same columns.
            compareheaders = None
            for rowindex in range(self._loaded_datasets_model.rowCount()):
                item = self._loaded_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:
                    dataset = envmonlib.Datasets().getDatasets()[rowindex]
                    if compareheaders == None:
                        compareheaders = dataset.getExportTableColumns()
                    else:
                        newheader = dataset.getExportTableColumns()
                        if len(compareheaders)==len(newheader) and \
                           all(compareheaders[i] == newheader[i] for i in range(len(compareheaders))):
                            pass # OK since export columns are equal.
                        else:
                            envmonlib.Logging().log("Can't use datasets with different export columns. Please try again.")
                            raise UserWarning("Can't use datasets with different export columns. Please try again.")
            # Concatenate selected datasets.        
            dataset = None
            for rowindex in range(self._loaded_datasets_model.rowCount()):
                item = self._loaded_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:        
                #             
                    if dataset == None:
                        # Deep copy of the first dataset.
                        dataset = copy.deepcopy(envmonlib.Datasets().getDatasets()[rowindex])
                    else:
                        # Append top node data and children. Start with a deep copy.
                        tmp_dataset = copy.deepcopy(envmonlib.Datasets().getDatasets()[rowindex])
                        for key, value in dataset.getDataDict():
                            dataset.addData(key, value)
                        for child in tmp_dataset.getChildren():
                            dataset.addChild(child)
            # Check.
            if (dataset == None) or (len(dataset.getChildren()) == 0):
                envmonlib.Logging().log("Selected datasets are empty. Please try again.")
                raise UserWarning("Selected datasets are empty. Please try again.")
            # Use the concatenated datasets as current data.
            self._main_activity.setCurrentData(dataset)    
        except UserWarning, e:
            QtGui.QMessageBox.warning(self._main_activity, "Warning", unicode(e))

