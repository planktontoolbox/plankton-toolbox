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
    graphdata_1 = PlotDataOneVariable()
    graphdata_1.addPlot(plot_name = u"First plot", 
                        y_array = [2,3,2,4,1,9], 
                        y_label = u'First')
    graphdata_1.addPlot(plot_name = u"Second plot", 
                        y_array = [1,2,3], 
                        y_label = u'Second')
    graphdata_1.addPlot(plot_name = u"Third plot", 
                        y_array = [12,10,6,3,9], 
                        y_label = u'Third')
    graph = XYGraph(graphdata_1)
    graph.plotGraph(combined = True)
    graph.plotGraph(combined = False)
    #
    graphdata_2 = PlotDataTwoVariables()
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
    graph = BarGraph(graphdata_2)
    graph.plotGraph(combined = True)
    graph.plotGraph(combined = False)
    #
    graphdata_3 = PlotDataThreeVariables()
    graphdata_3.addPlot(plot_name = u"First plot", 
                        x_array = [1,2,5,6,7,8], 
                        y_array = [20,30,20,40,10,90], 
                        z_array = [10,10,80,20,30,30], 
                        x_label = u'X First',
                        y_label = u'Y First',
                        z_label = u'Y First')
    graphdata_3.addPlot(plot_name = u"Second plot", 
                        x_array = [1,2,5,6,7,8], 
                        y_array = [2,3,2,4,1,9], 
                        z_array = [10,10,20,20,30,30], 
                        x_label = u'X Second',
                        y_label = u'Y Second',
                        z_label = u'Y Second')
    graphdata_3.addPlot(plot_name = u"Third plot", 
                        x_array = [10,20,50,60,70,80], 
                        y_array = [2,3,2,4,1,9], 
                        z_array = [10,60,20,90,30,30], 
                        x_label = u'X Third',
                        y_label = u'Y Third',
                        z_label = u'Y Third')
    #
    graph = ScatterGraph(graphdata_3)
    graph.plotGraph(combined = True)
    graph.plotGraph(combined = False)
    

class PlotData(object):
    """ 
    Abstract base class for data objects. 
    """
    
    def __init__(self):
        """ """
        super(PlotData, self).__init__()
        #
        self._plot_list = []
        
    def clear(self):
        """ """
        self._plot_list = []
        
    def removePlot(self, data_index = None):
        """ """
        
    def getPlotList(self):
        """ """
        return self._plot_list

        
class PlotDataOneVariable(PlotData):
    """ """
    
    def __init__(self):
        """ """
        super(PlotDataOneVariable, self).__init__()
        
    def addPlot(self,
                plot_name = u'', 
                y_array = [],
                x_label = u'Position in data array',
                y_label = u''):
        """ X data will automatically be created by Matplotlib (0, 1, 2, ...). """
        plotdict = {}
        plotdict[u'Plot name'] = plot_name
        plotdict[u'Y array'] = y_array
        plotdict[u'X label'] = x_label
        plotdict[u'Y label'] = y_label
        self._plot_list.append(plotdict)
        
class PlotDataTwoVariables(PlotData):
    """ """
    
    def __init__(self):
        """ """
        super(PlotDataTwoVariables, self).__init__()
        
    def addPlot(self,
                plot_name = u'', 
                x_array = [],
                y_array = [],
                x_label = u'',
                y_label = u''):
        """ X data will automatically be created by Matplotlib (0, 1, 2, ...). """
        plotdict = {}
        plotdict[u'Plot name'] = plot_name
        plotdict[u'X array'] = x_array
        plotdict[u'Y array'] = y_array
        plotdict[u'X label'] = x_label
        plotdict[u'Y label'] = y_label
        self._plot_list.append(plotdict)
        
class PlotDataThreeVariables(PlotData):
    """ """
    
    def __init__(self):
        """ """
        super(PlotDataThreeVariables, self).__init__()
        
    def addPlot(self,
                plot_name = u'', 
                x_array = [],
                y_array = [],
                z_array = [],
                x_label = u'',
                y_label = u'',
                z_label = u''):
        """ X data will automatically be created by Matplotlib (0, 1, 2, ...). """
        plotdict = {}
        plotdict[u'Plot name'] = plot_name
        plotdict[u'X array'] = x_array
        plotdict[u'Y array'] = y_array
        plotdict[u'Z array'] = z_array
        plotdict[u'X label'] = x_label
        plotdict[u'Y label'] = y_label
        plotdict[u'Z label'] = z_label
        self._plot_list.append(plotdict)
        
        
             
# Classes for different kinds of plots. Follows the "Template method" pattern.
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
        
class TimeSeriesGraph(GraphBase):
    def __init__(self, graph_data):
        """ """
        super(TimeSeriesGraph, self).__init__(graph_data)
        
class XYGraph(GraphBase):
    def __init__(self, graph_data):
        """ """
        super(XYGraph, self).__init__(graph_data)

    def plotGraph(self, combined = False):
        """ """
        plotlist = self._graph_data.getPlotList()
        fig = pyplot.figure()
        #
        if combined:
            subplot = fig.add_subplot(111)
            #
            for plotdict in plotlist:
                subplot.plot(plotdict[u'Y array'], )
            #
            leg = subplot.legend([data[u'Plot name'] for data in plotlist],
                            'upper center', shadow=True)
            #
#            subplot.grid(False)
#            subplot.set_ylim([-1,20])
            #
            subplot.set_title('X/Y Graph combined')
            # Use settings from first plot in list.
            subplot.set_xlabel(plotlist[0][u'X label'])
            subplot.set_ylabel(plotlist[0][u'Y label'])
            #
            pyplot.show()
        else:
            subplotcount = len(plotlist)
            # Calculate x min/maxlimits. TODO: 
            xmin = None
            xmax = None
            for plotdict in plotlist:
                if u'X array' in plotdict:                    
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
            for plotindex, plotdict in enumerate(plotlist):
                subplot = fig.add_subplot(subplotcount, 1, plotindex + 1)    
                subplot.plot(plotdict[u'Y array'], )

#                subplot.grid(False)
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

    def plotGraph(self, combined = False):
        """ """
        plotlist = self._graph_data.getPlotList()
        fig = pyplot.figure()
        #
        if combined:
            subplot = fig.add_subplot(111)
            #
            for plotdict in plotlist:
                subplot.bar(plotdict[u'X array'], plotdict[u'Y array'])
            #
            leg = subplot.legend([data[u'Plot name'] for data in plotlist],
                            'upper center', shadow=True)
            #
#            subplot.grid(False)
#            subplot.set_ylim([-1,20])
            #
            subplot.set_title('X/Y Graph combined')
            # Use settings from first plot in list.
            subplot.set_xlabel(plotlist[0][u'X label'])
            subplot.set_ylabel(plotlist[0][u'Y label'])
            #
            pyplot.show()
        else:
            subplotcount = len(plotlist)
            # Calculate x min/maxlimits. TODO: 
            xmin = None
            xmax = None
            for plotdict in plotlist:
                if u'X array' in plotdict:                    
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
            for plotindex, plotdict in enumerate(plotlist):
                subplot = fig.add_subplot(subplotcount, 1, plotindex + 1)    
                subplot.bar(plotdict[u'X array'], plotdict[u'Y array'])

#                subplot.grid(False)
                subplot.set_xlim([xmin, xmax + 1])
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
        
    def plotGraph(self, combined = False):
        """ """
        plotlist = self._graph_data.getPlotList()
        fig = pyplot.figure()
        #
        if combined:
            subplot = fig.add_subplot(111)
            #
            for plotdict in plotlist:
                subplot.scatter(plotdict[u'X array'], plotdict[u'Y array'], s = plotdict[u'Z array'], marker='^', c='r')
            #
            leg = subplot.legend([data[u'Plot name'] for data in plotlist],
                            'upper center', shadow=True)
            #
#            subplot.grid(False)
#            subplot.set_ylim([-1,20])
            #
            subplot.set_title('X/Y Graph combined')
            # Use settings from first plot in list.
            subplot.set_xlabel(plotlist[0][u'X label'])
            subplot.set_ylabel(plotlist[0][u'Y label'])
            #
            pyplot.show()
        else:
            subplotcount = len(plotlist)
            # Calculate x min/maxlimits. TODO: 
            xmin = None
            xmax = None
            for plotdict in plotlist:
                if u'X array' in plotdict:                    
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
            for plotindex, plotdict in enumerate(plotlist):
                subplot = fig.add_subplot(subplotcount, 1, plotindex + 1)    
                subplot.scatter(plotdict[u'X array'], plotdict[u'Y array'], s = plotdict[u'Z array'], marker='^', c='r')

#                subplot.grid(False)
                subplot.set_xlim([xmin, xmax + 1])
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

