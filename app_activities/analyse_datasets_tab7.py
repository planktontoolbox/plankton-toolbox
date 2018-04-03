#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

# import math
import sys
import numpy
# import scipy.stats as stats
# import scipy.stats.mstats as mstats

from PyQt5 import QtWidgets
from PyQt5 import QtCore

import toolbox_utils
import app_framework
import app_tools
import plankton_core

class AnalyseDatasetsTab7(QtWidgets.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab7, self).__init__()

    def set_main_activity(self, main_activity):
        """ """
        self._main_activity = main_activity
        self._analysisdata = main_activity.get_analysis_data()
                
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

    # ===== TAB: Statistics ===== 
    def content_statistics(self):
        """ """
        # Active widgets and connections.
#         introlabel = app_framework.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('AnalyseDatasetsTab7_intro'))
        # - Select parameter.
        self._parameter_list = QtWidgets.QComboBox()        
        self._parameter_list.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        # - Split by.
        self._splitby_year_checkbox = QtWidgets.QCheckBox('Year')
        self._splitby_year_checkbox.setChecked(False) 
        self._splitby_season_checkbox = QtWidgets.QCheckBox('Season')
        self._splitby_season_checkbox.setChecked(False) 
        self._splitby_month_checkbox = QtWidgets.QCheckBox('Month')
        self._splitby_month_checkbox.setChecked(False) 
        self._splitby_station_checkbox = QtWidgets.QCheckBox('Station')
        self._splitby_station_checkbox.setChecked(False) 
        self._splitby_visit_checkbox = QtWidgets.QCheckBox('Sampling event')
        self._splitby_visit_checkbox.setChecked(False) 
        self._splitby_depth_checkbox = QtWidgets.QCheckBox('Depth')
        self._splitby_depth_checkbox.setChecked(False) 
        self._splitby_taxon_checkbox = QtWidgets.QCheckBox('Scientific name')
        self._splitby_taxon_checkbox.setChecked(False) 
        # - View data.
        self._viewdata_button = QtWidgets.QPushButton('View data')
        self._viewdata_button.clicked.connect(self._view_data)                
        # - Calculate statistics.
        self._calcstatistics_button = QtWidgets.QPushButton('Calculate statistics')
        self._calcstatistics_button.clicked.connect(self._calc_stats)                
        # - Plot graph.
        self._plotgraphs_button = QtWidgets.QPushButton('Plot graph')
        self._plotgraphs_button.clicked.connect(self._plot_graph)                

        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        label1 = QtWidgets.QLabel('Parameter:')
        label2 = QtWidgets.QLabel('Split by:')
        stretchlabel1 = QtWidgets.QLabel('')
        gridrow = 0
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(stretchlabel1, gridrow, 1, 1, 2)
        form1.addWidget(label2, gridrow, 2, 1, 1)
        form1.addWidget(stretchlabel1, gridrow, 3, 1, 10)
        gridrow += 1
        form1.addWidget(self._parameter_list, gridrow, 0, 1, 1)
        form1.addWidget(self._splitby_year_checkbox, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self._splitby_season_checkbox, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self._splitby_month_checkbox, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self._splitby_station_checkbox, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self._splitby_visit_checkbox, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self._splitby_depth_checkbox, gridrow, 2, 1, 1)
        gridrow += 1
        form1.addWidget(self._splitby_taxon_checkbox, gridrow, 2, 1, 1)
        #
        hbox2 = QtWidgets.QHBoxLayout()
#         hbox2.addStretch(10)
        hbox2.addWidget(self._viewdata_button)
        hbox2.addWidget(self._calcstatistics_button)
        hbox2.addWidget(self._plotgraphs_button)
        hbox2.addStretch(10)
        #
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox2)
        self.setLayout(layout)                
        #
        return self
        
    def _calc_stats(self):
        """ """
        try:
            # Clear the statistical data and view the statistic area.
            statisticaldata = self._main_activity.get_statistical_data()
            statisticaldata.clear_data()
            self._main_activity.view_statistical_data()
            # Filtered data should be used.
            self._main_activity.update_filter() # Must be done before create_filtered_dataset().
            analysisdata = self._analysisdata.create_filtered_dataset()
            if not analysisdata:
                return # Can't create a report from an empty dataset.
            # Which parameter is selected?
            selectedparameter = str(self._parameter_list.currentText())
            # Split by.
            split_on_year = self._splitby_year_checkbox.isChecked()
            split_on_season = self._splitby_season_checkbox.isChecked()
            split_on_month = self._splitby_month_checkbox.isChecked()
            split_on_station = self._splitby_station_checkbox.isChecked()
            split_on_visit = self._splitby_visit_checkbox.isChecked()
            split_on_depth = self._splitby_depth_checkbox.isChecked()
            split_on_taxon = self._splitby_taxon_checkbox.isChecked()
            # Calculate the statistics.
            self._calc_statistics(analysisdata, statisticaldata,
                                      selectedparameter, 
                                      split_on_year,
                                      split_on_season,
                                      split_on_month,
                                      split_on_station,
                                      split_on_visit,
                                      split_on_depth,
                                      split_on_taxon)
            # View the result in the report area.
            self._main_activity.view_statistical_data()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def _calc_statistics(self, dataset, reportdata,
                        selectedparameter, 
                        split_on_year = False,
                        split_on_season = False,
                        split_on_month = False,
                        split_on_station = False,
                        split_on_visit = False,
                        split_on_depth = False,
                        split_on_taxon = False):
        """ """
        try:
            # Target list.
            data_dict = {}        
            # Create a dataset (table, not tree).
            tabledata = plankton_core.DatasetTable()
            reportdata.set_data(tabledata)
            # Header for result table.
            header_row = []
            header_row.append('Parameter')
            if split_on_year: header_row.append('Year')
            if split_on_season: header_row.append('Season')
            if split_on_month: header_row.append('Month')
            if split_on_station: header_row.append('Station')
            if split_on_visit: header_row.append('Sampling event')
            if split_on_depth: header_row.append('Depth')
            if split_on_taxon: header_row.append('Scientific name')
            header_row.append('Mean')
            header_row.append('Median')
            header_row.append('Std. dev.')
            header_row.append('Min')
            header_row.append('Max')
            header_row.append('Counted values')
            tabledata.set_header(header_row)
            # Extract values.
            yearkey = ''
            monthkey = ''
            seasonkey = ''
            stationkey = ''
            visitkey = ''
            depthkey = ''
            taxonkey = ''
            #
            for visitnode in dataset.get_children():
                visitdate = visitnode.get_data('sample_date')
                visitstation = visitnode.get_data('station_name')
                visitvisit = visitstation + ' ' + visitdate 
                visityear = str(visitdate[0:4])
                visitmonth = str(visitdate[5:7])
                visitseason = ''
                if visitmonth in ['12', '01','02']:
                    visitseason = 'Dec-Jan-Feb'
                elif visitmonth in ['03', '04','05']:
                    visitseason = 'Mar-Apr-May'
                elif visitmonth in ['06', '07','08']:
                    visitseason = 'Jun-Jul-Aug'
                elif visitmonth in ['09', '10','11']:
                    visitseason = 'Sep-Oct-Nov'
                #
                for samplenode in visitnode.get_children():
                    sample_min_depth_m = str(samplenode.get_data('sample_min_depth_m'))
                    sample_max_depth_m = str(samplenode.get_data('sample_max_depth_m'))
                    sampleminmaxdepth = sample_min_depth_m + '-' + sample_max_depth_m   
                    # Iterate over sample content. 
                    # Note: Create a level between sample and variabel.
                    grouped_size_lifestages = {}
                    for variablenode in samplenode.get_children():
                        group_key = variablenode.get_data('scientific_name')
                        group_key += ':' + variablenode.get_data('size_class') # Specific for phytoplankton.
                        group_key += ':' + variablenode.get_data('stage') # Specific for zooplankton.
                        group_key += ':' + variablenode.get_data('sex') # Specific for zooplankton.
                        if group_key not in grouped_size_lifestages:
                            grouped_size_lifestages[group_key] = [] # Starts a new group.
                        grouped_size_lifestages[group_key].append(variablenode)
                    
                    # Get variables from the new set of groups.
                    for group_key in grouped_size_lifestages.keys():
                        #
                        for variablenode in grouped_size_lifestages[group_key]:
                            variabletaxon = variablenode.get_data('scientific_name')
                            # Parameters.
                            parameter = variablenode.get_data('parameter')
                            unit = variablenode.get_data('unit')
                            parameternadunit = parameter + ' (' + unit + ')'
                            if parameternadunit == selectedparameter:
                                # Build split key.
                                splitkey = ''
                                if split_on_year: splitkey += visityear
                                splitkey += ':'
                                if split_on_season: splitkey += visitseason
                                splitkey += ':'
                                if split_on_month: splitkey += visitmonth
                                splitkey += ':'
                                if split_on_station: splitkey += visitstation
                                splitkey += ':'
                                if split_on_visit: splitkey += visitvisit
                                splitkey += ':'
                                if split_on_depth: splitkey += sampleminmaxdepth
                                splitkey += ':'
                                if split_on_taxon: splitkey += variabletaxon
                                # Add data.
                                if splitkey not in data_dict:
                                    data_dict[splitkey] = []
                                data_dict[splitkey].append(variablenode.get_data('value'))
                                 
            # Calculate result
            for key in sorted(data_dict.keys()):
                # Keys.
                keysplit = key.split(':')
                yearkey = keysplit[0]
                seasonkey = keysplit[1]
                monthkey = keysplit[2]
                stationkey = keysplit[3]
                visitkey = keysplit[4]
                depthkey = keysplit[5]
                taxonkey = keysplit[6]
                #
                try:
#                     data_list = map(float, data_dict[key]) # Not working in Python3.
#                    data_list = list(map(float, data_dict[key])) # ALT 1.
                    data_list =[float(x) for x in  data_dict[key]] # ALT 2. list comprehensions.
                    
                    # Calculate result by use of numpy. 
                    # Use float64 since we are using both small and big unit.
                    meanvalue = numpy.mean(data_list, dtype=numpy.float64)
                    medianvalue = numpy.median(data_list)
                    stddevvalue = numpy.std(data_list, dtype=numpy.float64)
                    minvalue = numpy.nanmin(data_list) 
                    maxvalue = numpy.nanmax(data_list)
                    countedvalues = len(data_list)
                except Exception as e:
                    meanvalue = '<ERROR>'
                    medianvalue = '<ERROR>'
                    stddevvalue = '<ERROR>'
                    minvalue = '<ERROR>'
                    maxvalue = '<ERROR>'
                    countedvalues = len(data_list)
                    #
                    print(', '.join(map(str, data_list))) # Print data.
                    print('Error in calc statistics: ' + str(e)) # Print exception.            
                # Create row.
                report_row = []
                report_row.append(selectedparameter)
                if split_on_year: report_row.append(yearkey)
                if split_on_season: report_row.append(seasonkey)
                if split_on_month: report_row.append(monthkey)
                if split_on_station: report_row.append(stationkey)
                if split_on_visit: report_row.append(visitkey)
                if split_on_depth: report_row.append(depthkey)
                if split_on_taxon: report_row.append(taxonkey)
                report_row.append(meanvalue)
                report_row.append(medianvalue)
                report_row.append(stddevvalue)
                report_row.append(minvalue)
                report_row.append(maxvalue)
                report_row.append(countedvalues)
                #
                tabledata.append_row(report_row)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def _view_data(self):
        """ """
        try:
            # Clear the statistical data and view the statistic area.
            statisticaldata = self._main_activity.get_statistical_data()
            statisticaldata.clear_data()
            self._main_activity.view_statistical_data()
            # Filtered data should be used.
            self._main_activity.update_filter() # Must be done before create_filtered_dataset().
            analysisdata = self._analysisdata.create_filtered_dataset()
            if not analysisdata:
                return # Can't create a report from an empty dataset.
            # Which parameter is selected?
            selectedparameter = str(self._parameter_list.currentText())
            # Split by.
            split_on_year = self._splitby_year_checkbox.isChecked()
            split_on_season = self._splitby_season_checkbox.isChecked()
            split_on_month = self._splitby_month_checkbox.isChecked()
            split_on_station = self._splitby_station_checkbox.isChecked()
            split_on_visit = self._splitby_visit_checkbox.isChecked()
            split_on_depth = self._splitby_depth_checkbox.isChecked()
            split_on_taxon = self._splitby_taxon_checkbox.isChecked()
            # Calculate the statistics.
            self._extract_values(analysisdata, statisticaldata,
                                      selectedparameter, 
                                      split_on_year,
                                      split_on_season,
                                      split_on_month,
                                      split_on_station,
                                      split_on_visit,
                                      split_on_depth,
                                      split_on_taxon)
            # View the result in the report area.
            self._main_activity.view_statistical_data()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def _extract_values(self, dataset, reportdata,
                        selectedparameter, 
                        split_on_year = False,
                        split_on_season = False,
                        split_on_month = False,
                        split_on_station = False,
                        split_on_visit = False,
                        split_on_depth = False,
                        split_on_taxon = False):
        """ """
        try:
            # Target list.
            data_dict = {}        
            # Create a dataset (table, not tree).
            tabledata = plankton_core.DatasetTable()
            reportdata.set_data(tabledata)
            # Extract values.
            yearkey = ''
            monthkey = ''
            seasonkey = ''
            stationkey = ''
            visitkey = ''
            depthkey = ''
            taxonkey = ''
            #
            for visitnode in dataset.get_children():
                visitdate = visitnode.get_data('sample_date')
                visitstation = visitnode.get_data('station_name')
                visitvisit = visitstation + ' ' + visitdate 
                visityear = str(visitdate[0:4])
                visitmonth = str(visitdate[5:7])
                visitseason = ''
                if visitmonth in ['12', '01','02']:
                    visitseason = 'Dec-Jan-Feb'
                elif visitmonth in ['03', '04','05']:
                    visitseason = 'Mar-Apr-May'
                elif visitmonth in ['06', '07','08']:
                    visitseason = 'Jun-Jul-Aug'
                elif visitmonth in ['09', '10','11']:
                    visitseason = 'Sep-Oct-Nov'
                #
                for samplenode in visitnode.get_children():
                    sample_min_depth_m = str(samplenode.get_data('sample_min_depth_m'))
                    sample_max_depth_m = str(samplenode.get_data('sample_max_depth_m'))
                    sampleminmaxdepth = sample_min_depth_m + '-' + sample_max_depth_m   
                    # Iterate over sample content. 
                    # Note: Create a level between sample and variabel.
                    grouped_size_lifestages = {}
                    for variablenode in samplenode.get_children():
                        group_key = variablenode.get_data('scientific_name')
                        group_key += ':' + variablenode.get_data('size_class') # Specific for phytoplankton.
                        group_key += ':' + variablenode.get_data('stage') # Specific for zooplankton.
                        group_key += ':' + variablenode.get_data('sex') # Specific for zooplankton.
                        if group_key not in grouped_size_lifestages:
                            grouped_size_lifestages[group_key] = [] # Starts a new group.
                        grouped_size_lifestages[group_key].append(variablenode)
                    
                    # Get variables from the new set of groups.
                    for group_key in grouped_size_lifestages.keys():
                        #
                        for variablenode in grouped_size_lifestages[group_key]:
                            variabletaxon = variablenode.get_data('scientific_name')
                            # Parameters.
                            parameter = variablenode.get_data('parameter')
                            unit = variablenode.get_data('unit')
                            parameternadunit = parameter + ' (' + unit + ')'
                            if parameternadunit == selectedparameter:
                                # Build split key.
                                splitkey = ''
                                if split_on_year: splitkey += visityear
                                splitkey += ':'
                                if split_on_season: splitkey += visitseason
                                splitkey += ':'
                                if split_on_month: splitkey += visitmonth
                                splitkey += ':'
                                if split_on_station: splitkey += visitstation
                                splitkey += ':'
                                if split_on_visit: splitkey += visitvisit
                                splitkey += ':'
                                if split_on_depth: splitkey += sampleminmaxdepth
                                splitkey += ':'
                                if split_on_taxon: splitkey += variabletaxon
                                # Add data.
                                if splitkey not in data_dict:
                                    data_dict[splitkey] = []
                                data_dict[splitkey].append(variablenode.get_data('value'))
                                 
            # Create empty result table.
            resulttable = []
            emptyrow = [''] * (1 + len(data_dict)) # Empty row.
            maxlength = 0
            for key in sorted(data_dict.keys()):
                datalistlength = len(data_dict[key])
                if datalistlength > maxlength:
                    maxlength = datalistlength
            for index in range(maxlength + 9): # Header rows and data rows.    
                resulttable.append(emptyrow[:]) # Clone.
            # Headers, multiple rows.
            resulttable[0][0] = 'Parameter:'
            resulttable[1][0] = 'Year:'
            resulttable[2][0] = 'Season:'
            resulttable[3][0] = 'Month:'
            resulttable[4][0] = 'Station:'
            resulttable[5][0] = 'Sampling event:'
            resulttable[6][0] = 'Depth:'
            resulttable[7][0] = 'Scientific name:'
                    
            # Calculate result
            for colindex, key in enumerate(sorted(data_dict.keys())):
                # Keys.
                keysplit = key.split(':')
                yearkey = keysplit[0]
                seasonkey = keysplit[1]
                monthkey = keysplit[2]
                stationkey = keysplit[3]
                visitkey = keysplit[4]
                depthkey = keysplit[5]
                taxonkey = keysplit[6]
                #
                resulttable[0][colindex + 1] = selectedparameter
                resulttable[1][colindex + 1] = yearkey
                resulttable[2][colindex + 1] = seasonkey
                resulttable[3][colindex + 1] = monthkey
                resulttable[4][colindex + 1] = stationkey
                resulttable[5][colindex + 1] = visitkey
                resulttable[6][colindex + 1] = depthkey
                resulttable[7][colindex + 1] = taxonkey
                # Data.
                resulttable[8][colindex + 1] = 'Values'
                for rowindex, value in enumerate(data_dict[key]):
                    resulttable[rowindex + 9][colindex + 1] = value
            # Header.
            header = emptyrow[:]
            tabledata.set_header(header)
            # Rows.
            for row in resulttable:
                tabledata.append_row(row)  
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
           
    def _plot_graph(self):
        """ """
        try:
            # Show the Graph plotter tool if hidden. 
            app_tools.ToolManager().show_tool_by_name('Graph plotter')
            graphtool = app_tools.ToolManager().get_tool_by_name('Graph plotter')
            graphtool.clear_plot_data()
            # Filtered data should be used.
            self._main_activity.update_filter() # Must be done before create_filtered_dataset().
            analysisdata = self._analysisdata.create_filtered_dataset()
            if not analysisdata:
                return # Can't create a report from an empty dataset.
            # Which parameter is selected?
            selectedparameter = str(self._parameter_list.currentText())
            # Split by.
            split_on_year = self._splitby_year_checkbox.isChecked()
            split_on_season = self._splitby_season_checkbox.isChecked()
            split_on_month = self._splitby_month_checkbox.isChecked()
            split_on_station = self._splitby_station_checkbox.isChecked()
            split_on_visit = self._splitby_visit_checkbox.isChecked()
            split_on_depth = self._splitby_depth_checkbox.isChecked()
            split_on_taxon = self._splitby_taxon_checkbox.isChecked()
            # Graph data.
            self._graph_plot_data = toolbox_utils.GraphPlotData(
                                        title = selectedparameter, 
                                        y_type = 'float',
                                        y_label = '')
            # Create subplots.
            self._extract_plot_values(analysisdata,
                                      selectedparameter, 
                                      split_on_year,
                                      split_on_season,
                                      split_on_month,
                                      split_on_station,
                                      split_on_visit,
                                      split_on_depth,
                                      split_on_taxon)
            # View in the graph-plot tool.    
            graphtool.set_chart_selection(chart = 'Boxplot chart',
                                        combined = True, stacked = False, y_log_scale = False)
            graphtool.set_plot_data(self._graph_plot_data)   
            
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
    
    def _extract_plot_values(self, dataset,
                        selectedparameter, 
                        split_on_year = False,
                        split_on_season = False,
                        split_on_month = False,
                        split_on_station = False,
                        split_on_visit = False,
                        split_on_depth = False,
                        split_on_taxon = False):
        """ """
        try:
            # Target list.
            data_dict = {}        
            #
            for visitnode in dataset.get_children():
                visitdate = visitnode.get_data('sample_date')
                visitstation = visitnode.get_data('station_name')
                visitvisit = visitstation + ' ' + visitdate 
                visityear = str(visitdate[0:4])
                visitmonth = str(visitdate[5:7])
                visitseason = ''
                if visitmonth in ['12', '01','02']:
                    visitseason = 'Dec-Jan-Feb'
                elif visitmonth in ['03', '04','05']:
                    visitseason = 'Mar-Apr-May'
                elif visitmonth in ['06', '07','08']:
                    visitseason = 'Jun-Jul-Aug'
                elif visitmonth in ['09', '10','11']:
                    visitseason = 'Sep-Oct-Nov'
                #
                for samplenode in visitnode.get_children():
                    sample_min_depth_m = str(samplenode.get_data('sample_min_depth_m'))
                    sample_max_depth_m = str(samplenode.get_data('sample_max_depth_m'))
                    sampleminmaxdepth = sample_min_depth_m + '-' + sample_max_depth_m   
                    # Iterate over sample content. 
                    # Note: Create a level between sample and variabel.
                    grouped_size_lifestages = {}
                    for variablenode in samplenode.get_children():
                        group_key = variablenode.get_data('scientific_name')
                        group_key += ':' + variablenode.get_data('size_class') # Specific for phytoplankton.
                        group_key += ':' + variablenode.get_data('stage') # Specific for zooplankton.
                        group_key += ':' + variablenode.get_data('sex') # Specific for zooplankton.
                        if group_key not in grouped_size_lifestages:
                            grouped_size_lifestages[group_key] = [] # Starts a new group.
                        grouped_size_lifestages[group_key].append(variablenode)
                    
                    # Get variables from the new set of groups.
                    for group_key in grouped_size_lifestages.keys():
                        #
                        for variablenode in grouped_size_lifestages[group_key]:
                            variabletaxon = variablenode.get_data('scientific_name')
                            # Parameters.
                            parameter = variablenode.get_data('parameter')
                            unit = variablenode.get_data('unit')
                            parameternadunit = parameter + ' (' + unit + ')'
                            if parameternadunit == selectedparameter:
                                # Build split key.
                                splitkey_list = []
                                if split_on_year: 
                                    splitkey_list.append(visityear)
                                if split_on_season: 
                                    splitkey_list.append(visitseason)
                                if split_on_month: 
                                    splitkey_list.append(visitmonth)
                                if split_on_station: 
                                    splitkey_list.append(visitstation)
                                if split_on_visit: 
                                    splitkey_list.append(visitvisit)
                                if split_on_depth: 
                                    splitkey_list.append(sampleminmaxdepth)
                                if split_on_taxon: 
                                    splitkey_list.append(variabletaxon)
                                #
                                splitkey = ':'.join(splitkey_list)
                                # Add data.
                                if splitkey not in data_dict:
                                    data_dict[splitkey] = []
                                data_dict[splitkey].append(variablenode.get_data('value'))     
            # Calculate result
            try:
                for key in sorted(data_dict.keys()):
                    self._graph_plot_data.add_plot(plot_name = key, y_array = data_dict[key])
            except UserWarning as e:
                QtWidgets.QMessageBox.warning(self, 'Warning', str(e))
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
