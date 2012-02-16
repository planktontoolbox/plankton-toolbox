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
        matrixcommands = []
        visitkeycommand = None
        samplekeycommand = None
        variablekeycommand = None
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
                    #
                    if matrixnode == u'Dataset':
                        matrixcommands.append(compile(u"dataset.addData('" + matrixkey + u"', " + matrixcommand + u")", '', 'exec'))
                    if matrixnode == u'Visit':
                        matrixcommands.append(compile(u"currentvisit.addData('" + matrixkey + u"', " + matrixcommand + u")", '', 'exec'))
                    elif matrixnode == u'Sample':
                        matrixcommands.append(compile(u"currentsample.addData('" + matrixkey + u"', " + matrixcommand + u")", '', 'exec'))
                    elif matrixnode == u'Variable':
                        matrixcommands.append(compile(u"currentvariable.addData('" + matrixkey + u"', " + matrixcommand + u")", '', 'exec'))
                    #
                    elif (matrixnode == u'INFO') and (matrixkey == u'Visit key'):
                        visitkeycommand = compile(u"keystring = " + matrixcommand, '', 'exec')
                    elif (matrixnode == u'INFO') and (matrixkey == u'Sample key'):
                        samplekeycommand = compile(u"keystring = " + matrixcommand, '', 'exec')
                    elif (matrixnode == u'INFO') and (matrixkey == u'Variable key'):
                        variablekeycommand = compile(u"keystring = " + matrixcommand, '', 'exec')
       
        except:
            print(u"Failed to parse import matrix.")
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
                    for cmd in matrixcommands:
                        exec(cmd)
                    # TODO: For test...
                    currentvariable.addData(u'PARAMETER', u'COUNTNR')
                    currentvariable.addData(u'VALUE', self._asText(u'COUNTNR'))
                    currentvariable.addData(u'UNIT', u'ind')           
        #
        except Exception as e:
            print("ERROR: Failed to parse imported data: %s" % (e.args[0]))

