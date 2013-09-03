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

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.toolbox.help_texts as help_texts
import envmonlib

class AnalyseDatasetsTab8(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab8, self).__init__()

    def setMainActivity(self, main_activity):
        """ """
        self._main_activity = main_activity
        self._analysisdata = main_activity.getAnalysisData()
                
    def clear(self):
        """ """
#         self._parameter_list.clear()
        
    def update(self):
        """ """
#         self.clear()
#         analysisdata = self._analysisdata.getData()
#         if analysisdata:        
#             # Search for all parameters in analysis data.
#             parameterset = set()
#             for visitnode in analysisdata.getChildren():
#                 for samplenode in visitnode.getChildren():
#                     for variablenode in samplenode.getChildren():
#                         parameterset.add(unicode(variablenode.getData(u"parameter")))
#             parameterlist = sorted(parameterset)
#             self._parameter_list.addItems(parameterlist)

    # ===== TAB: Reports ===== 
    def contentReports(self):
        """ """
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText(help_texts.HelpTexts().getText(u'AnalyseDatasetsTab8_intro'))
               
        # - Select parameter:
#         self._parameter_list = QtGui.QComboBox()        
#         self._parameter_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        #
        # Predefined graphs.
        self._report_1_button = QtGui.QPushButton("Zooplankton: Abundance m2 and m3, length median and mean")
        self.connect(self._report_1_button, QtCore.SIGNAL("clicked()"), self._createReport_1)                

        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
#         label1 = QtGui.QLabel("Parameter:")
        stretchlabel = QtGui.QLabel("")
#         form1.addWidget(label1, gridrow, 0, 1, 1)
#         form1.addWidget(self._parameter_list, gridrow, 1, 1, 1)
        form1.addWidget(stretchlabel, gridrow, 4, 1, 20)
        form1.addWidget(self._report_1_button, gridrow, 3, 1, 1)
#         gridrow += 1
#         form1.addWidget(self._addplot_2_button, gridrow, 3, 1, 1)
#         gridrow += 1
#         form1.addWidget(self._addplot_3_button, gridrow, 3, 1, 1)
#         gridrow += 1
#         form1.addWidget(self._addplot_4_button, gridrow, 3, 1, 1)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        self.setLayout(layout)                
        #
        return self
        
    def _createReport_1(self):
        """ """
        # Clear the report and view the report area.
        reportdata = self._main_activity.getReportData()
        reportdata.clearData()
        self._main_activity.viewReportData()
        # Filtered data should be used.
        self._main_activity.updateFilter() # Must be done before createFilteredDataset().
        analysisdata = self._analysisdata.createFilteredDataset()
        if not analysisdata:
            return # Can't create a report from an empty dataset.
        # Create the report.
        self._createReportZooplanktonAbundanceLengthMedianAndMean(analysisdata, reportdata)
        # View the result in the report area.
        self._main_activity.viewReportData()

    def _createReportZooplanktonAbundanceLengthMedianAndMean(self, dataset, reportdata):
        """ """
        # Create a dataset (table, not tree).
        tabledata = envmonlib.DatasetTable()
        reportdata.setData(tabledata)
        # Header.
        header_row = []
        header_row.append('Station name')
        header_row.append('Date')
        header_row.append('Sample min depth')
        header_row.append('Sample max depth')
        header_row.append('Taxon_name')
        header_row.append('Stage')
        header_row.append('Sex')
        header_row.append('Abundance (ind/m2)')
        header_row.append('Abundance (ind/m3)')
        header_row.append('Length (median)')
        header_row.append('Length (mean)')
        tabledata.setHeader(header_row)
        # Extract values for the plot.
        date = u'-'
        station_name = u'-'
        sample_min_depth = u'-'
        sample_max_depth = u'-'
        for visitnode in dataset.getChildren():
            station_name = visitnode.getData(u"station_name")
            date = visitnode.getData(u"date")
            for samplenode in visitnode.getChildren():
                sample_min_depth = samplenode.getData(u"sample_min_depth")
                sample_max_depth = samplenode.getData(u"sample_max_depth")
                
                # Iterate over sample content. 
                # Note: Create a level between sample and variabel.
                grouped_lifestages = {}
                for variablenode in samplenode.getChildren():
                    group_key = variablenode.getData(u'taxon_name')
                    group_key += u':' + variablenode.getData(u'stage') # Specific for zooplankton.
                    group_key += u':' + variablenode.getData(u'sex') # Specific for zooplankton.
                    if group_key not in grouped_lifestages:
                        grouped_lifestages[group_key] = [] # Starts a new group.
                    grouped_lifestages[group_key].append(variablenode)
                
                # Get variables from the new set of groups.
                for group_key in grouped_lifestages.keys():
                    # This should be available in each group.
                    taxon_name = u'-'
                    stage = u'-'
                    sex = u'-'
                    abundance_ind_m2 = u'-'
                    abundance_ind_m3 = u'-'
                    length_median = u'-'
                    length_mean = u'-'
                    #
                    for variablenode in grouped_lifestages[group_key]:
                        # This should be same for all variables in the group.                       
                        taxon_name = variablenode.getData(u'taxon_name')
                        stage = variablenode.getData(u'stage')
                        sex = variablenode.getData(u'sex')
                        # Parameters.
                        parameter = variablenode.getData(u'parameter')
                        unit = variablenode.getData(u'unit')
                        if (parameter == u'Abundance') and (unit == u'ind/m2'):
                            abundance_ind_m2 = variablenode.getData(u'value')
                        if (parameter == u'Abundance') and (unit == u'ind/m3'):
                            abundance_ind_m3 = variablenode.getData(u'value')
                        if parameter == u'Length (median)':
                            length_median = variablenode.getData(u'value')
                        if parameter == u'Length (mean)':
                            length_mean = variablenode.getData(u'value')
                    
                    # Organism group is finished. Add row to report.
                    report_row = []
                    report_row.append(station_name)
                    report_row.append(date)
                    report_row.append(sample_min_depth)
                    report_row.append(sample_max_depth)
                    report_row.append(taxon_name)
                    report_row.append(stage)
                    report_row.append(sex)
                    report_row.append(abundance_ind_m2)
                    report_row.append(abundance_ind_m3)
                    report_row.append(length_median)
                    report_row.append(length_mean)
                    #
                    tabledata.appendRow(report_row)

