#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import envmonlib

@envmonlib.singleton
class Datasets(object):
    """ Singleton object used to hold a list of datasets. """
    
    def __init__(self):
        """ """
        self._datasets = [] 

    def clear(self):
        """ """
        self._datasets = []
        
    def getDatasets(self):
        """ """
        return self._datasets 
        
    def getDatasetByIndex(self, index):
        """ """
        if len(self._datasets) > index:
            return self._datasets[index]
        return None 
        
    def addDataset(self, dataset_node):
        """ """
        self._datasets.append(dataset_node)
        
    def removeDatasetByIndex(self, index):
        """ """
        if (index >= 0) or (len(self._datasets) > index):
            del self._datasets[index]

