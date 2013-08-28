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

import math

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_manager as tool_manager
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
                        parameterset.add(unicode(variablenode.getData(u"parameter")))
            parameterlist = sorted(parameterset)
            self._parameter_list.addItems(parameterlist)

    # ===== TAB: Statistics ===== 
    def contentStatistics(self):
        """ """
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText(help_texts.HelpTexts().getText(u'AnalyseDatasetsTab7_intro'))
               
        # - Select parameter:
        self._parameter_list = QtGui.QComboBox()        
        self._parameter_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        #
        # Predefined graphs.
        self._calcstat_1_button = QtGui.QPushButton("Whole period")
        self.connect(self._calcstat_1_button, QtCore.SIGNAL("clicked()"), self._calcStat_1)                
        self._calcstat_2_button = QtGui.QPushButton("Monthly mean")
        self.connect(self._calcstat_2_button, QtCore.SIGNAL("clicked()"), self._calcStat_2)                
        self._calcstat_3_button = QtGui.QPushButton("Seasonal cycle")
        self.connect(self._calcstat_3_button, QtCore.SIGNAL("clicked()"), self._calcStat_3)                
#         self._calcstat_4_button = QtGui.QPushButton("Aaaaa")
#         self.connect(self._calcstat_4_button, QtCore.SIGNAL("clicked()"), self._calcStat_4)  



        self._calcstat_2_button.setEnabled(False)
        self._calcstat_3_button.setEnabled(False)



              

        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Parameter:")
        stretchlabel = QtGui.QLabel("")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(self._parameter_list, gridrow, 1, 1, 1)
        form1.addWidget(stretchlabel, gridrow,4, 1, 20)
        form1.addWidget(self._calcstat_1_button, gridrow, 3, 1, 1)
        gridrow += 1
        form1.addWidget(self._calcstat_2_button, gridrow, 3, 1, 1)
        gridrow += 1
        form1.addWidget(self._calcstat_3_button, gridrow, 3, 1, 1)
#         gridrow += 1
#         form1.addWidget(self._calcstat_4_button, gridrow, 3, 1, 1)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        self.setLayout(layout)                
        #
        return self
        
    def _calcStat_1(self):
        """ """
        # Clear the statistic data and view the statistic area.
        statisticdata = self._main_activity.getStatisticData()
        statisticdata.clearData()
        self._main_activity.viewStatisticData()
        # Filtered data should be used.
        self._main_activity.updateFilter() # Must be done before createFilteredDataset().
        analysisdata = self._analysisdata.createFilteredDataset()
        if not analysisdata:
            return # Can't create a report from an empty dataset.
        # Which parameter is selected?
        selectedparameter = unicode(self._parameter_list.currentText())
        # Calculate the statistics.
        self._calcStatWholePeriod(selectedparameter, analysisdata, statisticdata)
        # View the result in the report area.
        self._main_activity.viewStatisticData()
        
    def _calcStat_2(self):
        """ """
        
    def _calcStat_3(self):
        """ """
        
    def _calcStat_4(self):
        """ """
        
    def _calcStatWholePeriod(self, selectedparameter, dataset, reportdata):
        """ """
        
        stats = RunningStats()
        
        
        # Create a dataset (table, not tree).
        tabledata = envmonlib.DatasetTable()
        reportdata.setData(tabledata)
        # Header.
        header_row = []
        header_row.append('Year from')
        header_row.append('Year to')
        header_row.append('Parameter')
        header_row.append('Mean')
        header_row.append('Median')
        header_row.append('Std. dev.')
        tabledata.setHeader(header_row)
        # Extract values for the plot.
        year_start = None
        year_end = None
        for visitnode in dataset.getChildren():
            current_year = visitnode.getData(u"year")
            if ( year_start is None) or (current_year < year_start):
                year_start = current_year
            if ( year_end is None) or (current_year > year_end):
                year_end = current_year
#             year_end = visitnode.getData(u"year")
            for samplenode in visitnode.getChildren():
                # Iterate over sample content. 
                # Note: Create a level between sample and variabel.
                grouped_organisms = {}
                for variablenode in samplenode.getChildren():
                    group_key = variablenode.getData(u'taxon_name')
                    group_key += u':' + variablenode.getData(u'size_class') # Specific for phytoplankton.
                    group_key += u':' + variablenode.getData(u'stage') # Specific for zooplankton.
                    group_key += u':' + variablenode.getData(u'sex') # Specific for zooplankton.
                    if group_key not in grouped_organisms:
                        grouped_organisms[group_key] = [] # Starts a new group.
                    grouped_organisms[group_key].append(variablenode)
                
                # Get variables from the new set of groups.
                for group_key in grouped_organisms.keys():
                    # Target list.
#                     data_list = []
                    #
                    for variablenode in grouped_organisms[group_key]:
                        # Parameters.
                        parameter = variablenode.getData(u'parameter')
                        unit = variablenode.getData(u'unit')
                        if parameter == selectedparameter:
#                             data_list.append(variablenode.getData(u'value'))
                            
                            stats.push(variablenode.getData(u'value'))
                            
                    
        # Calculate statistics.
        mean = stats.mean()
        stddev = stats.standard_deviation() 
        median = u'???'
        
        
        report_row = []
        report_row.append(year_start)
        report_row.append(year_end)
        report_row.append(selectedparameter)
        report_row.append(mean)
        report_row.append(median)
        report_row.append(stddev)
        #
        tabledata.appendRow(report_row)


class RunningStats:
    """ """
    def __init__(self):
        self.n = 0
        self.old_m = 0
        self.new_m = 0
        self.old_s = 0
        self.new_s = 0

    def clear(self):
        self.n = 0

    def push(self, x):
        self.n += 1

        if self.n == 1:
            self.old_m = self.new_m = x
            self.old_s = 0
        else:
            self.new_m = self.old_m + (x - self.old_m) / self.n
            self.new_s = self.old_s + (x - self.old_m) * (x - self.new_m)

            self.old_m = self.new_m
            self.old_s = self.new_s

    def mean(self):
        return self.new_m if self.n else 0.0

    def variance(self):
        return self.new_s / (self.n - 1) if self.n > 1 else 0.0

    def standard_deviation(self):
        return math.sqrt(self.variance())

