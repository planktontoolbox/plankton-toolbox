#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
from PyQt6 import QtWidgets
from PyQt6 import QtCore

import toolbox_utils
import plankton_core
import app_framework
import app_tools

class AnalyseDatasetsTab5(QtWidgets.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab5, self).__init__()

    def set_main_activity(self, main_activity):
        """ """
        try:
            self._main_activity = main_activity
            self._analysisdata = main_activity.get_analysis_data()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
                
    def clear(self):
        """ """
        self._parameter_list.clear()
        
    def update(self):
        """ """
        try:
            self.clear()
            analysisdata = self._analysisdata.get_data()
            if analysisdata:        
                # Search for all parameters in analysis data.
                parameterset = set()
                for visitnode in analysisdata.get_children():
                    for samplenode in visitnode.get_children():
                        for variablenode in samplenode.get_children():
                            parameterset.add(variablenode.get_data('parameter') + ' (' + variablenode.get_data('unit') + ')')
                parameterlist = sorted(parameterset)
                self._parameter_list.addItems(parameterlist)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    # ===== TAB: Predefined graphs ===== 
    def content_predefined_graphs(self):
        """ """
        # Active widgets and connections.
#         introlabel = app_framework.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('AnalyseDatasetsTab5_intro'))
        # - Select parameter:
        self._parameter_list = QtWidgets.QComboBox()        
        self._parameter_list.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents)
        #
        # Predefined graphs.
        self._addplot_1_button = QtWidgets.QPushButton('Time series')
        self._addplot_1_button.clicked.connect(self._add_plot_1)                
        self._addplot_1_subplot_button = QtWidgets.QPushButton('Add plot')
        self._addplot_1_subplot_button.clicked.connect(self._add_sub_plot_1)                
        self._addplot_2_button = QtWidgets.QPushButton('Seasonal cycle')
        self._addplot_2_button.clicked.connect(self._add_plot_2)                
        self._addplot_2_subplot_button = QtWidgets.QPushButton('Add plot')
        self._addplot_2_subplot_button.clicked.connect(self._add_sub_plot_2)                
        self._addplot_3_button = QtWidgets.QPushButton('Values for taxa / station and date')
        self._addplot_3_button.clicked.connect(self._add_plot_3)                
        self._addplot_4_button = QtWidgets.QPushButton('Values for station and date / taxa')
        self._addplot_4_button.clicked.connect(self._add_plot_4)                

        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label1 = QtWidgets.QLabel('Parameter:')
        stretchlabel = QtWidgets.QLabel('')
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._parameter_list, gridrow, 1, 1, 1)
        form1.addWidget(stretchlabel, gridrow,4, 1, 20)
        form1.addWidget(self._addplot_1_button, gridrow, 3, 1, 1)
        form1.addWidget(self._addplot_1_subplot_button, gridrow, 4, 1, 1)
        gridrow += 1
        form1.addWidget(self._addplot_2_button, gridrow, 3, 1, 1)
        form1.addWidget(self._addplot_2_subplot_button, gridrow, 4, 1, 1)
        gridrow += 1
        form1.addWidget(self._addplot_3_button, gridrow, 3, 1, 1)
        gridrow += 1
        form1.addWidget(self._addplot_4_button, gridrow, 3, 1, 1)
        #
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        self.setLayout(layout)                
        #
        return self
        
    def _add_plot_1(self, subplot_only = False):
        """ """
        try:
            app_tools.ToolManager().show_tool_by_name('Graph plotter') # Show tool if hidden.
            graphtool = app_tools.ToolManager().get_tool_by_name('Graph plotter')
            if not subplot_only:
                graphtool.clear_plot_data()
            # Filtered data should be used.
            self._main_activity.update_filter() # Must be done before create_filtered_dataset().
            analysisdata = self._analysisdata.create_filtered_dataset()
            if not analysisdata:
                return # Can't plot from empty dataset
            # Which parameter is selected?
            selectedparameter = str(self._parameter_list.currentText())
            # 
            if not subplot_only:
                self._plotdata = toolbox_utils.GraphPlotData(
                                        title = 'Time series', 
                                        x_type = 'date',
                                        y_type = 'float',
                                        y_label = selectedparameter)
            #
            self._create_plot_data_for_time_series(selectedparameter, analysisdata, self._plotdata)
            # Plot.
            graphtool.set_chart_selection(chart = 'Scatter chart',
                                        combined = True, stacked = False, y_log_scale = False)
            graphtool.set_plot_data(self._plotdata)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def _add_sub_plot_1(self):
        """ """
        self._add_plot_1(subplot_only = True)
        
    def _add_plot_2(self, subplot_only = False):
        """ """
        try:
            app_tools.ToolManager().show_tool_by_name('Graph plotter') # Show tool if hidden.
            graphtool = app_tools.ToolManager().get_tool_by_name('Graph plotter')
            if not subplot_only:
                graphtool.clear_plot_data()
            # Filtered data should be used.
            self._main_activity.update_filter() # Must be done before create_filtered_dataset().
            analysisdata = self._analysisdata.create_filtered_dataset()
            if not analysisdata:
                return # Can't plot from empty dataset
            # Which parameter is selected?
            selectedparameter = str(self._parameter_list.currentText())
            # 
            if not subplot_only:
                self._plotdata = toolbox_utils.GraphPlotData(
                                        title = 'Seasonal cycle', 
                                        x_type = 'date',
    #                                     x_format = '%Y-%m-%d',
                                        x_format = '%m',
                                        y_type = 'float')
            #
            self._create_plot_data_for_seasonal_cycle(selectedparameter, analysisdata, self._plotdata)
            # Plot.
            graphtool.set_chart_selection(chart = 'Scatter chart',
                                        combined = True, stacked = False, y_log_scale = False)
            graphtool.set_plot_data(self._plotdata)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def _add_sub_plot_2(self):
        """ """
        try:
            self._add_plot_2(subplot_only = True)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def _add_plot_3(self):
        """ """
        try:
            app_tools.ToolManager().show_tool_by_name('Graph plotter') # Show tool if hidden.
            graphtool = app_tools.ToolManager().get_tool_by_name('Graph plotter')
            graphtool.clear_plot_data()
            # Filtered data should be used.
            self._main_activity.update_filter() # Must be done before create_filtered_dataset().
            analysisdata = self._analysisdata.create_filtered_dataset()
            if not analysisdata:
                return # Can't plot from empty dataset
            # Which parameter is selected?
            selectedparameter = str(self._parameter_list.currentText())
            # 
            plotdata = toolbox_utils.GraphPlotData(
    #                                 title = 'Values for taxa / station and date', 
                                    title = selectedparameter, 
                                    x_type = 'text',
                                    y_type = 'float',
                                    x_label = '',
                                    y_label = '')
            #
            self._add_plot_aaaaaaaaa(selectedparameter, analysisdata, plotdata)
            # Plot.
            graphtool.set_chart_selection(chart = 'Bar chart',
                                        combined = True, stacked = False, y_log_scale = False)
            graphtool.set_plot_data(plotdata)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def _add_plot_4(self):
        """ """
        try:
            app_tools.ToolManager().show_tool_by_name('Graph plotter') # Show tool if hidden.
            graphtool = app_tools.ToolManager().get_tool_by_name('Graph plotter')
            graphtool.clear_plot_data()
            # Filtered data should be used.
            self._main_activity.update_filter() # Must be done before create_filtered_dataset().
            analysisdata = self._analysisdata.create_filtered_dataset()
            if not analysisdata:
                return # Can't plot from empty dataset
            # Which parameter is selected?
            selectedparameter = str(self._parameter_list.currentText())
            # 
            plotdata = toolbox_utils.GraphPlotData(
                                    title = selectedparameter, 
                                    x_type = 'text',
                                    y_type = 'float',
                                    x_label = '',
                                    y_label = '')
            #
            self._add_plot_bbbbbbbbb(selectedparameter, analysisdata, plotdata)
            # Plot.
            graphtool.set_chart_selection(chart = 'Bar chart',
                                        combined = True, stacked = False, y_log_scale = False)
            graphtool.set_plot_data(plotdata)
            #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _create_plot_data_for_time_series(self, selectedparameter, dataset, plotdata):
        """ """
        try:
            # Extract values for the plot.
            date = None
            value = None
            date_list = []
            value_list = [] 
            for visitnode in dataset.get_children():
                date = visitnode.get_data('sample_date')
                for samplenode in visitnode.get_children():
                    for variablenode in samplenode.get_children():
                        parameter = variablenode.get_data('parameter') + ' (' + variablenode.get_data('unit') + ')'
                        if parameter == selectedparameter:                        
                            value = variablenode.get_data('value')
                            date_list.append(date)
                            value_list.append(value)               
            #                
            try:
                plotdata.add_plot(plot_name = selectedparameter, 
                                 x_array = date_list, 
                                 y_array = value_list, 
                                 x_label = '',
                                 y_label = '')
            except UserWarning as e:
                QtWidgets.QMessageBox.warning(self._main_activity, 'Warning', str(e))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _create_plot_data_for_seasonal_cycle(self, selectedparameter, dataset, plotdata):
        """ """
        try:
            # Extract values for the plot.
            date = None
            value = None
            date_list = []
            value_list = [] 
            for visitnode in dataset.get_children():
                # Replace year with '0000' seasonal cycle.
                date = visitnode.get_data('sample_date')
                try: 
                    date = str('2000' + date[4:])
                except:
                    continue # Skip to the next if date is invalid.
                #
                for samplenode in visitnode.get_children():
                    for variablenode in samplenode.get_children():
                        parameter = variablenode.get_data('parameter') + ' (' + variablenode.get_data('unit') + ')'
                        if parameter == selectedparameter:                        
                            value = variablenode.get_data('value')
                            date_list.append(date)
                            value_list.append(value)               
            #                
            try:
                plotdata.add_plot(plot_name = selectedparameter, 
                                 x_array = date_list, 
                                 y_array = value_list, 
                                 x_label = '',
                                 y_label = '')
            except UserWarning as e:
                QtWidgets.QMessageBox.warning(self._main_activity, 'Warning', str(e))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
    
    def _add_plot_aaaaaaaaa(self, selectedparameter, dataset, plotdata):
        """ """
        try:
            # Step 1: Create lists of visits and taxa.
            visit_set = set()
            taxon_set = set()
            for visitnode in dataset.get_children():
                #
                visit_set.add(str(visitnode.get_data('station_name')) + ' : ' + str(visitnode.get_data('sample_date'))) # Station name
                #
                for samplenode in visitnode.get_children():
                    #
                    for variablenode in samplenode.get_children():
                        #
                        taxonname = variablenode.get_data('scientific_name')
                        if taxonname:
                            taxon_set.add(taxonname)
                        else:
                            taxon_set.add('---')
            # Step 2: Create a station dictionary containing taxa and value for each taxa.
            visit_taxon_dict = {}
            for visit in visit_set:
                visit_taxon_dict[visit] = {} 
                for taxon in taxon_set:
                    visit_taxon_dict[visit][taxon] = 0.0
            # Step 3: Fill with data.
            for visitnode in dataset.get_children():
                #
                visit = (str(visitnode.get_data('station_name')) + ' : ' + str(visitnode.get_data('sample_date')))
                for samplenode in visitnode.get_children():
                    #
                    for variablenode in samplenode.get_children():
                        #
                        taxonname = variablenode.get_data('scientific_name')
                        if not taxonname:
                            taxonname = '---'
                        parameter = variablenode.get_data('parameter') + ' (' + variablenode.get_data('unit') + ')'
                        if parameter == selectedparameter:                        
                            value = variablenode.get_data('value')
                            try:
                                value = value.replace(',', '.').replace(' ', '') # Try/except if already float.
                            except:
                                pass
                            try:
                                visit_taxon_dict[visit][taxonname] += float(value)
                            except:
                                toolbox_utils.Logging().warning('Float conversion (2) failed: Station: ' + visit + 
                                       ' Taxon name: ' + taxonname + 
                                       ' Parameter: ' + selectedparameter + 
                                       ' Value: ' + str(variablenode.get_data('value')))
                                ###raise        
            # Step 4: Reorganize.
            visit_list = sorted(visit_set)
            taxon_list = sorted(taxon_set)
            #  Step 4: Add subplots.
            for taxonindex, taxon in enumerate(taxon_list):
                taxon_visit_value_list = []
                for stationindex, station in enumerate(visit_list):
                    taxon_visit_value_list.append(visit_taxon_dict[station][taxon])
                # 
                try:
                    plotdata.add_plot(plot_name = taxon, 
                                        x_array = visit_list, 
                                        y_array = taxon_visit_value_list, 
                                        x_label = '',
                                        y_label = selectedparameter)
                except UserWarning as e:
                    QtWidgets.QMessageBox.warning(self._main_activity, 'Warning', str(e))
            #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _add_plot_bbbbbbbbb(self, selectedparameter, dataset, plotdata):
        """ """
        try:
            # Step 1: Create lists of visits and taxa.
            visit_set = set()
            taxon_set = set()
            for visitnode in dataset.get_children():
                #
                visit_set.add(str(visitnode.get_data('station_name')) + ' : ' + str(visitnode.get_data('sample_date'))) # Station name
                #
                for samplenode in visitnode.get_children():
                    #
                    for variablenode in samplenode.get_children():
                        #
                        taxonname = variablenode.get_data('scientific_name')
                        if taxonname:
                            taxon_set.add(taxonname)
                        else:
                            taxon_set.add('---')
    #        # Step 2: Create a station dictionary containing taxa and value for each taxa.
            # Step 2: Create a taxa dictionary containing visits and value for each visit.
            taxon_visit_dict = {}
            for taxon in taxon_set:
                taxon_visit_dict[taxon] = {} 
                for visit in visit_set:
                    taxon_visit_dict[taxon][visit] = 0.0
            # Step 3: Fill with data.
            for visitnode in dataset.get_children():
                #
                visit = (str(visitnode.get_data('station_name')) + ' : ' + str(visitnode.get_data('sample_date')))
                for samplenode in visitnode.get_children():
                    #
                    for variablenode in samplenode.get_children():
                        #
                        taxonname = variablenode.get_data('scientific_name')
                        if not taxonname:
                            taxonname = '---'
                        parameter = variablenode.get_data('parameter') + ' (' + variablenode.get_data('unit') + ')'
                        if parameter == selectedparameter:                        
                            value = variablenode.get_data('value')
                            try:
                                value = value.replace(',', '.').replace(' ', '') # Try/except if already float.
                            except:
                                pass
                            try:
                                taxon_visit_dict[taxonname][visit] += float(value)
                            except:
                                toolbox_utils.Logging().warning('Float conversion failed: Visit: ' + visit + 
                                       ' Taxon name: ' + taxonname + 
                                       ' Parameter: ' + selectedparameter + 
                                       ' Value: ' + str(variablenode.get_data('value')))
                                ###raise        
            # Step 4: Reorganize.
            visit_list = sorted(visit_set)
            taxon_list = sorted(taxon_set)
            #  Step 4: Add subplots.
            for visitindex, visit in enumerate(visit_list):
                visit_taxon_value_list = []
                for taxonindex, taxon in enumerate(taxon_list):
                    visit_taxon_value_list.append(taxon_visit_dict[taxon][visit])
                # 
                try:
                    plotdata.add_plot(plot_name = visit, 
                                        x_array = taxon_list, 
                                        y_array = visit_taxon_value_list, 
                                        x_label = '',
                                        y_label = selectedparameter)
                except UserWarning as e:
                    QtWidgets.QMessageBox.warning(self._main_activity, 'Warning', str(e))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
