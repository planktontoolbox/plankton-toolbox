#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import numpy.ma
import datetime
import copy
# import matplotlib as mpl
import matplotlib.dates as mpl_dates
import matplotlib.font_manager as mpl_font_manager
# import matplotlib.figure as mpl_figure
import pylab # Usedfor color maps.
import matplotlib.pyplot as pyplot # Used when not embedded plotting.
###import mpl_toolkits.basemap as basemap

import toolbox_utils
import plankton_core

class GraphPlotData(object):
    """ Class containing data needed when plotting. 
        Valid data array types: 'text', 'integer', 'float', 'date', 'datetime'. 
    """
    
    def __init__(self,
                 title = '', 
                 x_label = '',
                 x_type = 'integer', # Alternatives: text, integer, float, date, datetime.
                 x_format = '', # Used for the datetime type. 
                 y_label = '',
                 y_type = '', # Alternatives: integer, float.
                 y_format = '', # Used for the datetime type. 
                 z_label = '',
                 z_type = '', # Alternatives: integer, float.
                 z_format = ''): # Used for the datetime type. 
        """ """
        super(GraphPlotData, self).__init__()
        #
        self._plot_list = []
        self._plotdata_info = {}
        #
        self._plotdata_info['title'] = title
        #
        self._plotdata_info['x_label'] = x_label
        self._plotdata_info['x_type'] = x_type
        self._plotdata_info['x_format'] = x_format
        #
        self._plotdata_info['y_label'] = y_label
        self._plotdata_info['y_type'] = y_type
        self._plotdata_info['y_format'] = y_format
        #
        self._plotdata_info['z_label'] = z_label
        self._plotdata_info['z_type'] = z_type
        self._plotdata_info['z_format'] = z_format
        
    def add_plot(self,
                plot_name = '', 
                x_label = '',
                x_array = None,
                y_label = '',
                y_array = None,
                z_label = '',
                z_array = None):
        """ """
        if (not y_array) or (len(y_array) == 0):
            toolbox_utils.Logging().warning('GraphPlotData.add_plot() must contain at least an y-array. Plot not added.')
            raise UserWarning('GraphPlotData.add_plot() must contain at least an y-array. Plot not added.')
            return
        #
        plotdict = {}
        plotdict['plot_name'] = plot_name
        plotdict['x_label'] = x_label
        plotdict['x_array'] = x_array
        #
        plotdict['y_label'] = y_label
        plotdict['y_array'] = y_array
        #
        plotdict['z_label'] = z_label
        plotdict['z_array'] = z_array
        #
        self._plot_list.append(plotdict)
               
    def clear(self):
        """ """
        self._plot_list = []
        
    def remove_plot_by_index(self, data_index = None):
        """ """
        if data_index: 
            if len(data_index) > data_index: 
                del self._plot_list[data_index]
        
    def get_plot_data_info(self):
        """ """
        return self._plotdata_info
    
    def set_plot_data_info(self, info):
        """ """
        self._plotdata_info = info
    
    def get_plot_list(self):
        """ """
        return self._plot_list    

    def set_plot_list(self, plotlist):
        """ """
        self._plot_list = plotlist

    def merge_data(self):
        """ Creates a common x array and add zero values for plots with no corresponding x value. """
        # Copy the plot list.
        newplotlist = copy.deepcopy(self._plot_list)
        # Create a unique list containing all x values.
        x_unique = []
        for plotdict in newplotlist:
            #
            x_array = plotdict['x_array']
            if (not x_array) or (len(x_array) == 0):
                # Generate x-array if it is missing.
                plotdict['x_array'] = list(numpy.arange(len(plotdict['y_array'])))                        
            #
            for item in plotdict['x_array']:
                if not item in x_unique:
                    x_unique.append(item)
        # Sort the list.                   
        x_unique.sort()
        #
        for plotdict in newplotlist:
            y_newarray = []
            z_newarray = []
            y_arrayasdict = dict(zip(plotdict['x_array'], plotdict['y_array']))
            if plotdict['z_array']:
                z_arrayasdict = dict(zip(plotdict['x_array'], plotdict['z_array']))
            #
            for x in x_unique:
                if x in y_arrayasdict:
                    y_newarray.append(y_arrayasdict[x])
                else:
                    y_newarray.append(0)
                #
                if plotdict['z_array']:           
                    if x in z_arrayasdict:
                        z_newarray.append(z_arrayasdict[x])
                    else:
                        z_newarray.append(0)        
            #
            plotdict['x_array'] = x_unique
            plotdict['y_array'] = y_newarray
            if plotdict['z_array']:      
                plotdict['z_array'] = z_newarray      
        #
        return newplotlist

    def get_min_max_values(self, 
                        array_name = 'x_array'):
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
                toolbox_utils.Logging().error('Chart data object is not an instance of the class GraphPlotData. Plotting terminated.')
                raise UserWarning('Chart data object is not an instance of the class GraphPlotData. Plotting terminated.')
            
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
        self._markers = ['o', 's', 'D', '^', '<']
        self._colors = ['b', 'r', 'c', 'm', 'k', 'g', 'y']
        self._symbols = ['-', '--', '-.', ':']
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
    
    def set_data(self, plot_data):
        """ """
        if not isinstance(plot_data, GraphPlotData):
            toolbox_utils.Logging().error('Chart data object is not an instance of the class GraphPlotData. Plotting terminated.')
            raise UserWarning('Chart data object is not an instance of the class GraphPlotData. Plotting terminated.')
        #
        self._data = plot_data
    
    def get_data(self, plot_data):
        """ """
        return self._data
    
    def _init_plotting(self):
        """ """
        if self._pyplot_used:         
            # Use pyplot for tests.
            self._figure = pyplot.figure()
        #
#        self._figure.subplots_adjust(hspace=1.0)
        self._figure.subplots_adjust(hspace=0.5)
        self._figure.subplots_adjust(top = 0.90, bottom = 0.14)
        #
        if self._data.get_plot_data_info()['title']:
            self._figure.suptitle(self._data.get_plot_data_info()['title'], verticalalignment = 'top', size = 'medium')
        
    def _add_legend(self, subplot):
        """ """
        font_properties = mpl_font_manager.FontProperties()
        font_properties.set_size('small')
        leg = subplot.legend(loc='best', fancybox=True, prop = font_properties)
        if leg:
            leg.get_frame().set_alpha(0.5)
            leg.draggable(state = True)

    def _finalize_plotting(self):
        """ """
        if self._pyplot_used:
#             pyplot.tight_layout()
            pyplot.show()
        else:
            self._figure.subplots_adjust(hspace=1.0)
            self._figure.subplots_adjust(top = 0.90, bottom = 0.14)
#             self._figure.tight_layout()
        
    def _format_array(self, data_type, data_array, data_format = ''):
        """ """
        #
        if data_type == 'text':
            # Convert to a sequence of integers.
            integer_array = []
            for index, value in enumerate(data_array):
                integer_array.append(index)
            return integer_array
        #
        if data_type == 'integer':
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
                toolbox_utils.Logging().warning('GraphPlotter.ChartBase: These values could not be converted to integer: "' + 
                                            '", "'.join(sorted(failedconversions_set)) + '"')
            # Masked arrays are needed for proper handling of missing values when plotting.
            return numpy.ma.masked_array(integer_array, numpy.isnan(integer_array))
        #
        elif data_type in ['', 'float']: # Test with float if type is not specified.
            float_array = []
            failedconversions_set = set() # Used in error log.
            #
            for value in data_array:
                try:
                    value = float(value.replace(',', '.').replace(' ', ''))
                    float_array.append(value)
                except:
                    failedconversions_set.add(unicode(value))
                    float_array.append(float('nan'))
            #
            if len(failedconversions_set) > 0:
                toolbox_utils.Logging().warning('GraphPlotter.ChartBase: These values could not be converted to float: "' + 
                                            '", "'.join(sorted(failedconversions_set)) + '"')
            # Masked arrays are needed for proper handling of missing values when plotting.
            return numpy.ma.masked_array(float_array, numpy.isnan(float_array))
        #
        elif data_type in ['date', 'datetime']: 
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
                toolbox_utils.Logging().warning('GraphPlotter.ChartBase: These values could not be converted to date or datetime: "' + 
                                            '", "'.join(sorted(failedconversions_set)) + '"')
            return datetime_array
        
    def plot_chart(self, **kwargs):
        """ Abstract. """
        raise NotImplementedError('The abstract method ChartBase.plot_chart() is not implement. ')

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

    def plot_chart(self, 
                  combined = False, 
                  stacked = False,
                  x_log_scale = False, 
                  y_log_scale = False,
                  **kwargs):
        """ """
        try: 
            x_type = self._data.get_plot_data_info()['x_type']
            x_format = self._data.get_plot_data_info()['x_format']
            y_type = self._data.get_plot_data_info()['y_type']
            y_format = self._data.get_plot_data_info()['y_format']
            # Line charts needs text (text, integer, data or datetime) for the x-axis and 
            # values (integer or float) for the y-axis.
            if not x_type in ['', 'text', 'integer', 'float', 'date', 'datetime']:
                toolbox_utils.Logging().warning('GraphPlotter.LineChart: Plot skipped, X-axis type not valid: ' + x_type)
                raise UserWarning('GraphPlotter.LineChart: Plot skipped, X-axis type not valid: ' + x_type)
            if not y_type in ['', 'integer', 'float']:
                toolbox_utils.Logging().warning('GraphPlotter.LineChart: Plot skipped, Y-axis type not valid: ' + y_type)
                raise UserWarning('GraphPlotter.LineChart: Plot skipped, Y-axis type not valid: ' + y_type)
            #
            self._init_plotting()
            plotlist = self._data.get_plot_list()
            
            if (x_type == 'text') or stacked:
                # All plots should have the same x axis items. 
                plotlist = self._data.merge_data()        
            # 
            if combined:
                # All data in one plot.
                subplot = self._figure.add_subplot(111)
                #
                y_array_acc = 0 # Accumulated values are needed when stacking.  
                #
                if x_log_scale and (x_type in ['', 'integer', 'float']):
                    subplot.set_xscale('log')
                if y_log_scale and (y_type in ['', 'integer', 'float']):
                    subplot.set_yscale('log')
                    y_array_acc = 0.1 # Log 0 not defined. 
                #
                for plotindex, plotdict in enumerate(plotlist):
                    #
                    x_array = plotdict['x_array']
                    y_array = plotdict['y_array']
                    #
                    if (not x_array) or (len(x_array) == 0):
                        # Generate x-array.
                        x_type = 'integer'
                        x_array = list(numpy.arange(len(y_array)))                        
                    #
                    if x_type == 'text':
                        x_integer_array = self._format_array(x_type, x_array, x_format)
                        y_masked_array = self._format_array(y_type, y_array, y_format)
                        #
                        subplot.set_xticklabels(x_array, rotation=20.0)
                        #
                        if stacked:
                            old_y_array_acc = y_array_acc
                            y_array_acc = y_array_acc + y_masked_array
                            subplot.plot(x_integer_array, 
                                         y_array_acc,
                                         label = plotdict['plot_name'],
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
                                         label = plotdict['plot_name'],
                                         marker = self._markers[plotindex % len(self._markers)],
                                         color = self._colors[plotindex % len(self._colors)])
                    #
                    elif x_type == 'integer':
                        x_masked_array = self._format_array('integer', x_array, x_format)
                        y_masked_array = self._format_array(y_type, y_array, y_format)
                        #
                        if stacked:
                            old_y_array_acc = y_array_acc
                            y_array_acc = y_array_acc + y_masked_array
                            subplot.plot(x_masked_array, 
                                         y_array_acc,
                                         label = plotdict['plot_name'],
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
                                         label = plotdict['plot_name'],
                                         marker = self._markers[plotindex % len(self._markers)])
                    #    
                    elif x_type == 'float':
                        x_masked_array = self._format_array('float', x_array, x_format)
                        y_masked_array = self._format_array(y_type, y_array, y_format)
                        #
                        if stacked:
                            old_y_array_acc = y_array_acc
                            y_array_acc = y_array_acc + y_masked_array
                            subplot.plot(x_masked_array, 
                                         y_array_acc,
                                         label = plotdict['plot_name'],
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
                                         label = plotdict['plot_name'],
                                         marker = self._markers[plotindex % len(self._markers)])
                    #    
                    elif x_type in ['date', 'datetime']:
                        """ """
                        x_datetime_array = self._format_array(x_type, x_array, x_format)
                        y_masked_array = self._format_array(y_type, y_array, y_format)
                        #
                        # 
                        if stacked:
                            old_y_array_acc = y_array_acc
                            y_array_acc = y_array_acc + y_masked_array
                            subplot.plot_date(x_datetime_array, 
                                              y_array_acc,
                                              label = plotdict['plot_name'],
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
                                              label = plotdict['plot_name'],
                                              marker = self._markers[plotindex % len(self._markers)], 
#                                               c = self._colors[plotindex % len(self._colors)],
                                              color = self._colors[plotindex % len(self._colors)])
                        #
                        subplot.xaxis.set_major_locator(mpl_dates.AutoDateLocator())
###                        subplot.xaxis.set_major_locator(mpl_dates.MonthLocator())
###                        subplot.xaxis.set_minor_locator(mpl_dates.WeekdayLocator())
                        if x_format:
                            subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter(x_format))
                        else:
                            subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
                        self._figure.autofmt_xdate(bottom = 0.2)   
                    #                      
                    else:
                        toolbox_utils.Logging().warning('GraphPlotter.LineChart: Not a valid type for the x axis: ' + x_type)
                        return
                # Legend.
                self._add_legend(subplot)                
                # Labels. Only one for combined plotting.
                subplot.set_xlabel(self._data.get_plot_data_info()['x_label'], size = 'medium')
                subplot.set_ylabel(self._data.get_plot_data_info()['y_label'], size = 'medium')
            else:
                # Divided into separate plots with a common x axis.
                subplotcount = len(plotlist)
                sharesubplotxaxis = None
                #
                for plotindex, plotdict in enumerate(plotlist):
                    x_array = plotdict['x_array']
                    y_array = plotdict['y_array']
                    #
                    subplot = self._figure.add_subplot(subplotcount, 1, plotindex + 1, sharex = sharesubplotxaxis)
                    if not sharesubplotxaxis: 
                        sharesubplotxaxis = subplot    
                    #
                    if x_log_scale and (x_type in ['', 'integer', 'float']):
                        subplot.set_xscale('log')
                    if y_log_scale and (y_type in ['', 'integer', 'float']):
                        subplot.set_yscale('log')
                    #
                    if (not x_array) or (len(x_array) == 0):
                        # Generate x-array.
                        x_array = list(numpy.arange(len(y_array)))                        
                    #
                    if x_type == 'text':
                        """ """
                        x_integer_array = self._format_array('text', x_array, x_format)
                        y_masked_array = self._format_array(y_type, y_array, y_format)
                        #
                        subplot.set_xticklabels(x_array)
                        #
                        subplot.plot(x_integer_array, 
                                     y_masked_array,
                                     label = plotdict['plot_name'],
                                     marker = self._markers[plotindex % len(self._markers)],
                                     color = self._colors[plotindex % len(self._colors)])   
                    #    
                    elif x_type == 'integer':
                        x_masked_array = self._format_array('integer', x_array, x_format)
                        y_masked_array = self._format_array(y_type, y_array, y_format)
                        #
                        subplot.plot(x_masked_array, 
                                     y_masked_array,
                                     label = plotdict['plot_name'],
                                     marker = self._markers[plotindex % len(self._markers)])
                    #    
                    elif x_type == 'float':
                        x_masked_array = self._format_array('float', x_array, x_format)
                        y_masked_array = self._format_array(y_type, y_array, y_format)
                        #
                        subplot.plot(x_masked_array, 
                                     y_masked_array,
                                     label = plotdict['plot_name'],
                                     marker = self._markers[plotindex % len(self._markers)])
                    #    
                    elif x_type in ['date', 'datetime']:
                        """ """
                        x_datetime_array = self._format_array(x_type, x_array, x_format)
                        y_masked_array = self._format_array(y_type, y_array, y_format)
                        #
                        # 
                        subplot.plot_date(x_datetime_array, 
                                          y_masked_array,
                                          label = plotdict['plot_name'],
                                          marker = self._markers[plotindex % len(self._markers)], 
                                          c = self._colors[plotindex % len(self._colors)])
                        #
                        subplot.xaxis.set_major_locator(mpl_dates.AutoDateLocator())
###                        subplot.xaxis.set_major_locator(mpl_dates.MonthLocator())
###                        subplot.xaxis.set_minor_locator(mpl_dates.WeekdayLocator())
                        if x_format:
                            subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter(x_format))
                        else:
                            subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
                        #
                        self._figure.autofmt_xdate(bottom = 0.2)   
                    #                      
                    else:
                        toolbox_utils.Logging().warning('GraphPlotter.LineChart: Not a valid type for the x axis. Type ' + x_type)
                    #
                    subplot.set_title(plotdict['plot_name'], size = 'medium')
                    subplot.set_ylabel(plotdict['y_label'])
                    #
                    if (plotindex + 1) == len(plotlist):
                        # Last subplot.
                        subplot.set_xlabel(self._data.get_plot_data_info()['x_label'])
#                        subplot.set_xticklabels(x_array, visible = True)
            #
            self._finalize_plotting()
        #
        except Exception as e:
            toolbox_utils.Logging().warning('GraphPlotter.LineChart: Plot skipped: %s' % (e.args[0]))
            raise


class BarChart(ChartBase):
    """ """
    def __init__(self, plot_data = None, figure = None):
        """ """
        super(BarChart, self).__init__(plot_data, figure)

    def plot_chart(self, 
                  combined = False, 
                  stacked = False,
                  y_log_scale = False,
                  **kwargs):
        """ """
        #
        try:
            x_type = self._data.get_plot_data_info()['x_type']
            x_format = self._data.get_plot_data_info()['x_format']
            y_type = self._data.get_plot_data_info()['y_type']
            y_format = self._data.get_plot_data_info()['y_format']
            # Bar charts needs text (text, integer, date or datetime) for the x-axis and 
            # values (integer or float) for the y-axis.
            if not x_type in ['', 'text', 'integer', 'float', 'date', 'datetime']:
                toolbox_utils.Logging().warning('GraphPlotter.BarChart: Plot skipped, X-axis type not valid: ' + x_type)
                raise UserWarning('GraphPlotter.BarChart: Plot skipped, X-axis type not valid: ' + x_type)
            if not y_type in ['', 'integer', 'float']:
                toolbox_utils.Logging().warning('GraphPlotter.BarChart: Plot skipped, Y-axis type not valid: ' + y_type)
                raise UserWarning('GraphPlotter.BarChart: Plot skipped, Y-axis type not valid: ' + y_type)
            #
            self._init_plotting()
            #
            plotlist = self._data.get_plot_list()
#             # Bar plots should have values in the x array.
#             if not plotlist[0]['x_array']:
#                 toolbox_utils.Logging().warning('GraphPlotter.BarChart: Plot skipped, X values are missing.')
#                 return
            # 
            # All plots should have the same x axis items. 
            plotlist = self._data.merge_data()        
            #
            if combined:
                # Get axes from first plot.
                x_axis = plotlist[0]['x_array']
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
                    x_array = plotdict['x_array']
                    y_array = plotdict['y_array']
#                     z_array = plotdict['z_array']
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
                leg = subplot.legend([data['plot_name'] for data in plotlist], 
                                     loc='best', fancybox=True, prop = font_properties)
                leg.get_frame().set_alpha(0.5)
    #            #
    #            if self._data.get_plot_data_info()['title']:
    #                subplot.set_title(self._data.get_plot_data_info()['title'], size = 'small')
                #
                subplot.set_xlabel(self._data.get_plot_data_info()['x_label'])
                subplot.set_ylabel(self._data.get_plot_data_info()['y_label'])
            else:
                # Get axes from first plot.
                x_axis = plotlist[0]['x_array']
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
                    x_array = plotdict['x_array']
                    y_array = plotdict['y_array']
                    z_array = plotdict['z_array']
                    #
                    rect = subplot.bar(x_axis_positions, 
                                       plotdict['y_array'],
                                       barwidth,
                                       color=colourmap(1.0 * plotindex / colourcount))
                    #
                    subplot.set_title(plotdict['plot_name'], size = 'medium')
                    subplot.set_ylabel(plotdict['y_label'])
                    #
                    if (plotindex + 1) == len(plotlist):
                        # Last subplot.
                        subplot.set_xlabel(self._data.get_plot_data_info()['x_label'])
                        subplot.set_xticklabels(x_array, rotation=20.0, visible = True)
            #
            self._finalize_plotting()
        #
        except Exception as e:
            toolbox_utils.Logging().warning('GraphPlotter.BarChart: Plot skipped: %s' % (e.args[0]))
            raise


class ScatterChart(ChartBase):
    """ """
    def __init__(self, plot_data = None, figure = None):
        """ """
        super(ScatterChart, self).__init__(plot_data, figure)
        
    def plot_chart(self, 
                  combined = False, 
                  x_log_scale = False, 
                  y_log_scale = False, 
                  **kwargs):
        """ """
        #
        try: 
            x_type = self._data.get_plot_data_info()['x_type']
            x_format = self._data.get_plot_data_info()['x_format']
            y_type = self._data.get_plot_data_info()['y_type']
            y_format = self._data.get_plot_data_info()['y_format']
            z_type = self._data.get_plot_data_info()['z_type']
            # Scatter charts needs text (text, integer, date or datetime) for the x-axis and 
            # values (integer or float) for the y-axis.
            if not x_type in ['', 'text', 'integer', 'float', 'date', 'datetime']:
                toolbox_utils.Logging().warning('GraphPlotter.PieChart: Plot skipped, X-axis type not valid: ' + x_type)
                raise UserWarning('GraphPlotter.PieChart: Plot skipped, X-axis type not valid: ' + x_type)
            if not y_type in ['', 'integer', 'float']:
                toolbox_utils.Logging().warning('GraphPlotter.PieChart: Plot skipped, Y-axis type not valid: ' + y_type)
                raise UserWarning('GraphPlotter.PieChart: Plot skipped, Y-axis type not valid: ' + y_type)
            if not z_type in ['', 'integer', 'float']:
                toolbox_utils.Logging().warning('GraphPlotter.PieChart: Plot skipped, Z-axis type not valid: ' + z_type)
                raise UserWarning('GraphPlotter.PieChart: Plot skipped, Z-axis type not valid: ' + z_type)
            # 
            self._init_plotting()
            # 
            plotlist = self._data.get_plot_list()
            # Scatter plots should have values in the x array.
            if not plotlist[0]['x_array']:
                toolbox_utils.Logging().warning('GraphPlotter.ScatterChart: Plot skipped, X values are missing.')
                return
            #
            if combined:
                subplot = self._figure.add_subplot(111)
                #
                if x_log_scale and (x_type in ['', 'integer', 'float']):
                    subplot.set_xscale('log')
                if y_log_scale and (y_type in ['', 'integer', 'float']):
                    subplot.set_yscale('log')
                #
                for plotindex, plotdict in enumerate(plotlist):
                    #
                    x_array = plotdict['x_array']
                    y_array = plotdict['y_array']
                    z_array = plotdict['z_array']
                    #

                    if x_type == 'text':
                        """ """
                        x_integer_array = self._format_array(x_type, x_array, x_format)
                        y_masked_array = self._format_array(y_type, y_array, y_format)
                        #
                        subplot.set_xticklabels(x_array, rotation=20.0)
                        #
                        if z_array:
                            subplot.scatter(x_integer_array, y_masked_array, s = z_array, 
                                            label = plotdict['plot_name'],
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        else:
                            subplot.scatter(x_integer_array, y_array, 
                                            label = plotdict['plot_name'],
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                    #     
                    elif x_type in ['integer', 'float']:
                        """ """
                        x_masked_array = self._format_array(x_type, x_array, x_format)
                        y_masked_array = self._format_array(y_type, y_array, y_format)
                        #
                        if z_array:
                            subplot.scatter(x_masked_array, y_masked_array, s = z_array, 
                                            label = plotdict['plot_name'],
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        else:
                            subplot.scatter(x_masked_array, y_masked_array, 
                                            label = plotdict['plot_name'],
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                    #     
                    elif x_type in ['date', 'datetime']:
                        """ """
                        x_datetime_array = self._format_array(x_type, x_array, x_format)
                        y_masked_array = self._format_array(y_type, y_array, y_format)
                        #
                        if z_array:
                            subplot.scatter(x_datetime_array, y_masked_array, s = z_array, 
                                            label = plotdict['plot_name'],
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        else:
                            subplot.scatter(x_datetime_array, y_masked_array, 
                                            label = plotdict['plot_name'],
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        #
                        subplot.xaxis.set_major_locator(mpl_dates.AutoDateLocator())
###                        subplot.xaxis.set_major_locator(mpl_dates.MonthLocator())
###                        subplot.xaxis.set_minor_locator(mpl_dates.WeekdayLocator())

                        if x_format:
                            subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter(x_format))
                        else:
                            subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
                        self._figure.autofmt_xdate(bottom = 0.2)   

                # Legend.
                self._add_legend(subplot)                
                # 
                subplot.set_xlabel(self._data.get_plot_data_info()['x_label'])
                subplot.set_ylabel(self._data.get_plot_data_info()['y_label'])
            else:



                subplotcount = len(plotlist)
                #
                share_x_axis = None
                #
                for plotindex, plotdict in enumerate(plotlist):
                    subplot = self._figure.add_subplot(subplotcount, 1, plotindex + 1, sharex = share_x_axis)    
                    if not share_x_axis: share_x_axis = subplot    
                    #
                    if x_log_scale and (x_type in ['', 'integer', 'float']):
                        subplot.set_xscale('log')
                    if y_log_scale and (y_type in ['', 'integer', 'float']):
                        subplot.set_yscale('log')
                    #
                    x_array = plotdict['x_array']
                    y_array = plotdict['y_array']
                    z_array = plotdict['z_array']
                    #
    #                x_array = numpy.float64(x_array)
    #                y_array = numpy.float64(y_array)
    #                if z_array:
    #                    z_array = numpy.float64(plotdict['z_array'])
                    #
                    if x_type == 'text':
                        """ """
                        x_integer_array = self._format_array(x_type, x_array, x_format)
                        y_masked_array = self._format_array(y_type, y_array, y_format)
                        #
                        subplot.set_xticklabels(x_array)
                        #
                        if z_array:
                            subplot.scatter(x_integer_array, y_masked_array, s = z_array, 
                                            label = plotdict['plot_name'],
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        else:
                            subplot.scatter(x_integer_array, y_array, 
                                            label = plotdict['plot_name'],
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                         
                    elif x_type in ['integer', 'float']:
                        """ """
                        if z_array:
                            subplot.scatter(x_array, y_array, s = z_array, 
                                            label = plotdict['plot_name'],
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        else:
                            subplot.scatter(x_array, y_array, 
                                            label = plotdict['plot_name'],
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                         
                    elif x_type in ['date', 'datetime']:
                        """ """
                        x_datetime_array = self._format_array(x_type, x_array, x_format)
                        y_masked_array = self._format_array(y_type, y_array, y_format)
                        #
                        if z_array:
                            subplot.scatter(x_datetime_array, y_masked_array, s = z_array, 
                                            label = plotdict['plot_name'],
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        else:
                            subplot.scatter(x_datetime_array, y_masked_array, 
                                            label = plotdict['plot_name'],
                                            marker = self._markers[plotindex % len(self._markers)], c = self._colors[plotindex % len(self._colors)])
                        #
                        subplot.xaxis.set_major_locator(mpl_dates.AutoDateLocator())
###                        subplot.xaxis.set_major_locator(mpl_dates.MonthLocator())
###                        subplot.xaxis.set_minor_locator(mpl_dates.WeekdayLocator())
                        if x_format:
                            subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter(x_format))
                        else:
                            subplot.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
                        self._figure.autofmt_xdate(bottom = 0.2)   

                    #
                    subplot.set_title(plotdict['plot_name'], size = 'medium')
                    subplot.set_ylabel(plotdict['y_label'])
                    #
                    if (plotindex + 1) == len(plotlist):
                        # Last subplot.
                        subplot.set_xlabel(self._data.get_plot_data_info()['x_label'])
                        subplot.set_xticklabels(plotdict['x_array'], rotation=20.0, visible = True)
            #
            self._finalize_plotting()
        #
        except Exception as e:
            toolbox_utils.Logging().warning('GraphPlotter.ScatterChart: Plot skipped: %s' % (e.args[0]))
            raise

                
class PieChart(ChartBase):
    """ """
    def __init__(self, plot_data = None, figure = None):
        """ """
        super(PieChart, self).__init__(plot_data, figure)
        
    def plot_chart(self, 
                  combined = False, # Not used.
                  x_log_scale = False, # Not used.
                  y_log_scale = False, # Not used. 
                  stacked = None): # Not used.
        """ """
        #
        try:            
            x_type = self._data.get_plot_data_info()['x_type']
            x_format = self._data.get_plot_data_info()['x_format']
            y_type = self._data.get_plot_data_info()['y_type']
            y_format = self._data.get_plot_data_info()['y_format']
            # Pie charts needs text (text, integer or datetime) for the x-axis and 
            # values (integer or float) for the y-axis.
            if not x_type in ['', 'text', 'integer', 'float', 'date', 'datetime']:
                toolbox_utils.Logging().warning('GraphPlotter.PieChart: Plot skipped, X-axis type not valid: ' + x_type)
                raise UserWarning('GraphPlotter.PieChart: Plot skipped, X-axis type not valid: ' + x_type)
            if not y_type in ['', 'integer', 'float']:
                toolbox_utils.Logging().warning('GraphPlotter.PieChart: Plot skipped, Y-axis type not valid: ' + y_type)
                raise UserWarning('GraphPlotter.PieChart: Plot skipped, Y-axis type not valid: ' + y_type)
            # 
            self._init_plotting()
            #
            plotlist = self._data.get_plot_list()
            #
            for plotindex, plotdict in enumerate(plotlist):
                subplot = self._figure.add_subplot(len(plotlist), 1, plotindex + 1)
                #
                if plotdict['x_array']:
                    # Remove invalid positions in both arrays.
                    x_array = plotdict['x_array']
                    y_array = plotdict['y_array']
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
                    y_array = plotdict['y_array']
                    y_cleaned = []
                    for index, item in enumerate(y_array):
                        try:
                            if not numpy.isnan(item):
                                y_cleaned.append(y_array[index])
                        except:
                            pass
                    subplot.pie(y_cleaned)
                #
                subplot.axis('equal') # A circle should be circular.
                #
                if plotdict['plot_name']:
                    subplot.set_title(plotdict['plot_name'], size = 'medium')
            #
            self._finalize_plotting()
        #
        except Exception as e:
            toolbox_utils.Logging().warning('GraphPlotter.PieChart: Plot skipped: %s' % (e.args[0]))
            raise

class BoxPlotChart(ChartBase):
    """ """
    def __init__(self, plot_data = None, figure = None):
        """ """
        super(BoxPlotChart, self).__init__(plot_data, figure)
        
    def plot_chart(self, 
                  combined = False, # Not used.
                  x_log_scale = False, # Not used.
                  y_log_scale = False, # Not used. 
                  stacked = None): # Not used.
        """ """
        #
        try:            
            x_type = self._data.get_plot_data_info()['x_type']
            x_format = self._data.get_plot_data_info()['x_format']
            y_type = self._data.get_plot_data_info()['y_type']
            y_format = self._data.get_plot_data_info()['y_format']
            # Pie charts needs text (text, integer or datetime) for the x-axis and 
            # values (integer or float) for the y-axis.
            if not y_type in ['', 'integer', 'float']:
                toolbox_utils.Logging().warning('GraphPlotter.BoxPlotChart: Plot skipped, Y-axis type not valid: ' + y_type)
                raise UserWarning('GraphPlotter.BoxPlotChart: Plot skipped, Y-axis type not valid: ' + y_type)
            # 
            self._init_plotting()
            #
            plotlist = self._data.get_plot_list()
            #
            array_list = []
            x_items = []
            #
            subplot = self._figure.add_subplot(111)
            #
            if y_log_scale and (y_type in ['', 'integer', 'float']):
                subplot.set_yscale('log')
            #
            for plotindex, plotdict in enumerate(plotlist):
                #
                # Remove invalid positions in y array.
                y_array = plotdict['y_array']
                y_cleaned = []
                for index, item in enumerate(y_array):
                    try:
                        if not numpy.isnan(item):
                            y_cleaned.append(y_array[index])
                    except:
                        pass
                #    
                array_list.append(y_cleaned)
                x_items.append(plotdict['plot_name'])    
            #
            subplot.boxplot(array_list)
            subplot.set_xticklabels(x_items, rotation=20.0)
            #
#             if plotdict['plot_name']:
#                 subplot.set_title(plotdict['plot_name'], size = 'medium')
            #
            self._finalize_plotting()
        #
        except Exception as e:
            toolbox_utils.Logging().warning('GraphPlotter.BoxPlotChart: Plot skipped: %s' % (e.args[0]))
            raise


class MapChart(ChartBase):
    """ """
    def __init__(self, plot_data = None, figure = None):
        """ """
        super(MapChart, self).__init__(plot_data, figure)
        
    def plot_chart(self, 
                  combined = False, 
                  x_log_scale = False, 
                  y_log_scale = False,
                  **kwargs):
        """ """
#         try:                    
#             x_type = self._data.get_plot_data_info()['x_type']
#             x_format = self._data.get_plot_data_info()['x_format']
#             y_type = self._data.get_plot_data_info()['y_type']
#             y_format = self._data.get_plot_data_info()['y_format']
#             z_type = self._data.get_plot_data_info()['z_type']
# #             # Map charts needs float values. 
# #             if not x_type in ['', 'float']:
# #                 toolbox_utils.Logging().warning('GraphPlotter.MapChart: Plot skipped, X-axis type not valid: ' + x_type)
# #                 raise UserWarning('GraphPlotter.MapChart: Plot skipped, X-axis type not valid: ' + x_type)
# #             if not y_type in ['', 'float']:
# #                 toolbox_utils.Logging().warning('GraphPlotter.MapChart: Plot skipped, Y-axis type not valid: ' + y_type)
# #                 raise UserWarning('GraphPlotter.MapChart: Plot skipped, Y-axis type not valid: ' + y_type)
# #             if not z_type in ['', 'integer', 'float']:
# #                 toolbox_utils.Logging().warning('GraphPlotter.MapChart: Plot skipped, Z-axis type not valid: ' + z_type)
# #                 raise UserWarning('GraphPlotter.MapChart: Plot skipped, Z-axis type not valid: ' + z_type)
#             # 
#             self._init_plotting()
#             
#             map_width_km = 1500
#             map_height_km = 1500
#             map_centre_lat = 60.0
#             map_centre_lon = 15.0
#             
#             #
#             subplot = self._figure.add_subplot(111)
#             #
#             m = basemap.Basemap(width = map_width_km * 1000,
#                                 height = map_height_km * 1000,
#                                 resolution = 'l', # Can be c (crude), l (low), i (intermediate), h (high), f (full) or None.
#                                 projection = 'tmerc', # 'tmerc', 'aeqd', ...
#                                 lat_0 = map_centre_lat,
#                                 lon_0 = map_centre_lon,
#                                 ax = subplot)
#             # 
# #             m.drawmapboundary(fill_color = 'aqua')
#             m.drawcoastlines(linewidth = 0.33)
#             m.drawcountries(linewidth = 0.2)
#             m.fillcontinents(
# #                              color = [0.8, 0.8, 0.8], # 'coral', 
# #                              lake_color = 'aqua',
#                              alpha = 0.5) # Transparency.
#             #
#             m.drawparallels(numpy.arange(-0,89, 2.0), linewidth = 0.125, linestyle = '--')
#             m.drawmeridians(numpy.arange(-180,180, 2.0), linewidth = 0.125, linestyle = '--')
#             #
#             plotlist = self._data.get_plot_list()
#             #
#             for plotindex, plotdict in enumerate(plotlist):
#                 #
#                 x_array = plotdict['x_array']
#                 y_array = plotdict['y_array']
#                 z_array = plotdict['z_array']
#                 #
#                 x_longitude, y_latitude = m(y_array, x_array)
#                 #
#                 msc = m.scatter(x_longitude, y_latitude, c = z_array, s = 25, edgecolors = 'none')
#                 ### msc = m.scatter(x_longitude, y_latitude, s = z_array, edgecolors = 'none')
#                 #
#                 # TODO: Can't handle multiple plots with different min/max.
#                 cbar = m.colorbar(msc, fig = self._figure, ax = subplot)
#                 cbar.set_label(self._data.get_plot_data_info()['z_label'], size = 'medium')
#             #
#             self._finalize_plotting()
#         #
#         except Exception as e:
#             toolbox_utils.Logging().warning('GraphPlotter.MapChart: Plot skipped: %s" % (e.args[0]))
#             raise


#
# Test.
#
def graphplotter_test():
    """ """
    print('Graph plotter test...')
    #
#     graph = MapChart()
#     #
#     data = GraphPlotData(
#                 title = 'Map test", 
#                 x_type = 'float',
#                 x_label = 'x as longitude',
#                 y_type = 'float',
#                 y_label = 'y as latitude',
#                 z_type = 'float',
#                 z_label = 'z as value')
#     data.add_plot(
#                 plot_name = 'First plot", 
#                 x_array = [55.0, 55.2, 55.4, 55.6],
#                 y_array = [15.0, 15.1, 15.2, 15.3],
#                 z_array = [10.0, 100.0, 200.0, 500.0])
#     data.add_plot(
#                 plot_name = 'Second plot", 
#                 x_array = [58.0, 58.2, 58.4, 58.6],
#                 y_array = [15.0, 15.1, 15.2, 15.3],
#                 z_array = [10.0, 100.0, 200.0, 500.0])
#     data.add_plot(
#                 plot_name = 'Third plot", 
#                 x_array = [56.0, 56.2, 56.4, 56.6],
#                 y_array = [16.0, 16.1, 16.2, 16.3],
#                 z_array = [10.0, 100.0, 200.0, 500.0])
# 
#     graph.set_data(data)
#     graph.plot_chart(combined = True, y_log_scale = False)
# 
#     return

#    graph = LineChart()
#    graph = BarChart()
#    graph = ScatterChart()
#    graph = PieChart()
    graph = BoxPlotChart()
    #
    data = GraphPlotData(
                title = 'X as text', 
                x_type = 'text',
                x_label = 'x as text',
                y_type = 'float',
                y_label = 'y as float')
    data.add_plot(
                plot_name = 'First plot', 
                x_array = ['A', 'B', 'C', 'D', ],
                y_array = [7.0, 88.5, 900.3, 9000])
    data.add_plot(
                plot_name = 'Second plot', 
                x_array = ['C', 'D', 'E', 'F', ],
                y_array = [2006, 2006.5, 2060.5, 2006])
    data.add_plot(
                plot_name = 'Third plot', 
                x_array = ['C', 'D', 'E', 'F', ],
                y_array = [1006, 1006.5, 3060.5, 1006])
    data.add_plot(
                plot_name = 'Fourth plot', 
                x_array = ['C', 'D', 'E', 'F', ],
                y_array = [3006, 3006.5, 3060.5, 3006])

    graph.set_data(data)
    graph.plot_chart(combined = False, y_log_scale = True)
    graph.plot_chart(combined = True, y_log_scale = True, stacked = False)
    graph.plot_chart(combined = True, y_log_scale = True, stacked = True)
    

    #return


    data = GraphPlotData(
                title = 'Y array only', 
                y_type = 'integer',
                y_label = 'y as integer')
    data.add_plot(
                plot_name = 'First plot', 
                y_array = [7, 88, 900, 9000])
    data.add_plot(
                plot_name = 'Second plot', 
                y_array = [2006, 2006, 20060, 2006])

    graph.set_data(data)
    graph.plot_chart(combined = False, y_log_scale = True)
    graph.plot_chart(combined = True, y_log_scale = True, stacked = False)
    graph.plot_chart(combined = True, y_log_scale = True, stacked = True)
    
    data = GraphPlotData(
                title = 'Y array only', 
                x_label = 'Autogenerated',
                y_type = 'float',
                y_label = 'y as float')
    data.add_plot(
                plot_name = 'First plot', 
                x_label = 'autogenerated',
                y_array = [7.0, 88.5, 900.3, 9000])
    data.add_plot(
                plot_name = 'Second plot', 
                x_label = 'autogenerated',
                y_array = [2006, 2006.5, 20060.5, 2006])

    graph.set_data(data)
    graph.plot_chart(combined = False, y_log_scale = True)
    graph.plot_chart(combined = True, y_log_scale = True, stacked = False)
    graph.plot_chart(combined = True, y_log_scale = True, stacked = True)
    
    data = GraphPlotData(
                        title = 'X as datetime', 
                        x_type = 'datetime',
                        x_label = 'x datetime',
                        y_type = 'integer',
                        y_label = 'y as integer')
    data.add_plot(plot_name = 'First plot', 
                        x_array = ['2012-03-07', '2012-04-01', '2012-05-10', '2012-06-20'], 
                        y_array = [2,4,1,9], 
                        x_label = 'xxx',
                        y_label = 'yyy')
    data.add_plot(plot_name = 'Second plot', 
                        x_array = ['2012-01-01', '2012-02-01', '2012-03-21', '2012-04-01', '2012-05-01', '2012-06-01', '2012-07-01', '2012-08-01'], 
                        y_array = [2,3,2,4,1,9,2,1], 
                        x_label = 'xxxxxx',
                        y_label = 'yyyyyy')

    graph.set_data(data)
    graph.plot_chart(combined = False, y_log_scale = True)
    graph.plot_chart(combined = True, y_log_scale = True, stacked = False)
    graph.plot_chart(combined = True, y_log_scale = True, stacked = True)

    
#     data_1.add_plot(
#                 plot_name = '1 plot", 
#                 y_array = [7.0, float('nan'), 88.0, 900.0, 9000.0], 
#                 y_label = 'Y first')
#     data_1.add_plot(
#                 plot_name = '2 plot", 
#                 y_array = [2006.0, 2006.0, 2006.0, 'nan', 2006.0], 
#                 y_label = 'Y first')
#     data_1.add_plot(
#                 plot_name = '3 plot", 
#                 y_array = [2006.0, 'NaN', 2006.0, 2006.0, 2006.0], 
#                 y_label = 'Y first')
#     data_1.add_plot(
#                 plot_name = '4 plot", 
#                 y_array = [2006.0, 2006.0, None, 2006.0, 2006.0], 
#                 y_label = 'Y first')
# 
#     graph = LineChart(plotdata_0)
#     graph.plot_chart(combined = False, y_log_scale = True)
#     graph.plot_chart(combined = True, y_log_scale = True)
#     
#     graph = PieChart(plotdata_0)
#     graph.plot_chart(combined = False)
    



#    plotdata_0 = GraphPlotData(
#                        title = 'One variable data object", 
#                        x_label = 'X (one variable)',
#                        y_label = 'Y (one variable)')
#
#    plotdata_0.add_plot(plot_name = '1 plot", 
#                        y_array = [7.0, float('nan'), 88.0, 900.0, 9000.0], 
#                        y_label = 'Y first')
#    plotdata_0.add_plot(plot_name = '2 plot", 
#                        y_array = [2006.0, 2006.0, 2006.0, 'nan', 2006.0], 
#                        y_label = 'Y first')
#    plotdata_0.add_plot(plot_name = '3 plot", 
#                        y_array = [2006.0, 'NaN', 2006.0, 2006.0, 2006.0], 
#                        y_label = 'Y first')
#    plotdata_0.add_plot(plot_name = '4 plot", 
#                        y_array = [2006.0, 2006.0, None, 2006.0, 2006.0], 
#                        y_label = 'Y first')
#
#    graph = LineChart(plotdata_0)
#    graph.plot_chart(combined = False, y_log_scale = True)
#    graph.plot_chart(combined = True, y_log_scale = True)
#    
#    graph = PieChart(plotdata_0)
#    graph.plot_chart(combined = False)
    
#     plotdata_1 = GraphPlotData(
#                         title = 'One variable data object", 
#                         x_label = 'X (one variable)',
#                         y_label = 'Y (one variable)')
#     
#     plotdata_1.add_plot(plot_name = 'First plot", 
#                         y_array = [2,3,2,4,1,9], 
#                         y_label = 'Y first')
#     plotdata_1.add_plot(plot_name = 'Second plot", 
#                         y_array = [1,2,3], 
#                         y_label = 'Y second')
#     plotdata_1.add_plot(plot_name = 'Third plot", 
#                         y_array = [12,10,6,3,9], 
#                         y_label = 'Y third')
#     #
#     plotdata_2 = GraphPlotData(
#                         title = 'Two variables data object", 
#                         x_label = 'X (two variable)',
#                         y_label = 'Y (two variable)')
#     plotdata_2.add_plot(plot_name = 'First plot", 
#                         x_array = [1,2,5,6,7,8], 
#                         y_array = [2,3,2,4,1,9], 
#                         x_label = 'X first',
#                         y_label = 'Y first')
#     plotdata_2.add_plot(plot_name = 'Second plot", 
#                         x_array = [4,5,6,7,8,9,10,11], 
#                         y_array = [2,3,2,4,1,9,2,1], 
#                         x_label = 'X second',
#                         y_label = 'Y second')
#     #
#     plotdata_3 = GraphPlotData(
#                         title = 'Three variables data object", 
#                         x_label = 'X (three variable)',
#                         y_label = 'Y (three variable)',
#                         z_label = 'Z (three variable)')
#     plotdata_3.add_plot(plot_name = 'First plot", 
#                         x_array = [1,2,5,6,7,8], 
#                         y_array = [20,30,20,40,10,90], 
#                         z_array = [10,10,80,20,30,30], 
#                         x_label = 'X First',
#                         y_label = 'Y First',
#                         z_label = 'Z First')
#     plotdata_3.add_plot(plot_name = 'Second plot", 
#                         x_array = [1,2,5,6,7,8], 
#                         y_array = [2,3,2,4,1,9], 
#                         z_array = [10,10,20,20,30,30], 
#                         x_label = 'X Second',
#                         y_label = 'Y Second',
#                         z_label = 'Z Second')
#     plotdata_3.add_plot(plot_name = 'Third plot", 
#                         x_array = [10,20,50,60,70,80], 
#                         y_array = [2,3,2,4,1,9], 
#                         z_array = [10,60,20,90,30,30], 
#                         x_label = 'X Third',
#                         y_label = 'Y Third',
#                         z_label = 'Z Third')
#     #
#     plotdata_4 = GraphPlotData(
#                         x_type = 'String',
#                         title = 'Two variables data object, string", 
#                         x_label = 'X (two variables)',
#                         y_label = 'Y (two variables)')
#     plotdata_4.add_plot(plot_name = 'Dinophysis acuta", 
#                         x_array = ['BY15','Släggö','cc','dd','ee'], 
#                         y_array = [10,30,5,5,1], 
#                         x_label = 'X First',
#                         y_label = 'Y First')
#     plotdata_4.add_plot(plot_name = 'Second plot", 
#                         x_array = ['cc','dd','ee','ff', 'gg', 'hh'], 
#                         y_array = [2,3,2,4,1,9], 
#                         x_label = 'X Second',
#                         y_label = 'Y Second')
#     plotdata_4.add_plot(plot_name = 'Third plot", 
#                         x_array = ['AA','BB','cc','dd','ee','ff'], 
#                         y_array = [5,5,5,1,2,3], 
#                         x_label = 'X Third',
#                         y_label = 'Y Third')
#     #
#     plotdata_5 = GraphPlotData(
#                         x_type = 'date',
#                         title = 'Two variables x:date", 
#                         x_label = 'X (date)',
#                         y_label = 'Y (two variable)')
#     plotdata_5.add_plot(plot_name = 'First plot", 
#                         x_array = ['2012-03-07', '2012-04-01', '2012-05-10', '2012-06-20'], 
#                         y_array = [2,4,1,9], 
#                         x_label = 'X first (date)',
#                         y_label = 'Y first')
#     plotdata_5.add_plot(plot_name = 'Second plot", 
#                         x_array = ['2012-01-01', '2012-02-01', '2012-03-21', '2012-04-01', '2012-05-01', '2012-06-01', '2012-07-01', '2012-08-01'], 
#                         y_array = [2,3,2,4,1,9,2,1], 
#                         x_label = 'X second (date)',
#                         y_label = 'Y second')
#     #
#     #
#     graph = LineChart(plotdata_1)
#     graph.plot_chart(combined = True, y_log_scale = True)
#     graph.plot_chart(combined = False, y_log_scale = True)
#     #
#     #
#     graph = LineChart(plotdata_2)
#     graph.plot_chart(combined = True, y_log_scale = True)
#     graph.plot_chart(combined = False, y_log_scale = True)
#     #
#     #
#     graph = BarChart(plotdata_2)
#     graph.plot_chart(combined = True, y_log_scale = False)
#     graph.plot_chart(combined = True, y_log_scale = False, stacked = True)
#     graph.plot_chart(combined = False, y_log_scale = True)
#     graph.plot_chart(combined = False, y_log_scale = True, stacked = True)
#     #
#     #
#     graph = ScatterChart(plotdata_2)
#     graph.plot_chart(combined = True, y_log_scale = False)
#     graph.plot_chart(combined = False, y_log_scale = True)
#     #
#     #
#     graph = ScatterChart(plotdata_3)
#     graph.plot_chart(combined = True, y_log_scale = False)
#     graph.plot_chart(combined = False, y_log_scale = True)
#     #
#     #
#     graph = BarChart(plotdata_4)
#     graph.plot_chart(combined = True, y_log_scale = False)
#     graph.plot_chart(combined = True, y_log_scale = False, stacked = True)
#     graph.plot_chart(combined = True, y_log_scale = False)
#     graph.plot_chart(combined = True, y_log_scale = False, stacked = True)
#     graph.plot_chart(combined = False, y_log_scale = False)
#     graph.plot_chart(combined = False, y_log_scale = False, stacked = True)
#     #
#     graph = PieChart(plotdata_2)
#     graph.plot_chart(combined = False, y_log_scale = False)
#     #
#     graph = PieChart(plotdata_4)
#     graph.plot_chart(combined = False, y_log_scale = False)
#     #
#     graph = LineChart(plotdata_5)
#     graph.plot_chart(combined = True, y_log_scale = True)
#     graph.plot_chart(combined = False, y_log_scale = True)

                
if __name__ == "__main__":
    graphplotter_test()

