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
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.utils_qt as utils_qt
import envmonlib

class AnalyseDatasetsTab6(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab6, self).__init__()
        #
        self._graph_plot_data = envmonlib.GraphPlotData()

    def setMainActivity(self, main_activity):
        """ """
        self._main_activity = main_activity
        self._analysisdata = main_activity.getAnalysisData()
                
    def clear(self):
        """ """
        self._x_axis_column_list.clear()
        self._x_axis_parameter_list.clear()
        self._x_axis_column_list.addItems([u"parameter:"])
        self._x_axis_column_list.setEnabled(False)
        self._x_axis_parameter_list.setEnabled(False)
        #
        self._y_axis_column_list.clear()
        self._y_axis_parameter_list.clear()
        self._y_axis_column_list.addItems([u"parameter:"])
        self._y_axis_column_list.setEnabled(False)
        self._y_axis_parameter_list.setEnabled(False)
        #
        self._z_axis_column_list.clear()
        self._z_axis_parameter_list.clear()
        self._z_axis_column_list.addItems([u"parameter:"])
        self._z_axis_column_list.setEnabled(False)
        self._z_axis_parameter_list.setEnabled(False)
        #
        self._updateEnabledDisabled()
        
    def update(self):
        """ """
        self.clear()
        currentdata = self._analysisdata.getData()
        if currentdata:        
            # For tab "Generic graphs".        
            self._x_axis_column_list.addItems([item[u'header'] for item in currentdata.getExportTableColumns()])
            self._y_axis_column_list.addItems([item[u'header'] for item in currentdata.getExportTableColumns()])
            self._z_axis_column_list.addItems([item[u'header'] for item in currentdata.getExportTableColumns()])
            # Search for all parameters in current data.
            parameterset = set()
            for visitnode in currentdata.getChildren():
                for samplenode in visitnode.getChildren():
                    for variablenode in samplenode.getChildren():
                        parameterset.add(variablenode.getData(u"parameter"))
            parameterlist = sorted(parameterset)
            #
            self._x_axis_parameter_list.addItems(parameterlist)
            self._y_axis_parameter_list.addItems(parameterlist)
            self._z_axis_parameter_list.addItems(parameterlist)
            #  Make combo-boxes visible.
            self._updateEnabledDisabled()

    # ===== TAB: Generic graphs ===== 
    def contentGenericGraphs(self):
        """ """
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Plot almost any combination of data you like. 
        These graphs are in general not as nice looking as the pre-defined graphs but are more flexible.
        """)        
        # Select type of data object.
        self._numberofvariables_list = QtGui.QComboBox()
        self._numberofvariables_list.addItems(["One variable (Y)", "Two variables (X and Y)", "Three variables (X, Y and Z)"])
        self.connect(self._numberofvariables_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._clearPlotData)                
        # - Select column for x-axis:
        self._x_axis_column_list = QtGui.QComboBox()
        self._x_axis_column_list.setMinimumContentsLength(20)
        self._x_axis_parameter_list = QtGui.QComboBox()        
        self._x_axis_parameter_list.setMinimumContentsLength(20)
        self._x_axistype_list = QtGui.QComboBox()
        self._x_axistype_list.addItems(["Integer", "Float", "Date", "Time", "Datetime", "Text"])
        self.connect(self._x_axis_column_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._updateEnabledDisabled)                
        # - Select column for y-axis:
        self._y_axis_column_list = QtGui.QComboBox()
        self._y_axis_column_list.setMinimumContentsLength(20)
        self._y_axis_parameter_list = QtGui.QComboBox()
        self._y_axis_parameter_list.setMinimumContentsLength(20)
        self._y_axistype_list = QtGui.QComboBox()
        self._y_axistype_list.addItems(["Integer", "Float", "Date", "Time", "Datetime", "Text"])
        self.connect(self._y_axis_column_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._updateEnabledDisabled)                
        # - Select column for z-axis:
        self._z_axis_column_list = QtGui.QComboBox()
        self._z_axis_column_list.setMinimumContentsLength(20)
        self._z_axis_parameter_list = QtGui.QComboBox()
        self._z_axis_parameter_list.setMinimumContentsLength(20)
        self._z_axistype_list = QtGui.QComboBox()
        self._z_axistype_list.addItems(["Integer", "Float", "Date", "Time", "Datetime", "Text"])
        self.connect(self._z_axis_column_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._updateEnabledDisabled)                
        # Info, current number of subplots.
        self._subplotsinfo_label = QtGui.QLabel()
        # Clear data object.
        self._clear_button = QtGui.QPushButton("Clear plot data")
        self.connect(self._clear_button, QtCore.SIGNAL("clicked()"), self._clearPlotData)                
        # Add subplot data to the Graph plotter tool.
        self._addsubplotdata_button = QtGui.QPushButton("Add plot data to Graph plotter")
        self.connect(self._addsubplotdata_button, QtCore.SIGNAL("clicked()"), self._addPlot)                

        # Layout widgets.
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(QtGui.QLabel("Select number of variables in each plot:"))
        hbox1.addWidget(self._numberofvariables_list)
        hbox1.addStretch(10)
        #
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Select x-axis:")
        label2 = QtGui.QLabel("Parameter:")
        label3 = QtGui.QLabel("Type:")
        stretchlabel = QtGui.QLabel("")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._x_axis_column_list, gridrow, 1, 1, 1)
        form1.addWidget(label2, gridrow, 2, 1, 1)
        form1.addWidget(self._x_axis_parameter_list, gridrow, 3, 1, 1)
        form1.addWidget(label3, gridrow, 4, 1, 1)
        form1.addWidget(self._x_axistype_list, gridrow, 5, 1, 1)
        form1.addWidget(stretchlabel, gridrow,6, 1, 20)
        gridrow += 1
        label1 = QtGui.QLabel("Select y-axis:")
        label2 = QtGui.QLabel("Parameter:")
        label3 = QtGui.QLabel("Type:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._y_axis_column_list, gridrow, 1, 1, 1)
        form1.addWidget(label2, gridrow, 2, 1, 1)
        form1.addWidget(self._y_axis_parameter_list, gridrow, 3, 1, 1)
        form1.addWidget(label3, gridrow, 4, 1, 1)
        form1.addWidget(self._y_axistype_list, gridrow, 5, 1, 1)
        form1.addWidget(stretchlabel, gridrow,6, 1, 20)
        gridrow += 1
        label1 = QtGui.QLabel("Select z-axis:")
        label2 = QtGui.QLabel("Parameter:")
        label3 = QtGui.QLabel("Type:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._z_axis_column_list, gridrow, 1, 1, 1)
        form1.addWidget(label2, gridrow, 2, 1, 1)
        form1.addWidget(self._z_axis_parameter_list, gridrow, 3, 1, 1)
        form1.addWidget(label3, gridrow, 4, 1, 1)
        form1.addWidget(self._z_axistype_list, gridrow, 5, 1, 1)
        form1.addWidget(stretchlabel, gridrow,6, 1, 20)
        #
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(self._subplotsinfo_label)
        hbox2.addStretch(10)
        hbox2.addWidget(self._clear_button)
        hbox2.addWidget(self._addsubplotdata_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(hbox1)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox2)
        self.setLayout(layout)                
        #
        self._updateEnabledDisabled()
        #
        return self
        
    def _clearPlotData(self):
        """ """
        self._graph_plot_data.clear()
        # Enable/disable x, y or z-related items.
        self._updateEnabledDisabled()
        #
        self._subplotsinfo_label.setText(u"No subplots.")

    def _updateEnabledDisabled(self):
        """ """
        # Default is one variable.
        self._x_axis_column_list.setEnabled(False)
        self._x_axis_parameter_list.setEnabled(False)
        self._x_axistype_list.setEnabled(False)
        self._y_axis_column_list.setEnabled(True)
        self._y_axis_parameter_list.setEnabled(True)
        self._y_axistype_list.setEnabled(True)
        self._z_axis_column_list.setEnabled(False)
        self._z_axis_parameter_list.setEnabled(False)
        self._z_axistype_list.setEnabled(False)
        if self._numberofvariables_list.currentIndex() == 1: # Two variables.
            self._x_axis_column_list.setEnabled(True)
            self._x_axis_parameter_list.setEnabled(True)
            self._x_axistype_list.setEnabled(True)                        
        elif self._numberofvariables_list.currentIndex() == 2: # Three variables.      
            self._x_axis_column_list.setEnabled(True)
            self._x_axis_parameter_list.setEnabled(True)
            self._x_axistype_list.setEnabled(True)                        
            self._z_axis_column_list.setEnabled(True)
            self._z_axis_parameter_list.setEnabled(True)
            self._z_axistype_list.setEnabled(True)        
        # Hide parameter column if not used.
        if self._x_axis_column_list.currentIndex()!= 0:
            self._x_axis_parameter_list.setEnabled(False)
        if self._y_axis_column_list.currentIndex() != 0:
            self._y_axis_parameter_list.setEnabled(False)
        if self._z_axis_column_list.currentIndex() != 0:
            self._z_axis_parameter_list.setEnabled(False)
            
#    def _addPlot(self):
#        """ """
#        currentdata = self._analysisdata.getData()
#        if not currentdata:
#            return # Can't plot from empty dataset
#        # Show the Graph plotter tool if hidden. 
#        tool_manager.ToolManager().showToolByName(u'Graph plotter')
#        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plotter')
#        # Selected columns.
#        x_column = unicode(self._x_axis_column_list.currentText())
#        y_column = unicode(self._y_axis_column_list.currentText())
#        z_column = unicode(self._y_axis_column_list.currentText())
#        # Selected parameters.
#        x_param = None
#        y_param = None
#        z_param = None
#        if x_column == u"Parameter:":
#            x_param = unicode(self._x_axis_parameter_list.currentText())
#        if y_column == u"Parameter:":
#            y_param = unicode(self._y_axis_parameter_list.currentText())
#        if z_column == u"Parameter:":
#            z_param = unicode(self._z_axis_parameter_list.currentText())
#        # Check exports columns backwards.
#        x_visit_key = None
#        x_sample_key = None                      
#        x_variable_key = None
#        y_visit_key = None
#        y_sample_key = None                      
#        y_variable_key = None
#        z_visit_key = None
#        z_sample_key = None                      
#        z_variable_key = None
#        if x_column != u"Parameter:":
#            for export_info in currentdata.getExportTableColumns():
#                if export_info.get('Header', u'') == x_column:
#                    if export_info.get('Node', u'') == 'Visit':
#                        x_visit_key =  export_info.get('Key', None)
#                    elif export_info.get('Node', u'') == 'Sample':
#                        x_sample_key =  export_info.get('Key', None)                        
#                    elif export_info.get('Node', u'') == 'Variable':
#                        x_variable_key =  export_info.get('Key', None)
#        if y_column != u"Parameter:":
#            for export_info in currentdata.getExportTableColumns():
#                if export_info.get('Header', u'') == y_column:
#                    if export_info.get('Node', u'') == 'Visit':
#                        y_visit_key =  export_info.get('Key', None)
#                    elif export_info.get('Node', u'') == 'Sample':
#                        y_sample_key =  export_info.get('Key', None)                        
#                    elif export_info.get('Node', u'') == 'Variable':
#                        y_variable_key =  export_info.get('Key', None)
#        if z_column != u"Parameter:":
#            for export_info in currentdata.getExportTableColumns():
#                if export_info.get('Header', u'') == z_column:
#                    if export_info.get('Node', u'') == 'Visit':
#                        z_visit_key =  export_info.get('Key', None)
#                    elif export_info.get('Node', u'') == 'Sample':
#                        z_sample_key =  export_info.get('Key', None)                        
#                    elif export_info.get('Node', u'') == 'Variable':
#                        z_variable_key =  export_info.get('Key', None)
#        
#        # Extract data.
#        x_data = []
#        y_data = []
#        z_data = []
#        x_value = None
#        y_value = None
#        z_value = None
#        #
#        
#        selected_dict = self._main_activity.getSelectDataDict()
#        selected_startdate = selected_dict[u'Start date']
#        selected_enddate = selected_dict[u'End date']
##        selected_stations = selected_dict[u'Stations']
#        selected_visits = selected_dict[u'Visits']
#        selected_minmaxdepth =  selected_dict[u'Min max depth']
#        selected_taxon = selected_dict[u'Taxon']
#        selected_trophy = selected_dict[u'Trophy']
#        
#        
#        
#        for visitnode in currentdata.getChildren():
#            
#            if selected_startdate > visitnode.getData(u'Date'):
#                continue
#            if selected_enddate < visitnode.getData(u'Date'):
#                continue
##            if visitnode.getData(u'Station name') not in selected_stations:
##                continue
#            if (visitnode.getData(u'Station name') + u' : ' + visitnode.getData(u'Date')) not in selected_visits:
#                continue
#
#            
#             
#            if x_visit_key: x_value = visitnode.getData(x_visit_key) # if x_visit_key else None
#            if y_visit_key: y_value = visitnode.getData(y_visit_key) # if y_visit_key else None
#            if z_visit_key: y_value = visitnode.getData(y_visit_key) # if y_visit_key else None
#            for samplenode in visitnode.getChildren():
#            
#                minmax = samplenode.getData(u'Sample min depth') + u'-' + samplenode.getData(u'Sample max depth')
#                if minmax not in selected_minmaxdepth:
#                    continue
#                
#                
#                if x_sample_key: x_value = samplenode.getData(x_sample_key) # if x_sample_key else None
#                if y_sample_key: y_value = samplenode.getData(y_sample_key) # if y_sample_key else None
#                if z_sample_key: y_value = samplenode.getData(y_sample_key) # if y_sample_key else None
#                for variablenode in samplenode.getChildren():
#                
#                    if variablenode.getData(u'Taxon name') not in selected_taxon:
#                        continue
#                    if variablenode.getData(u'Trophy') not in selected_trophy:
#                        continue
#                    
#                    
#                    
#                    #
#                    if x_variable_key: x_value = variablenode.getData(x_variable_key) # if x_variable_key else None
#                    if y_variable_key: y_value = variablenode.getData(y_variable_key) # if y_variable_key else None
#                    if z_variable_key: y_value = variablenode.getData(y_variable_key) # if y_variable_key else None
#                    #
#                    if x_param or y_param:
#                        parameter = variablenode.getData(u'Parameter')
#                        if x_param:
#                            if parameter == x_param:
#                                x_value = variablenode.getData(u'Value')
#                        if y_param:
#                            if parameter == y_param:
#                                y_value = variablenode.getData(u'Value')
#                    # If NOT both are parameters, add data on variable level.
#                    if not (x_param and y_param):
#                        # Add values to lists if both values are available.
#                        if (x_value and y_value):
#                            x_data.append(x_value)
#                            y_data.append(y_value)
#                        # Clear used values.
#                        if x_param: x_value = None    
#                        if y_param: y_value = None    
#                    # Clear used values.
#                    if x_variable_key: x_value = None    
#                    if x_variable_key: y_value = None
#                # If both are parameters, add data on sample level.     
#                if (x_param and y_param):
#                    # Add values to lists if both values are available.
#                    if (x_value and y_value):
#                        x_data.append(x_value)
#                        y_data.append(y_value)
#                        # Clear used values.
#                        if x_param: x_value = None    
#                        if y_param: y_value = None    
#                # Clear used values.
#                if x_sample_key: x_value = None    
#                if y_sample_key: y_value = None    
#            # Clear used values.
#            if x_visit_key: x_value = None    
#            if y_visit_key: y_value = None    
#        #
#
##        # Check if this is a time series or not.
##        selectedplotindex = self._plotindex_list.currentIndex() 
##        if selectedplotindex in [0, 1, 2, 3]:
##            graphtool.addTimeseriesPlot(selectedplotindex, x_data, y_data)
##        else:
##            graphtool.addXYPlot(selectedplotindex - 4, x_data, y_data)
#
#
#        # Convert numeric values. 
#        # TODO: Type info should be in import parser.
#        for index, item in enumerate(x_data):
#            try:
#                x_data[index] = item.replace(u',', u'.')
#            except:
#                pass
#        for index, item in enumerate(y_data):
#            try:
#                y_data[index] = item.replace(u',', u'.')
#            except:
#                pass
#
#
#
#        # Create plot data object.
##        self._graph_plot_data = envmonlib.PlotDataTwoVariables(x_type = u'',
##                                                  title = y_column + " / " + x_column, 
##                                                  x_label = x_column,
##                                                  y_label = y_column)
#
#        plotdatainfo = self._graph_plot_data.getPlotDataInfo()
#
#        plotdatainfo[u'Title'] = u'Generic graph'
##        plotdatainfo[u'X label'] = u''
##        plotdatainfo[u'Y label'] = u''
#        plotdatainfo[u'X type'] = unicode(self._x_axistype_list.currentText())
##        plotdatainfo[u'X format'] = u''
#        plotdatainfo[u'Y type'] = unicode(self._y_axistype_list.currentText())
##        plotdatainfo[u'Y format'] = u''
#
#        self._graph_plot_data.setPlotDataInfo(plotdatainfo)
#
#
#        # Add plot data.
#        self._graph_plot_data.addPlot(plot_name = y_column + " / " + x_column, 
#                         x_array = x_data, 
#                         y_array = y_data, 
#                         x_label = x_column,
#                         y_label = y_column)
#        # View in Graph plotter tool.
##        graphtool.setChartSelection(chart = u"Bar chart",
##                                    combined = True, stacked = False, y_log_scale = False)
#        graphtool.setPlotData(self._graph_plot_data)



##########################################################################################################


    def _addPlot(self):
        """ """
        # Show the Graph plotter tool if hidden. 
        tool_manager.ToolManager().showToolByName(u'Graph plotter')
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plotter')
        #
        # Selected columns.
        x_selected_column = unicode(self._x_axis_column_list.currentText())
        y_selected_column = unicode(self._y_axis_column_list.currentText())
        z_selected_column = unicode(self._z_axis_column_list.currentText())
        # Selected parameters.
        x_selected_param = unicode(self._x_axis_parameter_list.currentText())
        y_selected_param = unicode(self._y_axis_parameter_list.currentText())
        z_selected_param = unicode(self._z_axis_parameter_list.currentText())
        # Selected types.
        x_selected_type = unicode(self._x_axistype_list.currentText())
        y_selected_type = unicode(self._y_axistype_list.currentText())
        z_selected_type = unicode(self._z_axistype_list.currentText())
        #
        plotdatainfo = self._graph_plot_data.getPlotDataInfo()
        #
        plotdatainfo[u'title'] = u'Generic graph'
        plotdatainfo[u'x_label'] = x_selected_column if x_selected_column != u"Parameter:" else x_selected_param
        plotdatainfo[u'x_type'] = x_selected_type
        plotdatainfo[u'x_format'] = u''
        #
        plotdatainfo[u'y_label'] = y_selected_column if y_selected_column != u"Parameter:" else y_selected_param
        plotdatainfo[u'y_type'] = y_selected_type
        plotdatainfo[u'y_format'] = u''
        #
        plotdatainfo[u'z_label'] = z_selected_column if z_selected_column != u"Parameter:" else z_selected_param
        plotdatainfo[u'z_type'] = z_selected_type
        plotdatainfo[u'z_format'] = u''
        #
        # Add plot data.

#        x_data = [1,2,3] 
#        y_data = [4,5,6] 
#        z_data = [7,8,9] 
        x_column = u'x_column'
        y_column = u'y_column'
        z_column = u'z_column'


        #
        x_data, y_data, z_data = self._getFilteredData()
        #
        if x_data and (x_selected_type == u'Number'):
            for index, item in enumerate(x_data):
                try:
                    x_data[index] = float(item)
                except:
                    x_data[index] = 0.0
        if y_data and (y_selected_type == u'Number'):
            for index, item in enumerate(y_data):
                try:
                    y_data[index] = float(item)
                except:
                    y_data[index] = 0.0
        if z_data and (z_selected_type == u'Number'):
            for index, item in enumerate(z_data):
                try:
                    z_data[index] = float(item)
                except:
                    z_data[index] = 0.0
        
        
        
        
        
        plot_name = y_selected_column if y_selected_column != u"Parameter:" else y_selected_param + u' / ' + \
                    x_selected_column if x_selected_column != u"Parameter:" else x_selected_param
        x_label = u''
        x_array = None
        y_label = u''
        y_array = None
        z_label = u''
        z_array = None

        self._graph_plot_data.addPlot(
                        plot_name = y_column + " / " + x_column, 
                         x_label = x_selected_column if x_selected_column != u"Parameter:" else x_selected_param,
                         x_array = x_data,
                         y_label = y_selected_column if y_selected_column != u"Parameter:" else y_selected_param,
                         y_array = y_data, 
                         z_label = z_selected_column if z_selected_column != u"Parameter:" else z_selected_param,
                         z_array = z_data) 
        # View in Graph plotter tool.
        graphtool.setPlotData(self._graph_plot_data)


    
    
    
    def _getFilteredData(self):
        """ """
        currentdata = self._analysisdata.getData()
        if not currentdata:
            return # Can't plot from empty dataset
        # Selected columns.
        x_column = unicode(self._x_axis_column_list.currentText())
        y_column = unicode(self._y_axis_column_list.currentText())
        z_column = unicode(self._z_axis_column_list.currentText())
        # Selected types.
        x_selected_type = unicode(self._x_axistype_list.currentText())
        y_selected_type = unicode(self._y_axistype_list.currentText())
        z_selected_type = unicode(self._z_axistype_list.currentText())
        # Selected parameters.
        x_param = None
        y_param = None
        z_param = None
        if x_column == u"Parameter:":
            x_param = unicode(self._x_axis_parameter_list.currentText())
        if y_column == u"Parameter:":
            y_param = unicode(self._y_axis_parameter_list.currentText())
        if z_column == u"Parameter:":
            z_param = unicode(self._z_axis_parameter_list.currentText())
        # Check exports columns backwards. Export columns are declared in the dataset import parser files.
        x_visit_key = None
        x_sample_key = None                      
        x_variable_key = None
        y_visit_key = None
        y_sample_key = None                      
        y_variable_key = None
        z_visit_key = None
        z_sample_key = None                      
        z_variable_key = None
        if x_column != u"Parameter:":
            for export_info in currentdata.getExportTableColumns():
                if export_info.get('Header', u'') == x_column:
                    if export_info.get('Node', u'') == 'Visit':
                        x_visit_key =  export_info.get('Key', None)
                    elif export_info.get('Node', u'') == 'Sample':
                        x_sample_key =  export_info.get('Key', None)                        
                    elif export_info.get('Node', u'') == 'Variable':
                        x_variable_key =  export_info.get('Key', None)
        if y_column != u"Parameter:":
            for export_info in currentdata.getExportTableColumns():
                if export_info.get('Header', u'') == y_column:
                    if export_info.get('Node', u'') == 'Visit':
                        y_visit_key =  export_info.get('Key', None)
                    elif export_info.get('Node', u'') == 'Sample':
                        y_sample_key =  export_info.get('Key', None)                        
                    elif export_info.get('Node', u'') == 'Variable':
                        y_variable_key =  export_info.get('Key', None)
        if z_column != u"Parameter:":
            for export_info in currentdata.getExportTableColumns():
                if export_info.get('Header', u'') == z_column:
                    if export_info.get('Node', u'') == 'Visit':
                        z_visit_key =  export_info.get('Key', None)
                    elif export_info.get('Node', u'') == 'Sample':
                        z_sample_key =  export_info.get('Key', None)                        
                    elif export_info.get('Node', u'') == 'Variable':
                        z_variable_key =  export_info.get('Key', None)
                        
                        
        # Remove depending on selected number of variables:
        numberofvariables = self._numberofvariables_list.currentIndex() + 1
        #
        if numberofvariables in [1]: # One variables.
            x_param = None
            x_visit_key = None
            x_sample_key = None                      
            x_variable_key = None        
        if numberofvariables in [1, 2]: # One or two variables.
            z_param = None
            z_visit_key = None
            z_sample_key = None                      
            z_variable_key = None
                        
        # Extract data.
        x_data = []
        y_data = []
        z_data = []
        x_value = None
        y_value = None
        z_value = None
        # Get data for filtering.
        selected_dict = self._analysisdata.getSelectDataDict()
        selected_startdate = selected_dict[u'Start date']
        selected_enddate = selected_dict[u'End date']
#        selected_stations = selected_dict[u'Stations']
        selected_visits = selected_dict[u'Visits']
        selected_minmaxdepth =  selected_dict[u'Min max depth']
        selected_taxon = selected_dict[u'Taxon']
        selected_trophy = selected_dict[u'Trophy']
        # Iterate over visits. 
        for visitnode in currentdata.getChildren():
            # Filter.
            if selected_startdate > visitnode.getData(u'Date'):
                continue
            if selected_enddate < visitnode.getData(u'Date'):
                continue
#            if visitnode.getData(u'Station name') not in selected_stations:
#                continue
            if (unicode(visitnode.getData(u'Station name')) + u' : ' + unicode(visitnode.getData(u'Date'))) not in selected_visits:
                continue
            # Get data.
            if x_visit_key: x_value = visitnode.getData(x_visit_key) # if x_visit_key else None
            if y_visit_key: y_value = visitnode.getData(y_visit_key) # if y_visit_key else None
            if z_visit_key: z_value = visitnode.getData(z_visit_key) # if z_visit_key else None
            # Check if finished.
            if y_value and (numberofvariables == 1):
                y_data.append(y_value)
                x_value = y_value = z_value = None
                continue
            if x_value and y_value and (numberofvariables == 2):
                x_data.append(x_value)
                y_data.append(y_value)
                x_value = y_value = z_value = None
                continue            
            if x_value and y_value and z_value and (numberofvariables == 3):
                x_data.append(x_value)
                y_data.append(y_value)
                z_data.append(z_value)
                x_value = y_value = z_value = None
                continue            
            # Iterate over samples.
            for samplenode in visitnode.getChildren():
                # Filter.
                minmax = unicode(samplenode.getData(u'Sample min depth')) + u'-' + unicode(samplenode.getData(u'Sample max depth'))
                if minmax not in selected_minmaxdepth:
                    continue
                # Get data.
                if x_sample_key: x_value = samplenode.getData(x_sample_key) # if x_sample_key else None
                if y_sample_key: y_value = samplenode.getData(y_sample_key) # if y_sample_key else None
                if z_sample_key: z_value = samplenode.getData(z_sample_key) # if z_sample_key else None
                # Check if finished.
                if y_value and (numberofvariables == 1):
                    y_data.append(y_value)
                    x_value = y_value = z_value = None
                    continue
                if x_value and y_value and (numberofvariables == 2):
                    x_data.append(x_value)
                    y_data.append(y_value)
                    x_value = y_value = z_value = None
                    continue            
                if x_value and y_value and z_value and (numberofvariables == 3):
                    x_data.append(x_value)
                    y_data.append(y_value)
                    z_data.append(z_value)
                    x_value = y_value = z_value = None
                    continue            
                # Iterate over variables.
                for variablenode in samplenode.getChildren():
                    # Filter
                    if variablenode.getData(u'Taxon name') not in selected_taxon:
                        continue
                    if variablenode.getData(u'Trophy') not in selected_trophy:
                        continue
                    # Get data.
                    if x_variable_key: x_value = variablenode.getData(x_variable_key) # if x_variable_key else None
                    if y_variable_key: y_value = variablenode.getData(y_variable_key) # if y_variable_key else None
                    if z_variable_key: z_value = variablenode.getData(z_variable_key) # if z_variable_key else None
                    # Get parameter data.
                    if x_param or y_param or z_param:
                        parameter = variablenode.getData(u'Parameter')
                        if x_param:
                            if parameter == x_param:
                                x_value = variablenode.getData(u'Value')
                        if y_param:
                            if parameter == y_param:
                                y_value = variablenode.getData(u'Value')
                        if z_param:
                            if parameter == z_param:
                                z_value = variablenode.getData(u'Value')
                                
                    # Check if parameters are finished.
                    # Break the variable loop if all parameters are found.
#                    if y_param and y_value and (numberofvariables == 1):
#                        y_data.append(y_value)
#                        x_value = y_value = z_value = None
#                        break
                    if x_param and y_param and x_value and y_value and (numberofvariables == 2):
                        x_data.append(x_value)
                        y_data.append(y_value)
                        x_value = y_value = z_value = None
                        break            
                    if x_param and y_param and z_param and x_value and y_value and z_value and (numberofvariables == 3):
                        x_data.append(x_value)
                        y_data.append(y_value)
                        z_data.append(z_value)
                        x_value = y_value = z_value = None
                        break
                    # Check if finished.
                    if y_value and (numberofvariables == 1):
                        y_data.append(y_value)
                        x_value = y_value = z_value = None
                        continue
                    if x_value and y_value and (numberofvariables == 2):
                        x_data.append(x_value)
                        y_data.append(y_value)
                        x_value = y_value = z_value = None
                        continue            
                    if x_value and y_value and z_value and (numberofvariables == 3):
                        x_data.append(x_value)
                        y_data.append(y_value)
                        z_data.append(z_value)
                        x_value = y_value = z_value = None
                        continue            
        #
#        # Convert numeric values. 
#        # TODO: Type info should be in import parser.
#        if x_selected_type == u'Number':
#            for index, item in enumerate(x_data):
#                try:
#                    x_data[index] = item.replace(u',', u'.')
#                except:
#                    pass
#        if y_selected_type == u'Number':
#            for index, item in enumerate(y_data):
#                try:
#                    y_data[index] = item.replace(u',', u'.')
#                except:
#                    pass
#        if z_selected_type == u'Number':
#            for index, item in enumerate(z_data):
#                try:
#                    z_data[index] = item.replace(u',', u'.')
#                except:
#                    pass

        return x_data, y_data, z_data

#        # Create plot data object.
##        self._graph_plot_data = envmonlib.PlotDataTwoVariables(x_type = u'',
##                                                  title = y_column + " / " + x_column, 
##                                                  x_label = x_column,
##                                                  y_label = y_column)
#
#        plotdatainfo = self._graph_plot_data.getPlotDataInfo()
#
#        plotdatainfo[u'Title'] = u'Generic graph'
##        plotdatainfo[u'X label'] = u''
##        plotdatainfo[u'Y label'] = u''
#        plotdatainfo[u'X type'] = unicode(self._x_axistype_list.currentText())
##        plotdatainfo[u'X format'] = u''
#        plotdatainfo[u'Y type'] = unicode(self._y_axistype_list.currentText())
##        plotdatainfo[u'Y format'] = u''
#
##########        self._graph_plot_data.setPlotDataInfo(plotdatainfo)
#
#
#        # Add plot data.
#        self._graph_plot_data.addPlot(plot_name = y_column + " / " + x_column, 
#                         x_array = x_data, 
#                         y_array = y_data, 
#                         x_label = x_column,
#                         y_label = y_column)
#        # View in Graph plotter tool.
##        graphtool.setChartSelection(chart = u"Bar chart",
##                                    combined = True, stacked = False, y_log_scale = False)
#        graphtool.setPlotData(self._graph_plot_data)



