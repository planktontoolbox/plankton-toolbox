#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2011-2012 SMHI, Swedish Meteorological and Hydrological Institute 
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

#import numpy
import numpy.ma
import datetime
import copy
import matplotlib.dates as mpl_dates
import matplotlib.font_manager as mpl_font_manager


import matplotlib.pyplot as pyplot # ???????????????????


#ax1.set_xticklabels([])
#Similar for the yticklabels. However, you cannot share the x-axis with the plots that do have tick labels.




import pylab # For color maps
import envmonlib

class GraphPlotData(object):
    """ Class containing data needed when plotting. 
    
        View format: Text, 
                    Integer, 
                    Numeric: number of shown decimals,
                    Boolean,
                    Datetime: view format, 
                    Date: view format, 
                    Time: view format.

        Text, Integer, Numeric Boolean Datetime Date Time.
    """
    
    def __init__(self,
                 title = u'', 
                 x_label = u'',
                 x_type = u'Integer', # Text, Integer, Numeric Boolean Datetime Date Time.
                 x_format = None, # Used for date type. 
                 y_label = u'',
                 y_type = u'', # Text, Integer, Numeric Boolean Datetime Date Time.
                 y_format = None, # Used for date type. 
                 z_label = u'',
                 z_type = u'', # Text, Integer, Numeric Boolean Datetime Date Time.
                 z_format = None): # Used for date type. 
        """ """
        super(GraphPlotData, self).__init__()
        #
        self._plot_list = []
        self._plotdata_info = {}
        #
        self._plotdata_info[u'Title'] = title
        self._plotdata_info[u'X label'] = x_label
        self._plotdata_info[u'X type'] = x_type
        self._plotdata_info[u'X format'] = x_format
        #
        self._plotdata_info[u'Y label'] = y_label
        self._plotdata_info[u'Y type'] = y_type
        self._plotdata_info[u'Y format'] = y_format
        #
        self._plotdata_info[u'Z label'] = z_label
        self._plotdata_info[u'Z type'] = z_type
        self._plotdata_info[u'Z format'] = z_format
        
    def addPlot(self,
                plot_name = u'', 
                x_label = u'',
                x_array = None,
                y_label = u'',
                y_array = None,
                z_label = u'',
                z_array = None):
        """ """
        if (not y_array) or (len(y_array) == 0):
            envmonlib.Logging().warning(u"GraphPlotData.addPlot() must contain at least an Y-array. Plotting terminated.")
            return
        #
        plotdict = {}
        plotdict[u'Plot name'] = plot_name
        plotdict[u'X label'] = x_label
        plotdict[u'X array'] = x_array
        #
        plotdict[u'Y label'] = y_label
        plotdict[u'Y array'] = y_array
        #
        plotdict[u'Z label'] = z_label
        plotdict[u'Z array'] = z_array
        #
        self._plot_list.append(plotdict)
               
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
    
#    def getXMinMaxValues(self):
#        """ """
#        xmin = None
#        xmax = None
#        for plotdict in self._plot_list:
#            if (plotdict[u'X array']) and (len(plotdict[u'X array']) > 0):                    
#                xminvalue = min(plotdict[u'X array'])
#                xmaxvalue = max(plotdict[u'X array'])
#            else:
#                # x = position in array if x is missing.
#                xminvalue = 0
#                xmaxvalue = len(plotdict[u'Y array']) - 1
#            #
#            if not xmin: xmin = xminvalue
#            if not xmax: xmax = xmaxvalue
#            if xmin > xminvalue: xmin = xminvalue
#            if xmax < xmaxvalue: xmax = xmaxvalue
#        #
#        return xmin, xmax

#    def getYMinMaxValues(self):
#        """ """
#        ymin = None
#        ymax = None
#        for plotdict in self._plot_list:
#            if plotdict[u'Y array']:                    
#                yminvalue = min(plotdict[u'Y array'])
#                ymaxvalue = max(plotdict[u'Y array'])
#            else:
#                yminvalue = 0
#                ymaxvalue = 0
#            #
#            if not ymin: ymin = yminvalue
#            if not ymax: ymax = ymaxvalue
#            if ymin > yminvalue: ymin = yminvalue
#            if ymax < ymaxvalue: ymax = ymaxvalue
#        #
#        return ymin, ymax

#    def getZMinMaxValues(self):
#        """ """
#        zmin = None
#        zmax = None
#        for plotdict in self._plot_list:
#            if plotdict[u'Z array']:                    
#                zminvalue = min(plotdict[u'Z array'])
#                zmaxvalue = max(plotdict[u'Z array'])
#            else:
#                zyminvalue = 0
#                zmaxvalue = 0
#            #
#            if not zmin: zmin = zminvalue
#            if not zmax: zmax = zmaxvalue
#            if zmin > zminvalue: zmin = zminvalue
#            if zmax < zmaxvalue: zmax = zmaxvalue
#        #
#        return zmin, zmax

    def mergeData(self):
        """ Creates a common x array and add zero values for plots with no corresponding x value. """
        # Copy the plot list.
        plotlist = copy.deepcopy(self._plot_list)
        # Create a union list containing all x values.
        x_union = []
        for plotdict in plotlist:
            x_union = list(set(x_union) | set(plotdict[u'X array'])) # List union
        # Sorts the list.                   
        x_union.sort()
        #
        for plotdict in plotlist:
            newyarray = []
            yarrayasdict = dict(zip(plotdict[u'X array'], plotdict[u'Y array']))
            #
            for x in x_union:
                if x in yarrayasdict:
                    newyarray.append(yarrayasdict[x])
                else:
                    newyarray.append(0)        
            #
            plotdict[u'X array'] = x_union
            plotdict[u'Y array'] = newyarray      
        #
        return plotlist



class ChartBase(object):
    """ """
    
    def __init__(self, plot_data, figure):
        """ Abstract base class for charts. """
        #
        super(ChartBase, self).__init__()
        self._data = plot_data
        self._figure = figure
        #
        self._pyplot_used = False # Embedded in Qt or file plotting.
        if not self._figure:         
            self._pyplot_used = True  # Use pyplot for tests.

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
    
    def setData(self, plot_data):
        """ """
        self._data = plot_data
    
    def getData(self, plot_data):
        """ """
        return self._data
    
    def _initPlotting(self):
        """ """
        if self._pyplot_used:         
            # Use pyplot for tests.
            self._figure = pyplot.figure()
        #
#        if self._data.getPlotDataInfo()[u'Title']:
#            self._figure.suptitle(self._data.getPlotDataInfo()[u'Title'], verticalalignment = 'top', size = 'medium')
        # 
        self._markers = [u'o', u's', u'D', u'^', u'<']
        self._colors = ['b', 'r', 'c', 'm', 'k', 'g', 'y']
        self._symbols = ['-', '--', '-.', ':']
        
    def _finalizePlotting(self):
        """ """
        #
        if self._pyplot_used:
            pyplot.tight_layout()
            pyplot.show()
        else:
            self._figure.tight_layout()
        
    def _formatArray(self, data_type, data_array):
        """ """

        
        data_type = u'Number' # TEST:
        
        
        
        if data_type == u'Number':
            float_array = []
            failedconversions_set = set() # Used in error log.
            #
            for value in data_array:
                try:
                    value = float(value)
                    float_array.append(value)
                except:
                    failedconversions_set.add(value)
                    float_array.append(float('nan'))
            #
            if len(failedconversions_set) > 0:
                envmonlib.Logging().warning(u"GraphPlot: These values could not be converted to float: '" + 
                                            u"', '".join(sorted(failedconversions_set)) + u"'")
            #
            return numpy.ma.masked_array(float_array, numpy.isnan(float_array))
        #
        elif data_type == u'Text':
            # Convert to unicode.
            for index, value in enumerate(data_array):
                data_array[index] = unicode(value)
            return data_array
        #
        elif data_type == u'Datetime': 
            return data_array # TODO.
        #
        elif data_type == u'Date': 
            return data_array # TODO.
        #
        elif data_type == u'Time': 
            return data_array # TODO.
        #
        else:
            return data_array 
        
    def plotChart(self):
        """ Abstract. """
        raise NotImplementedError("The abstract method plotChart() is not implement. ")

class LineChart(ChartBase):
    """ """
    def __init__(self, plot_data, figure = None):
        """ """
        super(LineChart, self).__init__(plot_data, figure)

    def plotChart(self, 
                  combined = False, 
                  y_log_scale = False):
        """ """
        #
        self._initPlotting()
        #
        plotlist = self._data.getPlotList()
        x_type = self._data.getPlotDataInfo()[u'X type']
        # 
        if combined:
            subplot = self._figure.add_subplot(111)
            #
            if y_log_scale:
                subplot.set_yscale('log')
            #
            legendname_list = []
            #
            for plotindex, plotdict in enumerate(plotlist):
                #
                x_array = plotdict[u'X array']
                y_array = plotdict[u'Y array']
#                z_array = plotdict[u'Z array']
                if x_array and (x_type == u'Date'):
                    # Convert date strings.
                    x_date_array = []
                    for timestring in plotdict[u'X array']:
                        try:
                            time = datetime.datetime.strptime(timestring, '%Y-%m-%d')
                        except: 
                            time = datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S')
                        x_date_array.append(time)
                    # 
                    subplot.plot_date(x_date_array, plotdict[u'Y array'],
                                      marker = self._markers[plotindex % len(self._markers)], c =  self._colors[plotindex % len(self._colors)])
                    #
                    subplot.xaxis.set_major_locator(mpl_dates.MonthLocator())
                    subplot.xaxis.set_minor_locator(mpl_dates.WeekdayLocator())
                    subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter(u'%Y-%m-%d')) 
                    #
                    self._figure.autofmt_xdate(bottom = 0.2)                     
                else:
                    if (not x_array) or (len(x_array) == 0):
                        x_num_array = list(numpy.arange(len(y_array)))
                    else:
                        x_num_array = x_array[:] # TEST ????
                    #
                    
                    
                    
                    try: 
#                        y_floatarray = []
#                        failedconversions_set = set()
#                        for value in y_array:
#                            try:
##                                value = float(value.replace(u' ', u'').replace(u',', u'.'))
#                                value = float(value)
#                                y_floatarray.append(value)
#                            except:
#                                failedconversions_set.add(value)
#                                y_floatarray.append(float('nan'))
#                        if len(failedconversions_set) > 0:
#                            envmonlib.Logging().warning(u"GraphPlot: These values could not be converted to float: '" + 
#                                                        u"', '".join(sorted(failedconversions_set)) + u"'")
#
#                       
#                       
                        x_masked = self._formatArray(u'Integer', x_num_array)
                        y_masked = self._formatArray(u'Numeric', y_array)
    
    
    
    
    
                        subplot.plot(x_masked, y_masked,
                                     marker = self._markers[plotindex % len(self._markers)])
                        legendname_list.append(plotdict[u'Plot name'])
                    except Exception as e:
                        envmonlib.Logging().warning(u"DEBUG: Plot skipped: %s" % (e.args[0]))
                    
                    
                    
                    
#                    subplot.plot(x_num_array, y_array,
#                                 marker = self._markers[plotindex % len(self._markers)])
            #
            font_properties = mpl_font_manager.FontProperties()
            font_properties.set_size('small')
            leg = subplot.legend(legendname_list,
                                 loc='best', fancybox=True, prop = font_properties)
#            leg = subplot.legend([data[u'Plot name'] for data in plotlist],
#                                 loc='best', fancybox=True, prop = font_properties)
            leg.get_frame().set_alpha(0.5)
            #
            subplot.set_xlabel(self._data.getPlotDataInfo()[u'X label'])
            subplot.set_ylabel(self._data.getPlotDataInfo()[u'Y label'])
        else:
            subplotcount = len(plotlist)
            #
            sharesubplotxaxis = None
            #
            for plotindex, plotdict in enumerate(plotlist):
                x_array = plotdict[u'X array']
                y_array = plotdict[u'Y array']
#                z_array = plotdict[u'Z array']
                #
                subplot = self._figure.add_subplot(subplotcount, 1, plotindex + 1, sharex = sharesubplotxaxis)
                if not sharesubplotxaxis: sharesubplotxaxis = subplot    
                #
                if y_log_scale:
                    subplot.set_yscale('log')
                #
                if x_array and (x_type == u'Date'):
                    # Convert date strings.
                    x_date_array = []
                    for timestring in x_array:
                        try:
                            time = datetime.datetime.strptime(timestring, '%Y-%m-%d')
                        except: 
                            time = datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S')
                        x_date_array.append(time)
                    # 
                    subplot.plot_date(x_date_array, y_array,
                                      marker = self._markers[plotindex % len(self._markers)], c =  self._colors[plotindex % len(self._colors)])
                    #
                    subplot.xaxis.set_major_locator(mpl_dates.MonthLocator())
                    subplot.xaxis.set_minor_locator(mpl_dates.WeekdayLocator())
                    subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter(u'%Y-%m-%d')) 
                    #
                    self._figure.autofmt_xdate(bottom = 0.2)                     
                else:
                    if (not x_array) or (len(x_array) == 0):
                        x_num_array = list(numpy.arange(len(y_array)))
                    else:
                        x_num_array = x_array[:] # TEST ????
                    #   



                    try: 
                        y_floatarray = []
                        failedconversions_set = set()
                        containsvalidvalues = False
                        for value in y_array:
                            try:
#                                value = float(value.replace(u' ', u'').replace(u',', u'.'))
                                value = float(value)
                                y_floatarray.append(value)
                                containsvalidvalues = True
                            except:
                                failedconversions_set.add(value)
                                y_floatarray.append(float('nan'))
                        if len(failedconversions_set) > 0:
                            envmonlib.Logging().warning(u"GraphPlot: These values could not be converted to float: '" + 
                                                        u"', '".join(sorted(failedconversions_set)) + u"'")

                       
                        if containsvalidvalues:
                            x_masked = numpy.ma.masked_array(x_num_array, numpy.isnan(x_num_array))
                            y_masked = numpy.ma.masked_array(y_floatarray, numpy.isnan(y_floatarray))
        
                            subplot.plot(x_masked, y_masked,
                                         marker = self._markers[plotindex % len(self._markers)])
                    #
                    except Exception as e:
                        envmonlib.Logging().warning(u"DEBUG: Plot skipped: %s" % (e.args[0]))
                #
                subplot.set_title(plotdict[u'Plot name'], size = 'medium')
                subplot.set_ylabel(plotdict[u'Y label'])
                #
                if (plotindex + 1) == len(plotlist):
                    # Last subplot.
                    subplot.set_xlabel(self._data.getPlotDataInfo()[u'X label'])
#                    subplot.set_xticklabels(x_array, visible = True)                    
        #
        self._finalizePlotting()


class BarChart(ChartBase):
    """ """
    def __init__(self, plot_data, figure = None):
        """ """
        super(BarChart, self).__init__(plot_data, figure)

    def plotChart(self, 
                  combined = False, 
                  y_log_scale = False,
                  stacked = False):
        """ """
        #
        self._initPlotting()
        #
        plotlist = self._data.getPlotList()
        x_type = self._data.getPlotDataInfo()[u'X type'] 
        # All plots should have the same x axis items. 
        plotlist = self._data.mergeData()        
        #
        if combined:
            # Get axes from first plot.
            x_axis = plotlist[0][u'X array']
            x_axis_positions = numpy.arange(len(x_axis))
            # Set up width and color of bars.
            barwidth = (1.0 / (len(plotlist))) * 0.7
            colourcount = len(plotlist)
            colourmap = pylab.get_cmap('Dark2')
            #
            subplot = self._figure.add_subplot(111)
            #
            accumulatedplots = None
            if y_log_scale:
                subplot.set_yscale('log')
                accumulatedplots = [0.1] * len(x_axis) # For stacked bars. log(0) not defined.
            else:
                accumulatedplots = [0] * len(x_axis) # For stacked bars.
               
            #
            for plotindex, plotdict in enumerate(plotlist):
                #
                x_array = plotdict[u'X array']
                y_array = plotdict[u'Y array']
#                z_array = plotdict[u'Z array']
                #
                if stacked:
                    rect = subplot.bar(x_axis_positions, 
                                       y_array,
                                       0.7,
                                       color=colourmap(1.0 * plotindex / colourcount),
                                       bottom = accumulatedplots)
                    accumulatedplots = [(x + y) for x, y in zip(accumulatedplots, y_array)] # For stacked bars.
                else:                        
                    rect = subplot.bar(x_axis_positions + (plotindex * barwidth),
                                       y_array,
                                       barwidth,
                                       color=colourmap(1.0 * plotindex / colourcount))
            #
###            subplot.set_xticks(x_axis_positions + (barwidth * len(plotlist) * 0.5))
            subplot.set_xticks(x_axis_positions)
            subplot.set_xticklabels(x_array, rotation = 20.0)
            #
            font_properties = mpl_font_manager.FontProperties()
            font_properties.set_size('small')
            leg = subplot.legend([data[u'Plot name'] for data in plotlist], 
                                 loc='best', fancybox=True, prop = font_properties)
            leg.get_frame().set_alpha(0.5)
#            #
#            if self._data.getPlotDataInfo()[u'Title']:
#                subplot.set_title(self._data.getPlotDataInfo()[u'Title'], size = 'small')
            #
            subplot.set_xlabel(self._data.getPlotDataInfo()[u'X label'])
            subplot.set_ylabel(self._data.getPlotDataInfo()[u'Y label'])
        else:
            # Get axes from first plot.
            x_axis = plotlist[0][u'X array']
            x_axis_positions = numpy.arange(len(x_axis))
            # Set up width and color of bars.
            barwidth = 0.7
            colourcount = len(plotlist)
            colourmap = pylab.get_cmap('Dark2')
            #
            subplotcount = len(plotlist)
            #
            share_x_axis = None
            #
            for plotindex, plotdict in enumerate(plotlist):
            
                subplot = self._figure.add_subplot(subplotcount, 1, plotindex + 1, sharex = share_x_axis)    
                if not share_x_axis: share_x_axis = subplot    
                #
                if y_log_scale:
                    subplot.set_yscale('log')
                #
                x_array = plotdict[u'X array']
                y_array = plotdict[u'Y array']
                z_array = plotdict[u'Z array']
                #
                rect = subplot.bar(x_axis_positions, 
                                   plotdict[u'Y array'],
                                   barwidth,
                                   color=colourmap(1.0 * plotindex / colourcount))
                #
                subplot.set_title(plotdict[u'Plot name'], size = 'medium')
                subplot.set_ylabel(plotdict[u'Y label'])
                #
                if (plotindex + 1) == len(plotlist):
                    # Last subplot.
                    subplot.set_xlabel(self._data.getPlotDataInfo()[u'X label'])
                    subplot.set_xticklabels(x_array, rotation=20.0, visible = True)
        #
        self._finalizePlotting()


class ScatterChart(ChartBase):
    """ """
    def __init__(self, plot_data, figure = None):
        """ """
        super(ScatterChart, self).__init__(plot_data, figure)
        
    def plotChart(self, 
                  combined = False, 
                  y_log_scale = False):
        """ """
        self._initPlotting()
        # 
        plotlist = self._data.getPlotList()
        x_type = self._data.getPlotDataInfo()[u'X type']
        #
        if combined:
            subplot = self._figure.add_subplot(111)
            #
            if y_log_scale:
                subplot.set_yscale('log')
            #
            for plotindex, plotdict in enumerate(plotlist):
                #
                x_array = plotdict[u'X array']
                y_array = plotdict[u'Y array']
                z_array = plotdict[u'Z array']
                #
                if z_array:
                    subplot.scatter(x_array, y_array, s = z_array, 
                                    marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                else:
                    subplot.scatter(x_array, y_array, 
                                    marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
            #
            font_properties = mpl_font_manager.FontProperties()
            font_properties.set_size('small')
            leg = subplot.legend([data[u'Plot name'] for data in plotlist],
                                 loc='best', fancybox=True, prop = font_properties)
            leg.get_frame().set_alpha(0.5)
#            #
#            if self._data.getPlotDataInfo()[u'Title']:
#                subplot.set_title(self._data.getPlotDataInfo()[u'Title'])
#            else:
#                subplot.set_title('Scatter, combined') # Default.
            # 
            subplot.set_xlabel(self._data.getPlotDataInfo()[u'X label'])
            subplot.set_ylabel(self._data.getPlotDataInfo()[u'Y label'])
        else:
            subplotcount = len(plotlist)
            #
            share_x_axis = None
            #
            for plotindex, plotdict in enumerate(plotlist):
                subplot = self._figure.add_subplot(subplotcount, 1, plotindex + 1, sharex = share_x_axis)    
                if not share_x_axis: share_x_axis = subplot    
                #
                if y_log_scale:
                    subplot.set_yscale('log')
                #
                x_array = plotdict[u'X array']
                y_array = plotdict[u'Y array']
                z_array = plotdict[u'Z array']
                #
#                x_array = numpy.float64(x_array)
#                y_array = numpy.float64(y_array)
#                if z_array:
#                    z_array = numpy.float64(plotdict[u'Z array'])
                #
                if z_array:
                    subplot.scatter(x_array, y_array, s = z_array, 
                                    marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                else:
                    subplot.scatter(x_array, y_array, 
                                    marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                #
                subplot.set_title(plotdict[u'Plot name'], size = 'medium')
                subplot.set_ylabel(plotdict[u'Y label'])
                #
                if (plotindex + 1) == len(plotlist):
                    # Last subplot.
                    subplot.set_xlabel(self._data.getPlotDataInfo()[u'X label'])
                    subplot.set_xticklabels(plotdict[u'X array'], rotation=20.0, visible = True)
        #
        self._finalizePlotting()

                
class PieChart(ChartBase):
    """ """
    def __init__(self, plot_data, figure = None):
        """ """
        super(PieChart, self).__init__(plot_data, figure)
        
    def plotChart(self, 
                  combined = False, # Not used. 
                  y_log_scale = False): # Not used.
        """ """
        #
        self._initPlotting()
        #
        plotlist = self._data.getPlotList()
        #
        for plotindex, plotdict in enumerate(plotlist):
            subplot = self._figure.add_subplot(len(plotlist), 1, plotindex + 1)
            #
            if plotdict[u'X array']:
                # Remove invalid positions in both arrays.
                x_array = plotdict[u'X array']
                y_array = plotdict[u'Y array']
                y_cleaned = []
                x_labels = []
                for index, item in enumerate(y_array):
                    try:
                        if not numpy.isnan(item):
                            x_labels.append(unicode(x_array[index])) # Labels should be text.
                            y_cleaned.append(y_array[index])
                    except:
                        pass
                subplot.pie(y_cleaned, labels = x_labels)
            else:
                # Remove invalid positions in y array.
                y_array = plotdict[u'Y array']
                y_cleaned = []
                for index, item in enumerate(y_array):
                    try:
                        if not numpy.isnan(item):
                            y_cleaned.append(y_array[index])
                    except:
                        pass
                subplot.pie(y_cleaned)
            #
            subplot.axis(u'equal') # A circle should be circular.
            #
            if plotdict[u'Plot name']:
                subplot.set_title(plotdict[u'Plot name'], size = 'medium')
        #
        self._finalizePlotting()
        
#
# Test.
#
def graphplotter_test():
    """ """
    print("Graph plotter test...")
    #

    plotdata_0 = GraphPlotData(
                        title = u"One variable data object", 
                        x_label = u'X (one variable)',
                        y_label = u'Y (one variable)')

    plotdata_0.addPlot(plot_name = u"1 plot", 
                        y_array = [7.0, float('nan'), 88.0, 900.0, 9000.0], 
                        y_label = u'Y first')
    plotdata_0.addPlot(plot_name = u"2 plot", 
                        y_array = [2006.0, 2006.0, 2006.0, 'nan', 2006.0], 
                        y_label = u'Y first')
    plotdata_0.addPlot(plot_name = u"3 plot", 
                        y_array = [2006.0, 'NaN', 2006.0, 2006.0, 2006.0], 
                        y_label = u'Y first')
    plotdata_0.addPlot(plot_name = u"4 plot", 
                        y_array = [2006.0, 2006.0, None, 2006.0, 2006.0], 
                        y_label = u'Y first')

#    graph = LineChart(plotdata_0)
#    graph.plotChart(combined = False, y_log_scale = True)
#    graph.plotChart(combined = True, y_log_scale = True)
    
#    graph = BarChart(plotdata_0)
#    graph.plotChart(combined = False, y_log_scale = True)
#    graph.plotChart(combined = True, y_log_scale = True)
    
    graph = ScatterChart(plotdata_0)
    graph.plotChart(combined = False, y_log_scale = True)
    graph.plotChart(combined = True, y_log_scale = True)
    
#    graph = PieChart(plotdata_0)
#    graph.plotChart(combined = False, y_log_scale = False)
#    graph.plotChart(combined = False, y_log_scale = True)
    

    return

    
    plotdata_1 = GraphPlotData(
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
    plotdata_2 = GraphPlotData(
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
    plotdata_3 = GraphPlotData(
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
    plotdata_4 = GraphPlotData(
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
    plotdata_5 = GraphPlotData(
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
    graph = ScatterChart(plotdata_2)
    graph.plotChart(combined = True, y_log_scale = False)
    graph.plotChart(combined = False, y_log_scale = True)
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
    graph = PieChart(plotdata_2)
    graph.plotChart(combined = False, y_log_scale = False)
    #
    graph = PieChart(plotdata_4)
    graph.plotChart(combined = False, y_log_scale = False)
    #
    graph = LineChart(plotdata_5)
    graph.plotChart(combined = True, y_log_scale = True)
    graph.plotChart(combined = False, y_log_scale = True)

                
if __name__ == "__main__":
    graphplotter_test()

