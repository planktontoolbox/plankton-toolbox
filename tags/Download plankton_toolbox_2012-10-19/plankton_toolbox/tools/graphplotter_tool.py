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

import datetime
import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.tools.tool_base as tool_base
import json
import envmonlib
#
import matplotlib.backends.backend_qt4agg as mpl_backend
import matplotlib.figure as mpl_figure
import matplotlib.dates as mpl_dates
import matplotlib.ticker as mpl_ticker



class GraphPlotterTool(tool_base.ToolBase):
    """
    """
    def __init__(self, name, parentwidget):
        """ """
        # Filename used when saving chart to file.
        self._lastuseddirectory = '.'
        self._plotdata = None
        self._current_chart = None 
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(GraphPlotterTool, self).__init__(name, parentwidget)
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.setBaseSize(600,600)
        #
#        # Add and view simple data for test:
#        self._testData()
#        self._drawChart()
        
    def clearPlotData(self):
        """ """
        self.setPlotData(None)

    def setPlotData(self, plot_data):
        """ """
        self._figure.clear()
        self._canvas.draw()
        #
        if plot_data:
            if isinstance(plot_data, envmonlib.GraphPlotData):
                self._plotdata = plot_data
            else:
                # Invalid type. 
                self._plotdata = None
        else:
            self._plotdata = None
        #
        self._resetPlotdata()
        self._drawChart()

    def setChartSelection(self, 
                          chart = u"Line chart", # Line chart, Bar chart, Scatter chart, Pie chart.
                          combined = False,
                          stacked = False,
                          y_log_scale = False):
        """ """
        comboindex = self._charttype_list.findText(chart)
        if comboindex >= 0:  self._charttype_list.setCurrentIndex(comboindex)
        #
        self._combined_checkbox.setChecked(combined)
        self._stacked_checkbox.setChecked(stacked)
        self._ylogscale_checkbox.setChecked(y_log_scale)
        
    def _testData(self):
        """ """
        testdata = envmonlib.GraphPlotData(
                            title = u"Three variables data object", 
                            x_label = u'X (three variable)',
                            y_label = u'Y (three variable)',
                            z_label = u'Z (three variable)')
        testdata.addPlot(plot_name = u"First plot", 
                            x_array = [1,2,5,6,7,8], 
                            y_array = [20,30,20,40,10,90], 
                            z_array = [10,10,80,20,30,30], 
                            x_label = u'X First',
                            y_label = u'Y First',
                            z_label = u'Z First')
        testdata.addPlot(plot_name = u"Second plot", 
                            x_array = [1,2,3,30,35,40], 
                            y_array = [2,3,2,4,1,9], 
                            z_array = [10,10,20,20,30,30], 
                            x_label = u'X Second',
                            y_label = u'Y Second',
                            z_label = u'Z Second')
        testdata.addPlot(plot_name = u"Third plot", 
                            x_array = [6,8,9,10,15,20], 
                            y_array = [2,3,2,4,1,9], 
                            z_array = [10,60,20,90,30,30], 
                            x_label = u'X Third',
                            y_label = u'Y Third',
                            z_label = u'Z Third')
#        testdata = envmonlib.GraphPlotData(
#                            x_type = u'String',
#                            title = u"Two variables data object, string", 
#                            x_label = u'X (two variables)',
#                            y_label = u'Y (two variables)')
#        testdata.addPlot(plot_name = u"Dinophysis acuta", 
#                            x_array = [u'BY15',u'Släggö',u'cc','dd','ee'], 
#                            y_array = [10,30,5,5,1], 
#                            x_label = u'X First',
#                            y_label = u'Y First')
#        testdata.addPlot(plot_name = u"Second plot", 
#                            x_array = ['cc','dd','ee','ff', 'gg', 'hh'], 
#                            y_array = [2,3,2,4,1,9], 
#                            x_label = u'X Second',
#                            y_label = u'Y Second')
#        testdata.addPlot(plot_name = u"Third plot", 
#                            x_array = ['AA','BB','cc','dd','ee','ff'], 
#                            y_array = [5,5,5,1,2,3], 
#                            x_label = u'X Third',
#                            y_label = u'Y Third')
        #
        self.setPlotData(testdata)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Tab widget. 
        tabWidget = QtGui.QTabWidget()
        contentLayout.addWidget(tabWidget)
        tabWidget.addTab(self._createContentChart(), "Chart")
        tabWidget.addTab(self._createContentSettings(), "Settings")        
        tabWidget.addTab(self._createContentEditData(), "Edit data")        

    def _createContentChart(self):
        """ """
        widget = QtGui.QWidget()
        contentLayout = QtGui.QVBoxLayout()
        contentLayout.addLayout(self._createContentSelectChart())
        contentLayout.addLayout(self._createContentChartArea(), 10)
        #
        widget.setLayout(contentLayout)
        #
        return widget

    def _createContentSettings(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        self._timeseriesforat_edit = QtGui.QLineEdit(""" bo, ro, g^, ys""")
        self._xyplotformat_edit = QtGui.QLineEdit(""" bo, ro, g^, ys""")
        #
        self._editable_listview = utils_qt.ToolboxEditableQTableView()
        data = envmonlib.DatasetTable()
        data.setHeader([u'X label     ', u'Y label     ', u'Z label     '])
        data.appendRow([u'a', u'b', u'c'])
        data.appendRow([u'1', u'2', u'3'])
        self._editable_listview.tablemodel.setModeldata(data)
        self._editable_listview.tablemodel.reset() # Model data has changed.
        self._editable_listview.resizeColumnsToContents()
        #                
        self._resetsettings_button = QtGui.QPushButton("Reset")
#        self.connect(self._resetsettings_button, QtCore.SIGNAL("clicked()"), self._resetSettings)                
        #                
        self._applysettings_button = QtGui.QPushButton("Apply")
#        self.connect(self._applysettings_button, QtCore.SIGNAL("clicked()"), self._applySettings)                
        # Layout.
        form = QtGui.QFormLayout()
        form.addRow("Test 1:", self._timeseriesforat_edit)
        form.addRow("Test 2", self._xyplotformat_edit)
        form.addRow("'Plot labels", self._editable_listview)
        #
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(5)
        hbox.addWidget(self._resetsettings_button)
        hbox.addWidget(self._applysettings_button)
        #
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(form)
        vbox.addLayout(hbox, 10)
        # 
        widget.setLayout(vbox)
 
        
        # Under development...
        self._timeseriesforat_edit.setDisabled(True)
        self._xyplotformat_edit.setDisabled(True)
        self._editable_listview.setDisabled(True)
        self._resetsettings_button.setDisabled(True)
        self._applysettings_button.setDisabled(True)

        
        #
        return widget

    def _createContentEditData(self):
        """ """
        widget = QtGui.QWidget()
        # Active widgets and connections.
        self.plotdatainfo_textedit = QtGui.QTextEdit()
        self.plotdatalist_textedit = QtGui.QTextEdit()
        self._resetplotdata_button = QtGui.QPushButton("Reset")
        self.connect(self._resetplotdata_button, QtCore.SIGNAL("clicked()"), self._resetPlotdata)                
        #                
        self._applyplotdata_button = QtGui.QPushButton("Apply")
        self.connect(self._applyplotdata_button, QtCore.SIGNAL("clicked()"), self._applyPlotdata)                
        # Layout.
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(5)
        hbox.addWidget(self._resetplotdata_button)
        hbox.addWidget(self._applyplotdata_button)
        #
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.plotdatainfo_textedit, 5)
        layout.addWidget(self.plotdatalist_textedit, 10)
        layout.addLayout(hbox)

        widget.setLayout(layout)
        #
        return widget

    def _createContentSelectChart(self):
        """ """
        # Active widgets and connections.
        self._charttype_list = QtGui.QComboBox()
        self._charttype_list.addItems([u"Line chart",
                                       u"Bar chart",
                                       u"Scatter chart",
                                       u"Pie chart"])
#        self._charttype_list.setDisabled(True)
        self.connect(self._charttype_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._drawChart)
        #
        self._combined_checkbox = QtGui.QCheckBox("Combined")
        self._combined_checkbox.setChecked(False) 
#        self._combined_checkbox.setDisabled(True)
        self.connect(self._combined_checkbox, QtCore.SIGNAL("stateChanged(int)"), self._drawChart)
        #
        self._stacked_checkbox = QtGui.QCheckBox("Stacked")
        self._stacked_checkbox.setChecked(False) 
#        self._stacked_checkbox.setDisabled(True)
        self.connect(self._stacked_checkbox, QtCore.SIGNAL("stateChanged(int)"), self._drawChart)
        #
        self._ylogscale_checkbox = QtGui.QCheckBox("Y log scale")
        self._ylogscale_checkbox.setChecked(False) 
#        self._ylogscale_checkbox.setDisabled(True)
        self.connect(self._ylogscale_checkbox, QtCore.SIGNAL("stateChanged(int)"), self._drawChart)
        #                
        self._clear_button = QtGui.QPushButton("Clear")
        self.connect(self._clear_button, QtCore.SIGNAL("clicked()"), self.clearPlotData)                
        #                
        self._savecharttofile_button = QtGui.QPushButton("Save...")
        self.connect(self._savecharttofile_button, QtCore.SIGNAL("clicked()"), self._saveChartToFile)                
        # Layout widgets.
        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel("Chart type:"))
        layout.addWidget(self._charttype_list)
        layout.addWidget(self._combined_checkbox)
        layout.addWidget(self._stacked_checkbox)
        layout.addWidget(self._ylogscale_checkbox)
        layout.addStretch(5)
        layout.addWidget(self._clear_button)
        layout.addWidget(self._savecharttofile_button)
        #
        return layout
        
    def _createContentChartArea(self):
        """ """
        # Matplotlib figure and canvas for Qt4.
        self._figure = mpl_figure.Figure()
        self._canvas = mpl_backend.FigureCanvasQTAgg(self._figure)        
        self._canvas.show()
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._canvas)
        #
        return layout
        
    def _drawChart(self):
        """ """
        self._figure.clear()
        self._canvas.draw()
        #
        if not self._plotdata:
            return
        # User selections.
        selectedchart = unicode(self._charttype_list.currentText())
        combined = self._combined_checkbox.isChecked()
        stacked = self._stacked_checkbox.isChecked()
        ylogscale = self._ylogscale_checkbox.isChecked()
        # Draw selected chart.
        if selectedchart == u'Line chart':
            if self._plotdata.getPlotDataInfo()[u'X type'] != u'String':
                self._current_chart = envmonlib.LineChart(self._plotdata, figure = self._figure)
                self._current_chart.plotChart(combined = combined, y_log_scale = ylogscale)        
                self._canvas.draw()
        #
        if selectedchart == u'Bar chart':
            self._current_chart = envmonlib.BarChart(self._plotdata, figure = self._figure)
            self._current_chart.plotChart(combined = combined, stacked = stacked, y_log_scale = ylogscale)                
            self._canvas.draw()
        #
        if selectedchart == u'Scatter chart':
            if self._plotdata.getPlotDataInfo()[u'X type'] != u'String':
                self._current_chart = envmonlib.ScatterChart(self._plotdata, figure = self._figure)
                self._current_chart.plotChart(combined = combined, y_log_scale = ylogscale)                
                self._canvas.draw()
        #
        if selectedchart == u'Pie chart':
            self._current_chart = envmonlib.PieChart(self._plotdata, figure = self._figure)
            self._current_chart.plotChart()        
            self._canvas.draw()

    def _resetPlotdata(self):
        """ """
        if self._plotdata:
            self.plotdatainfo_textedit.setText(
                       json.dumps(self._plotdata.getPlotDataInfo(), 
                                  encoding = u'utf8', 
                                  sort_keys=True, indent=4))
            self.plotdatalist_textedit.setText(
                       json.dumps(self._plotdata.getPlotList(), 
                                  encoding = u'utf8', 
                                  sort_keys=True, indent=4))
        else:
            self.plotdatainfo_textedit.setText(u'')
            self.plotdatalist_textedit.setText(u'')
            
    def _applyPlotdata(self):
        """ """
        if self._plotdata:
            self._plotdata.setPlotDataInfo(
                                json.loads(unicode(self.plotdatainfo_textedit.toPlainText()), 
                                           encoding = u'utf8'))
            #
            self._plotdata.setPlotList(
                                json.loads(unicode(self.plotdatalist_textedit.toPlainText()), 
                                           encoding = u'utf8'))
        # Update chart.
        self._drawChart()

    def _saveChartToFile(self):
        """ """
        if self._plotdata:
            # Show select file dialog box.
            namefilter = 'Image file (*.png);;All files (*.*)'
            filename = QtGui.QFileDialog.getSaveFileName(
                            self,
                            'Save chart to file',
                            self._lastuseddirectory,
                            namefilter)
            filename = unicode(filename) # QString to unicode.
            # Check if user pressed ok or cancel.
            if filename:
                self._lastuseddirectory = os.path.dirname(filename)
                # Save to file.
                self._figure.savefig(filename, dpi = 300)

