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

import datetime
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import plankton_toolbox.toolbox.utils_qt as utils_qt
import plankton_toolbox.tools.tool_base as tool_base
#
import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
#from matplotlib.dates import DateFormatter  # ... , DayLocator, HourLocator, drange        
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
import matplotlib.dates as dates
import matplotlib.ticker as ticker
# FOR TEST:
from numpy import arange, sin, pi

class GraphPlotTool(tool_base.ToolBase):
    """
    """
    def __init__(self, name, parentwidget):
        """ """
        # Filename used when saving data to file.
        self._lastuseddirectory = '.'
        # Local storage of 4 timeseries and 4 X/Y-plots.
        self._ax_timeseries = [{'time':[], 'y':[]}, {'time':[], 'y':[]}, {'time':[], 'y':[]}, {'time':[], 'y':[]}]
        self._ax_xyplot = [{'x':[], 'y':[]}, {'x':[], 'y':[]}, {'x':[], 'y':[]}, {'x':[], 'y':[]}]        
        # Initialize parent. Should be called after other 
        # initialization since the base class calls _createContent().
        super(GraphPlotTool, self).__init__(name, parentwidget)
        # Where is the tool allowed to dock in the main window.
        self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)
        self.setBaseSize(600,600)

    def _createContent(self):
        """ """
        content = self._createScrollableContent()
        contentLayout = QtGui.QVBoxLayout()
        content.setLayout(contentLayout)
        # Tab widget for single point or table. 
        tabWidget = QtGui.QTabWidget()
        contentLayout.addWidget(tabWidget)
        tabWidget.addTab(self._createContentGraph(), "Graph")
        tabWidget.addTab(self._createContentSettings(), "Settings")        
#        contentLayout.addWidget(self._contentSaveResult())

    def _createContentGraph(self):
        """ """
        widget = QtGui.QWidget()
        contentLayout = QtGui.QVBoxLayout()
        contentLayout.addLayout(self._contentSelectDataset())
        contentLayout.addLayout(self._contentGraphArea(), 10)
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
        # Layout.
        layout = QtGui.QFormLayout()
        layout.addRow("Time series, format:", self._timeseriesforat_edit)
        layout.addRow("X/Y plot, format", self._xyplotformat_edit)
        #
        widget.setLayout(layout)
        #
        return widget

    def _contentSelectDataset(self):
        """ """
        # Active widgets and connections.
        self._viewplot_list = QtGui.QComboBox()
        self._viewplot_list.addItems(["Time series 1-4", 
                                       "Time series 1", "Time series 2", "Time series 3", "Time series 4", 
                                       "X/Y plots 1-4", 
                                       "X/Y plot 1", "X/Y plot 2", "X/Y plot 3", "X/Y plot 4"])
        self.connect(self._viewplot_list, QtCore.SIGNAL("currentIndexChanged(int)"), self._drawPlots)                
        self._clearselectedplot_button = QtGui.QPushButton("Clear")
        self.connect(self._clearselectedplot_button, QtCore.SIGNAL("clicked()"), self._clearSelectedPlot)                
        self._clearallplots_button = QtGui.QPushButton("Clear all")
        self.connect(self._clearallplots_button, QtCore.SIGNAL("clicked()"), self.clearAll)                
        # Layout widgets.
        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel("View:"))
        layout.addWidget(self._viewplot_list)
        layout.addWidget(self._clearselectedplot_button)
        layout.addWidget(self._clearallplots_button)
        layout.addStretch(5)
        #
        return layout
        
    def _contentGraphArea(self):
        """ """
        # Active widgets and connections.
        self._tableview = utils_qt.ToolboxQTableView()
        # Matplotlib.
#        self._figure = Figure(figsize=(5,4), dpi=100)
        self._figure = Figure()
        self._canvas = FigureCanvas(self._figure)        
        # TEST.
        ax = self._figure.add_subplot(111)        
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        ax.plot(t,s)
        #
        self._canvas.show()
        # Layout widgets.
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._canvas)
        #
        return layout
        
    def _contentSaveResult(self):
        """ """
        saveresultbox = QtGui.QGroupBox("Save graph", self)
        # Active widgets and connections.
        self._saveformat_list = QtGui.QComboBox()
        #
        self._saveformat_list.addItems(["Time series, combined",
                                         "Time series, 1-2",
                                         "Time series, 1-4",
                                         "X/Y plot, combined",
                                         "X/Y plot, 1-2",
                                         "X/Y plot, 3-4"])
        self._savegraph_button = QtGui.QPushButton("Save...")
        self.connect(self._savegraph_button, QtCore.SIGNAL("clicked()"), self._saveGraph)                
        # Layout widgets.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(QtGui.QLabel("Format:"))
        hbox1.addWidget(self._saveformat_list)
        hbox1.addWidget(self._savegraph_button)
        saveresultbox.setLayout(hbox1)
        #
        return saveresultbox

    def _saveGraph(self):
        """ """
        print('TEST: Save graph.')


    
    # === Public methods. ===    
    def clearAll(self):
        """ """
#        self._figure.clear()
#        self._canvas.draw()
        # Local storage of 4 timeseries and 4 X/Y-plots.
        self._ax_timeseries = [{'time':[], 'y':[]}, {'time':[], 'y':[]}, {'time':[], 'y':[]}, {'time':[], 'y':[]}]
        self._ax_xyplot = [{'x':[], 'y':[]}, {'x':[], 'y':[]}, {'x':[], 'y':[]}, {'x':[], 'y':[]}]
        #
        self._drawPlots()
        
    def addTimeseriesPlot(self, plotindex, time_table, y_table):
        """ """
        #
        if plotindex not in [0,1,2,3]:
            raise UserWarning('Plot index not valid for timeseries. Should be 0-3.')            
        #
        self._viewplot_list.setCurrentIndex(1 + plotindex) # "Time series, show latest added."
        #
        self._ax_timeseries[plotindex] = {'time':[], 'y':[]}
        for rowindex, timestring in enumerate(time_table):
            try:

                
                
                try:
                    time = datetime.datetime.strptime(timestring, '%Y-%m-%d')
                except: 
                    time = datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S')


                
                value = float(y_table[rowindex])
                self._ax_timeseries[plotindex]['time'].append(time)
                self._ax_timeseries[plotindex]['y'].append(value)
            except:
                print(u'ERROR. Convert error. Time:' + unicode(timestring) + ' Y:' + unicode(y_table[rowindex]))
        #
        self._drawPlots()

    def addXYPlot(self, plotindex, x_table, y_table):
        """ """
        #
        if plotindex not in [0,1,2,3]:
            raise UserWarning('Plot index not valid for X/Y-plot. Should be 0-3.')            
        #
        self._viewplot_list.setCurrentIndex(6 + plotindex) # "X/Y plots, show latest added."
        #
        self._ax_xyplot[plotindex] = {'x':[], 'y':[]}
        for rowindex, x in enumerate(x_table):
            try:
                time = float(x)
                value = float(y_table[rowindex])
                self._ax_xyplot[plotindex]['x'].append(time)
                self._ax_xyplot[plotindex]['y'].append(value)
            except:
                print(u'ERROR. Convert error. Time:' + unicode(x) + ' Y:' + unicode(y_table[rowindex]))
        #
        self._drawPlots()

    # === Private methods. ===    
    def _clearSelectedPlot(self):
        """ """
#        #
#        index = self._viewplot_list.currentIndex()
#        # Time series.
#        if index in [0]:
#            for ix in [0, 1, 2, 3]:
#                self._ax_timeseries[ix] = {'time':[], 'y':[]}
#        elif index in [1, 2, 3, 4]:
#            self._ax_timeseries[index - 1] = {'time':[], 'y':[]}
#        # X/Y plots.
#        elif index in [5]:
#            for ix in [0, 1, 2, 3]:
#                self._ax_xyplot[ix] = {'x':[], 'y':[]}
#        elif index in [6, 7, 8, 9]:
#            self._ax_xyplot[index - 6] = {'x':[], 'y':[]}
#        #
#        self._drawPlots()



        
        ### TEST TEST TEST
        ### TEST TEST TEST
        ### TEST TEST TEST
        
        
        import numpy as np
        import matplotlib.pyplot as plt
        
        N = 5
        menMeans = (20, 35, 30, 35, 27)
        menStd =   (2, 3, 4, 1, 2)
        
        ind = np.arange(N)  # the x locations for the groups
        width = 0.35       # the width of the bars
        
#        fig = plt.figure()
#        ax = fig.add_subplot(111)        
#        self._figure = Figure()
#        self._canvas = FigureCanvas(self._figure)        

        ax = self._figure.add_subplot(111)        
        
        
        rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)
        
        womenMeans = (25, 32, 34, 20, 25)
        womenStd =   (3, 5, 2, 3, 3)
        rects2 = ax.bar(ind+width, womenMeans, width, color='y', yerr=womenStd)
        
        # add some
        ax.set_ylabel('Scores')
        ax.set_title('Scores by group and gender')
        ax.set_xticks(ind+width)
        ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )
        
        ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        
        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                        ha='center', va='bottom')
        
        autolabel(rects1)
        autolabel(rects2)
        
        self._canvas.draw()






    def _drawPlots(self):
        """ """
        # Clear all plots before redrawing.
        self._figure.clear()
        self._canvas.draw()
        #
        if self._viewplot_list:
            if unicode(self._viewplot_list.currentText()) == "Time series 1-4":
                self._drawTimeseriesPlots()
            elif  unicode(self._viewplot_list.currentText()) == "Time series 1":
                self._drawTimeseriesPlot(0)
            elif  unicode(self._viewplot_list.currentText()) == "Time series 2":
                self._drawTimeseriesPlot(1)
            elif  unicode(self._viewplot_list.currentText()) == "Time series 3":
                self._drawTimeseriesPlot(2)
            elif  unicode(self._viewplot_list.currentText()) == "Time series 4":
                self._drawTimeseriesPlot(3)
            elif  unicode(self._viewplot_list.currentText()) == "X/Y plots 1-4":
                self._drawXYPlots()
            elif  unicode(self._viewplot_list.currentText()) == "X/Y plot 1":
                self._drawXYPlot(0)
            elif  unicode(self._viewplot_list.currentText()) == "X/Y plot 2":
                self._drawXYPlot(1)
            elif  unicode(self._viewplot_list.currentText()) == "X/Y plot 3":
                self._drawXYPlot(2)
            elif  unicode(self._viewplot_list.currentText()) == "X/Y plot 4":
                self._drawXYPlot(3)
            
    def _drawTimeseriesPlots(self):
        """ """
        for index in [0, 1, 2, 3]:
            self._drawTimeseriesPlot(index)
            
    def _drawTimeseriesPlot(self, plotindex):
        """ """
        plotformatlist = unicode(self._timeseriesforat_edit.text()).split(',')
        plotformat = plotformatlist[plotindex]
        #
        if 'time' in self._ax_timeseries[plotindex]: 
            if len(self._ax_timeseries[plotindex]['time']) > 0: 
                ax = self._figure.add_subplot(111)
                ax.plot(self._ax_timeseries[plotindex]['time'], self._ax_timeseries[plotindex]['y'], plotformat)
                #
                ax.set_xlim( self._ax_timeseries[plotindex]['time'][0], self._ax_timeseries[plotindex]['time'][-1] )
                
#                ax.xaxis.set_major_formatter( DateFormatter('%b') )        
#                ax.xaxis.set_major_formatter( DateFormatter('%Y-%m-%d') )        
#                ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
#                ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')

#                # every 3rd month
#                months    = MonthLocator(range(1,13), bymonthday=1, interval=3)
#                monthsFmt = DateFormatter("%Y-%b")
#                
#                ax.xaxis.set_major_locator(months)
#                ax.xaxis.set_major_formatter(monthsFmt)
    
                ax.xaxis.set_major_locator(dates.MonthLocator())
                ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))
                
                ax.xaxis.set_major_formatter(ticker.NullFormatter())
                ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
    
    
                self._figure.autofmt_xdate()
                #
                self._canvas.draw()
            
    def _drawXYPlots(self):
        """ """
#        for index in [0]:
#            self._drawXYPlot(index)
        for index in [0, 1, 2, 3]:
            self._drawXYPlot(index)
            
    def _drawXYPlot(self, plotindex):
        """ """
        plotformatlist = unicode(self._xyplotformat_edit.text()).split(',')
        plotformat = plotformatlist[plotindex]

        if 'x' in self._ax_xyplot[plotindex]: 
            if len(self._ax_xyplot[plotindex]['x']) > 0: 
                ax = self._figure.add_subplot(111)
                ax.plot(self._ax_xyplot[plotindex]['x'], self._ax_xyplot[plotindex]['y'], plotformat)
                #
                self._canvas.draw()




    def addTestPlot(self, parameter, station_list, taxon_list, taxon_station_value_list):
        """ """
        import numpy as np
#        import matplotlib.pyplot as plt
        
        # Clear all plots before redrawing.
        self._figure.clear()
        self._canvas.draw()

        
        N = len(station_list)
        ind = np.arange(N)  # the x locations for the groups
        width = (1.0 / (len(taxon_list))) * 0.7       # the width of the bars
        
        ax = self._figure.add_subplot(111)
        
        
        import pylab
        NUM_COLORS = len(taxon_list)
        
#        cm = pylab.get_cmap('gist_rainbow')
#        cm = pylab.get_cmap('Set1')
#        cm = pylab.get_cmap('Set2')
        cm = pylab.get_cmap('Dark2')
#        for i in range(NUM_COLORS):
#            color = cm(1.*i/NUM_COLORS)  # color will now be an RGBA tuple
#        
#        # or if you really want a generator:
#        cgen = (cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS))        
        
        
        
        
        
        

        rects_list = []                        
        for taxonindex, taxon in enumerate(taxon_list):
#            rects = ax.bar(ind + (taxonindex * width), taxon_station_value_list[taxonindex], width, color='r')
            rects = ax.bar(ind + (taxonindex * width), taxon_station_value_list[taxonindex], width, 
                           color=cm(1.0 * taxonindex / NUM_COLORS))
#            rects = ax.bar(ind + (taxonindex * width), taxon_station_value_list[taxonindex], width)
            rects_list.append(rects[0])
        
        
        # add some
        ax.set_ylabel(parameter)
        ax.set_title(parameter)
        ax.set_xticks(ind + (width * len(taxon_list) * 0.5))
        ax.set_xticklabels(station_list)
        
#        ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        ax.legend(rects_list, taxon_list)
        
#        def autolabel(rects):
#            # attach some text labels
#            for rect in rects:
#                height = rect.get_height()
#                ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
#                        ha='center', va='bottom')
#        
#        autolabel(rects1)
#        autolabel(rects2)
        
        self._canvas.draw()
        
    












