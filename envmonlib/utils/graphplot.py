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

import matplotlib.dates
#import matplotlib.pyplot as pyplot
import numpy
import pylab # For color maps
import datetime

def graphplot_test():
    """ """
    print("Graph plot test...")
    #
    plotdata_1 = PlotDataOneVariable(
                        title = u"One variable data object", 
                        x_label = u'X (one variable)',
                        y_label = u'Y (one variable)')
    
    plotdata_1.addPlot(plot_name = u"First plot", 
                        y_array = [2,3,2,4,1,9], 
                        y_label = u'Y first')
    plotdata_1.addPlot(plot_name = u"Second plot", 
                        y_array = [1,2,3], 
                        y_label = u'Y second')
    plotdata_1.addPlot(plot_name = u"Third plot", 
                        y_array = [12,10,6,3,9], 
                        y_label = u'Y third')
    #
    plotdata_2 = PlotDataTwoVariables(
                        title = u"Two variables data object", 
                        x_label = u'X (two variable)',
                        y_label = u'Y (two variable)')
    plotdata_2.addPlot(plot_name = u"First plot", 
                        x_array = [1,2,5,6,7,8], 
                        y_array = [2,3,2,4,1,9], 
                        x_label = u'X first',
                        y_label = u'Y first')
    plotdata_2.addPlot(plot_name = u"Second plot", 
                        x_array = [4,5,6,7,8,9,10,11], 
                        y_array = [2,3,2,4,1,9,2,1], 
                        x_label = u'X second',
                        y_label = u'Y second')
    #
    plotdata_3 = PlotDataThreeVariables(
                        title = u"Three variables data object", 
                        x_label = u'X (three variable)',
                        y_label = u'Y (three variable)',
                        z_label = u'Z (three variable)')
    plotdata_3.addPlot(plot_name = u"First plot", 
                        x_array = [1,2,5,6,7,8], 
                        y_array = [20,30,20,40,10,90], 
                        z_array = [10,10,80,20,30,30], 
                        x_label = u'X First',
                        y_label = u'Y First',
                        z_label = u'Z First')
    plotdata_3.addPlot(plot_name = u"Second plot", 
                        x_array = [1,2,5,6,7,8], 
                        y_array = [2,3,2,4,1,9], 
                        z_array = [10,10,20,20,30,30], 
                        x_label = u'X Second',
                        y_label = u'Y Second',
                        z_label = u'Z Second')
    plotdata_3.addPlot(plot_name = u"Third plot", 
                        x_array = [10,20,50,60,70,80], 
                        y_array = [2,3,2,4,1,9], 
                        z_array = [10,60,20,90,30,30], 
                        x_label = u'X Third',
                        y_label = u'Y Third',
                        z_label = u'Z Third')
    #
    plotdata_4 = PlotDataTwoVariables(
                        x_type = u'String',
                        title = u"Two variables data object, string", 
                        x_label = u'X (two variables)',
                        y_label = u'Y (two variables)')
    plotdata_4.addPlot(plot_name = u"Dinophysis acuta", 
                        x_array = [u'BY15',u'Släggö',u'cc','dd','ee'], 
                        y_array = [10,30,5,5,1], 
                        x_label = u'X First',
                        y_label = u'Y First')
    plotdata_4.addPlot(plot_name = u"Second plot", 
                        x_array = ['cc','dd','ee','ff', 'gg', 'hh'], 
                        y_array = [2,3,2,4,1,9], 
                        x_label = u'X Second',
                        y_label = u'Y Second')
    plotdata_4.addPlot(plot_name = u"Third plot", 
                        x_array = ['AA','BB','cc','dd','ee','ff'], 
                        y_array = [5,5,5,1,2,3], 
                        x_label = u'X Third',
                        y_label = u'Y Third')
    #
    plotdata_5 = PlotDataTwoVariables(
                        x_type = u'Date',
                        title = u"Two variables x:date", 
                        x_label = u'X (date)',
                        y_label = u'Y (two variable)')
    plotdata_5.addPlot(plot_name = u"First plot", 
                        x_array = [u'2012-03-07', u'2012-04-01', u'2012-05-10', u'2012-06-20'], 
                        y_array = [2,4,1,9], 
                        x_label = u'X first (date)',
                        y_label = u'Y first')
    plotdata_5.addPlot(plot_name = u"Second plot", 
                        x_array = [u'2012-01-01', u'2012-02-01', u'2012-03-21', u'2012-04-01', u'2012-05-01', u'2012-06-01', u'2012-07-01', u'2012-08-01'], 
                        y_array = [2,3,2,4,1,9,2,1], 
                        x_label = u'X second (date)',
                        y_label = u'Y second')
    #
    #
    graph = LineChart(plotdata_1)
    graph.plotChart(combined = True, y_log_scale = True)
    graph.plotChart(combined = False, y_log_scale = True)
    #
    #
    graph = LineChart(plotdata_2)
    graph.plotChart(combined = True, y_log_scale = True)
    graph.plotChart(combined = False, y_log_scale = True)
    #
    #
    graph = BarChart(plotdata_2)
    graph.plotChart(combined = True, y_log_scale = False)
    graph.plotChart(combined = True, y_log_scale = False, stacked = True)
    graph.plotChart(combined = False, y_log_scale = True)
    graph.plotChart(combined = False, y_log_scale = True, stacked = True)
    #
    #
    graph = ScatterChart(plotdata_3)
    graph.plotChart(combined = True, y_log_scale = False)
    graph.plotChart(combined = False, y_log_scale = True)
    #
    #
    graph = BarChart(plotdata_4)
    graph.plotChart(combined = True, y_log_scale = False)
    graph.plotChart(combined = True, y_log_scale = False, stacked = True)
    graph.plotChart(combined = True, y_log_scale = False)
    graph.plotChart(combined = True, y_log_scale = False, stacked = True)
    graph.plotChart(combined = False, y_log_scale = False)
    graph.plotChart(combined = False, y_log_scale = False, stacked = True)
    #
    graph = PieChart(plotdata_1)
    graph.plotChart(combined = False, y_log_scale = False)
    #
    graph = PieChart(plotdata_2)
    graph.plotChart(combined = False, y_log_scale = False)
    #
    graph = PieChart(plotdata_4)
    graph.plotChart(combined = False, y_log_scale = False)
    #
    graph = LineChart(plotdata_5)
    graph.plotChart(combined = True, y_log_scale = True)
    graph.plotChart(combined = False, y_log_scale = True)


class PlotData(object):
    """ Abstract base class for data objects. """
    
    def __init__(self):
        """ """
        super(PlotData, self).__init__()
        #
        self._plot_list = []
        self._plotdata_info = {}
        
    def clear(self):
        """ """
        self._plot_list = []
        
    def removePlot(self, data_index = None):
        """ """
        if data_index: 
            del self._plot_list[data_index]
        
    def getPlotList(self):
        """ """
        return self._plot_list
    
    def getPlotDataInfo(self):
        """ """
        return self._plotdata_info
    
    def getXMinMaxValues(self):
        """ """
        xmin = None
        xmax = None
        for plotdict in self._plot_list:
            if (u'X array' in plotdict) and (len(plotdict[u'X array']) > 0):                    
                xminvalue = min(plotdict[u'X array'])
                xmaxvalue = max(plotdict[u'X array'])
            else:
                # x = position in array if x is missing.
                xminvalue = 0
                xmaxvalue = len(plotdict[u'Y array']) - 1
            #
            if not xmin: xmin = xminvalue
            if not xmax: xmax = xmaxvalue
            if xmin > xminvalue: xmin = xminvalue
            if xmax < xmaxvalue: xmax = xmaxvalue
        #
        return xmin, xmax

    def getYMinMaxValues(self):
        """ """
        ymin = None
        ymax = None
        for plotdict in self._plot_list:
            if u'Y array' in plotdict:                    
                yminvalue = min(plotdict[u'Y array'])
                ymaxvalue = max(plotdict[u'Y array'])
            else:
                yminvalue = 0
                ymaxvalue = 0
            #
            if not ymin: ymin = yminvalue
            if not ymax: ymax = ymaxvalue
            if ymin > yminvalue: ymin = yminvalue
            if ymax < ymaxvalue: ymax = ymaxvalue
        #
        return ymin, ymax

    def mergeData(self):
        """ Creates a common x array and add zero values for plots with no corresponding x value. """
        
        # Create a union list containing all x values.
        x_union = []
        for plotdict in self._plot_list:
            x_union = list(set(x_union) | set(plotdict[u'X array'])) # List union
        # Sorts the list.                   
        x_union.sort()

#        print (x_union)

        for plotdict in self._plot_list:
            newyarray = []
            yarrayasdict = dict(zip(plotdict[u'X array'], plotdict[u'Y array']))
            
#            print(yarrayasdict)
            
            for x in x_union:
                if x in yarrayasdict:
                    newyarray.append(yarrayasdict[x])
                else:
                    newyarray.append(0)        
            #
#            print(yarrayasdict)
#            print (newyarray)
            #
            plotdict[u'X array'] = x_union[:]
            plotdict[u'Y array'] = newyarray[:]
        

class PlotDataOneVariable(PlotData):
    """ """
    
    def __init__(self,
                 title = u'', 
                 x_label = u'',
                 y_label = u'',
                 x_type = u'Integer', # Integer, Float, String, Date.
                 x_format = None,
                 y_type = u'', # Integer, Float.
                 y_format = None,):
        """ """
        super(PlotDataOneVariable, self).__init__()
        #
        self._plotdata_info[u'Title'] = title
        self._plotdata_info[u'X label'] = x_label
        self._plotdata_info[u'Y label'] = y_label
        self._plotdata_info[u'X type'] = x_type
        self._plotdata_info[u'X format'] = x_format
        self._plotdata_info[u'Y type'] = y_type
        self._plotdata_info[u'Y format'] = y_format
        
    def getAvailableCharts(self):
        """ """
        return {
                u'Line chart': {u'Parameters': [u'combined', u'stacked', u'y_log_scale']},
                }

    def addPlot(self,
                plot_name = u'', 
                y_array = [],
                x_label = u'Position in data array',
                y_label = u''):
        """ X data will automatically be created by Matplotlib (0, 1, 2, ...). """
        plotdict = {}
        plotdict[u'Plot name'] = plot_name
        plotdict[u'Y array'] = y_array
        #
        plotdict[u'X label'] = x_label
        plotdict[u'Y label'] = y_label
        self._plot_list.append(plotdict)


class PlotDataTwoVariables(PlotData):
    """ """
    
    def __init__(self,
                 title = u'', 
                 x_label = u'',
                 y_label = u'',
                 x_type = u'', # Integer, Float, String, Datetime.
                 x_format = None,
                 y_type = u'', # Integer, Float.
                 y_format = None):
        """ """
        super(PlotDataTwoVariables, self).__init__()
        #
        self._plotdata_info[u'Title'] = title
        self._plotdata_info[u'X label'] = x_label
        self._plotdata_info[u'Y label'] = y_label
        self._plotdata_info[u'X type'] = x_type
        self._plotdata_info[u'X format'] = x_format
        self._plotdata_info[u'Y type'] = y_type
        self._plotdata_info[u'Y format'] = y_format
        
    def getAvailableCharts(self):
        """ """
        return {
                u'Line chart': {u'Parameters': [u'combined', u'stacked', u'y_log_scale']},
                u'Bar chart': {u'Parameters': [u'combined', u'stacked', u'y_log_scale']},
                u'Scatter chart': {u'Parameters': [u'combined', u'y_log_scale']},
                u'Pie chart': {u'Parameters': []},
                }

    def addPlot(self,
                plot_name = u'', 
                x_array = [],
                y_array = [],
                x_type = u'', # Integer, Float, String, Datetime.
                x_format = None,
                y_type = u'', # Integer, Float.
                y_format = None,
                x_label = u'',
                y_label = u''):
        """ """
        plotdict = {}
        plotdict[u'Plot name'] = plot_name
        plotdict[u'X array'] = x_array
        plotdict[u'Y array'] = y_array
        #
        plotdict[u'X type'] = x_type
        plotdict[u'X format'] = x_format
        plotdict[u'Y type'] = y_type
        plotdict[u'Y format'] = y_format
        #
        plotdict[u'X label'] = x_label
        plotdict[u'Y label'] = y_label
        self._plot_list.append(plotdict)


class PlotDataThreeVariables(PlotData):
    """ """
    
    def __init__(self,
                 title = u'', 
                 x_label = u'',
                 y_label = u'',
                 z_label = u'',
                 x_type = u'', # Integer, Float, String, Datetime.
                 x_format = None,
                 y_type = u'', # Integer, Float.
                 y_format = None,
                 z_type = u'', # Integer, Float.
                 z_format = None):
        """ """
        super(PlotDataThreeVariables, self).__init__()
        #
        self._plotdata_info[u'Title'] = title
        self._plotdata_info[u'X label'] = x_label
        self._plotdata_info[u'Y label'] = y_label
        self._plotdata_info[u'Z label'] = z_label
        self._plotdata_info[u'X type'] = x_type
        self._plotdata_info[u'X format'] = x_format
        self._plotdata_info[u'Y type'] = y_type
        self._plotdata_info[u'Y format'] = y_format
        self._plotdata_info[u'Z type'] = z_type
        self._plotdata_info[u'Z format'] = z_format
        
    def getAvailableCharts(self):
        """ """
        return {
                u'Line chart': {u'Parameters': [u'combined', u'stacked', u'y_log_scale']},
                u'Bar chart': {u'Parameters': [u'combined', u'stacked', u'y_log_scale']},
                u'Scatter chart': {u'Parameters': [u'combined', u'y_log_scale']},
                }

    def addPlot(self,
                plot_name = u'', 
                x_array = [],
                y_array = [],
                z_array = [],
                x_label = u'',
                y_label = u'',
                z_label = u''):
        """ """
        plotdict = {}
        plotdict[u'Plot name'] = plot_name
        plotdict[u'X array'] = x_array
        plotdict[u'Y array'] = y_array
        plotdict[u'Z array'] = z_array
        #
        plotdict[u'X label'] = x_label
        plotdict[u'Y label'] = y_label
        plotdict[u'Z label'] = z_label
        self._plot_list.append(plotdict)


class ChartBase(object):
    """ """
    def __init__(self, graph_data):
        """ Abstract base class for  """
        super(ChartBase, self).__init__()
        #
        self._graph_data = graph_data
        #
#        self._settings = {}
#        self.default_settings()

#    def default_settings(self):
#        """ """
#        self._settings = {
#            "Title": None,
#            "X min": None,
#            "X max": None,
#            "Y min": None,
#            "Y max": None,
#            "X log": False,
#            "Y log": False,
#            "Legend position": None,
#            "Legend color map": None,
#            "Font": None,
#            "Font size": None,
#        }

#    def getSettings(self):
#        """ """
#        return self._settings
    
    def plotChart(self):
        """ Abstract."""


class LineChart(ChartBase):
    """ """
    def __init__(self, graph_data, figure = None):
        """ """
        super(LineChart, self).__init__(graph_data)
        self._figure = figure

    def plotChart(self, 
                  combined = False, 
                  y_log_scale = False):
        """ """
        plotlist = self._graph_data.getPlotList()
        x_type = self._graph_data.getPlotDataInfo()[u'X type']
        #
        if self._figure:
            fig = self._figure
        else:
            # Use pyplot for tests.
            import matplotlib.pyplot as pyplot    
            fig = pyplot.figure()
        #
        if combined:
            subplot = fig.add_subplot(111)
            #
            if y_log_scale:
                subplot.set_yscale('log')
            #
            markers = [u'o', u's', u'D', u'^', u'<']
            colours = [u'r', u'b', u'g', u'y', u'b']
            #
            for plotindex, plotdict in enumerate(plotlist):
                if x_type == u'Date':
                    # Convert date strings.
                    x_array = []
                    for timestring in plotdict[u'X array']:
                        try:
                            time = datetime.datetime.strptime(timestring, '%Y-%m-%d')
                        except: 
                            time = datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S')
                        x_array.append(time)
                    # 
                    subplot.plot_date(x_array, plotdict[u'Y array'],
                                      marker = markers[plotindex], c =  colours[plotindex])
                    #
                    subplot.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
                    subplot.xaxis.set_minor_locator(matplotlib.dates.WeekdayLocator())
                    subplot.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(u'%Y-%m-%d')) 
                    #
                    fig.autofmt_xdate(bottom = 0.2)                     
                else:
                    if u'X array' in plotdict: 
                        subplot.plot(plotdict[u'X array'], plotdict[u'Y array'])
                    else:
                        subplot.plot(plotdict[u'Y array'])
            #
            leg = subplot.legend([data[u'Plot name'] for data in plotlist],
                                 loc='best', fancybox=True)
            leg.get_frame().set_alpha(0.5)
            #
            if self._graph_data.getPlotDataInfo()[u'Title']:
                subplot.set_title(self._graph_data.getPlotDataInfo()[u'Title'])
            else:
                subplot.set_title('X/Y, combined')
            # 
            subplot.set_xlabel(self._graph_data.getPlotDataInfo()[u'X label'])
            subplot.set_ylabel(self._graph_data.getPlotDataInfo()[u'Y label'])
            #
            pyplot.tight_layout()
            pyplot.show()
        else:
            subplotcount = len(plotlist)
            #  Get min/max-limits or concatenate x axis items.
            xmin = None
            xmax = None
            if x_type == u'String':
                self._graph_data.mergeData()
            #
            share_x_axis = None
            #
            for plotindex, plotdict in enumerate(plotlist):
                subplot = fig.add_subplot(subplotcount, 1, plotindex + 1, sharex = share_x_axis)
                if not share_x_axis: share_x_axis = subplot    
                #
                if y_log_scale:
                    subplot.set_yscale('log')
                #
                if x_type == u'Date':
                    # Convert date strings.
                    x_array = []
                    for timestring in plotdict[u'X array']:
                        try:
                            time = datetime.datetime.strptime(timestring, '%Y-%m-%d')
                        except: 
                            time = datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S')
                        x_array.append(time)
                    # 
                    subplot.plot_date(x_array, plotdict[u'Y array'])
                    #
                    subplot.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
                    subplot.xaxis.set_minor_locator(matplotlib.dates.WeekdayLocator())
                    subplot.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(u'%Y-%m-%d')) 
                    #
                    fig.autofmt_xdate(bottom = 0.2)                     
                else:
                    if u'X array' in plotdict:
                        subplot.plot(plotdict[u'X array'], plotdict[u'Y array'])
                    else:
                        subplot.plot(plotdict[u'Y array']) 
                    #
                    if (xmin != None) and (xmax != None):
                        subplot.set_xlim([xmin, xmax])
                #
                subplot.axis(u'auto')
#                subplot.grid(False)
                #
                subplot.set_title(plotdict[u'Plot name'])
                # Use settings from first plot in list.
                subplot.set_xlabel(plotdict[u'X label'])
                subplot.set_ylabel(plotdict[u'Y label'])
            #
            pyplot.tight_layout()
            pyplot.show()


class BarChart(ChartBase):
    """ """
    def __init__(self, graph_data, figure = None):
        """ """
        super(BarChart, self).__init__(graph_data)
        self._figure = figure

    def plotChart(self, 
                  combined = False, 
                  y_log_scale = False,
                  stacked = False):
        """ """
        plotlist = self._graph_data.getPlotList()
        x_type = self._graph_data.getPlotDataInfo()[u'X type']
        #
        if self._figure:
            fig = self._figure
        else:
            # Use pyplot for tests.
            import matplotlib.pyplot as pyplot    
            fig = pyplot.figure()
        #
        if combined:
            # All plots should have the same x axis items.
            self._graph_data.mergeData()
            # Get axes from first plot.
            x_axis = plotlist[0][u'X array']
            x_axis_positions = numpy.arange(len(x_axis))
            # Set up width and color of bars.
            barwidth = (1.0 / (len(plotlist))) * 0.7
            colourcount = len(plotlist)
            colourmap = pylab.get_cmap('Dark2')
            #
#            subplot = fig.add_subplot(111)
            subplot = fig.add_subplot(111)
            #
            if y_log_scale:
                subplot.set_yscale('log')
            #        
            accumulatedplots = [0] * len(x_axis) # For stacked bars.
            #
            for plotindex, plotdict in enumerate(plotlist):
                #
                if stacked:
                    rect = subplot.bar(x_axis_positions, 
                                       plotdict[u'Y array'],
                                       0.7,
                                       color=colourmap(1.0 * plotindex / colourcount),
                                       bottom = accumulatedplots)
                    accumulatedplots = [(x + y) for x, y in zip(accumulatedplots, plotdict[u'Y array'])] # For stacked bars.
                else:                        
                    rect = subplot.bar(x_axis_positions + (plotindex * barwidth),
                                       plotdict[u'Y array'],
                                       barwidth,
                                       color=colourmap(1.0 * plotindex / colourcount))
            #
            subplot.set_xticks(x_axis_positions + (barwidth * len(plotlist) * 0.5))
            subplot.set_xticklabels(plotdict[u'X array'], rotation=20.0)
            #
            leg = subplot.legend([data[u'Plot name'] for data in plotlist],
                                 loc='best', fancybox=True)
            leg.get_frame().set_alpha(0.5)
            #
            if self._graph_data.getPlotDataInfo()[u'Title']:
                subplot.set_title(self._graph_data.getPlotDataInfo()[u'Title'])
            else:
                subplot.set_title('Bar, combined')
            #
            subplot.set_xlabel(self._graph_data.getPlotDataInfo()[u'X label'])
            subplot.set_ylabel(self._graph_data.getPlotDataInfo()[u'Y label'])
            #
            if not self._figure:
                pyplot.tight_layout()
                pyplot.show()
        else:
            # All plots should have the same x axis items.
            self._graph_data.mergeData()
            # Get axes from first plot.
            x_axis = plotlist[0][u'X array']
            x_axis_positions = numpy.arange(len(x_axis))
            # Set up width and color of bars.
            barwidth = 0.7
            colourcount = len(plotlist)
            colourmap = pylab.get_cmap('Dark2')
            #
            subplotcount = len(plotlist)
            #  Get min/max-limits or concatenate x axis items.
            xmin = None
            xmax = None
            if x_type == u'String':
                self._graph_data.mergeData()
            #
            share_x_axis = None
            #
            for plotindex, plotdict in enumerate(plotlist):
            
                subplot = fig.add_subplot(subplotcount, 1, plotindex + 1, sharex = share_x_axis)    
                if not share_x_axis: share_x_axis = subplot    
                #
                if y_log_scale:
                    subplot.set_yscale('log')
                #
                rect = subplot.bar(x_axis_positions, 
                                   plotdict[u'Y array'],
                                   barwidth,
                                   color=colourmap(1.0 * plotindex / colourcount))
                #
                subplot.set_xticks(x_axis_positions + (barwidth * 0.5))
                subplot.set_xticklabels(plotdict[u'X array'], rotation=20.0)
                #
                subplot.axis(u'auto')
                #
                subplot.set_title(plotdict[u'Plot name'])
                # Use settings from first plot in list.
                subplot.set_xlabel(plotdict[u'X label'])
                subplot.set_ylabel(plotdict[u'Y label'])
            #
            if not self._figure:
                pyplot.tight_layout()
                pyplot.show()


class PieChart(ChartBase):
    """ """
    def __init__(self, graph_data, figure = None):
        """ """
        super(PieChart, self).__init__(graph_data)
        self._figure = figure
        
    def plotChart(self, 
                  combined = False, 
                  y_log_scale = False):
        """ """
        #
        plotlist = self._graph_data.getPlotList()
        #
        if self._figure:
            fig = self._figure
        else:
            # Use pyplot for tests.
            import matplotlib.pyplot as pyplot    
            fig = pyplot.figure()
        #
        subplotcount = len(plotlist)
        #
        for plotindex, plotdict in enumerate(plotlist):
            subplot = fig.add_subplot(subplotcount, 1, plotindex + 1)
            if u'X array' in plotdict:    
                subplot.pie(plotdict[u'Y array'], labels=plotdict[u'X array'])
            else:
                subplot.pie(plotdict[u'Y array'])
#                subplot.pie(plotdict[u'Y array'], labels=plotdict[u'X array'], autopct='%1.1f%%', shadow=True)
            subplot.axis(u'equal')
            #
            subplot.set_title(plotdict[u'Plot name'])
        #
        pyplot.tight_layout()
        pyplot.show()

                
class ScatterChart(ChartBase):
    """ """
    def __init__(self, graph_data, figure = None):
        """ """
        super(ScatterChart, self).__init__(graph_data)
        self._figure = figure
        
    def plotChart(self, 
                  combined = False, 
                  y_log_scale = False):
        """ """
        plotlist = self._graph_data.getPlotList()
        x_type = self._graph_data.getPlotDataInfo()[u'X type']
        #
        if self._figure:
            fig = self._figure
        else:
            # Use pyplot for tests.
            import matplotlib.pyplot as pyplot    
            fig = pyplot.figure()
        #
        if combined:
            subplot = fig.add_subplot(111)
            #
            if y_log_scale:
                subplot.set_yscale('log')
            #
            markers = [u'o', u's', u'D', u'^', u'<']
            colours = [u'r', u'b', u'g', u'y', u'b']
            for plotindex, plotdict in enumerate(plotlist):
                subplot.scatter(plotdict[u'X array'], plotdict[u'Y array'], s = plotdict[u'Z array'], 
                                marker = markers[plotindex], c =  colours[plotindex])
            #
            leg = subplot.legend([data[u'Plot name'] for data in plotlist],
                                 loc='best', fancybox=True)
            leg.get_frame().set_alpha(0.5)
            #
            if self._graph_data.getPlotDataInfo()[u'Title']:
                subplot.set_title(self._graph_data.getPlotDataInfo()[u'Title'])
            else:
                subplot.set_title('Scatter, combined') # Default.
            # 
            subplot.set_xlabel(self._graph_data.getPlotDataInfo()[u'X label'])
            subplot.set_ylabel(self._graph_data.getPlotDataInfo()[u'Y label'])
            #
            pyplot.tight_layout()
            pyplot.show()
        else:
            subplotcount = len(plotlist)
            #  Concatenate x axis items if they contains texts.
            if x_type == u'String':
                self._graph_data.mergeData()
            #
            share_x_axis = None
            #
            markers = [u'o', u's', u'D', u'^', u'<']
            colours = [u'r', u'b', u'g', u'y', u'b']
            for plotindex, plotdict in enumerate(plotlist):
                subplot = fig.add_subplot(subplotcount, 1, plotindex + 1, sharex = share_x_axis)    
                if not share_x_axis: share_x_axis = subplot    
                #
                if y_log_scale:
                    subplot.set_yscale('log')
                #
                subplot.scatter(plotdict[u'X array'], plotdict[u'Y array'], s = plotdict[u'Z array'], 
                                marker = markers[plotindex], c =  colours[plotindex])
                #
                subplot.axis(u'auto')
                #
                subplot.set_title(plotdict[u'Plot name'])
                # Use settings from first plot in list.
                subplot.set_xlabel(plotdict[u'X label'])
                subplot.set_ylabel(plotdict[u'Y label'])
            #
            pyplot.tight_layout()
            pyplot.show()

                
if __name__ == "__main__":
    graphplot_test()

