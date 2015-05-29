#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_manager as tool_manager
# import plankton_toolbox.toolbox.utils_qt as utils_qt
# import plankton_toolbox.toolbox.help_texts as help_texts
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
        self._type_list_values = ["float", "integer", "text", "date", "datetime"]

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
        self._updateEnabledDisabledAndTypes()
        
    def update(self):
        """ """
        self.clear()
        analysisdata = self._analysisdata.getData()
        if analysisdata:        
            # For tab "Generic graphs".
            items = [item[u'header'] for item in analysisdata.getExportTableColumns()]        
            self._x_axis_column_list.addItems(items)
            self._y_axis_column_list.addItems(items)
            self._z_axis_column_list.addItems(items)
            # Search for all parameters in analysis data.
            parameterset = set()
            for visitnode in analysisdata.getChildren():
                for samplenode in visitnode.getChildren():
                    for variablenode in samplenode.getChildren():
                        parameterset.add(variablenode.getData(u'parameter') + u' (' + variablenode.getData(u'unit') + u')')
            parameterlist = sorted(parameterset)
            #
            self._x_axis_parameter_list.addItems(parameterlist)
            self._y_axis_parameter_list.addItems(parameterlist)
            self._z_axis_parameter_list.addItems(parameterlist)
            #  Make combo-boxes visible.
            self._updateEnabledDisabledAndTypes()

    # ===== TAB: Generic graphs ===== 
    def contentGenericGraphs(self):
        """ """
        # Active widgets and connections.
#         introlabel = utils_qt.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText(u'AnalyseDatasetsTab6_intro'))
        # Select type of data object.
        self._numberofvariables_list = QtGui.QComboBox()
        self._numberofvariables_list.addItems(["One variable (Y)", 
                                               "Two variables (X and Y)", 
                                               "Three variables (X, Y and Z)"])
        self._numberofvariables_list.setCurrentIndex(1)
        self.connect(self._numberofvariables_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._clearPlotData)                
        # - Select column for x-axis:
        self._x_axis_column_list = QtGui.QComboBox()
        self._x_axis_column_list.setMinimumContentsLength(20)
        self._x_axis_column_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._x_axis_parameter_list = QtGui.QComboBox()        
        self._x_axis_parameter_list.setMinimumContentsLength(20)
        self._x_axis_parameter_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._x_axistype_list = QtGui.QComboBox()
        self._x_axistype_list.addItems(self._type_list_values)
        self.connect(self._x_axis_column_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._updateEnabledDisabledAndTypes)                
        # - Select column for y-axis:
        self._y_axis_column_list = QtGui.QComboBox()
        self._y_axis_column_list.setMinimumContentsLength(20)
        self._y_axis_column_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._y_axis_parameter_list = QtGui.QComboBox()
        self._y_axis_parameter_list.setMinimumContentsLength(20)
        self._y_axis_parameter_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._y_axistype_list = QtGui.QComboBox()
        self._y_axistype_list.addItems(self._type_list_values)
        self.connect(self._y_axis_column_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._updateEnabledDisabledAndTypes)                
        # - Select column for z-axis:
        self._z_axis_column_list = QtGui.QComboBox()
        self._z_axis_column_list.setMinimumContentsLength(20)
        self._z_axis_column_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._z_axis_parameter_list = QtGui.QComboBox()
        self._z_axis_parameter_list.setMinimumContentsLength(20)
        self._z_axis_parameter_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self._z_axistype_list = QtGui.QComboBox()
        self._z_axistype_list.addItems(self._type_list_values)
        self.connect(self._z_axis_column_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._updateEnabledDisabledAndTypes)                
        # Clear data object.
        self._newgraph_button = QtGui.QPushButton("New graph")
        self.connect(self._newgraph_button, QtCore.SIGNAL("clicked()"), self._newGraphAndPlotData)                
        # Add subplot data to the Graph plotter tool.
        self._addsubplotdata_button = QtGui.QPushButton("Add plot to graph")
        self.connect(self._addsubplotdata_button, QtCore.SIGNAL("clicked()"), self._addSubplotData)                

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
        hbox2.addStretch(10)
        hbox2.addWidget(self._newgraph_button)
        hbox2.addWidget(self._addsubplotdata_button)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(hbox1)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox2)
        self.setLayout(layout)                
        #
        self._updateEnabledDisabledAndTypes()
        #
        return self
        
    def _clearPlotData(self):
        """ """
        self._graph_plot_data.clear()
        # Enable/disable x, y or z-related items.
        self._updateEnabledDisabledAndTypes()

    def _updateEnabledDisabledAndTypes(self):
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
        # Autoselect types.
        if self._analysisdata.getData():
            x_selected_column = unicode(self._x_axis_column_list.currentText())
            y_selected_column = unicode(self._y_axis_column_list.currentText())
            z_selected_column = unicode(self._z_axis_column_list.currentText())
            #
            if x_selected_column == u'parameter:':
                self._x_axistype_list.setCurrentIndex(0)
            else:
                for item in self._analysisdata.getData().getExportTableColumns():
                        if item[u'header'] == x_selected_column:
                            self._x_axistype_list.setCurrentIndex(self._type_list_values.index(item[u'view_format']))
            #
            if y_selected_column == u'parameter:':
                self._y_axistype_list.setCurrentIndex(0)
            else:
                for item in self._analysisdata.getData().getExportTableColumns():
                    if item[u'header'] == y_selected_column:
                        self._y_axistype_list.setCurrentIndex(self._type_list_values.index(item[u'view_format']))
            #
            if z_selected_column == u'parameter:':
                self._z_axistype_list.setCurrentIndex(0)
            else:
                for item in self._analysisdata.getData().getExportTableColumns():
                    if item[u'header'] == z_selected_column:
                        self._z_axistype_list.setCurrentIndex(self._type_list_values.index(item[u'view_format']))
            
    def _newGraphAndPlotData(self):
        """ """
        self._clearPlotData()
        self._addSubplotData()
    
    def _addSubplotData(self):
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
        plotdatainfo[u'x_label'] = x_selected_column if x_selected_column != u"parameter:" else x_selected_param
        plotdatainfo[u'x_type'] = x_selected_type
        plotdatainfo[u'x_format'] = u''
        #
        plotdatainfo[u'y_label'] = y_selected_column if y_selected_column != u"parameter:" else y_selected_param
        plotdatainfo[u'y_type'] = y_selected_type
        plotdatainfo[u'y_format'] = u''
        #
        plotdatainfo[u'z_label'] = z_selected_column if z_selected_column != u"parameter:" else z_selected_param
        plotdatainfo[u'z_type'] = z_selected_type
        plotdatainfo[u'z_format'] = u''
        #
        # Add plot data.
        x_data, y_data, z_data = self._getPlotData()
        #
        if x_data and (x_selected_type == u'float'):
            for index, item in enumerate(x_data):
                try:
                    x_data[index] = float(item)
                except:
                    x_data[index] = 0.0
        if y_data and (y_selected_type == u'float'):
            for index, item in enumerate(y_data):
                try:
                    y_data[index] = float(item)
                except:
                    y_data[index] = 0.0
        if z_data and (z_selected_type == u'float'):
            for index, item in enumerate(z_data):
                try:
                    z_data[index] = float(item)
                except:
                    z_data[index] = 0.0
        
        plot_name = y_selected_column if y_selected_column != u"parameter:" else y_selected_param
#         plot_name = y_selected_column if y_selected_column != u"parameter:" else y_selected_param + u' / ' + \
#                     x_selected_column if x_selected_column != u"parameter:" else x_selected_param
        #
        try:
            self._graph_plot_data.addPlot(
                            plot_name = plot_name, 
                             x_label = x_selected_column if x_selected_column != u"parameter:" else x_selected_param,
                             x_array = x_data,
                             y_label = y_selected_column if y_selected_column != u"parameter:" else y_selected_param,
                             y_array = y_data, 
                             z_label = z_selected_column if z_selected_column != u"parameter:" else z_selected_param,
                             z_array = z_data) 
        except UserWarning as e:
            QtGui.QMessageBox.warning(self._main_activity, "Warning", unicode(e))

        # View in Graph plotter tool.
        graphtool.setPlotData(self._graph_plot_data)

    
    def _getPlotData(self):
        """ """
        
        # Filtered data should be used.
        self._main_activity.updateFilter() # Must be done before createFilteredDataset().
        analysisdata = self._analysisdata.createFilteredDataset()
        if not analysisdata:
            return # Can't plot from empty dataset
        
        # Selected columns.
        x_column = unicode(self._x_axis_column_list.currentText())
        y_column = unicode(self._y_axis_column_list.currentText())
        z_column = unicode(self._z_axis_column_list.currentText())
        # Selected parameters.
        x_param = None
        y_param = None
        z_param = None
        if x_column == u"parameter:":
            x_param = unicode(self._x_axis_parameter_list.currentText())
        if y_column == u"parameter:":
            y_param = unicode(self._y_axis_parameter_list.currentText())
        if z_column == u"parameter:":
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
        if x_column != u"parameter:":
            for export_info in analysisdata.getExportTableColumns():
                if export_info.get('header', u'') == x_column:
                    if export_info.get('node', u'') == 'visit':
                        x_visit_key =  export_info.get('key', None)
                    elif export_info.get('node', u'') == 'sample':
                        x_sample_key =  export_info.get('key', None)                        
                    elif export_info.get('node', u'') == 'variable':
                        x_variable_key =  export_info.get('key', None)
        if y_column != u"parameter:":
            for export_info in analysisdata.getExportTableColumns():
                if export_info.get('header', u'') == y_column:
                    if export_info.get('node', u'') == 'visit':
                        y_visit_key =  export_info.get('key', None)
                    elif export_info.get('node', u'') == 'sample':
                        y_sample_key =  export_info.get('key', None)                        
                    elif export_info.get('node', u'') == 'variable':
                        y_variable_key =  export_info.get('key', None)
        if z_column != u"parameter:":
            for export_info in analysisdata.getExportTableColumns():
                if export_info.get('header', u'') == z_column:
                    if export_info.get('node', u'') == 'visit':
                        z_visit_key =  export_info.get('key', None)
                    elif export_info.get('node', u'') == 'sample':
                        z_sample_key =  export_info.get('key', None)                        
                    elif export_info.get('node', u'') == 'variable':
                        z_variable_key =  export_info.get('key', None)
                        
                        
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
        
        # Iterate over visits. 
        for visitnode in analysisdata.getChildren():
            # Get data.
            if x_visit_key: x_value = visitnode.getData(x_visit_key)
            if y_visit_key: y_value = visitnode.getData(y_visit_key)
            if z_visit_key: z_value = visitnode.getData(z_visit_key)
            # Check if finished.
            if (y_value is not None) and (numberofvariables == 1):
                y_data.append(y_value)
                if y_visit_key: y_value = None
                continue
            if (x_value is not None) and (y_value is not None) and (numberofvariables == 2):
                x_data.append(x_value)
                y_data.append(y_value)
                if x_visit_key: x_value = None
                if y_visit_key: y_value = None
                continue            
            if (x_value is not None) and (y_value is not None) and (z_value is not None) and (numberofvariables == 3):
                x_data.append(x_value)
                y_data.append(y_value)
                z_data.append(z_value)
                if x_visit_key: x_value = None
                if y_visit_key: y_value = None
                if z_visit_key: z_value = None
                continue            
            # Iterate over samples.
            for samplenode in visitnode.getChildren():
                # Get data.
                if x_sample_key: x_value = samplenode.getData(x_sample_key)
                if y_sample_key: y_value = samplenode.getData(y_sample_key)
                if z_sample_key: z_value = samplenode.getData(z_sample_key)
                # Check if finished.
                if (y_value is not None) and (numberofvariables == 1):
                    y_data.append(y_value)
                    if y_sample_key: y_value = None
                    continue
                if (x_value is not None) and (y_value is not None) and (numberofvariables == 2):
                    x_data.append(x_value)
                    y_data.append(y_value)
                    if x_sample_key: x_value = None
                    if y_sample_key: y_value = None
                    if z_sample_key: z_value = None
                    continue            
                if (x_value is not None) and (y_value is not None) and (z_value is not None) and (numberofvariables == 3):
                    x_data.append(x_value)
                    y_data.append(y_value)
                    z_data.append(z_value)
                    if x_sample_key: x_value = None
                    if y_sample_key: y_value = None
                    if z_sample_key: z_value = None
                    continue
            
                # Iterate over sample content. 
                # Note: Create a level between sample and variabel.
                grouped_lifestages = {}
                for variablenode in samplenode.getChildren():
                    group_key = variablenode.getData(u'scientific_name')
                    group_key += u':' + variablenode.getData(u'size_class') # For phytoplankton 
                    group_key += u':' + variablenode.getData(u'stage') # For zooplankton
                    group_key += u':' + variablenode.getData(u'sex') # For zooplankton
                
                    if group_key not in grouped_lifestages:
                        grouped_lifestages[group_key] = []
                    grouped_lifestages[group_key].append(variablenode)
                
                # Get parameters values from he group.
                for group_key in grouped_lifestages.keys():
                    if x_param:
                        x_value = None
                        for variablenode in grouped_lifestages[group_key]:
                            parameter = variablenode.getData(u'parameter') + u' (' + variablenode.getData(u'unit') + u')'
                            if parameter == x_param:
                                x_value = variablenode.getData(u'value')
#                                 break                    


                                                        
                            # Check if values are finished.
                            if (y_value is not None) and (numberofvariables == 1):
                                y_data.append(y_value)
                                if y_param: y_value = None
                                continue
                            if (x_value is not None) and (y_value is not None) and (numberofvariables == 2):
                                x_data.append(x_value)
                                y_data.append(y_value)
                                if x_param: x_value = None
                                if y_param: y_value = None
                                continue            
                            if (x_value is not None) and (y_value is not None) and (z_value is not None) and (numberofvariables == 3):
                                x_data.append(x_value)
                                y_data.append(y_value)
                                z_data.append(z_value)
                                if x_param: x_value = None
                                if y_param: y_value = None
                                if z_param: z_value = None
                                continue            


                    
                    #
                    if y_param:
                        y_value = None
                        for variablenode in grouped_lifestages[group_key]:
                            parameter = variablenode.getData(u'parameter') + u' (' + variablenode.getData(u'unit') + u')'
                            if parameter == y_param:
                                y_value = variablenode.getData(u'value')


                                                        
                            # Check if values are finished.
                            if (y_value is not None) and (numberofvariables == 1):
                                y_data.append(y_value)
                                if y_param: y_value = None
                                continue
                            if (x_value is not None) and (y_value is not None) and (numberofvariables == 2):
                                x_data.append(x_value)
                                y_data.append(y_value)
                                if x_param: x_value = None
                                if y_param: y_value = None
                                continue            
                            if (x_value is not None) and (y_value is not None) and (z_value is not None) and (numberofvariables == 3):
                                x_data.append(x_value)
                                y_data.append(y_value)
                                z_data.append(z_value)
                                if x_param: x_value = None
                                if y_param: y_value = None
                                if z_param: z_value = None
                                continue            


                    
                    #
                    if z_param:
                        z_value = None
                        for variablenode in grouped_lifestages[group_key]:
                            parameter = variablenode.getData(u'parameter') + u' (' + variablenode.getData(u'unit') + u')'
                            if parameter == z_param:
                                z_value = variablenode.getData(u'value')
#                                 break


                                                        
                            # Check if values are finished.
                            if (y_value is not None) and (numberofvariables == 1):
                                y_data.append(y_value)
                                if y_param: y_value = None
                                continue
                            if (x_value is not None) and (y_value is not None) and (numberofvariables == 2):
                                x_data.append(x_value)
                                y_data.append(y_value)
                                if x_param: x_value = None
                                if y_param: y_value = None
                                continue            
                            if (x_value is not None) and (y_value is not None) and (z_value is not None) and (numberofvariables == 3):
                                x_data.append(x_value)
                                y_data.append(y_value)
                                z_data.append(z_value)
                                if x_param: x_value = None
                                if y_param: y_value = None
                                if z_param: z_value = None
                                continue            


                    
#                     # Check if values are finished.
#                     if (y_value is not None) and (numberofvariables == 1):
#                         y_data.append(y_value)
#                         if y_param: y_value = None
#                         continue
#                     if (x_value is not None) and (y_value is not None) and (numberofvariables == 2):
#                         x_data.append(x_value)
#                         y_data.append(y_value)
#                         if x_param: x_value = None
#                         if y_param: y_value = None
#                         continue            
#                     if (x_value is not None) and (y_value is not None) and (z_value is not None) and (numberofvariables == 3):
#                         x_data.append(x_value)
#                         y_data.append(y_value)
#                         z_data.append(z_value)
#                         if x_param: x_value = None
#                         if y_param: y_value = None
#                         if z_param: z_value = None
#                         continue            

                    # Get other data from the group.    
                    for variablenode in grouped_lifestages[group_key]:                        
                        if x_variable_key: x_value = variablenode.getData(x_variable_key)
                        if y_variable_key: y_value = variablenode.getData(y_variable_key)
                        if z_variable_key: z_value = variablenode.getData(z_variable_key)
    
                        # Check if values are finished.
                        if (y_value is not None) and (numberofvariables == 1):
                            y_data.append(y_value)
                            if y_variable_key: y_value = None
                            continue
                        if (x_value is not None) and (y_value is not None) and (numberofvariables == 2):
                            x_data.append(x_value)
                            y_data.append(y_value)
                            if x_variable_key: x_value = None
                            if y_variable_key: y_value = None
                            continue            
                        if (x_value is not None) and (y_value is not None) and (z_value is not None) and (numberofvariables == 3):
                            x_data.append(x_value)
                            y_data.append(y_value)
                            z_data.append(z_value)
                            if x_variable_key: x_value = None
                            if y_variable_key: y_value = None
                            if z_variable_key: z_value = None
                            continue            
                    #                    
                    if x_param: x_value = None
                    if y_param: y_value = None
                    if z_param: z_value = None
                    if x_variable_key: x_value = None
                    if y_variable_key: y_value = None
                    if z_variable_key: z_value = None

        return x_data, y_data, z_data

