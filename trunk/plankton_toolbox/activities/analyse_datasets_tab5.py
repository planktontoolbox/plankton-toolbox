#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2011 SMHI, Swedish Meteorological and Hydrological Institute 
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

class AnalyseDatasetsTab5(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """
        super(AnalyseDatasetsTab5, self).__init__()

    def setMainActivity(self, main_activity):
        """ """
        self._main_activity = main_activity
                
    def clear(self):
        """ """
        self._parameter_list.clear()
        
    def update(self):
        """ """
        self.clear()
        currentdata = self._main_activity.getCurrentData()
        if currentdata:        
            # Search for all parameters in current data.
            parameterset = set()
            for visitnode in currentdata.getChildren():
                for samplenode in visitnode.getChildren():
                    for variablenode in samplenode.getChildren():
                        parameterset.add(variablenode.getData(u"Parameter"))
            parameterlist = sorted(parameterset)
            self._parameter_list.addItems(parameterlist)

    # ===== TAB: Prepared graphs ===== 
    def contentPreparedGraphs(self):
        """ """
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.
        """) 
               
        # - Select parameter:
        self._parameter_list = QtGui.QComboBox()        
        self._parameter_list.setMinimumContentsLength(20)
        #
        # Prepared graphs.
        self._addplot_1_button = QtGui.QPushButton("Plot 1. Aggreagated value / taxa / station (no filter)")
        self.connect(self._addplot_1_button, QtCore.SIGNAL("clicked()"), self._addPlot_1)                
        self._addplot_2_button = QtGui.QPushButton("Plot 2. Value / taxa / station and date")
        self.connect(self._addplot_2_button, QtCore.SIGNAL("clicked()"), self._addPlot_2)                
        self._addplot_3_button = QtGui.QPushButton("(Plot 3)")
        self.connect(self._addplot_3_button, QtCore.SIGNAL("clicked()"), self._addPlot_3)                
        self._addplot_4_button = QtGui.QPushButton("(Plot 4)")
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
        gridrow += 1
        form1.addWidget(self._addplot_2_button, gridrow, 3, 1, 1)
        gridrow += 1
        form1.addWidget(self._addplot_3_button, gridrow, 3, 1, 1)
        gridrow += 1
        form1.addWidget(self._addplot_4_button, gridrow, 3, 1, 1)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addStretch(1)
        self.setLayout(layout)                
        #
        return self
        
    def _addPlot_1(self):
        """ """
        currentdata = self._main_activity.getCurrentData()
        if not currentdata:        
            return
        #
        tool_manager.ToolManager().showToolByName(u'Graph plot') # Show tool if hidden.
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plot')

        # Step 1: Create lists of stations and taxa.
        station_set = set()
        taxon_set = set()
        for visitnode in currentdata.getChildren():
            station_set.add(visitnode.getData(u"Station name")) # Station name
            for samplenode in visitnode.getChildren():
                for variablenode in samplenode.getChildren():
                    taxonname = variablenode.getData(u"Taxon name")
                    if taxonname:
                        taxon_set.add(taxonname)
                    else:
                        taxon_set.add(u'---')
        # Step 2: Create a station dictionary containing taxa and value for each taxa.
        station_taxon_dict = {}
        for station in station_set:
            station_taxon_dict[station] = {} 
            for taxon in taxon_set:
                station_taxon_dict[station][taxon] = 0.0
        # Step 3. Which parameter is selected?
        selectedparameter = unicode(self._parameter_list.currentText())
        # Step 4: Fill with data.
        for visitnode in currentdata.getChildren():
            stationname = visitnode.getData(u"Station name")
            for samplenode in visitnode.getChildren():
                for variablenode in samplenode.getChildren():
                    taxonname = variablenode.getData(u"Taxon name")
                    if not taxonname:
                        taxonname = u'---'
                    parameter = variablenode.getData(u"Parameter")
                    if parameter == selectedparameter:                        
                        value = variablenode.getData(u"Value")
                        try:
#                            value = float(value.replace(u' ', u'').replace(u',', u'.'))
                            station_taxon_dict[stationname][taxonname] += float(value)
                        except:
                            print ("ERROR: Float conversion (1): Station: " + stationname + 
                                   " Taxon name: " + taxonname + " Value: " + unicode(variablenode.getData(u"Value")))
                            ###raise
        # Step 5: Reorganize. 
        station_list = sorted(station_set)
        taxon_list = sorted(taxon_set)
        taxon_station_value_list = []
        for taxonindex, taxon in enumerate(taxon_list):
            taxon_station_value_list.append([])
            for stationindex, station in enumerate(station_list):
                taxon_station_value_list[taxonindex].append(station_taxon_dict[station][taxon])
        # Step 6: Plot
        graphtool.addTestPlot(selectedparameter, station_list, taxon_list, taxon_station_value_list)
                
            
        
        
        
        
        
        
        
    def _addPlot_2(self):
        """ """

        selected_dict = self._main_activity.getSelectDataDict()
        selected_startdate = selected_dict[u'Start date']
        selected_enddate = selected_dict[u'End date']
#        selected_stations = selected_dict[u'Stations']
        selected_visits = selected_dict[u'Visits']
        selected_minmaxdepth =  selected_dict[u'Min max depth']
        selected_taxon = selected_dict[u'Taxon']
        selected_trophy = selected_dict[u'Trophy']
        
        currentdata = self._main_activity.getCurrentData()
        if not currentdata:        
            return
        #
        tool_manager.ToolManager().showToolByName(u'Graph plot') # Show tool if hidden.
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plot')

#       # Step 1: Create lists of stations and taxa.
        # Step 1: Create lists of visits and taxa.
#        station_set = set()
        visit_set = set()
        taxon_set = set()
        for visitnode in currentdata.getChildren():

            if selected_startdate > visitnode.getData(u'Date'):
                continue
            if selected_enddate < visitnode.getData(u'Date'):
                continue
#            if visitnode.getData(u'Station name') not in selected_stations:
#                continue
            if (visitnode.getData(u'Station name') + u' : ' + visitnode.getData(u'Date')) not in selected_visits:
                continue


#            station_set.add(visitnode.getData(u"Station name")) # Station name
            visit_set.add(visitnode.getData(u"Station name") + " : " + visitnode.getData(u"Date")) # Station name
            for samplenode in visitnode.getChildren():

                minmax = samplenode.getData(u'Sample min depth') + u'-' + samplenode.getData(u'Sample max depth')
                if minmax not in selected_minmaxdepth:
                    continue

                
                for variablenode in samplenode.getChildren():

                    if variablenode.getData(u'Taxon name') not in selected_taxon:
                        continue
                    if variablenode.getData(u'Trophy') not in selected_trophy:
                        continue


                    taxonname = variablenode.getData(u"Taxon name")
                    if taxonname:
                        taxon_set.add(taxonname)
                    else:
                        taxon_set.add(u'---')
        # Step 2: Create a station dictionary containing taxa and value for each taxa.
#        station_taxon_dict = {}
        visit_taxon_dict = {}
#        for station in station_set:
        for visit in visit_set:
#            station_taxon_dict[station] = {} 
            visit_taxon_dict[visit] = {} 
            for taxon in taxon_set:
#                station_taxon_dict[station][taxon] = 0.0
                visit_taxon_dict[visit][taxon] = 0.0
        # Step 3. Which parameter is selected?
        selectedparameter = unicode(self._parameter_list.currentText())
        # Step 4: Fill with data.
        for visitnode in currentdata.getChildren():

            if selected_startdate > visitnode.getData(u'Date'):
                continue
            if selected_enddate < visitnode.getData(u'Date'):
                continue
#            if visitnode.getData(u'Station name') not in selected_stations:
#                continue
            if (visitnode.getData(u'Station name') + u' : ' + visitnode.getData(u'Date')) not in selected_visits:
                continue


#            stationname = visitnode.getData(u"Station name")
            visit = (visitnode.getData(u'Station name') + u' : ' + visitnode.getData(u'Date'))
            for samplenode in visitnode.getChildren():

                minmax = samplenode.getData(u'Sample min depth') + u'-' + samplenode.getData(u'Sample max depth')
                if minmax not in selected_minmaxdepth:
                    continue

                
                for variablenode in samplenode.getChildren():

                    if variablenode.getData(u'Taxon name') not in selected_taxon:
                        continue
                    if variablenode.getData(u'Trophy') not in selected_trophy:
                        continue


                    taxonname = variablenode.getData(u"Taxon name")
                    if not taxonname:
                        taxonname = u'---'
                    parameter = variablenode.getData(u"Parameter")
                    if parameter == selectedparameter:                        
                        value = variablenode.getData(u"Value")
                        try:
#                            value = float(value.replace(u' ', u'').replace(u',', u'.'))
#                            station_taxon_dict[stationname][taxonname] += value

                            
                            
                            
#                            visit_taxon_dict[visit][taxonname] += value
                            visit_taxon_dict[visit][taxonname] += float(value)
                        except:
#                            print ("ERROR: Float conversion (2): Station: " + stationname + 
                            print ("ERROR: Float conversion (2): Station: " + visit + 
                                   " Taxon name: " + taxonname + " Value: " + unicode(variablenode.getData(u"Value")))
                            ###raise
        
        # Step 5: Reorganize.
    
        
        visit_list = sorted(visit_set)
        taxon_list = sorted(taxon_set)
        #
        plotdata = envmonlib.PlotDataTwoVariables(
                                x_type = u'String',
                                title = u"Taxa per station and date", 
                                x_label = u'Station',
                                y_label = selectedparameter)
        #
        for taxonindex, taxon in enumerate(taxon_list):
            taxon_visit_value_list = []
            for stationindex, station in enumerate(visit_list):
                taxon_visit_value_list.append(visit_taxon_dict[station][taxon])
            # 
            plotdata.addPlot(plot_name = taxon, 
                                x_array = visit_list, 
                                y_array = taxon_visit_value_list, 
                                x_label = station,
                                y_label = selectedparameter)
        # Step 6: Plot
        
#        graphtool.addTestPlot(selectedparameter, visit_list, taxon_list, taxon_visit_value_list)
        graphtool.addTestPlot_NEW(data_object = plotdata, chart_type = u'Bar chart')
        
        
        
        
         
##        station_list = sorted(station_set)
#        visit_list = sorted(visit_set)
#        taxon_list = sorted(taxon_set)
##        taxon_station_value_list = []
#        taxon_visit_value_list = []
#        for taxonindex, taxon in enumerate(taxon_list):
##            taxon_station_value_list.append([])
#            taxon_visit_value_list.append([])
##            for stationindex, station in enumerate(station_list):
#            for stationindex, station in enumerate(visit_list):
##                taxon_station_value_list[taxonindex].append(station_taxon_dict[station][taxon])
#                taxon_visit_value_list[taxonindex].append(visit_taxon_dict[station][taxon])
#        # Step 6: Plot
##        graphtool.addTestPlot(selectedparameter, station_list, taxon_list, taxon_station_value_list)
#        graphtool.addTestPlot(selectedparameter, visit_list, taxon_list, taxon_visit_value_list)
                
            
        
        
    def _addPlot_3(self):
        """ """
        
    def _addPlot_4(self):
        """ """
        
    def _addPlot(self):
        """ """
        currentdata = self._main_activity.getCurrentData()
        if not currentdata:
            return # Can't plot from empty dataset
        #
        tool_manager.ToolManager().showToolByName(u'Graph plot') # Show tool if hidden.
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plot')
        # Selected columns.
        x_column = unicode(self._x_axis_column_list.currentText())
        y_column = unicode(self._y_axis_column_list.currentText())
        # Selected parameters.
        x_param = None
        y_param = None
        if x_column == u"Parameter:":
            x_param = unicode(self._x_axis_parameter_list.currentText())
        if y_column == u"Parameter:":
            y_param = unicode(self._y_axis_parameter_list.currentText())
        # Check exports columns backwards.
        x_visit_key = None
        x_sample_key = None                      
        x_variable_key = None
        y_visit_key = None
        y_sample_key = None                      
        y_variable_key = None
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
        
        # Extract data.
        x_data = []
        y_data = []
        x_value = None
        y_value = None
        #
        
        
        selected_dict = self._main_activity.getSelectDataDict()
        selected_startdate = selected_dict[u'Start date']
        selected_enddate = selected_dict[u'End date']
#        selected_stations = selected_dict[u'Stations']
        selected_visits = selected_dict[u'Visits']
        selected_minmaxdepth =  selected_dict[u'Min max depth']
        selected_taxon = selected_dict[u'Taxon']
        selected_trophy = selected_dict[u'Trophy']
        
        
        
        for visitnode in currentdata.getChildren():
            
            if selected_startdate > visitnode.getData(u'Date'):
                continue
            if selected_enddate < visitnode.getData(u'Date'):
                continue
#            if visitnode.getData(u'Station name') not in selected_stations:
#                continue
            if (visitnode.getData(u'Station name') + u' : ' + visitnode.getData(u'Date')) not in selected_visits:
                continue

            
             
            if x_visit_key: x_value = visitnode.getData(x_visit_key) # if x_visit_key else None
            if y_visit_key: y_value = visitnode.getData(y_visit_key) # if y_visit_key else None
            for samplenode in visitnode.getChildren():
            
                minmax = samplenode.getData(u'Sample min depth') + u'-' + samplenode.getData(u'Sample max depth')
                if minmax not in selected_minmaxdepth:
                    continue
                
                
                if x_sample_key: x_value = samplenode.getData(x_sample_key) # if x_sample_key else None
                if y_sample_key: y_value = samplenode.getData(y_sample_key) # if y_sample_key else None
                for variablenode in samplenode.getChildren():
                
                    if variablenode.getData(u'Taxon name') not in selected_taxon:
                        continue
                    if variablenode.getData(u'Trophy') not in selected_trophy:
                        continue
                    
                    
                    
                    #
                    if x_variable_key: x_value = variablenode.getData(x_variable_key) # if x_variable_key else None
                    if y_variable_key: y_value = variablenode.getData(y_variable_key) # if y_variable_key else None
                    #
                    if x_param or y_param:
                        parameter = variablenode.getData(u'Parameter')
                        if x_param:
                            if parameter == x_param:
                                x_value = variablenode.getData(u'Value')
                        if y_param:
                            if parameter == y_param:
                                y_value = variablenode.getData(u'Value')
                    # If NOT both are parameters, add data on variable level.
                    if not (x_param and y_param):
                        # Add values to lists if both values are available.
                        if (x_value and y_value):
                            x_data.append(x_value)
                            y_data.append(y_value)
                        # Clear used values.
                        if x_param: x_value = None    
                        if y_param: y_value = None    
                    # Clear used values.
                    if x_variable_key: x_value = None    
                    if x_variable_key: y_value = None
                # If both are parameters, add data on sample level.     
                if (x_param and y_param):
                    # Add values to lists if both values are available.
                    if (x_value and y_value):
                        x_data.append(x_value)
                        y_data.append(y_value)
                        # Clear used values.
                        if x_param: x_value = None    
                        if y_param: y_value = None    
                # Clear used values.
                if x_sample_key: x_value = None    
                if y_sample_key: y_value = None    
            # Clear used values.
            if x_visit_key: x_value = None    
            if y_visit_key: y_value = None    
        #

        # Check if this is a time series or not.
        selectedplotindex = self._plotindex_list.currentIndex() 
        if selectedplotindex in [0, 1, 2, 3]:
            graphtool.addTimeseriesPlot(selectedplotindex, x_data, y_data)
        else:
            graphtool.addXYPlot(selectedplotindex - 4, x_data, y_data)

