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
        self._row = None


    
    def parseTableDataset(self, dataset, imported_table):
        """ Abstract method. """
        
    def reorganizeDataset(self):
        """ """
        
    def reformatDataset(self):
        """ """
        
    def _setHeader(self, header):
        """ """
        self._header = header
        
    def _setRow(self, row):
        """ """
        self._row = row
        
    def _asText(self, column_name):
        """ """
        if column_name in self._header:
            index = self._header.index(column_name)
            return self._row[index] if len(self._row) > index else u''
        else:
            return u''

    def _asFloat(self, column_name):
        """ """
        if column_name in self._header:
            index = self._header.index(column_name)
            if len(self._row) > index:
                try:
                    str = self._row[index]
                    str = str.replace(u' ', u'').replace(u',', u'.')
                    return float(str)
                except:
                    print(u"Failed to convert to float: " + self._row[index])
                    return None
        return None

