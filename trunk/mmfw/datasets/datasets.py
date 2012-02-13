#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Moray
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2011 SMHI, Swedish Meteorological and Hydrological Institute 
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

import mmfw

@mmfw.singleton
class Datasets(object):
    """ Singleton object used to hold a list of datasets. """
    
    def __init__(self):
        """ """
        self.__datasets = [] 

    def clear(self):
        """ """
        self.__datasets = []
        
    def getDatasets(self):
        """ """
        return self.__datasets 
        
    def getDatasetByIndex(self, index):
        """ """
        if len(self.__datasets) > index:
            return self.__datasets[index]
        return None 
        
    def addDataset(self, dataset_node):
        """ """
        self.__datasets.append(dataset_node)
        
    def removeDatasetByIndex(self, index):
        """ """
        if (index >= 0) or (len(self.__datasets) > index):
            del self.__datasets[index]

