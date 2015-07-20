#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import dateutil.parser
# import envmonlib
import toolbox_utils
import toolbox_core

class ParsedFormat(toolbox_utils.FormatBase):
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
        if 'Column:' in command:
            # An easier notation for "$Text('Example column')": "Column:Example column".
            # For simple column name mapping based on the format column.
            command = unicode(command.replace('Column:', '').strip())
            if view_format is None:
                command = 'self._asText("' + command + '")'
            elif view_format == 'text':
                command = 'self._asText("' + command + '")'
            elif view_format == 'integer':
                command = 'self._asInteger("' + command + '")'
            elif view_format == 'float':
                command = 'self._asFloat("' + command + '")'
            elif view_format == 'date':
                command = 'self._asDate("' + command + '")'
            else:
                command = 'self._asText("' + command + '")'
        #
        elif '$' in command:
            # Mapping for more advanced alternatives.
            command = command.replace('$Text(', 'self._asText(')
            command = command.replace('$Integer(', 'self._asInteger(')
            command = command.replace('$Float(', 'self._asFloat(')
            command = command.replace('$Date(', 'self._asDate(')
            command = command.replace('$Species(', 'self._speciesByKey(')
            command = command.replace('$Sizeclass(', 'self._sizeclassByKey(')
            command = command.replace('$SizeClass(', 'self._sizeclassByKey(') # Alternative spelling
            command = command.replace('$PlanktonGroup(', 'self._planktonGroup(')
#         else:
#             # For hard-coded values.
#             command = ''' + unicode(command.strip()) + ''"
        
        #
        if node_level == 'function_sample':
            command = command.replace('$CreateVariable(', 'self._createVariable(currentsample, ')
        if node_level == 'function_variable':
            command = command.replace('$CopyVariable(', 'self._copyVariable(currentvariable, ')
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
        commanddict['command_string'] = command_string
        commanddict['command'] = compile(command_string, '', 'exec')
        
        # For development:
        print('Parser command: ' + command_string)
        
        self._parsercommands.append(commanddict)
    
    def _asText(self, column_name):
        """ To be called from Excel-based parser. """
        column_name = unicode(column_name)
        if column_name in self._header:
            index = self._header.index(column_name)
            return self._row[index] if len(self._row) > index else ''
        else:
            return ''

    def _asInteger(self, column_name):
        """ To be called from Excel-based parser. """
        column_name = unicode(column_name)
        if column_name in self._header:
            index = self._header.index(column_name)
            if len(self._row) > index:
                try:
                    value = self._row[index]
                    if value:
                        value = value.replace(' ', '').replace(',', '.')
                        return int(round(float(value)))
                except:
                    toolbox_utils.Logging().warning('Parser: Failed to convert to integer: ' + self._row[index])
                    return self._row[index]
        return ''

    def _asFloat(self, column_name):
        """ To be called from Excel-based parser. """
        column_name = unicode(column_name)
        if column_name in self._header:
            index = self._header.index(column_name)
            if len(self._row) > index:
                try:
                    value = self._row[index]
                    if value:
                        value = value.replace(' ', '').replace(',', '.')
                        return float(value)
                except:
                    toolbox_utils.Logging().warning('Parser: Failed to convert to float: ' + self._row[index])
                    return self._row[index]
        return ''

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
                        return value.strftime('%Y-%m-%d')
                except:
                    toolbox_utils.Logging().warning('Parser: Failed to convert to date: ' + self._row[index])
                    return self._row[index]
        return ''

    def _speciesByKey(self, scientific_name, key):
        """ To be called from Excel-based parser. """
        scientific_name = unicode(scientific_name)
        key = unicode(key)
        return toolbox_utils.Species().getTaxonValue(scientific_name, key)

    def _sizeclassByKey(self, scientific_name, size_class, key):
        """ To be called from Excel-based parser. """
        scientific_name = unicode(scientific_name)
        key = unicode(key)
        size_class = unicode(size_class)
        value = toolbox_utils.Species().getBvolValue(scientific_name, size_class, key)
        if value:
            return value
        return ''

    def _planktonGroup(self, scientific_name):
        """ To be called from Excel-based parser. """
        scientific_name = unicode(scientific_name)
        return toolbox_utils.Species().getPlanktonGroupFromTaxonName(scientific_name)

    def _toStation(self, current_node, station_name, **kwargs):
        """ To be called from Excel-based parser. """
        # TODO: For test:
        station_name = unicode(station_name)
        current_node.addData('station_name', station_name)

    def _toPosition(self, current_node, latitude, longitude, **kwargs):
        """ To be called from Excel-based parser. """
        latitude = unicode(latitude)
        longitude = unicode(longitude)
#        print('DEBUG: _toPosition: ' + latitude + ' ' + longitude)

    def _createVariable(self, current_node, **kwargs):
        """ To be called from Excel-based parser. """
        if isinstance(current_node, toolbox_utils.VisitNode):
            newsample = toolbox_utils.SampleNode()
            current_node.addChild(newsample)
            variable = toolbox_utils.VariableNode()
            newsample.addChild(variable)
            variable.addData('parameter', kwargs['p'])    
            variable.addData('value', kwargs['v'])
            #variable.addData('value_float', kwargs['v'])    
            variable.addData('unit', kwargs['u'])    
        if isinstance(current_node, toolbox_utils.SampleNode):
            variable = toolbox_utils.VariableNode()
            current_node.addChild(variable)
            variable.addData('parameter', kwargs['p'])    
            variable.addData('value', kwargs['v'])    
            #variable.addData('value_float', kwargs['v'])    
            variable.addData('unit', kwargs['u'])    

    def _copyVariable(self, current_node, **kwargs):
        """ To be called from Excel-based parser. """
        if isinstance(current_node, toolbox_utils.VariableNode):
            variable = current_node.clone()
            variable.addData('parameter', kwargs['p'])    
            variable.addData('value', kwargs['v'])    
            #variable.addData('value_float', kwargs['v'])    
            variable.addData('unit', kwargs['u'])    

    def _modifyVariable(self, current_node, **kwargs):
        """ To be called from Excel-based parser. """
        if isinstance(current_node, toolbox_utils.VariableNode):
            current_node.addData('parameter', kwargs['p'])    
            current_node.addData('value', kwargs['v'])
            #current_node.addData('value_float', kwargs['v'])    
            current_node.addData('unit', kwargs['u'])    


