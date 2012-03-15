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

import datetime


import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import copy
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.tools.tool_manager as tool_manager

import mmfw
import plankton_toolbox.toolbox.utils_qt as utils_qt


class AnalyseDatasetsActivity(activity_base.ActivityBase):
    """
    """
    
    def __init__(self, name, parentwidget):
        """ """
        # Lists of datasets selected for analysis.
        self.__selected_datsets = []
        self.__copy_of_datsets = []
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
        contentLayout.addWidget(self.__contentCurrentDataTable(), 10)
    
    def __contentAnalyseTabs(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("", self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self.__contentSelectDatasets(), "Select dataset(s)")
        tabWidget.addTab(self.__contentFilterData(), "Filter data")
        tabWidget.addTab(self.__contentAggregateData(), "Aggregate data")
        tabWidget.addTab(self.__contentDrawGraph(), "Draw graph")
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    def __contentSelectDatasets(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.
        """)        
        # TEST.
        self.__TEST_select_button = QtGui.QPushButton("TEST: Select first dataset")
        self.connect(self.__TEST_select_button, QtCore.SIGNAL("clicked()"), self.__TEST_SelectDatasets)                

        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(self.__TEST_select_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addStretch(1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget
        

    def __TEST_SelectDatasets(self):
        """ """
        print('TEST Select dataset.')
        if len(mmfw.Datasets().getDatasets()) > 0:
            currentdataset = mmfw.Datasets().getDatasets()[0]
            self.__selected_datsets = [currentdataset] # Only one for test.
            # Make deep copy of datasets for analysis.
            self.__copy_of_datsets = [copy.deepcopy(currentdataset)] # Only one for test.
            # Add rows in comboboxes.
            self.__x_axis_column_list.addItems([item[u'Header'] for item in self.__copy_of_datsets[0].getExportTableColumns()])
            self.__y_axis_column_list.addItems([item[u'Header'] for item in self.__copy_of_datsets[0].getExportTableColumns()])

            # Search for all parameters.
            parameterlist = []
            for visitnode in self.__copy_of_datsets[0].getChildren():
                for samplenode in visitnode.getChildren():
                    for variablenode in samplenode.getChildren():
                        parameter = variablenode.getData(u"Parameter")
                        if parameter not in parameterlist:
                            parameterlist.append(parameter)
            parameterlist.sort()
            self.__x_axis_parameter_list.addItems(parameterlist)
            self.__y_axis_parameter_list.addItems(parameterlist)
        else:
            # Clear rows in comboboxes.
            self.__x_axis_column_list.clear()
            self.__x_axis_parameter_list.clear()
            self.__y_axis_column_list.clear()
            self.__y_axis_parameter_list.clear()
            self.__x_axis_column_list.addItems([u"Parameter:"])
            self.__y_axis_column_list.addItems([u"Parameter:"])
            

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
        widget = QtGui.QWidget()
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.
        """)        
        # - Select column for x-axis:
        self.__x_axis_column_list = QtGui.QComboBox()
        self.__x_axis_column_list.addItems([u"Parameter:"])
        self.__x_axis_parameter_list = QtGui.QComboBox()
        # - Add available column names.
#        self.__x_axis_column_list.addItems(self._matrix_list)                
        # - Select column for y-axis:
        self.__y_axis_column_list = QtGui.QComboBox()
        self.__y_axis_column_list.addItems([u"Parameter:"])        
        self.__y_axis_parameter_list = QtGui.QComboBox()
        # - Add available column names.
#        self.__x_axis_column_list.addItems(self._matrix_list)                

        # Draw graph.
        self.__cleargraphs_button = QtGui.QPushButton("Clear graphs")
        self.connect(self.__cleargraphs_button, QtCore.SIGNAL("clicked()"), self.__clearGraphs)                
        self.__plotindex_list = QtGui.QComboBox()
        self.__plotindex_list.addItems(["1", "2", "3", "4"])
        self.__addtimeseries_button = QtGui.QPushButton("Add time series plot")
        self.connect(self.__addtimeseries_button, QtCore.SIGNAL("clicked()"), self.__addTimeseriesPlot)                
        self.__addxyplot_button = QtGui.QPushButton("Add X/Y plot")
        self.connect(self.__addxyplot_button, QtCore.SIGNAL("clicked()"), self.__addXYPlot)                

        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Select column for x-axis (time series):")
        stretchlabel = QtGui.QLabel("")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__x_axis_column_list, gridrow, 1, 1, 1)
        form1.addWidget(self.__x_axis_parameter_list, gridrow, 2, 1, 1)
        form1.addWidget(stretchlabel, gridrow,3, 1, 9)
        gridrow += 1
#        label1 = QtGui.QLabel("Select column for y-axis:")
#        form1.addWidget(label1, gridrow, 0, 1, 1)
#        form1.addWidget(self.__y_axis_column_list, gridrow, 1, 1, 1)
        label1 = QtGui.QLabel("Select parameter:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__y_axis_column_list, gridrow, 1, 1, 1)
        form1.addWidget(self.__y_axis_parameter_list, gridrow, 2, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(self.__cleargraphs_button)
        hbox1.addWidget(QtGui.QLabel("Index:"))
        hbox1.addWidget(self.__plotindex_list)
        hbox1.addWidget(self.__addtimeseries_button)
        hbox1.addWidget(self.__addxyplot_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget
        
    def __clearGraphs(self):
        """ """
        tool_manager.ToolManager().showToolByName(u'Graph plot')
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plot')
        graphtool.clearAll()

    def __addTimeseriesPlot(self):
        """ """
        tool_manager.ToolManager().showToolByName(u'Graph plot')
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plot')       
        #
        x_data = []
        y_data = []
        date = None
        #
        selectedparameter = self.__y_axis_column_list.currentText()
        ""
        for visitnode in self.__copy_of_datsets[0].getChildren():
            try:
                date = visitnode.getData(u'Date')
                time = visitnode.getData(u'Time')
                time = time if time else u'00:00:00' # Add if zero.
                #
                date = datetime.datetime.strptime((date), '%Y-%m-%d')
    #            date = datetime.datetime.strptime((date + ' ' + time), '%Y-%m-%d %H:%M:%S')
            except:
                print(u'Wrong date...')
                continue
            #
            for samplenode in visitnode.getChildren():
                for variablenode in samplenode.getChildren():
                    parameter = variablenode.getData(u'Parameter')
                    #
#                    if parameter == u'TEMP':
                    if parameter == selectedparameter:
                        value = variablenode.getData(u'Value')
                        x_data.append(date)
                        y_data.append(value)
        #
        graphtool.addTimeseriesPlot(0, x_data, y_data)
            
                        
    def __addXYPlot(self):
        """ """
        
#        tool_manager.ToolManager().showToolByName(u'Graph plot')
#        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plot')        
#        
#        graphtool.addXYPlot(self.__plotindex_list.currentIndex(), [1,3,2,4], [6,4,1,3])
       
        
        
        
        
        
        
        tool_manager.ToolManager().showToolByName(u'Graph plot')
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plot')
        #
        x_param = None
        y_param = None
        x_column = self.__x_axis_column_list.currentText()
        if x_column == u"Parameter:":
            x_param = self.__x_axis_parameter_list.currentText()
        y_column = self.__y_axis_column_list.currentText()
        if y_column == u"Parameter:":
            y_param = self.__y_axis_parameter_list.currentText()
        #
        x_data = []
        y_data = []
        #
        for visitnode in self.__copy_of_datsets[0].getChildren():            
            for samplenode in visitnode.getChildren():
                variable_x = None
                variable_y = None
                for variablenode in samplenode.getChildren():
                    parameter = variablenode.getData(u'Parameter')
                    #
                    if parameter == x_param:
                        variable_x = variablenode.getData(u'Value')
                    #
                    if parameter == y_param:
                        variable_y = variablenode.getData(u'Value')
                #
                if (variable_x and variable_y):
                    x_data.append(variable_x)
                    y_data.append(variable_y)
        #
        graphtool.addXYPlot(self.__plotindex_list.currentIndex(), x_data, y_data)

    # ===== CURRENT DATA =====    
    def __contentCurrentDataTable(self):
        """ """
        selectdatabox = QtGui.QGroupBox("Current data", self)
        # Active widgets and connections.
        self.__currentdatatableview = utils_qt.ToolboxQTableView()
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.__currentdatatableview)
        selectdatabox.setLayout(layout) 
        #       
        return selectdatabox

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


