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

import envmonlib

class FormatBase(object):
    """ """
    def __init__(self):
        """ Abstract class for import formats. """
        super(FormatBase, self).__init__()
        #
        self._dataset = None
        self._header = []
        self._row = None
        self._parsercommands = []
    
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
        
    def appendParserCommand(self, command_string):
        """ """
        commanddict = {}
        commanddict[u'Command string'] = command_string
        commanddict[u'Command'] = compile(command_string, '', 'exec')
        self._parsercommands.append(commanddict)
    
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

    def _speciesByKey(self, taxon_name, key):
        """ """
        return envmonlib.Taxa().getTaxonValue(key, taxon_name)

    def _sizeclassByKey(self, taxon_name, size_class, key):
        """ """
#        # TODO: For test:
#        print("DEBUG: " + taxon_name)
        return envmonlib.Taxa().getSizeclassValue(key, taxon_name, size_class)

    def _toStation(self, current_node, station_name, **more):
        """ """
        # TODO: For test:
        current_node.addData(u'Station name', station_name)

    def _toPosition(self, current_node, latitude, longitude, **more):
        """ """
#        print(u'DEBUG: _toPosition: ' + latitude + u' ' + longitude)

    def _createVariable(self, current_node, **more):
        """ """
        if isinstance(current_node, envmonlib.VisitNode):
            newsample = envmonlib.SampleNode()
            current_node.addChild(newsample)
            variable = envmonlib.VariableNode()
            newsample.addChild(variable)
            variable.addData(u'Parameter', more[u'p'])    
            variable.addData(u'Value', unicode(more[u'v']))    
            #variable.addData(u'Value float', more[u'v'])    
            variable.addData(u'Unit', more[u'u'])    
        if isinstance(current_node, envmonlib.SampleNode):
            variable = envmonlib.VariableNode()
            current_node.addChild(variable)
            variable.addData(u'Parameter', more[u'p'])    
            variable.addData(u'Value', unicode(more[u'v']))    
            #variable.addData(u'Value float', more[u'v'])    
            variable.addData(u'Unit', more[u'u'])    

    def _copyVariable(self, current_node, **more):
        """ """
        if isinstance(current_node, envmonlib.VariableNode):
            variable = current_node.clone()
            variable.addData(u'Parameter', more[u'p'])    
            variable.addData(u'Value', unicode(more[u'v']))    
            #variable.addData(u'Value float', more[u'v'])    
            variable.addData(u'Unit', more[u'u'])    

    def _modifyVariable(self, current_node, **more):
        """ """
        if isinstance(current_node, envmonlib.VariableNode):
            current_node.addData(u'Parameter', more[u'p'])    
            current_node.addData(u'Value', unicode(more[u'v']))    
            #current_node.addData(u'Value float', more[u'v'])    
            current_node.addData(u'Unit', more[u'u'])    


