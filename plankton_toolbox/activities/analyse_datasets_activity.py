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

import os.path
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.analyse_datasets_tab1 as tab1
import plankton_toolbox.activities.analyse_datasets_tab2 as tab2
import plankton_toolbox.activities.analyse_datasets_tab3 as tab3
import plankton_toolbox.activities.analyse_datasets_tab4 as tab4
import plankton_toolbox.activities.analyse_datasets_tab5 as tab5
import plankton_toolbox.activities.analyse_datasets_tab6 as tab6
import plankton_toolbox.activities.analyse_datasets_tab7 as tab7
import plankton_toolbox.activities.analyse_datasets_tab8 as tab8
import envmonlib

class AnalyseDatasetsActivity(activity_base.ActivityBase):
    """
    """
    def __init__(self, name, parentwidget):
        """ """
        # Create object containing analysis data.
        self._analysisdata = envmonlib.AnalysisData()
        self._statisticdata = envmonlib.StatisticData()
        self._reportdata = envmonlib.ReportData()
        
        # Filename used when saving data to file.
        self._lastuseddirectory = '.'
        # Create tab widgets.
        self._tab1widget = tab1.AnalyseDatasetsTab1()
        self._tab2widget = tab2.AnalyseDatasetsTab2()
        self._tab3widget = tab3.AnalyseDatasetsTab3()
        self._tab4widget = tab4.AnalyseDatasetsTab4()
        self._tab5widget = tab5.AnalyseDatasetsTab5()
        self._tab6widget = tab6.AnalyseDatasetsTab6()
        self._tab7widget = tab7.AnalyseDatasetsTab7()
        self._tab8widget = tab8.AnalyseDatasetsTab8()
        # 
        self._tab1widget.setMainActivity(self)
        self._tab2widget.setMainActivity(self)
        self._tab3widget.setMainActivity(self)
        self._tab4widget.setMainActivity(self)
        self._tab5widget.setMainActivity(self)
        self._tab6widget.setMainActivity(self)
        self._tab7widget.setMainActivity(self)
        self._tab8widget.setMainActivity(self)
        # Initialize parent.
        super(AnalyseDatasetsActivity, self).__init__(name, parentwidget)

    def getAnalysisData(self):
        """ """
        return self._analysisdata 
        
    def getStatisticData(self):
        """ """
        return self._statisticdata 
        
    def getReportData(self):
        """ """
        return self._reportdata 
        
    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = QtGui.QLabel('<h2>' + self.objectName() + '</h2>', self)
        self._activityheader.setTextFormat(QtCore.Qt.RichText)
        self._activityheader.setAlignment(QtCore.Qt.AlignHCenter)
        self._activityheader.setStyleSheet(""" 
            * { color: white; background-color: #00677f; }
            """)
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self._contentAnalyseTabs())
        contentLayout.addWidget(self._contentAnalysisDataTable(), 10)
        contentLayout.addWidget(self._contentSaveAnalysisData())
    
    def _contentAnalyseTabs(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("", self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._tab1widget.contentSelectDatasets(), "Select dataset(s)")
        tabWidget.addTab(self._tab2widget.contentPrepareData(), "Clean up")
        tabWidget.addTab(self._tab3widget.contentAggregateData(), "Aggregate/complement data")
        tabWidget.addTab(self._tab4widget.contentSelectData(), "Filter")
        tabWidget.addTab(self._tab5widget.contentPredefinedGraphs(), "Predefined graphs")
        tabWidget.addTab(self._tab6widget.contentGenericGraphs(), "Generic graphs")
        tabWidget.addTab(self._tab7widget.contentStatistics(), "Statistics")
        tabWidget.addTab(self._tab8widget.contentReports(), "Reports")
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    # ===== ANALYSIS DATA =====    
    def _contentAnalysisDataTable(self):
        """ """
        # Active widgets and connections.
        analysisdatagroupbox = QtGui.QGroupBox("Analysis data, filtered data, statistical data and report data", self)
        # Active widgets and connections.
        self._viewdata_list = QtGui.QComboBox()
        self._viewdata_list.addItems(["Analysis data",
                                      "Filtered analysis data",
                                      "Statistic data",
                                      "Report data",
                                      "Hide data (to increase performance)"])
        self.connect(self._viewdata_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._viewDataListChanged)                
        #
#        self._hidedata_checkbox = QtGui.QCheckBox("Hide data")
#        self._hidedata_checkbox.setChecked(False)
#        self.connect(self._hidedata_checkbox, QtCore.SIGNAL("clicked()"), self._viewHideDataChanged)                
        #
        self._refreshfiltereddata_button = QtGui.QPushButton("Refresh filtered data") # TODO:
        self._refreshfiltereddata_button.hide()
        self.connect(self._refreshfiltereddata_button, QtCore.SIGNAL("clicked()"), self._refreshFilteredData)                
        #
        self._tableview = utils_qt.ToolboxQTableView()
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(QtGui.QLabel("View:"))
        hbox1.addWidget(self._viewdata_list)
#        hbox1.addWidget(self._hidedata_checkbox)
        hbox1.addWidget(self._refreshfiltereddata_button)
        hbox1.addStretch(5)
        #
        layout.addLayout(hbox1)
        layout.addWidget(self._tableview)
        #
        analysisdatagroupbox.setLayout(layout)
        #
        return analysisdatagroupbox

    def _viewDataListChanged(self, row_index):
        """ """
        if row_index == 1:
            self._refreshfiltereddata_button.show()
        else:
            self._refreshfiltereddata_button.hide()
        #
        self.updateViewedData()
        
    def _refreshFilteredData(self):
        """ """
        # Note: row_index used inside updateViewedData().
        self.updateViewedData()
        
    def _viewHideDataChanged(self):
        """ """
        self.updateViewedData()
        
    def _contentSaveAnalysisData(self):
        """ """
        saveresultbox = QtGui.QGroupBox("Export data", self)
        # Active widgets and connections.
        self._saveformat_list = QtGui.QComboBox()
        self._saveformat_list.addItems(["Tab delimited text file (*.txt)",
                                         "Excel file (*.xlsx)"])
        self._savedataset_button = QtGui.QPushButton("Save...")
        self.connect(self._savedataset_button, QtCore.SIGNAL("clicked()"), self._saveAnalysisData)                
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
        
#     def setAnalysisData(self, analysis_data):
#         """ """
#         self._analysisdata = analysis_data
#         self.updateViewedData()
#         self.updateAllTabs()    
    
    def updateViewedDataAndTabs(self):
        """ """
        self.updateViewedData()
        self.updateAllTabs()
        
    def hideViewedData(self):
        """ """
        # Clear table.
        self._tableview.tablemodel.setModeldata(None)
        self._refreshViewedDataTable()

        
    def updateViewedData(self):
        """ """
        # Clear table.
        self._tableview.tablemodel.setModeldata(None)
        self._refreshViewedDataTable()
        # 
        if not self._analysisdata.getData():
            return
        #
        selectedviewindex = self._viewdata_list.currentIndex()
        if selectedviewindex == 0:
            # View analysis data.
            # Convert from tree model to table model.
            targetdataset = envmonlib.DatasetTable()
            self._analysisdata.getData().convertToTableDataset(targetdataset)
            # View model.
            self._tableview.tablemodel.setModeldata(targetdataset)
            self._refreshViewedDataTable()
        elif selectedviewindex == 1:
            # View filtered data only.
            self._tab4widget.updateFilter() # Must be done before createFilteredDataset().
            filtereddataset = self._analysisdata.createFilteredDataset()
            # Convert from tree model to table model.
            targetdataset = envmonlib.DatasetTable()
            filtereddataset.convertToTableDataset(targetdataset)
            # View model.
            self._tableview.tablemodel.setModeldata(targetdataset)
            self._refreshViewedDataTable()
        elif selectedviewindex == 2:
            # Statistic data.
            self._tableview.tablemodel.setModeldata(self._statisticdata.getData())
            self._refreshViewedDataTable()
        elif selectedviewindex == 3:
            # Report data.
            self._tableview.tablemodel.setModeldata(self._reportdata.getData())
            self._refreshViewedDataTable()
        else:
            # Hide data.
            self._tableview.tablemodel.setModeldata(None)
            self._refreshViewedDataTable()
        
    def _refreshViewedDataTable(self):
        """ """
        self._tableview.tablemodel.reset() # Model data has changed.
        self._tableview.resizeColumnsToContents()

    def _saveAnalysisData(self):
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

    def clearAllTabs(self):
        """ """
        self._tab1widget.clear()
        self._tab2widget.clear()
        self._tab3widget.clear()
        self._tab4widget.clear()
        self._tab5widget.clear()
        self._tab6widget.clear()
        self._tab7widget.clear()
        self._tab8widget.clear()

    def updateAllTabs(self):
        """ """
        self._tab1widget.update()
        self._tab2widget.update()
        self._tab3widget.update()
        self._tab4widget.update()
        self._tab5widget.update()
        self._tab6widget.update()
        self._tab7widget.update()
        self._tab8widget.update()

    def updateFilter(self):
        """ Must be done before calls to createFilteredDataset(). """
        self._tab4widget.updateFilter()

    def viewAnalysisData(self):
        """ """
        if self._viewdata_list.currentIndex() < 4: # 4 = hide.
            self._viewdata_list.setCurrentIndex(0)
            self.updateViewedData()

    def viewStatisticData(self):
        """ """
        if self._viewdata_list.currentIndex() < 4: # 4 = hide.
            self._viewdata_list.setCurrentIndex(2)
            self.updateViewedData()

    def viewReportData(self):
        """ """
        if self._viewdata_list.currentIndex() < 4: # 4 = hide.
            self._viewdata_list.setCurrentIndex(3)
            self.updateViewedData()

