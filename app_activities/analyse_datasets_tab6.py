#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from PyQt5 import QtWidgets
from PyQt5 import QtCore
import plankton_toolbox.tools.tool_manager as tool_manager
# import plankton_toolbox.toolbox.utils_qt as utils_qt
# import plankton_toolbox.toolbox.help_texts as help_texts

import toolbox_utils
import plankton_core

class AnalyseDatasetsTab6(QtWidgets.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab6, self).__init__()
        #
        self._graph_plot_data = toolbox_utils.GraphPlotData()
        self._type_list_values = ["float", "integer", "text", "date", "datetime"]

    def set_main_activity(self, main_activity):
        """ """
        self._main_activity = main_activity
        self._analysisdata = main_activity.get_analysis_data()
                
    def clear(self):
        """ """
        self._x_axis_column_list.clear()
        self._x_axis_parameter_list.clear()
        self._x_axis_column_list.addItems(['parameter:'])
        self._x_axis_column_list.setEnabled(False)
        self._x_axis_parameter_list.setEnabled(False)
        #
        self._y_axis_column_list.clear()
        self._y_axis_parameter_list.clear()
        self._y_axis_column_list.addItems(['parameter:'])
        self._y_axis_column_list.setEnabled(False)
        self._y_axis_parameter_list.setEnabled(False)
        #
        self._z_axis_column_list.clear()
        self._z_axis_parameter_list.clear()
        self._z_axis_column_list.addItems(['parameter:'])
        self._z_axis_column_list.setEnabled(False)
        self._z_axis_parameter_list.setEnabled(False)
        #
        self._update_enabled_disabled_and_types()
        
    def update(self):
        """ """
        self.clear()
        analysisdata = self._analysisdata.get_data()
        if analysisdata:        
            # For tab "Generic graphs".
            items = [item['header'] for item in analysisdata.get_export_table_columns()]        
            self._x_axis_column_list.addItems(items)
            self._y_axis_column_list.addItems(items)
            self._z_axis_column_list.addItems(items)
            # Search for all parameters in analysis data.
            parameterset = set()
            for visitnode in analysisdata.get_children():
                for samplenode in visitnode.get_children():
                    for variablenode in samplenode.get_children():
                        parameterset.add(variablenode.get_data('parameter') + ' (' + variablenode.get_data('unit') + ')')
            parameterlist = sorted(parameterset)
            #
            self._x_axis_parameter_list.addItems(parameterlist)
            self._y_axis_parameter_list.addItems(parameterlist)
            self._z_axis_parameter_list.addItems(parameterlist)
            #  Make combo-boxes visible.
            self._update_enabled_disabled_and_types()

    # ===== TAB: Generic graphs ===== 
    def content_generic_graphs(self):
        """ """
        # Active widgets and connections.
#         introlabel = app_framework.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('AnalyseDatasetsTab6_intro'))
        # Select type of data object.
        self._numberofvariables_list = QtWidgets.QComboBox()
        self._numberofvariables_list.addItems(["One variable (Y)", 
                                               "Two variables (X and Y)", 
                                               "Three variables (X, Y and Z)"])
        self._numberofvariables_list.setCurrentIndex(1)
        self._numberofvariables_list.currentIndexChanged(int)'), self._clear_plot_data)                
        # - Select column for x-axis:
        self._x_axis_column_list = QtWidgets.QComboBox()
        self._x_axis_column_list.setMinimumContentsLength(20)
        self._x_axis_column_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self._x_axis_parameter_list = QtWidgets.QComboBox()        
        self._x_axis_parameter_list.setMinimumContentsLength(20)
        self._x_axis_parameter_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self._x_axistype_list = QtWidgets.QComboBox()
        self._x_axistype_list.addItems(self._type_list_values)
        self._x_axis_column_list.currentIndexChanged(int)'), self._update_enabled_disabled_and_types)                
        # - Select column for y-axis:
        self._y_axis_column_list = QtWidgets.QComboBox()
        self._y_axis_column_list.setMinimumContentsLength(20)
        self._y_axis_column_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self._y_axis_parameter_list = QtWidgets.QComboBox()
        self._y_axis_parameter_list.setMinimumContentsLength(20)
        self._y_axis_parameter_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self._y_axistype_list = QtWidgets.QComboBox()
        self._y_axistype_list.addItems(self._type_list_values)
        self._y_axis_column_list.currentIndexChanged(int)'), self._update_enabled_disabled_and_types)                
        # - Select column for z-axis:
        self._z_axis_column_list = QtWidgets.QComboBox()
        self._z_axis_column_list.setMinimumContentsLength(20)
        self._z_axis_column_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self._z_axis_parameter_list = QtWidgets.QComboBox()
        self._z_axis_parameter_list.setMinimumContentsLength(20)
        self._z_axis_parameter_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self._z_axistype_list = QtWidgets.QComboBox()
        self._z_axistype_list.addItems(self._type_list_values)
        self._z_axis_column_list.currentIndexChanged(int)'), self._update_enabled_disabled_and_types)                
        # Clear data object.
        self._newgraph_button = QtWidgets.QPushButton('New graph')
        self._newgraph_button.clicked(self._new_graph_and_plot_data)                
        # Add subplot data to the Graph plotter tool.
        self._addsubplotdata_button = QtWidgets.QPushButton('Add plot to graph')
        self._addsubplotdata_button.clicked(self._add_subplot_data)                

        # Layout widgets.
        #
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(QtWidgets.QLabel('Select number of variables in each plot:'))
        hbox1.addWidget(self._numberofvariables_list)
        hbox1.addStretch(10)
        #
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label1 = QtWidgets.QLabel('Select x-axis:')
        label2 = QtWidgets.QLabel('Parameter:')
        label3 = QtWidgets.QLabel('Type:')
        stretchlabel = QtWidgets.QLabel('')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._x_axis_column_list, gridrow, 1, 1, 1)
        form1.addWidget(label2, gridrow, 2, 1, 1)
        form1.addWidget(self._x_axis_parameter_list, gridrow, 3, 1, 1)
        form1.addWidget(label3, gridrow, 4, 1, 1)
        form1.addWidget(self._x_axistype_list, gridrow, 5, 1, 1)
        form1.addWidget(stretchlabel, gridrow,6, 1, 20)
        gridrow += 1
        label1 = QtWidgets.QLabel('Select y-axis:')
        label2 = QtWidgets.QLabel('Parameter:')
        label3 = QtWidgets.QLabel('Type:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._y_axis_column_list, gridrow, 1, 1, 1)
        form1.addWidget(label2, gridrow, 2, 1, 1)
        form1.addWidget(self._y_axis_parameter_list, gridrow, 3, 1, 1)
        form1.addWidget(label3, gridrow, 4, 1, 1)
        form1.addWidget(self._y_axistype_list, gridrow, 5, 1, 1)
        form1.addWidget(stretchlabel, gridrow,6, 1, 20)
        gridrow += 1
        label1 = QtWidgets.QLabel('Select z-axis:')
        label2 = QtWidgets.QLabel('Parameter:')
        label3 = QtWidgets.QLabel('Type:')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._z_axis_column_list, gridrow, 1, 1, 1)
        form1.addWidget(label2, gridrow, 2, 1, 1)
        form1.addWidget(self._z_axis_parameter_list, gridrow, 3, 1, 1)
        form1.addWidget(label3, gridrow, 4, 1, 1)
        form1.addWidget(self._z_axistype_list, gridrow, 5, 1, 1)
        form1.addWidget(stretchlabel, gridrow,6, 1, 20)
        #
        hbox2 = QtWidgets.QHBoxLayout()
#         hbox2.addStretch(10)
        hbox2.addWidget(self._newgraph_button)
        hbox2.addWidget(self._addsubplotdata_button)
        hbox2.addStretch(10)
        #
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(hbox1)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox2)
        self.setLayout(layout)                
        #
        self._update_enabled_disabled_and_types()
        #
        return self
        
    def _clear_plot_data(self):
        """ """
        self._graph_plot_data.clear()
        # Enable/disable x, y or z-related items.
        self._update_enabled_disabled_and_types()

    def _update_enabled_disabled_and_types(self):
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
        if self._analysisdata.get_data():
            x_selected_column = unicode(self._x_axis_column_list.currentText())
            y_selected_column = unicode(self._y_axis_column_list.currentText())
            z_selected_column = unicode(self._z_axis_column_list.currentText())
            #
            if x_selected_column == 'parameter:':
                self._x_axistype_list.setCurrentIndex(0)
            else:
                for item in self._analysisdata.get_data().get_export_table_columns():
                        if item['header'] == x_selected_column:
                            self._x_axistype_list.setCurrentIndex(self._type_list_values.index(item['view_format']))
            #
            if y_selected_column == 'parameter:':
                self._y_axistype_list.setCurrentIndex(0)
            else:
                for item in self._analysisdata.get_data().get_export_table_columns():
                    if item['header'] == y_selected_column:
                        self._y_axistype_list.setCurrentIndex(self._type_list_values.index(item['view_format']))
            #
            if z_selected_column == 'parameter:':
                self._z_axistype_list.setCurrentIndex(0)
            else:
                for item in self._analysisdata.get_data().get_export_table_columns():
                    if item['header'] == z_selected_column:
                        self._z_axistype_list.setCurrentIndex(self._type_list_values.index(item['view_format']))
            
    def _new_graph_and_plot_data(self):
        """ """
        self._clear_plot_data()
        self._add_subplot_data()
    
    def _add_subplot_data(self):
        """ """
        # Show the Graph plotter tool if hidden. 
        tool_manager.ToolManager().show_tool_by_name('Graph plotter')
        graphtool = tool_manager.ToolManager().get_tool_by_name('Graph plotter')
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
        plotdatainfo = self._graph_plot_data.get_plot_data_info()
        #
        plotdatainfo['x_label'] = x_selected_column if x_selected_column != 'parameter:' else x_selected_param
        plotdatainfo['x_type'] = x_selected_type
        plotdatainfo['x_format'] = ''
        #
        plotdatainfo['y_label'] = y_selected_column if y_selected_column != 'parameter:' else y_selected_param
        plotdatainfo['y_type'] = y_selected_type
        plotdatainfo['y_format'] = ''
        #
        plotdatainfo['z_label'] = z_selected_column if z_selected_column != 'parameter:' else z_selected_param
        plotdatainfo['z_type'] = z_selected_type
        plotdatainfo['z_format'] = ''
        #
        # Add plot data.
        x_data, y_data, z_data = self._get_plot_data()
        #
        if x_data and (x_selected_type == 'float'):
            for index, item in enumerate(x_data):
                try:
                    value = item.replace(',', '.').replace(' ', '') # Try/except if already float.
                except: pass
                try:
                    x_data[index] = float(value)
                except:
                    x_data[index] = 0.0
        if y_data and (y_selected_type == 'float'):
            for index, item in enumerate(y_data):
                try:
                    value = item.replace(',', '.').replace(' ', '') # Try/except if already float.
                except: pass
                try:
                    y_data[index] = float(value)
                except:
                    y_data[index] = 0.0
        if z_data and (z_selected_type == 'float'):
            for index, item in enumerate(z_data):
                try:
                    value = item.replace(',', '.').replace(' ', '') # Try/except if already float.
                except: pass
                try:
                    z_data[index] = float(value)
                except:
                    z_data[index] = 0.0
        
        plot_name = y_selected_column if y_selected_column != 'parameter:' else y_selected_param
#         plot_name = y_selected_column if y_selected_column != 'parameter:' else y_selected_param + ' / ' + \
#                     x_selected_column if x_selected_column != 'parameter:' else x_selected_param
        #
        try:
            self._graph_plot_data.add_plot(
                            plot_name = plot_name, 
                             x_label = x_selected_column if x_selected_column != 'parameter:' else x_selected_param,
                             x_array = x_data,
                             y_label = y_selected_column if y_selected_column != 'parameter:' else y_selected_param,
                             y_array = y_data, 
                             z_label = z_selected_column if z_selected_column != 'parameter:' else z_selected_param,
                             z_array = z_data) 
        except UserWarning as e:
            QtWidgets.QMessageBox.warning(self._main_activity, 'Warning', unicode(e))

        # View in Graph plotter tool.
        graphtool.set_plot_data(self._graph_plot_data)

    
    def _get_plot_data(self):
        """ """
        
        # Filtered data should be used.
        self._main_activity.update_filter() # Must be done before create_filtered_dataset().
        analysisdata = self._analysisdata.create_filtered_dataset()
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
        if x_column == 'parameter:':
            x_param = unicode(self._x_axis_parameter_list.currentText())
        if y_column == 'parameter:':
            y_param = unicode(self._y_axis_parameter_list.currentText())
        if z_column == 'parameter:':
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
        if x_column != 'parameter:':
            for export_info in analysisdata.get_export_table_columns():
                if export_info.get('header', '') == x_column:
                    if export_info.get('node', '') == 'visit':
                        x_visit_key =  export_info.get('key', None)
                    elif export_info.get('node', '') == 'sample':
                        x_sample_key =  export_info.get('key', None)                        
                    elif export_info.get('node', '') == 'variable':
                        x_variable_key =  export_info.get('key', None)
        if y_column != 'parameter:':
            for export_info in analysisdata.get_export_table_columns():
                if export_info.get('header', '') == y_column:
                    if export_info.get('node', '') == 'visit':
                        y_visit_key =  export_info.get('key', None)
                    elif export_info.get('node', '') == 'sample':
                        y_sample_key =  export_info.get('key', None)                        
                    elif export_info.get('node', '') == 'variable':
                        y_variable_key =  export_info.get('key', None)
        if z_column != 'parameter:':
            for export_info in analysisdata.get_export_table_columns():
                if export_info.get('header', '') == z_column:
                    if export_info.get('node', '') == 'visit':
                        z_visit_key =  export_info.get('key', None)
                    elif export_info.get('node', '') == 'sample':
                        z_sample_key =  export_info.get('key', None)                        
                    elif export_info.get('node', '') == 'variable':
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
        for visitnode in analysisdata.get_children():
            # Get data.
            if x_visit_key: x_value = visitnode.get_data(x_visit_key)
            if y_visit_key: y_value = visitnode.get_data(y_visit_key)
            if z_visit_key: z_value = visitnode.get_data(z_visit_key)
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
            for samplenode in visitnode.get_children():
                # Get data.
                if x_sample_key: x_value = samplenode.get_data(x_sample_key)
                if y_sample_key: y_value = samplenode.get_data(y_sample_key)
                if z_sample_key: z_value = samplenode.get_data(z_sample_key)
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
                for variablenode in samplenode.get_children():
                    group_key = variablenode.get_data('scientific_name')
                    group_key += ':' + variablenode.get_data('size_class') # For phytoplankton 
                    group_key += ':' + variablenode.get_data('stage') # For zooplankton
                    group_key += ':' + variablenode.get_data('sex') # For zooplankton
                
                    if group_key not in grouped_lifestages:
                        grouped_lifestages[group_key] = []
                    grouped_lifestages[group_key].append(variablenode)
                
                # Get parameters values from he group.
                for group_key in grouped_lifestages.keys():
                    if x_param:
                        x_value = None
                        for variablenode in grouped_lifestages[group_key]:
                            parameter = variablenode.get_data('parameter') + ' (' + variablenode.get_data('unit') + ')'
                            if parameter == x_param:
                                x_value = variablenode.get_data('value')
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
                            parameter = variablenode.get_data('parameter') + ' (' + variablenode.get_data('unit') + ')'
                            if parameter == y_param:
                                y_value = variablenode.get_data('value')


                                                        
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
                            parameter = variablenode.get_data('parameter') + ' (' + variablenode.get_data('unit') + ')'
                            if parameter == z_param:
                                z_value = variablenode.get_data('value')
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
                        if x_variable_key: x_value = variablenode.get_data(x_variable_key)
                        if y_variable_key: y_value = variablenode.get_data(y_variable_key)
                        if z_variable_key: z_value = variablenode.get_data(z_variable_key)
    
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

