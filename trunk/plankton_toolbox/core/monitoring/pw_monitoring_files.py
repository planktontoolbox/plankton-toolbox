#!/usr/bin/env python
# -*- coding:iso-8859-1 -*-
#
# Project: Plankton toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010 SMHI, Swedish Meteorological and Hydrological Institute 
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

"""

"""

import codecs

class MonitoringFiles(object):
    """ 
    """
    def __init__(self):
        """ """
        self._metadata = {} # Metadata for the dataset.
        
class PwCsv(MonitoringFiles):
    """ 
    """
    def __init__(self):
        """ """
        super(PwCsv, self).__init__()
        self._sample = {} # Information related to sample.
        self._data = {} # Data set containing header and rows.
        self._aggregated_data = {} # Precalculated aggregations of data.

    def importFile(self, fileName = None, encoding = 'utf-8'):
        """ """
        if fileName == None:
            raise UserWarning('File name is missing.')
        file = None
        try:
            file = codecs.open(fileName, mode = 'r', encoding = 'iso-8859-1')
            separator = ',' # Use ',' as item separator.
            
            # Read data header. Same header used for data and aggregated data.
            self._data['header'] = []
            self._aggregated_data['header'] = []
            for headeritem in file.readline().split(separator):
                item = headeritem.strip().strip('"').strip()
                self._data['header'].append(item)
                self._aggregated_data['header'].append(item)
                
            # Empty line.
            file.readline()
            
            # Read data rows. Continue until empty line occurs.
            self._data['rows'] = []
            row = file.readline()
            while len(row.strip()) > 0:
                rowitems = []
                for item in row.split(separator):
                    rowitems.append(item.strip().strip('"').strip())
                self._data['rows'].append(rowitems) 
                row = file.readline()
            
            # Read aggregated data rows. Continue until empty line occurs.
            self._aggregated_data['rows'] = []
            row = file.readline()
            while len(row.strip()) > 0:
                rowitems = []
                for item in row.split(separator):
                    rowitems.append(item.strip().strip('"').strip())
                self._aggregated_data['rows'].append(rowitems) 
                row = file.readline()
                         
            # Read total counted.
            row = file.readline() # Not used...TODO
            row = file.readline() # Empty.
            
            # Read total counted.
            row = file.readline() # Not used...TODO
            row = file.readline() # Empty.
            
            # Read champer and magnification info.
#            self._aggregated_data['rows'] = []
            row = file.readline()
            while len(row.strip()) > 0:
                rowitems = []
                for item in row.split(separator):
                    rowitems.append(item.strip().strip('"').strip())
#                self._aggregated_data['rows'].append(rowitems) # Not used...TODO 
                row = file.readline()
                         
            # Read info related to sample.
            row = file.readline()
            while len(row.strip()) > 0:
                key, value = row.split(separator)
                self._sample[key.strip().strip('"').strip()] = value.strip().strip('"').strip()
                row = file.readline()
                
        except (IOError, OSError):
            raise
        finally:
            if file: file.close()

    def exportAsJson(self, file = None, encoding = 'utf-8'):
        """ """
        if file == None:
            raise UserWarning('File name is missing.')
        outdata = open(file, 'w')
        
        jsonexport = {}
        jsonexport['metadata'] = {}
        jsonexport['sample'] = self._sample
        jsonexport['data'] = self._data
        jsonexport['aggregated_data'] = self._aggregated_data
        outdata.write(json.dumps(jsonexport, encoding = encoding, 
                                 sort_keys=True, indent=4))
# OLD:        
#        outdata.write(json.dumps(self._taxaObject.getTaxonList(), 
#                                 encoding = encoding, sort_keys=True, indent=4))
        outdata.close()
