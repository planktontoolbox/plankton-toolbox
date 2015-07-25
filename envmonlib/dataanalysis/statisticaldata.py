#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

# import envmonlib
import toolbox_utils
import toolbox_core

class StatisticalData(object):
    """
    Should contain table oriented data, see toolbox_core.DatasetTable().
    """
    def __init__(self):
        """ """
        self._data = None
        # Initialize parent.
        super(StatisticalData, self).__init__()

    def clear_data(self):
        """ """
        self._data = None
        
    def setData(self, analysisdata):
        """ """
        self._data = analysisdata
        
    def get_data(self):
        """ """
        return self._data
    

