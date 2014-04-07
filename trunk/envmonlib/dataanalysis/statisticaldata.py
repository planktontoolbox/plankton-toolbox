#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

# import envmonlib

class StatisticalData(object):
    """
    Should contain table oriented data, see envmonlib.DatasetTable().
    """
    def __init__(self):
        """ """
        self._data = None
        # Initialize parent.
        super(StatisticalData, self).__init__()

    def clearData(self):
        """ """
        self._data = None
        
    def setData(self, analysisdata):
        """ """
        self._data = analysisdata
        
    def getData(self):
        """ """
        return self._data
    

