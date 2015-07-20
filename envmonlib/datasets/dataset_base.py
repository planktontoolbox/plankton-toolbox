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

class DatasetBase(object):
    def __init__(self):
        """ Base class for datasets, mainly used for metadata. """
        super(DatasetBase, self).__init__()
        self._metadata = {}
        
    def clear(self):
        """ """
        self._metadata = {}

    def getMetadata(self, key):
        """ """
        return self._metadata.get(key, '')

    def addMetadata(self, key, value):
        """ """
        self._metadata[key] = value

    def saveAsTextFile(self, file_name):
        """ """
        toolbox_utils.TextFiles().writeTableDataset(self, file_name)

    def saveAsExcelFile(self, file_name):
        """ """
        toolbox_utils.ExcelFiles().writeTableDataset(self, file_name)

