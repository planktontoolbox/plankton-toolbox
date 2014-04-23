#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2011-2013 SMHI, Swedish Meteorological and Hydrological Institute 
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

import dateutil.parser
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
        command = command.replace(u'$Integer(', u'self._asInteger(')
        command = command.replace(u'$Float(', u'self._asFloat(')
        command = command.replace(u'$Date(', u'self._asDate(')
        command = command.replace(u'$Species(', u'self._speciesByKey(')
        command = command.replace(u'$Sizeclass(', u'self._sizeclassByKey(')
        command = command.replace(u'$PlanktonGroup(', u'self._planktonGroup(')
        #
        if node_level == u'function_sample':
            command = command.replace(u'$CreateVariable(', u'self._createVariable(currentsample, ')
        if node_level == u'function_variable':
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
        commanddict[u'command_string'] = command_string
        commanddict[u'command'] = compile(command_string, '', 'exec')
        self._parsercommands.append(commanddict)
    
    def _asText(self, column_name):
        """ """
        if column_name in self._header:
            index = self._header.index(column_name)
            return self._row[index] if len(self._row) > index else u''
        else:
            return u''

    def _asInteger(self, column_name):
        """ """
        if column_name in self._header:
            index = self._header.index(column_name)
            if len(self._row) > index:
                try:
                    value = self._row[index]
                    value = value.replace(u' ', u'').replace(u',', u'.')
                    return int(round(float(value)))
                except:
                    envmonlib.Logging().warning(u"Parser: Failed to convert to integer: " + self._row[index])
                    return self._row[index]
#                except Exception as e:
#                    print(u"Parser: Failed to convert to integer: %s" % (e.args[0]))                
#                    return self._row[index]
        return u''

    def _asFloat(self, column_name):
        """ """
        if column_name in self._header:
            index = self._header.index(column_name)
            if len(self._row) > index:
                try:
                    value = self._row[index]
                    if value == '':
                        return u''
                    value = value.replace(u' ', u'').replace(u',', u'.')
                    return float(value)
                except:
                    envmonlib.Logging().warning(u"Parser: Failed to convert to float: " + self._row[index])
                    return self._row[index]
        return u''

    def _asDate(self, column_name):
        """ Reformat to match the ISO format. (2000-01-01) """
        if column_name in self._header:
            index = self._header.index(column_name)
            if len(self._row) > index:
                try:
                    value = dateutil.parser.parse(self._row[index])
#                    value = value
                    return value.strftime(u'%Y-%m-%d')
                except:
                    envmonlib.Logging().warning(u"Parser: Failed to convert to float: " + self._row[index])
                    return self._row[index]
        return u''

    def _speciesByKey(self, taxon_name, key):
        """ """
        return envmonlib.Species().getTaxonValue(taxon_name, key)

    def _sizeclassByKey(self, taxon_name, size_class, key):
        """ """
        return envmonlib.Species().getBvolValue(taxon_name, size_class, key)

    def _planktonGroup(self, taxon_name):
        """ """
        return envmonlib.Species().getPlanktonGroupFromTaxonName(taxon_name)

    def _toStation(self, current_node, station_name, **kwargs):
        """ """
        # TODO: For test:
        current_node.addData(u'station_name', station_name)

    def _toPosition(self, current_node, latitude, longitude, **kwargs):
        """ """
#        print(u'DEBUG: _toPosition: ' + latitude + u' ' + longitude)

    def _createVariable(self, current_node, **kwargs):
        """ """
        if isinstance(current_node, envmonlib.VisitNode):
            newsample = envmonlib.SampleNode()
            current_node.addChild(newsample)
            variable = envmonlib.VariableNode()
            newsample.addChild(variable)
            variable.addData(u'parameter', kwargs[u'p'])    
            variable.addData(u'value', kwargs[u'v'])
            #variable.addData(u'value_float', kwargs[u'v'])    
            variable.addData(u'unit', kwargs[u'u'])    
        if isinstance(current_node, envmonlib.SampleNode):
            variable = envmonlib.VariableNode()
            current_node.addChild(variable)
            variable.addData(u'parameter', kwargs[u'p'])    
            variable.addData(u'value', kwargs[u'v'])    
            #variable.addData(u'value_float', kwargs[u'v'])    
            variable.addData(u'unit', kwargs[u'u'])    

    def _copyVariable(self, current_node, **kwargs):
        """ """
        if isinstance(current_node, envmonlib.VariableNode):
            variable = current_node.clone()
            variable.addData(u'parameter', kwargs[u'p'])    
            variable.addData(u'value', kwargs[u'v'])    
            #variable.addData(u'value_float', kwargs[u'v'])    
            variable.addData(u'unit', kwargs[u'u'])    

    def _modifyVariable(self, current_node, **kwargs):
        """ """
        if isinstance(current_node, envmonlib.VariableNode):
            current_node.addData(u'parameter', kwargs[u'p'])    
            current_node.addData(u'value', kwargs[u'v'])
            #current_node.addData(u'value_float', kwargs[u'v'])    
            current_node.addData(u'unit', kwargs[u'u'])    

