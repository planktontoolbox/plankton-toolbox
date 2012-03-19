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

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
#import datetime
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

    # ===== TAB: Select dataset(s) ===== 
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
        
        # Clear rows in comboboxes.
        self.__x_axis_column_list.clear()
        self.__x_axis_parameter_list.clear()
        self.__y_axis_column_list.clear()
        self.__y_axis_parameter_list.clear()
        self.__x_axis_column_list.addItems([u"Parameter:"])
        self.__y_axis_column_list.addItems([u"Parameter:"])

        
        
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
            
#        else:
#            # Clear rows in comboboxes.
#            self.__x_axis_column_list.clear()
#            self.__x_axis_parameter_list.clear()
#            self.__y_axis_column_list.clear()
#            self.__y_axis_parameter_list.clear()
#            self.__x_axis_column_list.addItems([u"Parameter:"])
#            self.__y_axis_column_list.addItems([u"Parameter:"])
        #    
        self.__updateCurrentData()
            

    # ===== TAB: Filter data ===== 
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


    # ===== TAB: Aggregate data ===== 
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


    # ===== TAB: Draw graph ===== 
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
        self.__plotindex_list = QtGui.QComboBox()
        self.__plotindex_list.addItems(["Time series 1", "Time series 2", "Time series 3", "Time series 4", 
                                       "X/Y plot 1", "X/Y plot 2", "X/Y plot 3", "X/Y plot 4"])
        self.__addplot_button = QtGui.QPushButton("Add plot")
        self.connect(self.__addplot_button, QtCore.SIGNAL("clicked()"), self.__addPlot)                
#        self.__addxyplot_button = QtGui.QPushButton("Add X/Y plot")
#        self.connect(self.__addxyplot_button, QtCore.SIGNAL("clicked()"), self.__addXYPlot)                

        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Select x-axis:")
        stretchlabel = QtGui.QLabel("")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__x_axis_column_list, gridrow, 1, 1, 1)
        form1.addWidget(self.__x_axis_parameter_list, gridrow, 2, 1, 1)
        form1.addWidget(stretchlabel, gridrow,3, 1, 9)
        gridrow += 1
#        label1 = QtGui.QLabel("Select column for y-axis:")
#        form1.addWidget(label1, gridrow, 0, 1, 1)
#        form1.addWidget(self.__y_axis_column_list, gridrow, 1, 1, 1)
        label1 = QtGui.QLabel("Select y-axis:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self.__y_axis_column_list, gridrow, 1, 1, 1)
        form1.addWidget(self.__y_axis_parameter_list, gridrow, 2, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(QtGui.QLabel("Select plot:"))
        hbox1.addWidget(self.__plotindex_list)
        hbox1.addWidget(self.__addplot_button)
#        hbox1.addWidget(self.__addxyplot_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox1)
        widget.setLayout(layout)                
        #
        return widget
        
#    def __addPlot(self):
#        """ """
#        selectedplotindex = self.__plotindex_list.currentIndex() 
#        if selectedplotindex in [0, 1, 2, 3]:
#            self.__addTimeseriesPlot(selectedplotindex)
#        else:
#            self.__addXYPlot(selectedplotindex - 4)
#        
#    def __addTimeseriesPlot(self, plot_index):
#        """ """
#        tool_manager.ToolManager().showToolByName(u'Graph plot')
#        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plot')       
#        #
#        x_data = []
#        y_data = []
#        date = None
#        #
#        selectedparameter = unicode(self.__y_axis_parameter_list.currentText())
#        ""
#        for visitnode in self.__copy_of_datsets[0].getChildren():
#            try:
#                date = visitnode.getData(u'Date')
#            except:
#                print(u'Wrong date...')
#                continue
#            #
#            for samplenode in visitnode.getChildren():
#                for variablenode in samplenode.getChildren():
#                    parameter = variablenode.getData(u'Parameter')
#                    #
##                    if parameter == u'TEMP':
#                    if parameter == selectedparameter:
#                        value = variablenode.getData(u'Value')
#                        x_data.append(date)
#                        y_data.append(value)
#        #
#        graphtool.addTimeseriesPlot(plot_index, x_data, y_data)
#            
#                        
#    def __addXYPlot(self, plot_index):
    def __addPlot(self):
        """ """
        tool_manager.ToolManager().showToolByName(u'Graph plot') # Show tool if hidden.
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plot')
        # Selected columns.
        x_column = unicode(self.__x_axis_column_list.currentText())
        y_column = unicode(self.__y_axis_column_list.currentText())
        # Selected parameters.
        x_param = None
        y_param = None
        if x_column == u"Parameter:":
            x_param = unicode(self.__x_axis_parameter_list.currentText())
        if y_column == u"Parameter:":
            y_param = unicode(self.__y_axis_parameter_list.currentText())
        # Check exports columns backwards.
        x_visit_key = None
        x_sample_key = None                      
        x_variable_key = None
        y_visit_key = None
        y_sample_key = None                      
        y_variable_key = None
        if x_column != u"Parameter:":
            for export_info in self.__copy_of_datsets[0].getExportTableColumns():
                if export_info.get('Header', u'') == x_column:
                    if export_info.get('Node', u'') == 'Visit':
                        x_visit_key =  export_info.get('Key', None)
                    elif export_info.get('Node', u'') == 'Sample':
                        x_sample_key =  export_info.get('Key', None)                        
                    elif export_info.get('Node', u'') == 'Variable':
                        x_variable_key =  export_info.get('Key', None)
        if y_column != u"Parameter:":
            for export_info in self.__copy_of_datsets[0].getExportTableColumns():
                if export_info.get('Header', u'') == y_column:
                    if export_info.get('Node', u'') == 'Visit':
                        y_visit_key =  export_info.get('Key', None)
                    elif export_info.get('Node', u'') == 'Sample':
                        y_sample_key =  export_info.get('Key', None)                        
                    elif export_info.get('Node', u'') == 'Variable':
                        y_variable_key =  export_info.get('Key', None)
        
        # Extract data.
        x_data = []
        y_data = []
        x_value = None
        y_value = None
        #
        for visitnode in self.__copy_of_datsets[0].getChildren(): 
            if x_visit_key: x_value = visitnode.getData(x_visit_key) # if x_visit_key else None
            if y_visit_key: y_value = visitnode.getData(y_visit_key) # if y_visit_key else None
            for samplenode in visitnode.getChildren():
                if x_sample_key: x_value = samplenode.getData(x_sample_key) # if x_sample_key else None
                if y_sample_key: y_value = samplenode.getData(y_sample_key) # if y_sample_key else None
                for variablenode in samplenode.getChildren():
                    #
                    if x_variable_key: x_value = variablenode.getData(x_variable_key) # if x_variable_key else None
                    if y_variable_key: y_value = variablenode.getData(y_variable_key) # if y_variable_key else None
                    #
                    if x_param or y_param:
                        parameter = variablenode.getData(u'Parameter')
                        if x_param:
                            if parameter == x_param:
                                x_value = variablenode.getData(u'Value')
                        if y_param:
                            if parameter == y_param:
                                y_value = variablenode.getData(u'Value')
                    # If NOT both are parameters, add data on variable level.
                    if not (x_param and y_param):
                        # Add values to lists if both values are available.
                        if (x_value and y_value):
                            x_data.append(x_value)
                            y_data.append(y_value)
                        # Clear used values.
                        if x_param: x_value = None    
                        if y_param: y_value = None    
                    # Clear used values.
                    if x_variable_key: x_value = None    
                    if x_variable_key: y_value = None
                # If both are parameters, add data on sample level.     
                if (x_param and y_param):
                    # Add values to lists if both values are available.
                    if (x_value and y_value):
                        x_data.append(x_value)
                        y_data.append(y_value)
                        # Clear used values.
                        if x_param: x_value = None    
                        if y_param: y_value = None    
                # Clear used values.
                if x_sample_key: x_value = None    
                if y_sample_key: y_value = None    
            # Clear used values.
            if x_visit_key: x_value = None    
            if y_visit_key: y_value = None    
        #

        
#        graphtool.addXYPlot(plot_index, x_data, y_data)
        selectedplotindex = self.__plotindex_list.currentIndex() 
        if selectedplotindex in [0, 1, 2, 3]:
            graphtool.addTimeseriesPlot(selectedplotindex, x_data, y_data)
        else:
            graphtool.addXYPlot(selectedplotindex - 4, x_data, y_data)



    # ===== CURRENT DATA =====    
    def __contentCurrentDataTable(self):
        """ """
        # Active widgets and connections.
        currentdatagroupbox = QtGui.QGroupBox("Current data", self)
        #
        # Active widgets and connections.
        self.__tableview = utils_qt.ToolboxQTableView()
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.__tableview)
        #
        currentdatagroupbox.setLayout(layout)
        #
        return currentdatagroupbox

    def __updateCurrentData(self):
        """ """



        # Note: Only one for test.
        if len(self.__copy_of_datsets[0].getChildren()) <= 0:
            # Clear table.
            self.__tableview.tablemodel.setModeldata(None)
            self.__refreshResultTable()
        else:
            # MMFW:
            
###            dataset = self.__copy_of_datsets

            
###            dataset = toolbox_datasets.ToolboxDatasets().getDatasetByIndex(index - 1)
            if isinstance(self.__copy_of_datsets[0], mmfw.DatasetTable):
                """ """
#                TODO: Not allowed.

#                self.__tableview.tablemodel.setModeldata(dataset)
#                self.__refreshResultTable()
            elif isinstance(self.__copy_of_datsets[0], mmfw.DatasetNode):
                # Tree dataset must be converted to table dataset before viewing.
                targetdataset = mmfw.DatasetTable()
                self.__copy_of_datsets[0].convertToTableDataset(targetdataset)
                #
                self.__tableview.tablemodel.setModeldata(targetdataset)
                self.__refreshResultTable()
    
    def __refreshResultTable(self):
        """ """
        self.__tableview.tablemodel.reset() # Model data has changed.
        self.__tableview.resizeColumnsToContents()


