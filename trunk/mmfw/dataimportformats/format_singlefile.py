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
        #
        try:
            for matrixrow in importmatrixrows:
                matrixnode = matrixrow.get(u'Node', u'') 
                matrixkey = matrixrow.get(u'Key', u'') 
                matrixcommand = matrixrow.get(u'Command', u'')            
                #    
                ### TODO: Replace:
                # $Text(   --> self.asText(
                # $Year(   --> self.asYear(
                # $Datetime(   --> self.asDatetime(
                # $Date(   --> self.asDate(
                # $Time(   --> self.asTime(
                # $Int(   --> self.asInt(
                # $Float(   --> self.asFloat(
                # $Position(   --> self.asPosition(
                # $Station(   --> self.asStation(
                # $Param(   --> self.asParam(
                matrixcommand = matrixcommand.replace(u'$Text(', u'self.asText(')
                #
                if matrixnode == u'Visit':
                    matrixcommands.append(compile(u"currentvisit.addData('" + matrixkey + u"', " + matrixcommand + u")", '', 'exec'))
                if matrixnode == u'Sample':
                    matrixcommands.append(compile(u"currentsample.addData('" + matrixkey + u"', " + matrixcommand + u")", '', 'exec'))
                if matrixnode == u'Variable':
                    matrixcommands.append(compile(u"currentvariable.addData('" + matrixkey + u"', " + matrixcommand + u")", '', 'exec'))
        except:
            print(u"Failed to parse import matrix.")
        #
        try:
            
            self.setHeader(imported_table.getHeader())
            
            # Iterate over rows in imported_table.            
#            fieldseparator = None
            for rowindex, row in enumerate(imported_table.getRows()):
#                # Convert to unicode.
#                row = unicode(row, self.field_encoding, 'strict')
#                # Check if header row.
#                if rowindex == 0:
#                    fieldseparator = self.getSeparator(row)
#                    row = [item.strip() for item in row.split(fieldseparator)]
#                    self.setHeader(row)
#                else:
#                    row = [item.strip() for item in row.split(fieldseparator)]
                    self._row = row 
                    # === Get or create nodes. ===
                    currentvisit = None
                    currentsample = None
                    currentvariable = None
                    # Check if visit exists. Create or reuse.
                    keystring = self.asText(u'SDATE') + ':' + \
                                self.asText(u'STATN')
                    currentvisit = dataset.getVisitLookup(keystring)
                    if not currentvisit:
                        currentvisit = mmfw.VisitNode()
                        dataset.addChild(currentvisit)    
                        currentvisit.setIdString(keystring)
                    # Check if sample exists. Create or reuse.
                    keystring = self.asText(u'SDATE') + ':' + \
                                self.asText(u'STATN') + ':' + \
                                self.asText(u'SMPNO')
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
                    currentvariable.addData(u'PARAMETER', u'COUNTNR')
                    currentvariable.addData(u'VALUE', self.asText(u'COUNTNR'))
                    currentvariable.addData(u'UNIT', u'ind')           
        #
        except Exception as e:
            print("ERROR: Failed to parse imported data: %s" % (e.args[0]))

