#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2011-2012 SMHI, Swedish Meteorological and Hydrological Institute 
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

class ParsedFormat(envmonlib.FormatBase):
    """ """
    def __init__(self):
        """ Abstract class for parsed import formats. """
        super(ParsedFormat, self).__init__()
        #
        self._parsercommands = []
    
    def replaceMethodKeywords(self, parse_command, node_level = None):
        """ """
        command = parse_command
        #
        command = command.replace(u'$Text(', u'self._asText(')
        command = command.replace(u'$Float(', u'self._asFloat(')
        command = command.replace(u'$Species(', u'self._speciesByKey(')
        command = command.replace(u'$Sizeclass(', u'self._sizeclassByKey(')
        command = command.replace(u'$PlanktonGroup(', u'self._planktonGroup(')
        #
        if node_level == u'FUNCTION Sample':
            command = command.replace(u'$CreateVariable(', u'self._createVariable(currentsample, ')
        if node_level == u'FUNCTION Variable':
            command = command.replace(u'$CopyVariable(', u'self._copyVariable(currentvariable, ')
        ### TODO: Also replace:
        # $Text(   --> self._asText(
        # $Year(   --> self._asYear(
        # $Datetime(   --> self._asDatetime(
        # $Date(   --> self._asDate(
        # $Time(   --> self._asTime(
        # $Int(   --> self._asInt(
        # $Float(   --> self._asFloat(
        # $Position(   --> self._asPosition(
        # $Station(   --> self._asStation(
        # $Param(   --> self._asParam(
        #
        return command
        
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
        return envmonlib.Species().getTaxonValue(taxon_name, key)

    def _sizeclassByKey(self, taxon_name, size_class, key):
        """ """
        return envmonlib.Species().getBvolValue(key, taxon_name, size_class)

    def _planktonGroup(self, taxon_name):
        """ """
        return envmonlib.Species().getPlanktonGroupFromTaxonName(taxon_name)

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


