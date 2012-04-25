#!/usr/bin/env python
# -*- coding:utf-8 -*-

class GraphPlotBase(object):
    def __init__(self):
        """ Base class for  """
        super(GraphPlotBase, self).__init__()
        
        self._settings = {}
        
        self._plot_list = []
        
        
        
        time_table = None
        value_table = None
        
        
    def defaultSettings(self):
        """ """
        self._settings = {
            "Title": None,
            "X label": None,
            "Y label": None,
            "X min": None,
            "X max": None,
            "Y min": None,
            "Y max": None,
            "X log": False,
            "Y log": False,
#            "": ,
#            "": ,
            "Legend position": None,
            "Legend color map": None,
            "font": None,
            "Font size": None
                          
            }
    
    def clear(self):
        """ """
        self._settings = {}
        
    def addPlot(self,
                plot_type = None, # XP plot, Time series, Bar plot, ...
                  title = None,
                  x_label = None, 
                  y_label = None, 
                 
                ):
        """ """
        
    def removePlot(self, axis_index = None):
        """ """
        
    def SetLegend(self, 
                  axis_list = None):
                  axis_list = None):
                  axis_list = None):
        """ """
             
    def updateSettings(self, **kwargs):
        """ """
        
    def getSettins(self):
        """ """
             
class TimeSeriesPlot(GraphPlotBase):
    def __init__(self):
        """ Base class for  """
        super(TimeSeriesPlot, self).__init__()
        
class XYPlot(GraphPlotBase):
    def __init__(self):
        """ Base class for  """
        super(XYPlot, self).__init__()
        
class BarPlot(GraphPlotBase):
    def __init__(self):
        """ Base class for  """
        super(BarPlot, self).__init__()
        
                

