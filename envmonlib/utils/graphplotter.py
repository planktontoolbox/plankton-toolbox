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

import numpy.ma
import datetime
import copy
import matplotlib as mpl
import matplotlib.dates as mpl_dates
import matplotlib.font_manager as mpl_font_manager
# import matplotlib.figure as mpl_figure
import pylab # Usedfor color maps.
import matplotlib.pyplot as pyplot # Used when not embedded plotting.
import mpl_toolkits.basemap as basemap

import envmonlib

class GraphPlotData(object):
    """ Class containing data needed when plotting. 
        Valid data array types: 'text', 'integer', 'float', 'date', 'datetime'. 
    """
    
    def __init__(self,
                 title = u'', 
                 x_label = u'',
                 x_type = u'integer', # Alternatives: text, integer, float, date, datetime.
                 x_format = u'', # Used for the datetime type. 
                 y_label = u'',
                 y_type = u'', # Alternatives: integer, float.
                 y_format = u'', # Used for the datetime type. 
                 z_label = u'',
                 z_type = u'', # Alternatives: integer, float.
                 z_format = u''): # Used for the datetime type. 
        """ """
        super(GraphPlotData, self).__init__()
        #
        self._plot_list = []
        self._plotdata_info = {}
        #
        self._plotdata_info[u'title'] = title
        #
        self._plotdata_info[u'x_label'] = x_label
        self._plotdata_info[u'x_type'] = x_type
        self._plotdata_info[u'x_format'] = x_format
        #
        self._plotdata_info[u'y_label'] = y_label
        self._plotdata_info[u'y_type'] = y_type
        self._plotdata_info[u'y_format'] = y_format
        #
        self._plotdata_info[u'z_label'] = z_label
        self._plotdata_info[u'z_type'] = z_type
        self._plotdata_info[u'z_format'] = z_format
        
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
            envmonlib.Logging().warning(u"GraphPlotData.addPlot() must contain at least an y-array. Plot not added.")
            raise UserWarning(u"GraphPlotData.addPlot() must contain at least an y-array. Plot not added.")
            return
        #
        plotdict = {}
        plotdict[u'plot_name'] = plot_name
        plotdict[u'x_label'] = x_label
        plotdict[u'x_array'] = x_array
        #
        plotdict[u'y_label'] = y_label
        plotdict[u'y_array'] = y_array
        #
        plotdict[u'z_label'] = z_label
        plotdict[u'z_array'] = z_array
        #
        self._plot_list.append(plotdict)
               
    def clear(self):
        """ """
        self._plot_list = []
        
    def removePlotByIndex(self, data_index = None):
        """ """
        if data_index: 
            if len(data_index) > data_index: 
                del self._plot_list[data_index]
        
    def getPlotDataInfo(self):
        """ """
        return self._plotdata_info
    
    def setPlotDataInfo(self, info):
        """ """
        self._plotdata_info = info
    
    def getPlotList(self):
        """ """
        return self._plot_list    

    def setPlotList(self, plotlist):
        """ """
        self._plot_list = plotlist

    def mergeData(self):
        """ Creates a common x array and add zero values for plots with no corresponding x value. """
        # Copy the plot list.
        newplotlist = copy.deepcopy(self._plot_list)
        # Create a unique list containing all x values.
        x_unique = []
        for plotdict in newplotlist:
            #
            x_array = plotdict[u'x_array']
            if (not x_array) or (len(x_array) == 0):
                # Generate x-array if it is missing.
                plotdict[u'x_array'] = list(numpy.arange(len(plotdict[u'y_array'])))                        
            #
            for item in plotdict[u'x_array']:
                if not item in x_unique:
                    x_unique.append(item)
        # Sort the list.                   
        x_unique.sort()
        #
        for plotdict in newplotlist:
            y_newarray = []
            z_newarray = []
            y_arrayasdict = dict(zip(plotdict[u'x_array'], plotdict[u'y_array']))
            if plotdict[u'z_array']:
                z_arrayasdict = dict(zip(plotdict[u'x_array'], plotdict[u'z_array']))
            #
            for x in x_unique:
                if x in y_arrayasdict:
                    y_newarray.append(y_arrayasdict[x])
                else:
                    y_newarray.append(0)
                #
                if plotdict[u'z_array']:           
                    if x in z_arrayasdict:
                        z_newarray.append(z_arrayasdict[x])
                    else:
                        z_newarray.append(0)        
            #
            plotdict[u'x_array'] = x_unique
            plotdict[u'y_array'] = y_newarray
            if plotdict[u'z_array']:      
                plotdict[u'z_array'] = z_newarray      
        #
        return newplotlist

    def getMinMaxValues(self, 
                        array_name = u'x_array'):
        """ """
        result_min = None
        result_max = None
        for plotdict in self._plot_list:
            if (plotdict[array_name]) and (len(plotdict[array_name]) > 0):                    
                minvalue = min(plotdict[array_name])
                maxvalue = max(plotdict[array_name])
            else:
                # x = position in array if the x-array is missing.
                minvalue = 0
                maxvalue = len(plotdict[array_name]) - 1
            #
            if not min: result_min = minvalue
            if not max: result_max = maxvalue
            if result_min > minvalue: result_min = minvalue
            if result_max < maxvalue: result_max = maxvalue
        #
        return result_min, result_max



class ChartBase(object):
    """ Abstract base class for charts. """
    
    def __init__(self, plot_data = None, figure = None):
        """ """
        super(ChartBase, self).__init__()
        #
        if plot_data:
            if not isinstance(plot_data, GraphPlotData):
                envmonlib.Logging().error(u"Chart data object is not an instance of the class GraphPlotData. Plotting terminated.")
                raise UserWarning("Chart data object is not an instance of the class GraphPlotData. Plotting terminated.")
            
        self._data = plot_data
        self._figure = figure
        #
        if self._figure:         
            self._pyplot_used = False # Embedded (in Qt, Tkinter, etc.) or used for file plotting.
        else:
            self._pyplot_used = True  # Use pyplot for tests and for 'manual' file creation.

#        self._settings = {}
        self.default_settings()

    def default_settings(self):
        """ """
        self._markers = [u'o', u's', u'D', u'^', u'<']
        self._colors = [u'b', u'r', u'c', u'm', u'k', u'g', u'y']
        self._symbols = [u'-', u'--', u'-.', u':']
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
        if not isinstance(plot_data, GraphPlotData):
            envmonlib.Logging().error(u"Chart data object is not an instance of the class GraphPlotData. Plotting terminated.")
            raise UserWarning("Chart data object is not an instance of the class GraphPlotData. Plotting terminated.")
        #
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
#        self._figure.subplots_adjust(hspace=1.0)
        self._figure.subplots_adjust(hspace=0.5)
        self._figure.subplots_adjust(top = 0.90, bottom = 0.14)
        #
        if self._data.getPlotDataInfo()[u'title']:
            self._figure.suptitle(self._data.getPlotDataInfo()[u'title'], verticalalignment = 'top', size = 'medium')
        
    def _addLegend(self, subplot):
        """ """
        font_properties = mpl_font_manager.FontProperties()
        font_properties.set_size('small')
        leg = subplot.legend(loc='best', fancybox=True, prop = font_properties)
        if leg:
            leg.get_frame().set_alpha(0.5)
            leg.draggable(state = True)

    def _finalizePlotting(self):
        """ """
        if self._pyplot_used:
#             pyplot.tight_layout()
            pyplot.show()
        else:
            self._figure.subplots_adjust(hspace=1.0)
            self._figure.subplots_adjust(top = 0.90, bottom = 0.14)
#             self._figure.tight_layout()
        
    def _formatArray(self, data_type, data_array):
        """ """
        #
        if data_type == u'text':
            # Convert to a sequence of integers.
            integer_array = []
            for index, value in enumerate(data_array):
                integer_array.append(index)
            return integer_array
        #
        if data_type == u'integer':
            integer_array = []
            failedconversions_set = set() # Used in error log.
            #
            for value in data_array:
                try:
                    value = int(value)
                    integer_array.append(value)
                except:
                    failedconversions_set.add(unicode(value))
                    integer_array.append(int('nan'))
            #
            if len(failedconversions_set) > 0:
                envmonlib.Logging().warning(u"GraphPlotter.ChartBase: These values could not be converted to integer: '" + 
                                            u"', '".join(sorted(failedconversions_set)) + u"'")
            # Masked arrays are needed for proper handling of missing values when plotting.
            return numpy.ma.masked_array(integer_array, numpy.isnan(integer_array))
        #
        elif data_type in [u'', u'float']: # Test with float if type is not specified.
            float_array = []
            failedconversions_set = set() # Used in error log.
            #
            for value in data_array:
                try:
                    value = float(value)
                    float_array.append(value)
                except:
                    failedconversions_set.add(unicode(value))
                    float_array.append(float('nan'))
            #
            if len(failedconversions_set) > 0:
                envmonlib.Logging().warning(u"GraphPlotter.ChartBase: These values could not be converted to float: '" + 
                                            u"', '".join(sorted(failedconversions_set)) + u"'")
            # Masked arrays are needed for proper handling of missing values when plotting.
            return numpy.ma.masked_array(float_array, numpy.isnan(float_array))
        #
        elif data_type in [u'date', u'datetime']: 
            # Convert date strings. 
            # Automatic detection of '2000-01-01' and '2000-01-01 12:00:00' formats.
            datetime_array = []
            failedconversions_set = set() # Used in error log.
            for timestring in data_array:
                try:
                    try:
                        time = datetime.datetime.strptime(timestring, '%Y-%m-%d')
                    except: 
                        time = datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S')
                    datetime_array.append(time)
                except:
                    failedconversions_set.add(unicode(timestring))
            #
            if len(failedconversions_set) > 0:
                envmonlib.Logging().warning(u"GraphPlotter.ChartBase: These values could not be converted to date or datetime: '" + 
                                            u"', '".join(sorted(failedconversions_set)) + u"'")
            return datetime_array
        
    def plotChart(self, **kwargs):
        """ Abstract. """
        raise NotImplementedError("The abstract method ChartBase.plotChart() is not implement. ")

class LineChart(ChartBase):
    """ Line chart.
        - Plots x- and y-arrays. Z-array not used.
        - If only the  y-array is available the x-array will be generated.
        - Valid x-types: text, integer, float, date or datetime.
        - Valid y-types: integer or float.
        
    """
    def __init__(self, plot_data = None, figure = None):
        """ """
        super(LineChart, self).__init__(plot_data, figure)

    def plotChart(self, 
                  combined = False, 
                  stacked = False,
                  x_log_scale = False, 
                  y_log_scale = False,
                  **kwargs):
        """ """
        try: 
            x_type = self._data.getPlotDataInfo()[u'x_type']
            y_type = self._data.getPlotDataInfo()[u'y_type']
            # Line charts needs text (text, integer, data or datetime) for the x-axis and 
            # values (integer or float) for the y-axis.
            if not x_type in [u'', u'text', u'integer', u'date', u'datetime']:
                envmonlib.Logging().warning(u"GraphPlotter.LineChart: Plot skipped, X-axis type not valid: " + x_type)
                raise UserWarning(u"GraphPlotter.LineChart: Plot skipped, X-axis type not valid: " + x_type)
            if not y_type in [u'', u'integer', u'float']:
                envmonlib.Logging().warning(u"GraphPlotter.LineChart: Plot skipped, Y-axis type not valid: " + y_type)
                raise UserWarning(u"GraphPlotter.LineChart: Plot skipped, Y-axis type not valid: " + y_type)
            #
            self._initPlotting()
            plotlist = self._data.getPlotList()
            
            if (x_type == u'text') or stacked:
                # All plots should have the same x axis items. 
                plotlist = self._data.mergeData()        
            # 
            if combined:
                # All data in one plot.
                subplot = self._figure.add_subplot(111)
                #
                y_array_acc = 0 # Accumulated values are needed when stacking.  
                #
                if x_log_scale and (x_type in [u'', u'integer', u'float']):
                    subplot.set_xscale('log')
                if y_log_scale and (y_type in [u'', u'integer', u'float']):
                    subplot.set_yscale('log')
                    y_array_acc = 0.1 # Log 0 not defined. 
                #
                for plotindex, plotdict in enumerate(plotlist):
                    #
                    x_array = plotdict[u'x_array']
                    y_array = plotdict[u'y_array']
                    #
                    if (not x_array) or (len(x_array) == 0):
                        # Generate x-array.
                        x_type = u'integer'
                        x_array = list(numpy.arange(len(y_array)))                        
                    #
                    if x_type == u'text':
                        x_integer_array = self._formatArray(x_type, x_array)
                        y_masked_array = self._formatArray(y_type, y_array)
                        #
                        subplot.set_xticklabels(x_array)
                        #
                        if stacked:
                            old_y_array_acc = y_array_acc
                            y_array_acc = y_array_acc + y_masked_array
                            subplot.plot(x_integer_array, 
                                         y_array_acc,
                                         label = plotdict[u'plot_name'],
                                         marker = self._markers[plotindex % len(self._markers)],
                                         color = self._colors[plotindex % len(self._colors)])
                            subplot.fill_between(x_integer_array,
                                                old_y_array_acc,
                                                y_array_acc,
                                                color = self._colors[plotindex % len(self._colors)],
                                                alpha = 0.5)                     
                        else:
                            subplot.plot(x_integer_array, 
                                         y_masked_array,
                                         label = plotdict[u'plot_name'],
                                         marker = self._markers[plotindex % len(self._markers)],
                                         color = self._colors[plotindex % len(self._colors)])
                    #
                    elif x_type == u'integer':
                        x_masked_array = self._formatArray(u'integer', x_array)
                        y_masked_array = self._formatArray(y_type, y_array)
                        #
                        if stacked:
                            old_y_array_acc = y_array_acc
                            y_array_acc = y_array_acc + y_masked_array
                            subplot.plot(x_masked_array, 
                                         y_array_acc,
                                         label = plotdict[u'plot_name'],
                                         marker = self._markers[plotindex % len(self._markers)],
                                         color = self._colors[plotindex % len(self._colors)])
                            subplot.fill_between(x_masked_array,
                                                old_y_array_acc,
                                                y_array_acc,
                                                color = self._colors[plotindex % len(self._colors)],
                                                alpha = 0.5)                     
                        else:
                            subplot.plot(x_masked_array, 
                                         y_masked_array,
                                         label = plotdict[u'plot_name'],
                                         marker = self._markers[plotindex % len(self._markers)])
                    #    
                    elif x_type == u'float':
                        x_masked_array = self._formatArray(u'float', x_array)
                        y_masked_array = self._formatArray(y_type, y_array)
                        #
                        if stacked:
                            old_y_array_acc = y_array_acc
                            y_array_acc = y_array_acc + y_masked_array
                            subplot.plot(x_masked_array, 
                                         y_array_acc,
                                         label = plotdict[u'plot_name'],
                                         marker = self._markers[plotindex % len(self._markers)],
                                         color = self._colors[plotindex % len(self._colors)])
                            subplot.fill_between(x_masked_array,
                                                old_y_array_acc,
                                                y_array_acc,
                                                color = self._colors[plotindex % len(self._colors)],
                                                alpha = 0.5)                     
                        else:
                            subplot.plot(x_masked_array, 
                                         y_masked_array,
                                         label = plotdict[u'plot_name'],
                                         marker = self._markers[plotindex % len(self._markers)])
                    #    
                    elif x_type in [u'date', u'datetime']:
                        """ """
                        x_datetime_array = self._formatArray(x_type, x_array)
                        y_masked_array = self._formatArray(y_type, y_array)
                        #
                        # 
                        if stacked:
                            old_y_array_acc = y_array_acc
                            y_array_acc = y_array_acc + y_masked_array
                            subplot.plot_date(x_datetime_array, 
                                              y_array_acc,
                                              label = plotdict[u'plot_name'],
                                              marker = self._markers[plotindex % len(self._markers)], 
#                                               c = self._colors[plotindex % len(self._colors)],
                                              color = self._colors[plotindex % len(self._colors)])
                            subplot.fill_between(x_datetime_array,
                                                old_y_array_acc,
                                                y_array_acc,
                                                color = self._colors[plotindex % len(self._colors)],
                                                alpha = 0.5)                     
                        else:
                            subplot.plot_date(x_datetime_array, 
                                              y_masked_array,
                                              label = plotdict[u'plot_name'],
                                              marker = self._markers[plotindex % len(self._markers)], 
#                                               c = self._colors[plotindex % len(self._colors)],
                                              color = self._colors[plotindex % len(self._colors)])
                        #
                        subplot.xaxis.set_major_locator(mpl_dates.MonthLocator())
                        subplot.xaxis.set_minor_locator(mpl_dates.WeekdayLocator())
                        subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter(u'%Y-%m-%d')) 
                        self._figure.autofmt_xdate(bottom = 0.2)   
                    #                      
                    else:
                        envmonlib.Logging().warning(u"GraphPlotter.LineChart: Not a valid type for the x axis: " + x_type)
                        return
                # Legend.
                self._addLegend(subplot)                
                # Labels. Only one for combined plotting.
                subplot.set_xlabel(self._data.getPlotDataInfo()[u'x_label'], size = 'medium')
                subplot.set_ylabel(self._data.getPlotDataInfo()[u'y_label'], size = 'medium')
            else:
                # Divided into separate plots with a common x axis.
                subplotcount = len(plotlist)
                sharesubplotxaxis = None
                #
                for plotindex, plotdict in enumerate(plotlist):
                    x_array = plotdict[u'x_array']
                    y_array = plotdict[u'y_array']
                    #
                    subplot = self._figure.add_subplot(subplotcount, 1, plotindex + 1, sharex = sharesubplotxaxis)
                    if not sharesubplotxaxis: 
                        sharesubplotxaxis = subplot    
                    #
                    if x_log_scale and (x_type in [u'', u'integer', u'float']):
                        subplot.set_xscale('log')
                    if y_log_scale and (y_type in [u'', u'integer', u'float']):
                        subplot.set_yscale('log')
                    #
                    if (not x_array) or (len(x_array) == 0):
                        # Generate x-array.
                        x_array = list(numpy.arange(len(y_array)))                        
                    #
                    if x_type == u'text':
                        """ """
                        x_integer_array = self._formatArray(u'text', x_array)
                        y_masked_array = self._formatArray(y_type, y_array)
                        #
                        subplot.set_xticklabels(x_array)
                        #
                        subplot.plot(x_integer_array, 
                                     y_masked_array,
                                     label = plotdict[u'plot_name'],
                                     marker = self._markers[plotindex % len(self._markers)],
                                     color = self._colors[plotindex % len(self._colors)])   
                    #    
                    elif x_type == u'integer':
                        x_masked_array = self._formatArray(u'integer', x_array)
                        y_masked_array = self._formatArray(y_type, y_array)
                        #
                        subplot.plot(x_masked_array, 
                                     y_masked_array,
                                     label = plotdict[u'plot_name'],
                                     marker = self._markers[plotindex % len(self._markers)])
                    #    
                    elif x_type == u'float':
                        x_masked_array = self._formatArray(u'float', x_array)
                        y_masked_array = self._formatArray(y_type, y_array)
                        #
                        subplot.plot(x_masked_array, 
                                     y_masked_array,
                                     label = plotdict[u'plot_name'],
                                     marker = self._markers[plotindex % len(self._markers)])
                    #    
                    elif x_type in [u'date', u'datetime']:
                        """ """
                        x_datetime_array = self._formatArray(x_type, x_array)
                        y_masked_array = self._formatArray(y_type, y_array)
                        #
                        # 
                        subplot.plot_date(x_datetime_array, 
                                          y_masked_array,
                                          label = plotdict[u'plot_name'],
                                          marker = self._markers[plotindex % len(self._markers)], 
                                          c = self._colors[plotindex % len(self._colors)])
                        #
                        subplot.xaxis.set_major_locator(mpl_dates.MonthLocator())
                        subplot.xaxis.set_minor_locator(mpl_dates.WeekdayLocator())
                        subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter(u'%Y-%m-%d')) 
                        #
                        self._figure.autofmt_xdate(bottom = 0.2)   
                    #                      
                    else:
                        envmonlib.Logging().warning(u"GraphPlotter.LineChart: Not a valid type for the x axis. Type " + x_type)
                    #
                    subplot.set_title(plotdict[u'plot_name'], size = 'medium')
                    subplot.set_ylabel(plotdict[u'y_label'])
                    #
                    if (plotindex + 1) == len(plotlist):
                        # Last subplot.
                        subplot.set_xlabel(self._data.getPlotDataInfo()[u'x_label'])
#                        subplot.set_xticklabels(x_array, visible = True)
            #
            self._finalizePlotting()
        #
        except Exception as e:
            envmonlib.Logging().warning(u"GraphPlotter.LineChart: Plot skipped: %s" % (e.args[0]))
            raise


class BarChart(ChartBase):
    """ """
    def __init__(self, plot_data = None, figure = None):
        """ """
        super(BarChart, self).__init__(plot_data, figure)

    def plotChart(self, 
                  combined = False, 
                  stacked = False,
                  y_log_scale = False,
                  **kwargs):
        """ """
        #
        try:
            x_type = self._data.getPlotDataInfo()[u'x_type']
            y_type = self._data.getPlotDataInfo()[u'y_type']
            # Bar charts needs text (text, integer, date or datetime) for the x-axis and 
            # values (integer or float) for the y-axis.
            if not x_type in [u'text', u'integer', u'date', u'datetime']:
                envmonlib.Logging().warning(u"GraphPlotter.BarChart: Plot skipped, X-axis type not valid: " + x_type)
                raise UserWarning(u"GraphPlotter.BarChart: Plot skipped, X-axis type not valid: " + x_type)
            if not y_type in [u'integer', u'float']:
                envmonlib.Logging().warning(u"GraphPlotter.BarChart: Plot skipped, Y-axis type not valid: " + y_type)
                raise UserWarning(u"GraphPlotter.BarChart: Plot skipped, Y-axis type not valid: " + y_type)
            #
            self._initPlotting()
            #
            plotlist = self._data.getPlotList()
#             # Bar plots should have values in the x array.
#             if not plotlist[0][u'x_array']:
#                 envmonlib.Logging().warning(u"GraphPlotter.BarChart: Plot skipped, X values are missing.")
#                 return
            # 
            # All plots should have the same x axis items. 
            plotlist = self._data.mergeData()        
            #
            if combined:
                # Get axes from first plot.
                x_axis = plotlist[0][u'x_array']
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
                    x_array = plotdict[u'x_array']
                    y_array = plotdict[u'y_array']
#                     z_array = plotdict[u'z_array']
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
                leg = subplot.legend([data[u'plot_name'] for data in plotlist], 
                                     loc='best', fancybox=True, prop = font_properties)
                leg.get_frame().set_alpha(0.5)
    #            #
    #            if self._data.getPlotDataInfo()[u'title']:
    #                subplot.set_title(self._data.getPlotDataInfo()[u'title'], size = 'small')
                #
                subplot.set_xlabel(self._data.getPlotDataInfo()[u'x_label'])
                subplot.set_ylabel(self._data.getPlotDataInfo()[u'y_label'])
            else:
                # Get axes from first plot.
                x_axis = plotlist[0][u'x_array']
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
                    x_array = plotdict[u'x_array']
                    y_array = plotdict[u'y_array']
                    z_array = plotdict[u'z_array']
                    #
                    rect = subplot.bar(x_axis_positions, 
                                       plotdict[u'y_array'],
                                       barwidth,
                                       color=colourmap(1.0 * plotindex / colourcount))
                    #
                    subplot.set_title(plotdict[u'plot_name'], size = 'medium')
                    subplot.set_ylabel(plotdict[u'y_label'])
                    #
                    if (plotindex + 1) == len(plotlist):
                        # Last subplot.
                        subplot.set_xlabel(self._data.getPlotDataInfo()[u'x_label'])
                        subplot.set_xticklabels(x_array, rotation=20.0, visible = True)
            #
            self._finalizePlotting()
        #
        except Exception as e:
            envmonlib.Logging().warning(u"GraphPlotter.BarChart: Plot skipped: %s" % (e.args[0]))
            raise


class ScatterChart(ChartBase):
    """ """
    def __init__(self, plot_data = None, figure = None):
        """ """
        super(ScatterChart, self).__init__(plot_data, figure)
        
    def plotChart(self, 
                  combined = False, 
                  x_log_scale = False, 
                  y_log_scale = False, 
                  **kwargs):
        """ """
        #
        try: 
            x_type = self._data.getPlotDataInfo()[u'x_type']
            y_type = self._data.getPlotDataInfo()[u'y_type']
            z_type = self._data.getPlotDataInfo()[u'z_type']
            # Scatter charts needs text (text, integer, date or datetime) for the x-axis and 
            # values (integer or float) for the y-axis.
            if not x_type in [u'text', u'integer', u'date', u'datetime']:
                envmonlib.Logging().warning(u"GraphPlotter.PieChart: Plot skipped, X-axis type not valid: " + x_type)
                raise UserWarning(u"GraphPlotter.PieChart: Plot skipped, X-axis type not valid: " + x_type)
            if not y_type in [u'integer', u'float']:
                envmonlib.Logging().warning(u"GraphPlotter.PieChart: Plot skipped, Y-axis type not valid: " + y_type)
                raise UserWarning(u"GraphPlotter.PieChart: Plot skipped, Y-axis type not valid: " + y_type)
            if not z_type in [u'', u'integer', u'float']:
                envmonlib.Logging().warning(u"GraphPlotter.PieChart: Plot skipped, Z-axis type not valid: " + z_type)
                raise UserWarning(u"GraphPlotter.PieChart: Plot skipped, Z-axis type not valid: " + z_type)
            # 
            self._initPlotting()
            # 
            plotlist = self._data.getPlotList()
            # Scatter plots should have values in the x array.
            if not plotlist[0][u'x_array']:
                envmonlib.Logging().warning(u"GraphPlotter.ScatterChart: Plot skipped, X values are missing.")
                return
            #
            if combined:
                subplot = self._figure.add_subplot(111)
                #
                if x_log_scale and (x_type in [u'', u'integer', u'float']):
                    subplot.set_xscale('log')
                if y_log_scale and (y_type in [u'', u'integer', u'float']):
                    subplot.set_yscale('log')
                #
                for plotindex, plotdict in enumerate(plotlist):
                    #
                    x_array = plotdict[u'x_array']
                    y_array = plotdict[u'y_array']
                    z_array = plotdict[u'z_array']
                    #

                    if x_type == u'text':
                        """ """
                        x_integer_array = self._formatArray(x_type, x_array)
                        y_masked_array = self._formatArray(y_type, y_array)
                        #
                        subplot.set_xticklabels(x_array)
                        #
                        if z_array:
                            subplot.scatter(x_integer_array, y_masked_array, s = z_array, 
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        else:
                            subplot.scatter(x_integer_array, y_array, 
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                    #     
                    elif x_type in [u'integer', u'float']:
                        """ """
                        x_masked_array = self._formatArray(x_type, x_array)
                        y_masked_array = self._formatArray(y_type, y_array)
                        #
                        if z_array:
                            subplot.scatter(x_masked_array, y_masked_array, s = z_array, 
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        else:
                            subplot.scatter(x_masked_array, y_masked_array, 
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                    #     
                    elif x_type in [u'date', u'datetime']:
                        """ """
                        x_datetime_array = self._formatArray(x_type, x_array)
                        y_masked_array = self._formatArray(y_type, y_array)
                        #
                        if z_array:
                            subplot.scatter(x_datetime_array, y_masked_array, s = z_array, 
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        else:
                            subplot.scatter(x_datetime_array, y_masked_array, 
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        #
                        subplot.xaxis.set_major_locator(mpl_dates.MonthLocator())
                        subplot.xaxis.set_minor_locator(mpl_dates.WeekdayLocator())
                        subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter(u'%Y-%m-%d')) 
                        self._figure.autofmt_xdate(bottom = 0.2)   

                # Legend.
                self._addLegend(subplot)                
                # 
                subplot.set_xlabel(self._data.getPlotDataInfo()[u'x_label'])
                subplot.set_ylabel(self._data.getPlotDataInfo()[u'y_label'])
            else:



                subplotcount = len(plotlist)
                #
                share_x_axis = None
                #
                for plotindex, plotdict in enumerate(plotlist):
                    subplot = self._figure.add_subplot(subplotcount, 1, plotindex + 1, sharex = share_x_axis)    
                    if not share_x_axis: share_x_axis = subplot    
                    #
                    if x_log_scale and (x_type in [u'', u'integer', u'float']):
                        subplot.set_xscale('log')
                    if y_log_scale and (y_type in [u'', u'integer', u'float']):
                        subplot.set_yscale('log')
                    #
                    x_array = plotdict[u'x_array']
                    y_array = plotdict[u'y_array']
                    z_array = plotdict[u'z_array']
                    #
    #                x_array = numpy.float64(x_array)
    #                y_array = numpy.float64(y_array)
    #                if z_array:
    #                    z_array = numpy.float64(plotdict[u'z_array'])
                    #
                    if x_type == u'text':
                        """ """
                        x_integer_array = self._formatArray(x_type, x_array)
                        y_masked_array = self._formatArray(y_type, y_array)
                        #
                        subplot.set_xticklabels(x_array)
                        #
                        if z_array:
                            subplot.scatter(x_integer_array, y_masked_array, s = z_array, 
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        else:
                            subplot.scatter(x_integer_array, y_array, 
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                         
                    elif x_type in [u'integer', u'float']:
                        """ """
                        if z_array:
                            subplot.scatter(x_array, y_array, s = z_array, 
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        else:
                            subplot.scatter(x_array, y_array, 
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                         
                    elif x_type in [u'date', u'datetime']:
                        """ """
                        x_datetime_array = self._formatArray(x_type, x_array)
                        y_masked_array = self._formatArray(y_type, y_array)
                        #
                        if z_array:
                            subplot.scatter(x_datetime_array, y_masked_array, s = z_array, 
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        else:
                            subplot.scatter(x_datetime_array, y_masked_array, 
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        #
                        subplot.xaxis.set_major_locator(mpl_dates.MonthLocator())
                        subplot.xaxis.set_minor_locator(mpl_dates.WeekdayLocator())
                        subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter(u'%Y-%m-%d')) 
                        self._figure.autofmt_xdate(bottom = 0.2)   

                    #
                    subplot.set_title(plotdict[u'plot_name'], size = 'medium')
                    subplot.set_ylabel(plotdict[u'y_label'])
                    #
                    if (plotindex + 1) == len(plotlist):
                        # Last subplot.
                        subplot.set_xlabel(self._data.getPlotDataInfo()[u'x_label'])
                        subplot.set_xticklabels(plotdict[u'x_array'], rotation=20.0, visible = True)
            #
            self._finalizePlotting()
        #
        except Exception as e:
            envmonlib.Logging().warning(u"GraphPlotter.ScatterChart: Plot skipped: %s" % (e.args[0]))
            raise

                
class PieChart(ChartBase):
    """ """
    def __init__(self, plot_data = None, figure = None):
        """ """
        super(PieChart, self).__init__(plot_data, figure)
        
    def plotChart(self, 
                  combined = False, # Not used.
                  x_log_scale = False, # Not used.
                  y_log_scale = False, # Not used. 
                  stacked = None): # Not used.
        """ """
        #
        try:            
            x_type = self._data.getPlotDataInfo()[u'x_type']
            y_type = self._data.getPlotDataInfo()[u'y_type']
            # Pie charts needs text (text, integer or datetime) for the x-axis and 
            # values (integer or float) for the y-axis.
            if not x_type in [u'text', u'integer', u'date', u'datetime']:
                envmonlib.Logging().warning(u"GraphPlotter.PieChart: Plot skipped, X-axis type not valid: " + x_type)
                raise UserWarning(u"GraphPlotter.PieChart: Plot skipped, X-axis type not valid: " + x_type)
            if not y_type in [u'integer', u'float']:
                envmonlib.Logging().warning(u"GraphPlotter.PieChart: Plot skipped, Y-axis type not valid: " + y_type)
                raise UserWarning(u"GraphPlotter.PieChart: Plot skipped, Y-axis type not valid: " + y_type)
            # 
            self._initPlotting()
            #
            plotlist = self._data.getPlotList()
            #
            for plotindex, plotdict in enumerate(plotlist):
                subplot = self._figure.add_subplot(len(plotlist), 1, plotindex + 1)
                #
                if plotdict[u'x_array']:
                    # Remove invalid positions in both arrays.
                    x_array = plotdict[u'x_array']
                    y_array = plotdict[u'y_array']
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
                    y_array = plotdict[u'y_array']
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
                if plotdict[u'plot_name']:
                    subplot.set_title(plotdict[u'plot_name'], size = 'medium')
            #
            self._finalizePlotting()
        #
        except Exception as e:
            envmonlib.Logging().warning(u"GraphPlotter.PieChart: Plot skipped: %s" % (e.args[0]))
            raise


class MapChart(ChartBase):
    """ """
    def __init__(self, plot_data = None, figure = None):
        """ """
        super(MapChart, self).__init__(plot_data, figure)
        
    def plotChart(self, 
                  combined = False, 
                  x_log_scale = False, 
                  y_log_scale = False, 
                  **kwargs):
        """ """
        try:                    
            x_type = self._data.getPlotDataInfo()[u'x_type']
            y_type = self._data.getPlotDataInfo()[u'y_type']
            z_type = self._data.getPlotDataInfo()[u'z_type']
#             # Map charts needs float values. 
#             if not x_type in [u'float']:
#                 envmonlib.Logging().warning(u"GraphPlotter.MapChart: Plot skipped, X-axis type not valid: " + x_type)
#                 raise UserWarning(u"GraphPlotter.MapChart: Plot skipped, X-axis type not valid: " + x_type)
#             if not y_type in [u'float']:
#                 envmonlib.Logging().warning(u"GraphPlotter.MapChart: Plot skipped, Y-axis type not valid: " + y_type)
#                 raise UserWarning(u"GraphPlotter.MapChart: Plot skipped, Y-axis type not valid: " + y_type)
#             if not z_type in [u'integer', u'float']:
#                 envmonlib.Logging().warning(u"GraphPlotter.MapChart: Plot skipped, Z-axis type not valid: " + z_type)
#                 raise UserWarning(u"GraphPlotter.MapChart: Plot skipped, Z-axis type not valid: " + z_type)
            # 
            self._initPlotting()
            
            map_width_km = 1500
            map_height_km = 1500
            map_centre_lat = 60.0
            map_centre_lon = 15.0
            
            #
            subplot = self._figure.add_subplot(111)
            #
            m = basemap.Basemap(width = map_width_km * 1000,
                                height = map_height_km * 1000,
                                resolution = u'l', # Can be c (crude), l (low), i (intermediate), h (high), f (full) or None.
                                projection = 'tmerc', # 'tmerc', 'aeqd', ...
                                lat_0 = map_centre_lat,
                                lon_0 = map_centre_lon,
                                ax = subplot)
            # 
#             m.drawmapboundary(fill_color = 'aqua')
            m.drawcoastlines(linewidth = 0.33)
            m.drawcountries(linewidth = 0.2)
            m.fillcontinents(
#                              color = [0.8, 0.8, 0.8], # 'coral', 
#                              lake_color = 'aqua',
                             alpha = 0.5) # Transparency.
            #
            m.drawparallels(numpy.arange(-0,89, 2.0), linewidth = 0.125, linestyle = '--')
            m.drawmeridians(numpy.arange(-180,180, 2.0), linewidth = 0.125, linestyle = '--')
            #
            plotlist = self._data.getPlotList()
            #
            for plotindex, plotdict in enumerate(plotlist):
                #
                x_array = plotdict[u'x_array']
                y_array = plotdict[u'y_array']
                z_array = plotdict[u'z_array']
                #
                x_longitude, y_latitude = m(y_array, x_array)
                #
                msc = m.scatter(x_longitude, y_latitude, c = z_array, s = 25, edgecolors = 'none')
                ### msc = m.scatter(x_longitude, y_latitude, s = z_array, edgecolors = 'none')
                #
                # TODO: Can't handle multiple plots with different min/max.
                cbar = m.colorbar(msc, fig = self._figure, ax = subplot)
                cbar.set_label(self._data.getPlotDataInfo()[u'z_label'], size = 'medium')
            #
            self._finalizePlotting()
        #
        except Exception as e:
            envmonlib.Logging().warning(u"GraphPlotter.MapChart: Plot skipped: %s" % (e.args[0]))
            raise


#
# Test.
#
def graphplotter_test():
    """ """
    print("Graph plotter test...")
    #
    graph = MapChart()
    #
    data = GraphPlotData(
                title = u"Map test", 
                x_type = u'float',
                x_label = u'x as longitude',
                y_type = u'float',
                y_label = u'y as latitude',
                z_type = u'float',
                z_label = u'z as value')
    data.addPlot(
                plot_name = u"First plot", 
                x_array = [55.0, 55.2, 55.4, 55.6],
                y_array = [15.0, 15.1, 15.2, 15.3],
                z_array = [10.0, 100.0, 200.0, 500.0])
    data.addPlot(
                plot_name = u"Second plot", 
                x_array = [58.0, 58.2, 58.4, 58.6],
                y_array = [15.0, 15.1, 15.2, 15.3],
                z_array = [10.0, 100.0, 200.0, 500.0])
    data.addPlot(
                plot_name = u"Third plot", 
                x_array = [56.0, 56.2, 56.4, 56.6],
                y_array = [16.0, 16.1, 16.2, 16.3],
                z_array = [10.0, 100.0, 200.0, 500.0])

    graph.setData(data)
    graph.plotChart(combined = True, y_log_scale = False)

    return

#    graph = LineChart()
#    graph = BarChart()
#    graph = ScatterChart()
    graph = PieChart()
    #
    data = GraphPlotData(
                title = u"X as text", 
                x_type = u'text',
                x_label = u'x as text',
                y_type = u'float',
                y_label = u'y as float')
    data.addPlot(
                plot_name = u"First plot", 
                x_array = [u'A', u'B', u'C', u'D', ],
                y_array = [7.0, 88.5, 900.3, 9000])
    data.addPlot(
                plot_name = u"Second plot", 
                x_array = [u'C', u'D', u'E', u'F', ],
                y_array = [2006, 2006.5, 2060.5, 2006])
    data.addPlot(
                plot_name = u"Third plot", 
                x_array = [u'C', u'D', u'E', u'F', ],
                y_array = [1006, 1006.5, 3060.5, 1006])
    data.addPlot(
                plot_name = u"Fourth plot", 
                x_array = [u'C', u'D', u'E', u'F', ],
                y_array = [3006, 3006.5, 3060.5, 3006])

    graph.setData(data)
    graph.plotChart(combined = False, y_log_scale = True)
    graph.plotChart(combined = True, y_log_scale = True, stacked = False)
    graph.plotChart(combined = True, y_log_scale = True, stacked = True)
    

    #return


    data = GraphPlotData(
                title = u"Y array only", 
                y_type = u'integer',
                y_label = u'y as integer')
    data.addPlot(
                plot_name = u"First plot", 
                y_array = [7, 88, 900, 9000])
    data.addPlot(
                plot_name = u"Second plot", 
                y_array = [2006, 2006, 20060, 2006])

    graph.setData(data)
    graph.plotChart(combined = False, y_log_scale = True)
    graph.plotChart(combined = True, y_log_scale = True, stacked = False)
    graph.plotChart(combined = True, y_log_scale = True, stacked = True)
    
    data = GraphPlotData(
                title = u"Y array only", 
                x_label = u'Autogenerated',
                y_type = u'float',
                y_label = u'y as float')
    data.addPlot(
                plot_name = u"First plot", 
                x_label = u'autogenerated',
                y_array = [7.0, 88.5, 900.3, 9000])
    data.addPlot(
                plot_name = u"Second plot", 
                x_label = u'autogenerated',
                y_array = [2006, 2006.5, 20060.5, 2006])

    graph.setData(data)
    graph.plotChart(combined = False, y_log_scale = True)
    graph.plotChart(combined = True, y_log_scale = True, stacked = False)
    graph.plotChart(combined = True, y_log_scale = True, stacked = True)
    
    data = GraphPlotData(
                        title = u"X as datetime", 
                        x_type = u'datetime',
                        x_label = u'x datetime',
                        y_type = u'integer',
                        y_label = u'y as integer')
    data.addPlot(plot_name = u"First plot", 
                        x_array = [u'2012-03-07', u'2012-04-01', u'2012-05-10', u'2012-06-20'], 
                        y_array = [2,4,1,9], 
                        x_label = u'xxx',
                        y_label = u'yyy')
    data.addPlot(plot_name = u"Second plot", 
                        x_array = [u'2012-01-01', u'2012-02-01', u'2012-03-21', u'2012-04-01', u'2012-05-01', u'2012-06-01', u'2012-07-01', u'2012-08-01'], 
                        y_array = [2,3,2,4,1,9,2,1], 
                        x_label = u'xxxxxx',
                        y_label = u'yyyyyy')

    graph.setData(data)
    graph.plotChart(combined = False, y_log_scale = True)
    graph.plotChart(combined = True, y_log_scale = True, stacked = False)
    graph.plotChart(combined = True, y_log_scale = True, stacked = True)

    
#     data_1.addPlot(
#                 plot_name = u"1 plot", 
#                 y_array = [7.0, float('nan'), 88.0, 900.0, 9000.0], 
#                 y_label = u'Y first')
#     data_1.addPlot(
#                 plot_name = u"2 plot", 
#                 y_array = [2006.0, 2006.0, 2006.0, 'nan', 2006.0], 
#                 y_label = u'Y first')
#     data_1.addPlot(
#                 plot_name = u"3 plot", 
#                 y_array = [2006.0, 'NaN', 2006.0, 2006.0, 2006.0], 
#                 y_label = u'Y first')
#     data_1.addPlot(
#                 plot_name = u"4 plot", 
#                 y_array = [2006.0, 2006.0, None, 2006.0, 2006.0], 
#                 y_label = u'Y first')
# 
#     graph = LineChart(plotdata_0)
#     graph.plotChart(combined = False, y_log_scale = True)
#     graph.plotChart(combined = True, y_log_scale = True)
#     
#     graph = PieChart(plotdata_0)
#     graph.plotChart(combined = False)
    



#    plotdata_0 = GraphPlotData(
#                        title = u"One variable data object", 
#                        x_label = u'X (one variable)',
#                        y_label = u'Y (one variable)')
#
#    plotdata_0.addPlot(plot_name = u"1 plot", 
#                        y_array = [7.0, float('nan'), 88.0, 900.0, 9000.0], 
#                        y_label = u'Y first')
#    plotdata_0.addPlot(plot_name = u"2 plot", 
#                        y_array = [2006.0, 2006.0, 2006.0, 'nan', 2006.0], 
#                        y_label = u'Y first')
#    plotdata_0.addPlot(plot_name = u"3 plot", 
#                        y_array = [2006.0, 'NaN', 2006.0, 2006.0, 2006.0], 
#                        y_label = u'Y first')
#    plotdata_0.addPlot(plot_name = u"4 plot", 
#                        y_array = [2006.0, 2006.0, None, 2006.0, 2006.0], 
#                        y_label = u'Y first')
#
#    graph = LineChart(plotdata_0)
#    graph.plotChart(combined = False, y_log_scale = True)
#    graph.plotChart(combined = True, y_log_scale = True)
#    
#    graph = PieChart(plotdata_0)
#    graph.plotChart(combined = False)
    
#     plotdata_1 = GraphPlotData(
#                         title = u"One variable data object", 
#                         x_label = u'X (one variable)',
#                         y_label = u'Y (one variable)')
#     
#     plotdata_1.addPlot(plot_name = u"First plot", 
#                         y_array = [2,3,2,4,1,9], 
#                         y_label = u'Y first')
#     plotdata_1.addPlot(plot_name = u"Second plot", 
#                         y_array = [1,2,3], 
#                         y_label = u'Y second')
#     plotdata_1.addPlot(plot_name = u"Third plot", 
#                         y_array = [12,10,6,3,9], 
#                         y_label = u'Y third')
#     #
#     plotdata_2 = GraphPlotData(
#                         title = u"Two variables data object", 
#                         x_label = u'X (two variable)',
#                         y_label = u'Y (two variable)')
#     plotdata_2.addPlot(plot_name = u"First plot", 
#                         x_array = [1,2,5,6,7,8], 
#                         y_array = [2,3,2,4,1,9], 
#                         x_label = u'X first',
#                         y_label = u'Y first')
#     plotdata_2.addPlot(plot_name = u"Second plot", 
#                         x_array = [4,5,6,7,8,9,10,11], 
#                         y_array = [2,3,2,4,1,9,2,1], 
#                         x_label = u'X second',
#                         y_label = u'Y second')
#     #
#     plotdata_3 = GraphPlotData(
#                         title = u"Three variables data object", 
#                         x_label = u'X (three variable)',
#                         y_label = u'Y (three variable)',
#                         z_label = u'Z (three variable)')
#     plotdata_3.addPlot(plot_name = u"First plot", 
#                         x_array = [1,2,5,6,7,8], 
#                         y_array = [20,30,20,40,10,90], 
#                         z_array = [10,10,80,20,30,30], 
#                         x_label = u'X First',
#                         y_label = u'Y First',
#                         z_label = u'Z First')
#     plotdata_3.addPlot(plot_name = u"Second plot", 
#                         x_array = [1,2,5,6,7,8], 
#                         y_array = [2,3,2,4,1,9], 
#                         z_array = [10,10,20,20,30,30], 
#                         x_label = u'X Second',
#                         y_label = u'Y Second',
#                         z_label = u'Z Second')
#     plotdata_3.addPlot(plot_name = u"Third plot", 
#                         x_array = [10,20,50,60,70,80], 
#                         y_array = [2,3,2,4,1,9], 
#                         z_array = [10,60,20,90,30,30], 
#                         x_label = u'X Third',
#                         y_label = u'Y Third',
#                         z_label = u'Z Third')
#     #
#     plotdata_4 = GraphPlotData(
#                         x_type = u'String',
#                         title = u"Two variables data object, string", 
#                         x_label = u'X (two variables)',
#                         y_label = u'Y (two variables)')
#     plotdata_4.addPlot(plot_name = u"Dinophysis acuta", 
#                         x_array = [u'BY15',u'Släggö',u'cc','dd','ee'], 
#                         y_array = [10,30,5,5,1], 
#                         x_label = u'X First',
#                         y_label = u'Y First')
#     plotdata_4.addPlot(plot_name = u"Second plot", 
#                         x_array = ['cc','dd','ee','ff', 'gg', 'hh'], 
#                         y_array = [2,3,2,4,1,9], 
#                         x_label = u'X Second',
#                         y_label = u'Y Second')
#     plotdata_4.addPlot(plot_name = u"Third plot", 
#                         x_array = ['AA','BB','cc','dd','ee','ff'], 
#                         y_array = [5,5,5,1,2,3], 
#                         x_label = u'X Third',
#                         y_label = u'Y Third')
#     #
#     plotdata_5 = GraphPlotData(
#                         x_type = u'date',
#                         title = u"Two variables x:date", 
#                         x_label = u'X (date)',
#                         y_label = u'Y (two variable)')
#     plotdata_5.addPlot(plot_name = u"First plot", 
#                         x_array = [u'2012-03-07', u'2012-04-01', u'2012-05-10', u'2012-06-20'], 
#                         y_array = [2,4,1,9], 
#                         x_label = u'X first (date)',
#                         y_label = u'Y first')
#     plotdata_5.addPlot(plot_name = u"Second plot", 
#                         x_array = [u'2012-01-01', u'2012-02-01', u'2012-03-21', u'2012-04-01', u'2012-05-01', u'2012-06-01', u'2012-07-01', u'2012-08-01'], 
#                         y_array = [2,3,2,4,1,9,2,1], 
#                         x_label = u'X second (date)',
#                         y_label = u'Y second')
#     #
#     #
#     graph = LineChart(plotdata_1)
#     graph.plotChart(combined = True, y_log_scale = True)
#     graph.plotChart(combined = False, y_log_scale = True)
#     #
#     #
#     graph = LineChart(plotdata_2)
#     graph.plotChart(combined = True, y_log_scale = True)
#     graph.plotChart(combined = False, y_log_scale = True)
#     #
#     #
#     graph = BarChart(plotdata_2)
#     graph.plotChart(combined = True, y_log_scale = False)
#     graph.plotChart(combined = True, y_log_scale = False, stacked = True)
#     graph.plotChart(combined = False, y_log_scale = True)
#     graph.plotChart(combined = False, y_log_scale = True, stacked = True)
#     #
#     #
#     graph = ScatterChart(plotdata_2)
#     graph.plotChart(combined = True, y_log_scale = False)
#     graph.plotChart(combined = False, y_log_scale = True)
#     #
#     #
#     graph = ScatterChart(plotdata_3)
#     graph.plotChart(combined = True, y_log_scale = False)
#     graph.plotChart(combined = False, y_log_scale = True)
#     #
#     #
#     graph = BarChart(plotdata_4)
#     graph.plotChart(combined = True, y_log_scale = False)
#     graph.plotChart(combined = True, y_log_scale = False, stacked = True)
#     graph.plotChart(combined = True, y_log_scale = False)
#     graph.plotChart(combined = True, y_log_scale = False, stacked = True)
#     graph.plotChart(combined = False, y_log_scale = False)
#     graph.plotChart(combined = False, y_log_scale = False, stacked = True)
#     #
#     graph = PieChart(plotdata_2)
#     graph.plotChart(combined = False, y_log_scale = False)
#     #
#     graph = PieChart(plotdata_4)
#     graph.plotChart(combined = False, y_log_scale = False)
#     #
#     graph = LineChart(plotdata_5)
#     graph.plotChart(combined = True, y_log_scale = True)
#     graph.plotChart(combined = False, y_log_scale = True)

                
if __name__ == "__main__":
    graphplotter_test()

