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

from mpl_toolkits.mplot3d import Axes3D

import matplotlib
import matplotlib.pyplot as pyplot
from matplotlib.figure import Figure
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
import matplotlib.dates as dates
import matplotlib.ticker as ticker

def graphplot_test():
    """ """
    print("Graph plot test...")
    #
    graphdata_1 = PlotDataOneVariable(
                        title = u"One variable data object", 
                        x_label = u'X (one variable)',
                        y_label = u'Y (one variable)')
    
    graphdata_1.addPlot(plot_name = u"First plot", 
                        y_array = [2,3,2,4,1,9], 
                        y_label = u'Y first')
    graphdata_1.addPlot(plot_name = u"Second plot", 
                        y_array = [1,2,3], 
                        y_label = u'Y second')
    graphdata_1.addPlot(plot_name = u"Third plot", 
                        y_array = [12,10,6,3,9], 
                        y_label = u'Y third')
    #
    graphdata_2 = PlotDataTwoVariables(
                        title = u"Two variable data object", 
                        x_label = u'X (two variable)',
                        y_label = u'Y (two variable)')
    graphdata_2.addPlot(plot_name = u"First plot", 
                        x_array = [1,2,5,6,7,8], 
                        y_array = [2,3,2,4,1,9], 
                        x_label = u'X first',
                        y_label = u'Y first')
    graphdata_2.addPlot(plot_name = u"Second plot", 
                        x_array = [4,5,6,7,8,9], 
                        y_array = [2,3,2,4,1,9], 
                        x_label = u'X second',
                        y_label = u'Y second')
    #
    graphdata_3 = PlotDataThreeVariables(
                        title = u"Three variable data object", 
                        x_label = u'X (three variable)',
                        y_label = u'Y (three variable)',
                        z_label = u'Z (three variable)')
    graphdata_3.addPlot(plot_name = u"First plot", 
                        x_array = [1,2,5,6,7,8], 
                        y_array = [20,30,20,40,10,90], 
                        z_array = [10,10,80,20,30,30], 
                        x_label = u'X First',
                        y_label = u'Y First',
                        z_label = u'Z First')
    graphdata_3.addPlot(plot_name = u"Second plot", 
                        x_array = [1,2,5,6,7,8], 
                        y_array = [2,3,2,4,1,9], 
                        z_array = [10,10,20,20,30,30], 
                        x_label = u'X Second',
                        y_label = u'Y Second',
                        z_label = u'Z Second')
    graphdata_3.addPlot(plot_name = u"Third plot", 
                        x_array = [10,20,50,60,70,80], 
                        y_array = [2,3,2,4,1,9], 
                        z_array = [10,60,20,90,30,30], 
                        x_label = u'X Third',
                        y_label = u'Y Third',
                        z_label = u'Z Third')
    #
    graphdata_4 = PlotDataTwoVariables(
                        x_type = u'String',
                        title = u"Two variable data object, string", 
                        x_label = u'X (two variables)',
                        y_label = u'Y (two variables)')
    graphdata_4.addPlot(plot_name = u"First plot", 
                        x_array = ['aa','bb','cc','dd','ee','ff'], 
                        y_array = [20,30,20,40,10,90], 
                        x_label = u'X First',
                        y_label = u'Y First')
    graphdata_4.addPlot(plot_name = u"Second plot", 
                        x_array = ['cc','dd','ee','ff', 'gg', 'hh'], 
                        y_array = [2,3,2,4,1,9], 
                        x_label = u'X Second',
                        y_label = u'Y Second')
    graphdata_4.addPlot(plot_name = u"Third plot", 
                        x_array = ['aa','bb','cc','dd','ee','ff'], 
                        y_array = [2,3,2,4,1,9], 
                        x_label = u'X Third',
                        y_label = u'Y Third')
    #
    #
    graph = XYGraph(graphdata_1)
    graph.plotGraph(combined = True, y_log_scale = True)
    graph.plotGraph(combined = False, y_log_scale = True)
    #
    #
    graph = XYGraph(graphdata_2)
    graph.plotGraph(combined = True, y_log_scale = True)
    graph.plotGraph(combined = False, y_log_scale = True)
    #
    #
    graph = BarGraph(graphdata_2)
    graph.plotGraph(combined = True, y_log_scale = True)
    graph.plotGraph(combined = False, y_log_scale = True)
    #
    #
    graph = ScatterGraph(graphdata_3)
    graph.plotGraph(combined = True, y_log_scale = True)
    graph.plotGraph(combined = False, y_log_scale = True)
    #
    #
    graph = BarGraph(graphdata_4)
    graph.plotGraph(combined = True, y_log_scale = True)
    graph.plotGraph(combined = False, y_log_scale = True)


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
                xmaxvalue = len(plotdict[u'Y array'])
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


class PlotDataOneVariable(PlotData):
    """ """
    
    def __init__(self,
                 title = u'', 
                 x_label = u'',
                 y_label = u'',
                 x_type = u'Integer', # Integer, Float, String, Datetime.
                 x_format = None,
                 y_type = u'', # Integer, Float, String, Datetime.
                 y_format = None,
                 z_type = u'', # Integer, Float, String, Datetime.
                 z_format = None):
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
                 y_type = u'', # Integer, Float, String, Datetime.
                 y_format = None,
                 z_type = u'', # Integer, Float, String, Datetime.
                 z_format = None):
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
        
    def addPlot(self,
                plot_name = u'', 
                x_array = [],
                y_array = [],
                x_type = u'', # Integer, Float, String, Datetime.
                x_format = None,
                y_type = u'', # Integer, Float, String, Datetime.
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
                 y_type = u'', # Integer, Float, String, Datetime.
                 y_format = None,
                 z_type = u'', # Integer, Float, String, Datetime.
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


class GraphBase(object):
    def __init__(self, graph_data):
        """ Abstract base class for  """
        super(GraphBase, self).__init__()
        #
        self._graph_data = graph_data
        #
        self._settings = {}
        self.default_settings()

    def default_settings(self):
        """ """
        self._settings = {
            "Title": None,
            "X min": None,
            "X max": None,
            "Y min": None,
            "Y max": None,
            "X log": False,
            "Y log": False,
#            "Legend position": None,
#            "Legend color map": None,
#            "Font": None,
#            "Font size": None,
        }

    def getSettings(self):
        """ """
        return self._settings
    
    def plotGraph(self):
        """ """
        
class XYGraph(GraphBase):
    def __init__(self, graph_data):
        """ """
        super(XYGraph, self).__init__(graph_data)

    def plotGraph(self, combined = False, y_log_scale = False):
        """ """
        plotlist = self._graph_data.getPlotList()
        fig = pyplot.figure()
        #
        if combined:
            subplot = fig.add_subplot(111)
            #
            if y_log_scale:
                subplot.set_yscale('log')
            #
            for plotdict in plotlist:
                if u'X array' in plotdict: 
                    subplot.plot(plotdict[u'X array'], plotdict[u'Y array'])
                else:
                    subplot.plot(plotdict[u'Y array'])
            #
            leg = subplot.legend([data[u'Plot name'] for data in plotlist],
                            'upper center', shadow=True)
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
            if self._graph_data.getPlotDataInfo()[u'X type'] == u'String':
                """ """
            else:
                xmin, xmax = self._graph_data.getXMinMaxValues()
            #
            for plotindex, plotdict in enumerate(plotlist):
                subplot = fig.add_subplot(subplotcount, 1, plotindex + 1)    
                #
                if y_log_scale:
                    subplot.set_yscale('log')
                #
                if u'X array' in plotdict: 
                    subplot.plot(plotdict[u'X array'], plotdict[u'Y array'])
                else:
                    subplot.plot(plotdict[u'Y array'])

#                subplot.grid(False)
                if (xmin != None) and (xmax != None):
                    subplot.set_xlim([xmin, xmax])
#                subplot.set_ylim([-1,20])
                #
                subplot.set_title(plotdict[u'Plot name'])
                # Use settings from first plot in list.
                subplot.set_xlabel(plotdict[u'X label'])
                subplot.set_ylabel(plotdict[u'Y label'])
            #
            pyplot.tight_layout()
            pyplot.show()


class BarGraph(GraphBase):
    def __init__(self, graph_data):
        """ """
        super(BarGraph, self).__init__(graph_data)

    def plotGraph(self, combined = False, y_log_scale = False):
        """ """
        plotlist = self._graph_data.getPlotList()
        fig = pyplot.figure()
        #
        if combined:
#            subplot = fig.add_subplot(111)
            subplot = fig.add_subplot(111)
            #
            if y_log_scale:
                subplot.set_yscale('log')
            #
            for plotdict in plotlist:
                subplot.bar(range(len(plotdict[u'X array'])), plotdict[u'Y array'])
            #
            subplot.set_xticklabels(plotdict[u'X array'], rotation=20.0)
            #
            leg = subplot.legend([data[u'Plot name'] for data in plotlist],
                            'upper center', shadow=True)
            #
            if self._graph_data.getPlotDataInfo()[u'Title']:
                subplot.set_title(self._graph_data.getPlotDataInfo()[u'Title'])
            else:
                subplot.set_title('Bar, combined')
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
            if self._graph_data.getPlotDataInfo()[u'X type'] == u'String':
                """ """
            else:
                xmin, xmax = self._graph_data.getXMinMaxValues()
            #
            for plotindex, plotdict in enumerate(plotlist):
                subplot = fig.add_subplot(subplotcount, 1, plotindex + 1)    
                #
                if y_log_scale:
                    subplot.set_yscale('log')
                #
                subplot.bar(range(len(plotdict[u'X array'])), plotdict[u'Y array'])
                #
                subplot.set_xticklabels(plotdict[u'X array'], rotation=20.0)

#                subplot.grid(False)
                if (xmin != None) and (xmax != None):
                    subplot.set_xlim([xmin, xmax])
#                subplot.set_ylim([-1,20])
                #
                subplot.set_title(plotdict[u'Plot name'])
                # Use settings from first plot in list.
                subplot.set_xlabel(plotdict[u'X label'])
                subplot.set_ylabel(plotdict[u'Y label'])
            #
            pyplot.tight_layout()
            pyplot.show()


class ScatterGraph(GraphBase):
    def __init__(self, graph_data):
        """ """
        super(ScatterGraph, self).__init__(graph_data)
        
    def plotGraph(self, combined = False, y_log_scale = False):
        """ """
        plotlist = self._graph_data.getPlotList()
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
                            'upper center', shadow=True)
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
            #  Get min/max-limits or concatenate x axis items.
            xmin = None
            xmax = None
            if self._graph_data.getPlotDataInfo()[u'X type'] == u'String':
                """ """
            else:
                xmin, xmax = self._graph_data.getXMinMaxValues()
            #
            markers = [u'o', u's', u'D', u'^', u'<']
            colours = [u'r', u'b', u'g', u'y', u'b']
            for plotindex, plotdict in enumerate(plotlist):
                subplot = fig.add_subplot(subplotcount, 1, plotindex + 1)    
                #
                if y_log_scale:
                    subplot.set_yscale('log')
                #
                subplot.scatter(plotdict[u'X array'], plotdict[u'Y array'], s = plotdict[u'Z array'], 
                                marker = markers[plotindex], c =  colours[plotindex])

#                subplot.grid(False)
                if (xmin != None) and (xmax != None):
                    subplot.set_xlim([xmin, xmax])
#                subplot.set_ylim([-1,20])
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

