#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.tools.tool_manager as tool_manager
# import plankton_toolbox.toolbox.utils_qt as utils_qt
# import plankton_toolbox.toolbox.help_texts as help_texts
import envmonlib

class AnalyseDatasetsTab5(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab5, self).__init__()

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

    # ===== TAB: Predefined graphs ===== 
    def contentPredefinedGraphs(self):
        """ """
        # Active widgets and connections.
#         introlabel = utils_qt.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText(u'AnalyseDatasetsTab5_intro'))
        # - Select parameter:
        self._parameter_list = QtGui.QComboBox()        
        self._parameter_list.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        #
        # Predefined graphs.
        self._addplot_1_button = QtGui.QPushButton("Time series")
        self.connect(self._addplot_1_button, QtCore.SIGNAL("clicked()"), self._addPlot_1)                
        self._addplot_1_subplot_button = QtGui.QPushButton("Add plot")
        self.connect(self._addplot_1_subplot_button, QtCore.SIGNAL("clicked()"), self._addSubPlot_1)                
        self._addplot_2_button = QtGui.QPushButton("Seasonal cycle")
        self.connect(self._addplot_2_button, QtCore.SIGNAL("clicked()"), self._addPlot_2)                
        self._addplot_2_subplot_button = QtGui.QPushButton("Add plot")
        self.connect(self._addplot_2_subplot_button, QtCore.SIGNAL("clicked()"), self._addSubPlot_2)                
        self._addplot_3_button = QtGui.QPushButton("Values for taxa / station and date")
        self.connect(self._addplot_3_button, QtCore.SIGNAL("clicked()"), self._addPlot_3)                
        self._addplot_4_button = QtGui.QPushButton("Values for station and date / taxa")
        self.connect(self._addplot_4_button, QtCore.SIGNAL("clicked()"), self._addPlot_4)                

        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Parameter:")
        stretchlabel = QtGui.QLabel("")
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
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        self.setLayout(layout)                
        #
        return self
        
    def _addPlot_1(self, subplot_only = False):
        """ """
        tool_manager.ToolManager().showToolByName(u'Graph plotter') # Show tool if hidden.
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plotter')
        if not subplot_only:
            graphtool.clearPlotData()
        # Filtered data should be used.
        self._main_activity.updateFilter() # Must be done before createFilteredDataset().
        analysisdata = self._analysisdata.createFilteredDataset()
        if not analysisdata:
            return # Can't plot from empty dataset
        # Which parameter is selected?
        selectedparameter = unicode(self._parameter_list.currentText())
        # 
        if not subplot_only:
            self._plotdata = envmonlib.GraphPlotData(
                                    title = u'Time series', 
                                    x_type = u'date',
                                    y_type = u'float',
                                    y_label = selectedparameter)
        #
        self._createPlotDataForTimeSeries(selectedparameter, analysisdata, self._plotdata)
        # Plot.
        graphtool.setChartSelection(chart = u"Scatter chart",
                                    combined = True, stacked = False, y_log_scale = False)
        graphtool.setPlotData(self._plotdata)
        
    def _addSubPlot_1(self):
        """ """
        self._addPlot_1(subplot_only = True)
        
    def _addPlot_2(self, subplot_only = False):
        """ """
        tool_manager.ToolManager().showToolByName(u'Graph plotter') # Show tool if hidden.
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plotter')
        if not subplot_only:
            graphtool.clearPlotData()
        # Filtered data should be used.
        self._main_activity.updateFilter() # Must be done before createFilteredDataset().
        analysisdata = self._analysisdata.createFilteredDataset()
        if not analysisdata:
            return # Can't plot from empty dataset
        # Which parameter is selected?
        selectedparameter = unicode(self._parameter_list.currentText())
        # 
        if not subplot_only:
            self._plotdata = envmonlib.GraphPlotData(
                                    title = u'Seasonal cycle', 
                                    x_type = u'date',
#                                     x_format = u'%Y-%m-%d',
                                    x_format = u'%m',
                                    y_type = u'float')
        #
        self._createPlotDataForSeasonalCycle(selectedparameter, analysisdata, self._plotdata)
        # Plot.
        graphtool.setChartSelection(chart = u"Scatter chart",
                                    combined = True, stacked = False, y_log_scale = False)
        graphtool.setPlotData(self._plotdata)
        
    def _addSubPlot_2(self):
        """ """
        self._addPlot_2(subplot_only = True)
        
    def _addPlot_3(self):
        """ """
        tool_manager.ToolManager().showToolByName(u'Graph plotter') # Show tool if hidden.
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plotter')
        graphtool.clearPlotData()
        # Filtered data should be used.
        self._main_activity.updateFilter() # Must be done before createFilteredDataset().
        analysisdata = self._analysisdata.createFilteredDataset()
        if not analysisdata:
            return # Can't plot from empty dataset
        # Which parameter is selected?
        selectedparameter = unicode(self._parameter_list.currentText())
        # 
        plotdata = envmonlib.GraphPlotData(
#                                 title = u'Values for taxa / station and date', 
                                title = selectedparameter, 
                                x_type = u'text',
                                y_type = u'float',
                                x_label = u'',
                                y_label = u'')
        #
        self._addPlotAaaaaaaaa(selectedparameter, analysisdata, plotdata)
        # Plot.
        graphtool.setChartSelection(chart = u"Bar chart",
                                    combined = True, stacked = False, y_log_scale = False)
        graphtool.setPlotData(plotdata)
        
        
    def _addPlot_4(self):
        """ """
        tool_manager.ToolManager().showToolByName(u'Graph plotter') # Show tool if hidden.
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plotter')
        graphtool.clearPlotData()
        # Filtered data should be used.
        self._main_activity.updateFilter() # Must be done before createFilteredDataset().
        analysisdata = self._analysisdata.createFilteredDataset()
        if not analysisdata:
            return # Can't plot from empty dataset
        # Which parameter is selected?
        selectedparameter = unicode(self._parameter_list.currentText())
        # 
        plotdata = envmonlib.GraphPlotData(
                                title = selectedparameter, 
                                x_type = u'text',
                                y_type = u'float',
                                x_label = u'',
                                y_label = u'')
        #
        self._addPlotBbbbbbbbb(selectedparameter, analysisdata, plotdata)
        # Plot.
        graphtool.setChartSelection(chart = u"Bar chart",
                                    combined = True, stacked = False, y_log_scale = False)
        graphtool.setPlotData(plotdata)

    def _createPlotDataForTimeSeries(self, selectedparameter, dataset, plotdata):
        """ """
        # Extract values for the plot.
        date = None
        value = None
        date_list = []
        value_list = [] 
        for visitnode in dataset.getChildren():
            date = visitnode.getData(u"date")
            for samplenode in visitnode.getChildren():
                for variablenode in samplenode.getChildren():
                    parameter = variablenode.getData(u"parameter") + u' (' + variablenode.getData(u'unit') + u')'
                    if parameter == selectedparameter:                        
                        value = variablenode.getData(u"value")
                        date_list.append(date)
                        value_list.append(value)               
        #                
        try:
            plotdata.addPlot(plot_name = selectedparameter, 
                             x_array = date_list, 
                             y_array = value_list, 
                             x_label = u'',
                             y_label = u'')
        except UserWarning, e:
            QtGui.QMessageBox.warning(self._main_activity, "Warning", unicode(e))


    def _createPlotDataForSeasonalCycle(self, selectedparameter, dataset, plotdata):
        """ """
        # Extract values for the plot.
        date = None
        value = None
        date_list = []
        value_list = [] 
        for visitnode in dataset.getChildren():
            # Replace year with '0000' seasonal cycle.
            date = visitnode.getData(u"date")
            try: 
                date = unicode(u'2000' + date[4:])
            except:
                continue # Skip to the next if date is invalid.
            #
            for samplenode in visitnode.getChildren():
                for variablenode in samplenode.getChildren():
                    parameter = variablenode.getData(u"parameter") + u' (' + variablenode.getData(u'unit') + u')'
                    if parameter == selectedparameter:                        
                        value = variablenode.getData(u"value")
                        date_list.append(date)
                        value_list.append(value)               
        #                
        try:
            plotdata.addPlot(plot_name = selectedparameter, 
                             x_array = date_list, 
                             y_array = value_list, 
                             x_label = u'',
                             y_label = u'')
        except UserWarning, e:
            QtGui.QMessageBox.warning(self._main_activity, "Warning", unicode(e))
    
    def _addPlotAaaaaaaaa(self, selectedparameter, dataset, plotdata):
        """ """
        # Step 1: Create lists of visits and taxa.
        visit_set = set()
        taxon_set = set()
        for visitnode in dataset.getChildren():
            #
            visit_set.add(unicode(visitnode.getData(u"station_name")) + " : " + unicode(visitnode.getData(u"date"))) # Station name
            #
            for samplenode in visitnode.getChildren():
                #
                for variablenode in samplenode.getChildren():
                    #
                    taxonname = variablenode.getData(u"scientific_name")
                    if taxonname:
                        taxon_set.add(taxonname)
                    else:
                        taxon_set.add(u'---')
        # Step 2: Create a station dictionary containing taxa and value for each taxa.
        visit_taxon_dict = {}
        for visit in visit_set:
            visit_taxon_dict[visit] = {} 
            for taxon in taxon_set:
                visit_taxon_dict[visit][taxon] = 0.0
        # Step 3: Fill with data.
        for visitnode in dataset.getChildren():
            #
            visit = (unicode(visitnode.getData(u'station_name')) + u' : ' + unicode(visitnode.getData(u'date')))
            for samplenode in visitnode.getChildren():
                #
                for variablenode in samplenode.getChildren():
                    #
                    taxonname = variablenode.getData(u"scientific_name")
                    if not taxonname:
                        taxonname = u'---'
                    parameter = variablenode.getData(u"parameter") + u' (' + variablenode.getData(u'unit') + u')'
                    if parameter == selectedparameter:                        
                        value = variablenode.getData(u"value")
                        try:
                            visit_taxon_dict[visit][taxonname] += float(value)
                        except:
                            envmonlib.Logging().warning("Float conversion (2) failed: Station: " + visit + 
                                   " Taxon name: " + taxonname + 
                                   " Parameter: " + selectedparameter + 
                                   " Value: " + unicode(variablenode.getData(u"value")))
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
                plotdata.addPlot(plot_name = taxon, 
                                    x_array = visit_list, 
                                    y_array = taxon_visit_value_list, 
                                    x_label = u'',
                                    y_label = selectedparameter)
            except UserWarning, e:
                QtGui.QMessageBox.warning(self._main_activity, "Warning", unicode(e))

    def _addPlotBbbbbbbbb(self, selectedparameter, dataset, plotdata):
        """ """
        # Step 1: Create lists of visits and taxa.
        visit_set = set()
        taxon_set = set()
        for visitnode in dataset.getChildren():
            #
            visit_set.add(unicode(visitnode.getData(u"station_name")) + " : " + unicode(visitnode.getData(u"date"))) # Station name
            #
            for samplenode in visitnode.getChildren():
                #
                for variablenode in samplenode.getChildren():
                    #
                    taxonname = variablenode.getData(u"scientific_name")
                    if taxonname:
                        taxon_set.add(taxonname)
                    else:
                        taxon_set.add(u'---')
#        # Step 2: Create a station dictionary containing taxa and value for each taxa.
        # Step 2: Create a taxa dictionary containing visits and value for each visit.
        taxon_visit_dict = {}
        for taxon in taxon_set:
            taxon_visit_dict[taxon] = {} 
            for visit in visit_set:
                taxon_visit_dict[taxon][visit] = 0.0
        # Step 3: Fill with data.
        for visitnode in dataset.getChildren():
            #
            visit = (unicode(visitnode.getData(u'station_name')) + u' : ' + unicode(visitnode.getData(u'date')))
            for samplenode in visitnode.getChildren():
                #
                for variablenode in samplenode.getChildren():
                    #
                    taxonname = variablenode.getData(u"scientific_name")
                    if not taxonname:
                        taxonname = u'---'
                    parameter = variablenode.getData(u"parameter") + u' (' + variablenode.getData(u'unit') + u')'
                    if parameter == selectedparameter:                        
                        value = variablenode.getData(u"value")
                        try:
                            taxon_visit_dict[taxonname][visit] += float(value)
                        except:
                            envmonlib.Logging().warning("Float conversion failed: Visit: " + visit + 
                                   " Taxon name: " + taxonname + 
                                   " Parameter: " + selectedparameter + 
                                   " Value: " + unicode(variablenode.getData(u"value")))
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
                plotdata.addPlot(plot_name = visit, 
                                    x_array = taxon_list, 
                                    y_array = visit_taxon_value_list, 
                                    x_label = u'',
                                    y_label = selectedparameter)
            except UserWarning, e:
                QtGui.QMessageBox.warning(self._main_activity, "Warning", unicode(e))

