#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2012 SMHI, Swedish Meteorological and Hydrological Institute 
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
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.activities.activity_base as activity_base
import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.toolbox_datasets as toolbox_datasets
import envmonlib

class ScreeningActivity(activity_base.ActivityBase):
    """ Used for screening of content of loaded datasets. """
    
    def __init__(self, name, parentwidget):
        """ """
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(ScreeningActivity, self).__init__(name, parentwidget)
        # Listen for changes in the toolbox dataset list.
        self.connect(toolbox_datasets.ToolboxDatasets(), 
                     QtCore.SIGNAL("datasetListChanged"), 
                     self.update)
        # Data object used for plotting.
        self._graph_plot_data = envmonlib.GraphPlotData()

    def update(self):
        """ """
        self.updateColumnList()
        self.updateParameterList()
        
    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Add activity name at top.
        self._activityheader = QtGui.QLabel('<h2>' + self.objectName() + '</h2>', self)
        self._activityheader.setTextFormat(QtCore.Qt.RichText)
        self._activityheader.setAlignment(QtCore.Qt.AlignHCenter)
        self._activityheader.setStyleSheet(""" 
            * { color: white; background-color: #00677f; }
            """)
        contentLayout.addWidget(self._activityheader)
        # Add content to the activity.
        contentLayout.addWidget(self._contentScreeningTabs())

    def _contentScreeningTabs(self):
        """ """
        # Active widgets and connections.
        selectdatabox = QtGui.QGroupBox("", self)
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self._contentCodeListScreening(), "Code lists")
        tabWidget.addTab(self._contentSpeciesScreening(), "Species")
        tabWidget.addTab(self._contentCheckColumnValues(), "Column values")
        tabWidget.addTab(self._contentPlotParameters(), "Plot parameters")
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(tabWidget)
        selectdatabox.setLayout(layout)        
        #
        return selectdatabox

    def _contentCodeListScreening(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.<br/><br/>
        """)        
        #
        self._codelistscreening_button = QtGui.QPushButton("Code list screening")
        self.connect(self._codelistscreening_button, QtCore.SIGNAL("clicked()"), self._codeListScreening)                
        # Layout widgets.
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._codelistscreening_button)
        hbox1.addStretch(10)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(hbox1)
        layout.addStretch(1)
        widget.setLayout(layout)                
        #
        return widget

    def _codeListScreening(self):
        """ """
        # Screening results is only shown in the toolbox log.
        tool_manager.ToolManager().showToolByName(u'Toolbox logging')
        #
        try:
            envmonlib.Logging().log(u"") # Empty line.
            envmonlib.Logging().log("Code list screening started...")
            envmonlib.Logging().startAccumulatedLogging()
            self._writeToStatusBar("Code list screening in progress...")
            # Perform screening.
            codetypes_set = envmonlib.ScreeningManager().codeListScreening(toolbox_datasets.ToolboxDatasets().getDatasets())
        finally:
            envmonlib.Logging().logAllAccumulatedRows()    
            envmonlib.Logging().log("Screening was done on these code types: " + 
                                    unicode(sorted(codetypes_set)))
            envmonlib.Logging().log("Code list screening done.")
            self._writeToStatusBar("")

    def _contentSpeciesScreening(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.<br/><br/>
        """)        
        #
        self._speciesscreening_button = QtGui.QPushButton("Species screening")
        self.connect(self._speciesscreening_button, QtCore.SIGNAL("clicked()"), self._speciesScreening)                
        self._bvolscreening_button = QtGui.QPushButton("BVOL screening")
        self.connect(self._bvolscreening_button, QtCore.SIGNAL("clicked()"), self._bvolScreening)                
        # Layout widgets.
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._speciesscreening_button)
        hbox1.addWidget(self._bvolscreening_button)
        hbox1.addStretch(10)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(hbox1)
        layout.addStretch(1)
        widget.setLayout(layout)                
        #
        return widget

    def _speciesScreening(self):
        """ """
        # Screening results is only shown in the toolbox log.
        tool_manager.ToolManager().showToolByName(u'Toolbox logging')
        #
        try:
            envmonlib.Logging().log(u"") # Empty line.
            envmonlib.Logging().log("Species screening started...")
            envmonlib.Logging().startAccumulatedLogging()
            self._writeToStatusBar("Species screening in progress...")
            # Perform screening.
            envmonlib.ScreeningManager().speciesScreening(toolbox_datasets.ToolboxDatasets().getDatasets())
        finally:
            envmonlib.Logging().logAllAccumulatedRows()    
            envmonlib.Logging().log(u"Species screening done.")
            self._writeToStatusBar("")

    def _bvolScreening(self):
        """ """
        # Screening results is only shown in the toolbox log.
        tool_manager.ToolManager().showToolByName(u'Toolbox logging')
        #
        try:
            envmonlib.Logging().log(u"") # Empty line.
            envmonlib.Logging().log("BVOL Species screening started...")
            envmonlib.Logging().startAccumulatedLogging()
            self._writeToStatusBar("BVOL Species screening in progress...")
            # Perform screening.
            envmonlib.ScreeningManager().bvolSpeciesScreening(toolbox_datasets.ToolboxDatasets().getDatasets())
        finally:
            envmonlib.Logging().logAllAccumulatedRows()    
            envmonlib.Logging().log(u"BVOL Species screening done.")
            self._writeToStatusBar("")

    def _contentCheckColumnValues(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.<br/><br/>
        """)        
        #
        self._column_list = QtGui.QComboBox()
        self._column_list.setMinimumContentsLength(30)
        self._column_list.setEnabled(False)
        #
        self.connect(self._column_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._updateColumnContent)                
        # Column content.
##        self._content_list = utils_qt.SelectableQListView()
##        self._content_list = QtGui.QListWidget()
        self._content_list = QtGui.QTextEdit()
#        self._content_list.setMaximumHeight(200)
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Column:")
        label2 = QtGui.QLabel("Content:")
        form1.addWidget(label1, gridrow, 0, 1, 1)
        form1.addWidget(label2, gridrow, 1, 1, 1)
        gridrow += 1
        form1.addWidget(self._column_list, gridrow, 0, 1, 1)
        form1.addWidget(self._content_list, gridrow, 1, 10, 1)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1, 10)
        layout.addStretch(1)
        widget.setLayout(layout)                
        #
        return widget

    def updateColumnList(self):
        """ """
        self._column_list.clear()
        self._content_list.clear()
        datasets = toolbox_datasets.ToolboxDatasets().getDatasets()
        if datasets and (len(datasets) > 0):        
            columns_set = set()
            for dataset in toolbox_datasets.ToolboxDatasets().getDatasets():
                for column in dataset.getExportTableColumns():
                    columns_set.add(column[u'Header']) 
            #    
            self._column_list.addItems(sorted(columns_set))
            self._column_list.setEnabled(True)
        else:
            self._column_list.clear()
            self._column_list.setEnabled(False)
                               
    def _updateColumnContent(self, selected_row):
        """ """
        datasets = toolbox_datasets.ToolboxDatasets().getDatasets()
        self._content_list.clear()
        if not (datasets and (len(datasets) > 0)):        
            return # Empty data.
        #
        columncontent_set = set()
        selectedcolumn = unicode(self._column_list.currentText())
        # Search for export column corresponding model element.
        nodelevel = u''
        key = u''
        for dataset in datasets:
            for info_dict in dataset.getExportTableColumns():
                if info_dict[u'Header'] == selectedcolumn:
                    nodelevel = info_dict[u'Node']
                    key = info_dict[u'Key']
                    break # Break loop.
            if nodelevel:
                break # Also break next loop.
        #
        for dataset in datasets:
            for visitnode in dataset.getChildren():
                if nodelevel == u'Visit':
                    if key in visitnode.getDataDict().keys():
                        columncontent_set.add(unicode(visitnode.getData(key)))
                    else:
                        columncontent_set.add(u'') # Add empty field.
                    continue    
                #
                for samplenode in visitnode.getChildren():
                    if nodelevel == u'Sample':
                        if key in samplenode.getDataDict().keys():
                            columncontent_set.add(unicode(samplenode.getData(key)))
                        else:
                            columncontent_set.add(u'') # Add empty field.
                        continue    
                    #
                    for variablenode in samplenode.getChildren():
                        if nodelevel == u'Variable':
                            if key in variablenode.getDataDict().keys():
                                columncontent_set.add(unicode(variablenode.getData(key)))
                            else:
                                columncontent_set.add(u'') # Add empty field.
                            continue    
        # Content list.
#        self._content_list.addItems(sorted(columncontent_set))
        for row in sorted(columncontent_set): 
            self._content_list.append(row)

    def _contentPlotParameters(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        introlabel = utils_qt.RichTextQLabel()
        introlabel.setText("""
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua.<br/><br/>
        """)        
        #
        self._parameter_list = utils_qt.SelectableQListView()       
        #
        clearall_label = utils_qt.ClickableQLabel("Clear all")
        markall_label = utils_qt.ClickableQLabel("Mark all")
        self.connect(clearall_label, QtCore.SIGNAL("clicked()"), self._parameter_list.uncheckAll)                
        self.connect(markall_label, QtCore.SIGNAL("clicked()"), self._parameter_list.checkAll)                
        #
        self._plotparameterscreening_button = QtGui.QPushButton("Plot selected parameters")
        self.connect(self._plotparameterscreening_button, QtCore.SIGNAL("clicked()"), self._plotScreening)                
        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Parameters:")
        form1.addWidget(label1, gridrow, 0, 1, 2)
        gridrow += 1
        form1.addWidget(self._parameter_list, gridrow, 0, 1, 10)
        gridrow += 5
        form1.addWidget(clearall_label, gridrow, 0, 1, 1)
        form1.addWidget(markall_label, gridrow, 1, 1, 1)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(self._plotparameterscreening_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(form1)
        layout.addLayout(hbox1)
        layout.addStretch(5)
        widget.setLayout(layout)                
        #
        return widget
        # Layout widgets.
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self._codelistscreening_button)
        hbox1.addStretch(10)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(introlabel)
        layout.addLayout(hbox1)
        layout.addStretch(1)
        widget.setLayout(layout)                
        #
        return widget

    def updateParameterList(self):
        """ """
        self._parameter_list.clear()
        datasets = toolbox_datasets.ToolboxDatasets().getDatasets()
        if datasets and (len(datasets) > 0):        
            parameter_set = set()
            for dataset in toolbox_datasets.ToolboxDatasets().getDatasets():
                for visitnode in dataset.getChildren():
                    for samplenode in visitnode.getChildren():
                        for variablenode in samplenode.getChildren():
                            parameter_set.add(variablenode.getData(u"Parameter"))
            self._parameter_list.setList(sorted(parameter_set))

    def _plotScreening(self):
        """ """
        # Show the Graph plotter tool if hidden. 
        tool_manager.ToolManager().showToolByName(u'Graph plotter')
        graphtool = tool_manager.ToolManager().getToolByName(u'Graph plotter')
        graphtool.clearPlotData()
        # The same plot data object is reused.
        self._graph_plot_data.clear()
        # One plot for each selected parameter.
        for parameter in self._parameter_list.getSelectedDataList():
            self._addPlot(parameter)
        # View in the graph-plot tool.    
        graphtool.setChartSelection(chart = u"Line chart",
                                    combined = True, stacked = False, y_log_scale = True)
        graphtool.setPlotData(self._graph_plot_data)   

    def _addPlot(self, parameter):
        """ """
        datasets = toolbox_datasets.ToolboxDatasets().getDatasets()
        #
        yarray = []
        unit_set = set() # In case of different units on the same parameter.
        #
        if datasets and (len(datasets) > 0):        
            for dataset in toolbox_datasets.ToolboxDatasets().getDatasets():
                for visitnode in dataset.getChildren():
                    for samplenode in visitnode.getChildren():
                        for variablenode in samplenode.getChildren():
                            if variablenode.getData(u"Parameter") == parameter:
                                unit_set.add(variablenode.getData(u"Unit"))
                                value = variablenode.getData(u"Value")
                                yarray.append(value)                  
        #
        units = u' --- '.join(sorted(unit_set))
        parameter_unit = parameter + u' (' + units + u')' 
        #
        self._graph_plot_data.addPlot(plot_name = parameter_unit, y_array = yarray)

