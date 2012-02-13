#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: 
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

class FormatBase(object):
    """ """
    def __init__(self):
        """ Abstract class for import formats. """
        super(FormatBase, self).__init__()
        #
        self._dataset = None
        self._header = []
        self._headerdict = {} # Name to index.
        self._row = None

    def importDataset(self, dataset, zipfile_name):
        """ Abstract method. """
        
    def reorganizeDataset(self):
        """ """
        
    def reformatDataset(self):
        """ """
        
    def basicScreening(self):
        """ """

    def setHeader(self, header):
        """ """
        self._header = header
        self._headerdict = {} # Name to index.
        for index, name in enumerate(header):
            self._headerdict[name] = index
        
    def asText(self, column_name):
        """ """
        if column_name in self._headerdict:
            return self._row[self._headerdict[column_name]]
        else:
            return u''

    def getSeparator(self, row):
        """ """
        if u'\t' in row: 
            return u'\t'
        elif u';' in row: 
            return u';' 


