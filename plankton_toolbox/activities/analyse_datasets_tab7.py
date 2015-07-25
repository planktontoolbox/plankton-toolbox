#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

# import math
import numpy
# import scipy.stats as stats
# import scipy.stats.mstats as mstats

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
# import plankton_toolbox.tools.tool_manager as tool_manager
# import plankton_toolbox.toolbox.utils_qt as utils_qt
# import plankton_toolbox.toolbox.help_texts as help_texts
import plankton_toolbox.tools.tool_manager as tool_manager
# import envmonlib
import toolbox_utils
import toolbox_core

class AnalyseDatasetsTab7(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab7, self).__init__()

    def setMainActivity(self, main_activity):
        """ """
        self._main_activity = main_activity
        self._analysisdata = main_activity.getAnalysisData()
                
    def clear(self):
        """ """
        self._parameter_list.clear()
        
    def update(self):
        """ """
        self.clear()
        analysisdata = self._analysisdata.get_data()
        if analysisdata:        
            # Search for all parameters in analysis data.
            parameterset = set()
            for visitnode in analysisdata.getChildren():
                for samplenode in visitnode.getChildren():
                    for variablenode in samplenode.getChildren():
                        parameterset.add(variablenode.get_data('parameter') + ' (' + variablenode.get_data('unit') + ')')
            parameterlist = sorted(parameterset)
            self._parameter_list.addItems(parameterlist)

    # ===== TAB: Statistics ===== 
    def contentStatistics(self):
        """ """
        # Active widgets and connections.
#         introlabel = utils_qt.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('AnalyseDatasetsTab7_intro'))
        # - Select parameter.
        self._parameter_list = QtGui.QComboBox()        
        self._parameter_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        # - Split by.
        self._splitby_year_checkbox = QtGui.QCheckBox('Year')
        self._splitby_year_checkbox.setChecked(False) 
        self._splitby_season_checkbox = QtGui.QCheckBox('Season')
        self._splitby_season_checkbox.setChecked(False) 
        self._splitby_month_checkbox = QtGui.QCheckBox('Month')
        self._splitby_month_checkbox.setChecked(False) 
        self._splitby_station_checkbox = QtGui.QCheckBox('Station')
        self._splitby_station_checkbox.setChecked(False) 
        self._splitby_visit_checkbox = QtGui.QCheckBox('Sampling event')
        self._splitby_visit_checkbox.setChecked(False) 
        self._splitby_depth_checkbox = QtGui.QCheckBox('Depth')
        self._splitby_depth_checkbox.setChecked(False) 
        self._splitby_taxon_checkbox = QtGui.QCheckBox('Scientific name')
        self._splitby_taxon_checkbox.setChecked(False) 
        # - View data.
        self._viewdata_button = QtGui.QPushButton('View data')
        self.connect(self._viewdata_button, QtCore.SIGNAL('clicked()'), self._viewData)                
        # - Calculate statistics.
        self._calcstatistics_button = QtGui.QPushButton('Calculate statistics')
        self.connect(self._calcstatistics_button, QtCore.SIGNAL('clicked()'), self._calcStats)                
        # - Plot graph.
        self._plotgraphs_button = QtGui.QPushButton('Plot graph')
        self.connect(self._plotgraphs_button, QtCore.SIGNAL('clicked()'), self._plotGraph)                

        # Layout widgets.
        form1 = QtGui.QGridLayout()
        label1 = QtGui.QLabel('Parameter:')
        label2 = QtGui.QLabel('Split by:')
        stretchlabel1 = QtGui.QLabel('')
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
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addStretch(10)
        hbox2.addWidget(self._viewdata_button)
        hbox2.addWidget(self._calcstatistics_button)
        hbox2.addWidget(self._plotgraphs_button)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        layout.addLayout(hbox2)
        self.setLayout(layout)                
        #
        return self
        
    def _calcStats(self):
        """ """
        # Clear the statistical data and view the statistic area.
        statisticaldata = self._main_activity.getStatisticalData()
        statisticaldata.clear_data()
        self._main_activity.viewStatisticalData()
        # Filtered data should be used.
        self._main_activity.updateFilter() # Must be done before create_filtered_dataset().
        analysisdata = self._analysisdata.create_filtered_dataset()
        if not analysisdata:
            return # Can't create a report from an empty dataset.
        # Which parameter is selected?
        selectedparameter = unicode(self._parameter_list.currentText())
        # Split by.
        split_on_year = self._splitby_year_checkbox.isChecked()
        split_on_season = self._splitby_season_checkbox.isChecked()
        split_on_month = self._splitby_month_checkbox.isChecked()
        split_on_station = self._splitby_station_checkbox.isChecked()
        split_on_visit = self._splitby_visit_checkbox.isChecked()
        split_on_depth = self._splitby_depth_checkbox.isChecked()
        split_on_taxon = self._splitby_taxon_checkbox.isChecked()
        # Calculate the statistics.
        self._calcStatistics(analysisdata, statisticaldata,
                                  selectedparameter, 
                                  split_on_year,
                                  split_on_season,
                                  split_on_month,
                                  split_on_station,
                                  split_on_visit,
                                  split_on_depth,
                                  split_on_taxon)
        # View the result in the report area.
        self._main_activity.viewStatisticalData()
        
    def _calcStatistics(self, dataset, reportdata,
                        selectedparameter, 
                        split_on_year = False,
                        split_on_season = False,
                        split_on_month = False,
                        split_on_station = False,
                        split_on_visit = False,
                        split_on_depth = False,
                        split_on_taxon = False):
        """ """
        # Target list.
        data_dict = {}        
        # Create a dataset (table, not tree).
        tabledata = toolbox_core.DatasetTable()
        reportdata.setData(tabledata)
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
        tabledata.setHeader(header_row)
        # Extract values.
        yearkey = ''
        monthkey = ''
        seasonkey = ''
        stationkey = ''
        visitkey = ''
        depthkey = ''
        taxonkey = ''
        #
        for visitnode in dataset.getChildren():
            visitdate = visitnode.get_data('date')
            visitstation = visitnode.get_data('station_name')
            visitvisit = visitstation + ' ' + visitdate 
            visityear = unicode(visitdate[0:4])
            visitmonth = unicode(visitdate[5:7])
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
            for samplenode in visitnode.getChildren():
                sample_min_depth = unicode(samplenode.get_data('sample_min_depth'))
                sample_max_depth = unicode(samplenode.get_data('sample_max_depth'))
                sampleminmaxdepth = sample_min_depth + '-' + sample_max_depth   
                # Iterate over sample content. 
                # Note: Create a level between sample and variabel.
                grouped_size_lifestages = {}
                for variablenode in samplenode.getChildren():
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
                data_list = map(float, data_dict[key])
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
                print(', '.join(map(unicode, data_list))) # Print data.
                print 'Error in calc statistics: ' + e # Print exception.            
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
            tabledata.appendRow(report_row)


    def _viewData(self):
        """ """
        # Clear the statistical data and view the statistic area.
        statisticaldata = self._main_activity.getStatisticalData()
        statisticaldata.clear_data()
        self._main_activity.viewStatisticalData()
        # Filtered data should be used.
        self._main_activity.updateFilter() # Must be done before create_filtered_dataset().
        analysisdata = self._analysisdata.create_filtered_dataset()
        if not analysisdata:
            return # Can't create a report from an empty dataset.
        # Which parameter is selected?
        selectedparameter = unicode(self._parameter_list.currentText())
        # Split by.
        split_on_year = self._splitby_year_checkbox.isChecked()
        split_on_season = self._splitby_season_checkbox.isChecked()
        split_on_month = self._splitby_month_checkbox.isChecked()
        split_on_station = self._splitby_station_checkbox.isChecked()
        split_on_visit = self._splitby_visit_checkbox.isChecked()
        split_on_depth = self._splitby_depth_checkbox.isChecked()
        split_on_taxon = self._splitby_taxon_checkbox.isChecked()
        # Calculate the statistics.
        self._extractValues(analysisdata, statisticaldata,
                                  selectedparameter, 
                                  split_on_year,
                                  split_on_season,
                                  split_on_month,
                                  split_on_station,
                                  split_on_visit,
                                  split_on_depth,
                                  split_on_taxon)
        # View the result in the report area.
        self._main_activity.viewStatisticalData()
        
    def _extractValues(self, dataset, reportdata,
                        selectedparameter, 
                        split_on_year = False,
                        split_on_season = False,
                        split_on_month = False,
                        split_on_station = False,
                        split_on_visit = False,
                        split_on_depth = False,
                        split_on_taxon = False):
        """ """
        # Target list.
        data_dict = {}        
        # Create a dataset (table, not tree).
        tabledata = toolbox_core.DatasetTable()
        reportdata.setData(tabledata)
        # Extract values.
        yearkey = ''
        monthkey = ''
        seasonkey = ''
        stationkey = ''
        visitkey = ''
        depthkey = ''
        taxonkey = ''
        #
        for visitnode in dataset.getChildren():
            visitdate = visitnode.get_data('date')
            visitstation = visitnode.get_data('station_name')
            visitvisit = visitstation + ' ' + visitdate 
            visityear = unicode(visitdate[0:4])
            visitmonth = unicode(visitdate[5:7])
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
            for samplenode in visitnode.getChildren():
                sample_min_depth = unicode(samplenode.get_data('sample_min_depth'))
                sample_max_depth = unicode(samplenode.get_data('sample_max_depth'))
                sampleminmaxdepth = sample_min_depth + '-' + sample_max_depth   
                # Iterate over sample content. 
                # Note: Create a level between sample and variabel.
                grouped_size_lifestages = {}
                for variablenode in samplenode.getChildren():
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
        tabledata.setHeader(header)
        # Rows.
        for row in resulttable:
            tabledata.appendRow(row)  
           
    def _plotGraph(self):
        """ """
        # Show the Graph plotter tool if hidden. 
        tool_manager.ToolManager().show_tool_by_name('Graph plotter')
        graphtool = tool_manager.ToolManager().get_tool_by_name('Graph plotter')
        graphtool.clear_plot_data()
        # Filtered data should be used.
        self._main_activity.updateFilter() # Must be done before create_filtered_dataset().
        analysisdata = self._analysisdata.create_filtered_dataset()
        if not analysisdata:
            return # Can't create a report from an empty dataset.
        # Which parameter is selected?
        selectedparameter = unicode(self._parameter_list.currentText())
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
        self._extractPlotValues(analysisdata,
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
        
    def _extractPlotValues(self, dataset,
                        selectedparameter, 
                        split_on_year = False,
                        split_on_season = False,
                        split_on_month = False,
                        split_on_station = False,
                        split_on_visit = False,
                        split_on_depth = False,
                        split_on_taxon = False):
        """ """
        # Target list.
        data_dict = {}        
        #
        for visitnode in dataset.getChildren():
            visitdate = visitnode.get_data('date')
            visitstation = visitnode.get_data('station_name')
            visitvisit = visitstation + ' ' + visitdate 
            visityear = unicode(visitdate[0:4])
            visitmonth = unicode(visitdate[5:7])
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
            for samplenode in visitnode.getChildren():
                sample_min_depth = unicode(samplenode.get_data('sample_min_depth'))
                sample_max_depth = unicode(samplenode.get_data('sample_max_depth'))
                sampleminmaxdepth = sample_min_depth + '-' + sample_max_depth   
                # Iterate over sample content. 
                # Note: Create a level between sample and variabel.
                grouped_size_lifestages = {}
                for variablenode in samplenode.getChildren():
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
                self._graph_plot_data.addPlot(plot_name = key, y_array = data_dict[key])
        except UserWarning as e:
            QtGui.QMessageBox.warning(self, 'Warning', unicode(e))
