#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import dateutil.parser
import envmonlib

class ParsedFormat(envmonlib.FormatBase):
    """ """
    def __init__(self):
        """ Abstract class for parsed import formats. """
        super(ParsedFormat, self).__init__()
        #
        self._parsercommands = []
    
    def replaceMethodKeywords(self, parse_command, node_level = None, view_format = None):
        """ Mapping between Excel parser code and python code."""
        command = unicode(parse_command.strip())
        #
        if u'Column:' in command:
            # An easier notation for "$Text('Example column')": "Column:Example column".
            # For simple column name mapping based on the format column.
            command = unicode(command.replace(u'Column:', u'').strip())
            if view_format is None:
                command = u"self._asText(u'" + command + u"')"
            elif view_format == u'text':
                command = u"self._asText(u'" + command + u"')"
            elif view_format == u'integer':
                command = u"self._asInteger(u'" + command + u"')"
            elif view_format == u'float':
                command = u"self._asFloat(u'" + command + u"')"
            elif view_format == u'date':
                command = u"self._asDate(u'" + command + u"')"
            else:
                command = u"self._asText(" + command + u")"
        #
        elif u'$' in command:
            # Mapping for more advanced alternatives.
            command = command.replace(u'$Text(', u'self._asText(')
            command = command.replace(u'$Integer(', u'self._asInteger(')
            command = command.replace(u'$Float(', u'self._asFloat(')
            command = command.replace(u'$Date(', u'self._asDate(')
            command = command.replace(u'$Species(', u'self._speciesByKey(')
            command = command.replace(u'$Sizeclass(', u'self._sizeclassByKey(')
            command = command.replace(u'$SizeClass(', u'self._sizeclassByKey(') # Alternative spelling
            command = command.replace(u'$PlanktonGroup(', u'self._planktonGroup(')
#         else:
#             # For hard-coded values.
#             command = u"'" + unicode(command.strip()) + u"'"
        
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
        
        # For development:
        print(u'Parser command: ' + command_string)
        
        self._parsercommands.append(commanddict)
    
    def _asText(self, column_name):
        """ To be called from Excel-based parser. """
        column_name = unicode(column_name)
        if column_name in self._header:
            index = self._header.index(column_name)
            return self._row[index] if len(self._row) > index else u''
        else:
            return u''

    def _asInteger(self, column_name):
        """ To be called from Excel-based parser. """
        column_name = unicode(column_name)
        if column_name in self._header:
            index = self._header.index(column_name)
            if len(self._row) > index:
                try:
                    value = self._row[index]
                    if value:
                        value = value.replace(u' ', u'').replace(u',', u'.')
                        return int(round(float(value)))
                except:
                    envmonlib.Logging().warning(u"Parser: Failed to convert to integer: " + self._row[index])
                    return self._row[index]
        return u''

    def _asFloat(self, column_name):
        """ To be called from Excel-based parser. """
        column_name = unicode(column_name)
        if column_name in self._header:
            index = self._header.index(column_name)
            if len(self._row) > index:
                try:
                    value = self._row[index]
                    if value:
                        value = value.replace(u' ', u'').replace(u',', u'.')
                        return float(value)
                except:
                    envmonlib.Logging().warning(u"Parser: Failed to convert to float: " + self._row[index])
                    return self._row[index]
        return u''

    def _asDate(self, column_name):
        """ Reformat to match the ISO format. (2000-01-01)
        To be called from Excel-based parser. """
        column_name = unicode(column_name)
        if column_name in self._header:
            index = self._header.index(column_name)
            if len(self._row) > index:
                try:
                    value = dateutil.parser.parse(self._row[index])
                    if value:
                        return value.strftime(u'%Y-%m-%d')
                except:
                    envmonlib.Logging().warning(u"Parser: Failed to convert to date: " + self._row[index])
                    return self._row[index]
        return u''

    def _speciesByKey(self, scientific_name, key):
        """ To be called from Excel-based parser. """
        scientific_name = unicode(scientific_name)
        key = unicode(key)
        return envmonlib.Species().getTaxonValue(scientific_name, key)

    def _sizeclassByKey(self, scientific_name, size_class, key):
        """ To be called from Excel-based parser. """
        scientific_name = unicode(scientific_name)
        key = unicode(key)
        size_class = unicode(size_class)
        value = envmonlib.Species().getBvolValue(scientific_name, size_class, key)
        if value:
            return value
        return u''

    def _planktonGroup(self, scientific_name):
        """ To be called from Excel-based parser. """
        scientific_name = unicode(scientific_name)
        return envmonlib.Species().getPlanktonGroupFromTaxonName(scientific_name)

    def _toStation(self, current_node, station_name, **kwargs):
        """ To be called from Excel-based parser. """
        # TODO: For test:
        station_name = unicode(station_name)
        current_node.addData(u'station_name', station_name)

    def _toPosition(self, current_node, latitude, longitude, **kwargs):
        """ To be called from Excel-based parser. """
        latitude = unicode(latitude)
        longitude = unicode(longitude)
#        print(u'DEBUG: _toPosition: ' + latitude + u' ' + longitude)

    def _createVariable(self, current_node, **kwargs):
        """ To be called from Excel-based parser. """
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
        """ To be called from Excel-based parser. """
        if isinstance(current_node, envmonlib.VariableNode):
            variable = current_node.clone()
            variable.addData(u'parameter', kwargs[u'p'])    
            variable.addData(u'value', kwargs[u'v'])    
            #variable.addData(u'value_float', kwargs[u'v'])    
            variable.addData(u'unit', kwargs[u'u'])    

    def _modifyVariable(self, current_node, **kwargs):
        """ To be called from Excel-based parser. """
        if isinstance(current_node, envmonlib.VariableNode):
            current_node.addData(u'parameter', kwargs[u'p'])    
            current_node.addData(u'value', kwargs[u'v'])
            #current_node.addData(u'value_float', kwargs[u'v'])    
            current_node.addData(u'unit', kwargs[u'u'])    


