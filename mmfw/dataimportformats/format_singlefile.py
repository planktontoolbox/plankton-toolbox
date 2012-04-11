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

class FormatSingleFile(mmfw.FormatBase):
    """ Import format for single file. """
    def __init__(self):
        """ Import format for single file. """
        super(FormatSingleFile, self).__init__()

    def parseTableDataset(self, dataset, imported_table):
        """ """
        self._dataset = dataset        
        #        
        importmatrixrows = dataset.getImportMatrixRows()
        #
        visitkeycommand = None
        samplekeycommand = None
#        variablekeycommand = None
        #
        try:
            for matrixrow in importmatrixrows:
                matrixnode = matrixrow.get(u'Node', u'') 
                matrixkey = matrixrow.get(u'Key', u'') 
                matrixcommand = matrixrow.get(u'Command', u'')
                if matrixcommand:         
                    #    
                    ### TODO: Replace:
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
                    matrixcommand = matrixcommand.replace(u'$Text(', u'self._asText(')
                    matrixcommand = matrixcommand.replace(u'$Float(', u'self._asFloat(')
                    matrixcommand = matrixcommand.replace(u'$Species(', u'self._speciesByKey(')
                    matrixcommand = matrixcommand.replace(u'$Sizeclass(', u'self._sizeclassByKey(')
                    #
                    if matrixnode == u'Dataset':
                        commandstring = u"dataset.addData('" + matrixkey + u"', " + matrixcommand + u")"
                        self.appendMatrixCommand(commandstring)
                    if matrixnode == u'Visit':
                        commandstring = u"currentvisit.addData('" + matrixkey + u"', " + matrixcommand + u")"
                        self.appendMatrixCommand(commandstring)
                    elif matrixnode == u'Sample':
                        commandstring = u"currentsample.addData('" + matrixkey + u"', " + matrixcommand + u")"
                        self.appendMatrixCommand(commandstring)
                    elif matrixnode == u'Variable':
                        commandstring = u"currentvariable.addData('" + matrixkey + u"', " + matrixcommand + u")"
                        self.appendMatrixCommand(commandstring)
                    #
                    elif (matrixnode == u'INFO') and (matrixkey == u'Visit key'):
                        commandstring = u"keystring = " + matrixcommand
                        visitkeycommand = compile(commandstring, '', 'exec')
                    elif (matrixnode == u'INFO') and (matrixkey == u'Sample key'):
                        commandstring = u"keystring = " + matrixcommand
                        samplekeycommand = compile(commandstring, '', 'exec')
#                    elif (matrixnode == u'INFO') and (matrixkey == u'Variable key'):
#                        commandstring = u"keystring = " + matrixcommand
#                        variablekeycommand = compile(commandstring, '', 'exec')
                    #
                    elif matrixnode == u'FUNCTION Dataset':
                        matrixkey = matrixkey.replace(u'()', u'') # Remove () from function name and add later.
                        commandstring = u"self._" + matrixkey + u"(dataset, "  + matrixcommand + u")"
                        self.appendMatrixCommand(commandstring)
                    elif matrixnode == u'FUNCTION Visit':
                        matrixkey = matrixkey.replace(u'()', u'') # Remove () from function name and add later.
                        commandstring = u"self._" + matrixkey + u"(currentvisit, "  + matrixcommand + u")"
                        self.appendMatrixCommand(commandstring)
                    elif matrixnode == u'FUNCTION Sample':
                        matrixkey = matrixkey.replace(u'()', u'') # Remove () from function name and add later.
                        commandstring = u"self._" + matrixkey + u"(currentsample, "  + matrixcommand + u")"
                        self.appendMatrixCommand(commandstring)
                    elif matrixnode == u'FUNCTION Variable':
                        matrixkey = matrixkey.replace(u'()', u'') # Remove () from function name and add later.
                        commandstring = u"self._" + matrixkey + u"(currentvariable, "  + matrixcommand + u")"
                        self.appendMatrixCommand(commandstring)
       
        except:
            print(u"Failed to parse import matrix: " + commandstring)
        #
        try:
            # Base class must know header for _asText(), etc.
            self._setHeader(imported_table.getHeader())
            # Iterate over rows in imported_table.            
            for row in imported_table.getRows():
                    # Current row to base class.
                    self._setRow(row) 
                    # === Get or create nodes. ===
                    currentvisit = None
                    currentsample = None
                    currentvariable = None
                    # Check if visit exists. Create or reuse.
                    keystring = None
                    exec(visitkeycommand) # Command assigns keystring.
                    currentvisit = dataset.getVisitLookup(keystring)
                    if not currentvisit:
                        currentvisit = mmfw.VisitNode()
                        dataset.addChild(currentvisit)    
                        currentvisit.setIdString(keystring)
                    # Check if sample exists. Create or reuse.
                    keystring = None
                    exec(samplekeycommand) # Command assigns keystring.
                    currentsample = dataset.getSampleLookup(keystring)
                    if not currentsample:
                        currentsample = mmfw.SampleNode()
                        currentvisit.addChild(currentsample)    
                        currentsample.setIdString(keystring)    
                    # Add all variables in row.
                    currentvariable = mmfw.VariableNode()
                    currentsample.addChild(currentvariable)    
                    # === Parse row and add fields on nodes. ===
                    for cmd in self._matrixcommands:
                        try:
                            exec(cmd[u'Command'])
                        except Exception as e:
                            pass
#                            print("ERROR: Failed to parse command: %s" % (e.args[0]))
#                            print("- Command string: %s" % (cmd[u'Command string']))
        #
        except Exception as e:
            print("ERROR: Failed to parse imported data: %s" % (e.args[0]))

