#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2013 SMHI, Swedish Meteorological and Hydrological Institute 
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

# import math
import numpy
# import scipy.stats as stats
# import scipy.stats.mstats as mstats

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
# import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.toolbox.help_texts as help_texts
import envmonlib

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
        analysisdata = self._analysisdata.getData()
        if analysisdata:        
            # Search for all parameters in analysis data.
            parameterset = set()
            for visitnode in analysisdata.getChildren():
                for samplenode in visitnode.getChildren():
                    for variablenode in samplenode.getChildren():
                        parameterset.add(variablenode.getData(u'parameter') + u' (' + variablenode.getData(u'unit') + u')')
            parameterlist = sorted(parameterset)
            self._parameter_list.addItems(parameterlist)

    # ===== TAB: Statistics ===== 
    def contentStatistics(self):
        """ """
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText(help_texts.HelpTexts().getText(u'AnalyseDatasetsTab7_intro'))
              
        # - Select parameter.
        self._parameter_list = QtGui.QComboBox()        
        self._parameter_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        # - Split by.
        self._splitby_year_checkbox = QtGui.QCheckBox("Year")
        self._splitby_year_checkbox.setChecked(False) 
        self._splitby_season_checkbox = QtGui.QCheckBox("Season")
        self._splitby_season_checkbox.setChecked(False) 
        self._splitby_month_checkbox = QtGui.QCheckBox("Month")
        self._splitby_month_checkbox.setChecked(False) 
        self._splitby_station_checkbox = QtGui.QCheckBox("Station")
        self._splitby_station_checkbox.setChecked(False) 
        self._splitby_visit_checkbox = QtGui.QCheckBox("Sampling event")
        self._splitby_visit_checkbox.setChecked(False) 
        self._splitby_depth_checkbox = QtGui.QCheckBox("Depth")
        self._splitby_depth_checkbox.setChecked(False) 
        self._splitby_taxon_checkbox = QtGui.QCheckBox("Taxon")
        self._splitby_taxon_checkbox.setChecked(False) 
        # - Calculate statistics.
        self._calcstatistics_button = QtGui.QPushButton("Calculate statistics")
        self.connect(self._calcstatistics_button, QtCore.SIGNAL("clicked()"), self._calcStats)                

        # Layout widgets.
        form1 = QtGui.QGridLayout()
        label1 = QtGui.QLabel("Parameter:")
        label2 = QtGui.QLabel("Split by:")
        stretchlabel1 = QtGui.QLabel("")
        stretchlabel2 = QtGui.QLabel("")
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
        hbox2.addWidget(self._calcstatistics_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
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
        statisticaldata.clearData()
        self._main_activity.viewStatisticalData()
        # Filtered data should be used.
        self._main_activity.updateFilter() # Must be done before createFilteredDataset().
        analysisdata = self._analysisdata.createFilteredDataset()
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
        tabledata = envmonlib.DatasetTable()
        reportdata.setData(tabledata)
        # Header for result table.
        header_row = []
        header_row.append(u'Parameter')
        if split_on_year: header_row.append(u'Year')
        if split_on_season: header_row.append(u'Season')
        if split_on_month: header_row.append(u'Month')
        if split_on_station: header_row.append(u'Station')
        if split_on_visit: header_row.append(u'Sampling event')
        if split_on_depth: header_row.append(u'Depth')
        if split_on_taxon: header_row.append(u'Taxon')
        header_row.append(u'Mean')
        header_row.append(u'Median')
        header_row.append(u'Std. dev.')
        header_row.append(u'Min')
        header_row.append(u'Max')
        header_row.append(u'Counted values')
        tabledata.setHeader(header_row)
        # Extract values for the plot.
        yearkey = u''
        monthkey = u''
        seasonkey = u''
        stationkey = u''
        visitkey = u''
        depthkey = u''
        taxonkey = u''
        #
        for visitnode in dataset.getChildren():
            visitdate = visitnode.getData(u'date')
            visitstation = visitnode.getData(u'station_name')
            visitvisit = visitstation + u' ' + visitdate 
            visityear = unicode(visitdate[0:4])
            visitmonth = unicode(visitdate[5:7])
            visitseason = u''
            if visitmonth in [u'12', u'01',u'02']:
                visitseason = u'dec-jan-feb'
            elif visitmonth in [u'03', u'04',u'05']:
                visitseason = u'mar-apr-may'
            elif visitmonth in [u'06', u'07',u'08']:
                visitseason = u'jun-jul-aug'
            elif visitmonth in [u'09', u'10',u'11']:
                visitseason = u'sep-oct-nov'
            #
            for samplenode in visitnode.getChildren():
                sample_min_depth = unicode(samplenode.getData(u'sample_min_depth'))
                sample_max_depth = unicode(samplenode.getData(u'sample_max_depth'))
                sampleminmaxdepth = sample_min_depth + u'-' + sample_max_depth   
                # Iterate over sample content. 
                # Note: Create a level between sample and variabel.
                grouped_size_lifestages = {}
                for variablenode in samplenode.getChildren():
                    group_key = variablenode.getData(u'taxon_name')
                    group_key += u':' + variablenode.getData(u'size_class') # Specific for phytoplankton.
                    group_key += u':' + variablenode.getData(u'stage') # Specific for zooplankton.
                    group_key += u':' + variablenode.getData(u'sex') # Specific for zooplankton.
                    if group_key not in grouped_size_lifestages:
                        grouped_size_lifestages[group_key] = [] # Starts a new group.
                    grouped_size_lifestages[group_key].append(variablenode)
                
                # Get variables from the new set of groups.
                for group_key in grouped_size_lifestages.keys():
                    #
                    for variablenode in grouped_size_lifestages[group_key]:
                        variabletaxon = variablenode.getData(u'taxon_name')
                        # Parameters.
                        parameter = variablenode.getData(u'parameter')
                        unit = variablenode.getData(u'unit')
                        parameternadunit = parameter + u' (' + unit + u')'
                        if parameternadunit == selectedparameter:
                            # Build split key.
                            splitkey = u''
                            if split_on_year: splitkey += visityear
                            splitkey += u':'
                            if split_on_season: splitkey += visitseason
                            splitkey += u':'
                            if split_on_month: splitkey += visitmonth
                            splitkey += u':'
                            if split_on_station: splitkey += visitstation
                            splitkey += u':'
                            if split_on_visit: splitkey += visitvisit
                            splitkey += u':'
                            if split_on_depth: splitkey += sampleminmaxdepth
                            splitkey += u':'
                            if split_on_taxon: splitkey += variabletaxon
                            # Add data.
                            if splitkey not in data_dict:
                                data_dict[splitkey] = []
                            data_dict[splitkey].append(variablenode.getData(u'value'))
                             
        # Calculate result
        for key in sorted(data_dict.keys()):
            # Keys.
            keysplit = key.split(u':')
            yearkey = keysplit[0]
            seasonkey = keysplit[1]
            monthkey = keysplit[2]
            stationkey = keysplit[3]
            visitkey = keysplit[4]
            depthkey = keysplit[5]
            taxonkey = keysplit[6]
            # Data.
            data_list = data_dict[key]
            # Calculate result by use of numpy. 
            # Use float64 since we are using both small and big unit. 
            meanvalue = numpy.mean(data_list, dtype=numpy.float64)
            medianvalue = numpy.median(data_list)
            stddevvalue = numpy.std(data_list, dtype=numpy.float64)
            minvalue = numpy.nanmin(data_list) 
            maxvalue = numpy.nanmax(data_list)
            countedvalues = len(data_list)        
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
