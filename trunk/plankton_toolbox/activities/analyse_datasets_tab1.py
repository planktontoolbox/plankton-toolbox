#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2013 SMHI, Swedish Meteorological and Hydrological Institute 
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
# import copy
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
import plankton_toolbox.toolbox.help_texts as help_texts
import envmonlib

class AnalyseDatasetsTab1(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab1, self).__init__()

    def setMainActivity(self, main_activity):
        """ """
        self._main_activity = main_activity
        self._analysisdata = main_activity.getAnalysisData()
                
    def clear(self):
        """ """
        
    def update(self):
        """ """        

    # ===== TAB: Select dataset(s) ===== 
    def contentSelectDatasets(self):
        """ """
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText(help_texts.HelpTexts().getText(u'AnalyseDatasetsTab1_intro'))
#         introlabel.setText("""
#         Select dataset(s) to be analyzed. 
#         Note that "Analysis data" contains a working copy of one or several loaded datasets. 
#         Rows in "Analysis data" can be removed, added or aggregated during the analysis.
#         """)
        #
        loaded_datasets_listview = QtGui.QListView()
        loaded_datasets_listview.setMaximumHeight(80)
#        view.setMinimumWidth(500)
        self._loaded_datasets_model = QtGui.QStandardItemModel()
        loaded_datasets_listview.setModel(self._loaded_datasets_model)
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
                     QtCore.SIGNAL("datasetListChanged"), 
                     self._updateImportedDatasetList)
        #
        self._clearanalysisdata_button = QtGui.QPushButton("Clear analysis data")
        self.connect(self._clearanalysisdata_button, QtCore.SIGNAL("clicked()"), self._clearAnalysisData)                
        self._copydatasets_button = QtGui.QPushButton("Load marked dataset(s) for analysis")
        self.connect(self._copydatasets_button, QtCore.SIGNAL("clicked()"), self._copyDatasetsForAnalysis)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._clearanalysisdata_button)
        hbox1.addStretch(10)
        hbox1.addWidget(self._copydatasets_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addWidget(loaded_datasets_listview)
        layout.addStretch(5)
        layout.addLayout(hbox1)
        self.setLayout(layout)                
        #
        return self

    def _updateImportedDatasetList(self):
        """ """
        self._loaded_datasets_model.clear()        
        for rowindex, dataset in enumerate(toolbox_datasets.ToolboxDatasets().getDatasets()):
            item = QtGui.QStandardItem(u"Dataset-" + unicode(rowindex) + 
                                       u".   Source: " + dataset.getMetadata(u'file_name'))
            item.setCheckState(QtCore.Qt.Checked)
#            item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            self._loaded_datasets_model.appendRow(item)

    def _clearAnalysisData(self):
        """ """
        self._main_activity.viewAnalysisData()
#         self._analysisdata.setData(None)    
        self._main_activity.getAnalysisData().clearData()    
        self._main_activity.getStatisticData().clearData()    
        self._main_activity.getReportData().clearData()    
        self._main_activity.updateViewedDataAndTabs() 

    def _copyDatasetsForAnalysis(self):
        """ """
        try:
            self._main_activity.viewAnalysisData()
            # Clear analysis data
            self._analysisdata.clearData()
            self._main_activity.updateViewedDataAndTabs() 
            # Create a list of selected datasets.        
            datasets = []
            for rowindex in range(self._loaded_datasets_model.rowCount()):
                item = self._loaded_datasets_model.item(rowindex, 0)
                if item.checkState() == QtCore.Qt.Checked:        
                    datasets.append(envmonlib.Datasets().getDatasets()[rowindex])
            # Use the datasets for analysis.
            self._analysisdata.copyDatasetsToAnalysisData(datasets)  
            # Check.
            if (self._analysisdata.getData() == None) or (len(self._analysisdata.getData().getChildren()) == 0):
                envmonlib.Logging().log("Selected datasets are empty.")
                raise UserWarning("Selected datasets are empty.")
            self._main_activity.updateViewedDataAndTabs() 
        #
        except UserWarning, e:
            QtGui.QMessageBox.warning(self._main_activity, "Warning", unicode(e))

