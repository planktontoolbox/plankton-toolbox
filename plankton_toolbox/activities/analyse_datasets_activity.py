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
import plankton_toolbox.activities.activity_base as activity_base

class AnalyseDatasetsActivity(activity_base.ActivityBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent.
        super(AnalyseDatasetsActivity, self).__init__(name, parentwidget)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self.__activityheader = QtGui.QLabel('<h2>' + self.objectName() + '</h2>', self)
        self.__activityheader.setTextFormat(QtCore.Qt.RichText)
        self.__activityheader.setAlignment(QtCore.Qt.AlignHCenter)
        self.__activityheader.setStyleSheet(""" 
            * { color: white; background-color: #00677f; }
            """)
        contentLayout.addWidget(self.__activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self.__contentAnalyseTabs())
        contentLayout.addWidget(self.__contentLoadedDatasets(), 10)
    
    def __contentAnalyseTabs(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("", self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self.__contentFilterData(), "Filter data")
        tabWidget.addTab(self.__contentAggregateData(), "Aggregate data")
        tabWidget.addTab(self.__contentDrawGraph(), "Draw graph")
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    def __contentFilterData(self):
        """ """
        # Active widgets and connections.

        # Layout.
        widget = QtGui.QWidget()        
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
#        layout.addWidget(selectionbox)
#        layout.addWidget(resultbox)
        #
        return widget

    def __contentAggregateData(self):
        """ """
        # Active widgets and connections.

        # Layout.
        widget = QtGui.QWidget()        
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
#        layout.addWidget(selectionbox)
#        layout.addWidget(resultbox)
        #
        return widget

    def __contentDrawGraph(self):
        """ """
        # Active widgets and connections.

        # Layout.
        widget = QtGui.QWidget()        
        layout = QtGui.QVBoxLayout()
        widget.setLayout(layout)
#        layout.addWidget(selectionbox)
#        layout.addWidget(resultbox)
        #
        return widget

    # ===== LOADED DATASETS =====    
    def __contentLoadedDatasets(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("Current data", self)
        #
#        self.__datasets_table = utils_qt.ToolboxQTableView()
#        self.__datasets_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
#        
#        self.__datasettabledata.clear()
#        self.__datasettabledata.setHeader([u'Dataset      ', 
#                                           u'Type         ', 
#                                           u'Content      ', 
#                                           u'File         ', 
#                                           u'File path    ',
#                                           u'Matrix       ',
#                                           u'Import column',
#                                           u'Export column'])
#        self.__datasets_table.tablemodel.setModeldata(self.__datasettabledata)
#        self.__datasets_table.resizeColumnsToContents()
#        
#        self.__datasets_table.selectionModel.Rows
#        
#        # Listen for changes in the toolbox dataset list.
#        self.connect(toolbox_datasets.ToolboxDatasets(), 
#             QtCore.SIGNAL("datasetListChanged"), 
#             self.__updateDatasetList)
#        # Connection for selected row.
#        self.connect(self.__datasets_table.selectionModel, 
#                     QtCore.SIGNAL("currentRowChanged(QModelIndex, QModelIndex)"), 
#                     self.__selectionChanged)                
#        # Buttons.
#        self.__unloadalldatasets_button = QtGui.QPushButton("Unload all datasets")
#        self.__unloadmarkeddatasets_button = QtGui.QPushButton("Unload marked dataset(s)")
#        # Button connections.
#        self.connect(self.__unloadalldatasets_button, QtCore.SIGNAL("clicked()"), self.__unloadAllDatasets)                
#        self.connect(self.__unloadmarkeddatasets_button, QtCore.SIGNAL("clicked()"), self.__unloadMarkedDatasets)                
#        # Layout widgets.
#        buttonlayout = QtGui.QHBoxLayout()
#        buttonlayout.addWidget(self.__unloadalldatasets_button)
#        buttonlayout.addWidget(self.__unloadmarkeddatasets_button)
#        buttonlayout.addStretch(5)
#        #
#        widget = QtGui.QWidget()        
#        layout = QtGui.QVBoxLayout()
#        widget.setLayout(layout)
#        layout.addWidget(self.__datasets_table)
#        layout.addLayout(buttonlayout)
#        selectdatabox.setLayout(layout) 
        #       
        return selectdatabox


