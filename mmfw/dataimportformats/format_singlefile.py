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
import datetime

class FormatSingleFile(mmfw.FormatBase):
    """ Import format for single file. """
    def __init__(self):
        """ Import format for single file. """
        super(FormatSingleFile, self).__init__()

    def importDataset(self, dataset, filename):
        """ """
        self._dataset = dataset        
        self._filename = filename        
        self.field_encoding = u'cp1252'
        #        
        importmatrixrows = dataset.getImportMatrixRows()
        
        matrixcommands = []
        
        for matrixrow in importmatrixrows:
            matrixnode = matrixrow.get(u'Node', u'') 
            matrixkey = matrixrow.get(u'Key', u'') 
            matrixcommand = matrixrow.get(u'Command', u'')
            
            matrixcommand = matrixcommand.replace(u'$Text(', u'self.asText(')
            
            if matrixnode == u'Visit':
                matrixcommands.append(compile(u"currentvisit.addData('" + matrixkey + u"', " + matrixcommand + u")", '', 'exec'))
            if matrixnode == u'Sample':
                matrixcommands.append(compile(u"currentsample.addData('" + matrixkey + u"', " + matrixcommand + u")", '', 'exec'))
            if matrixnode == u'Variable':
                matrixcommands.append(compile(u"currentvariable.addData('" + matrixkey + u"', " + matrixcommand + u")", '', 'exec'))
            
        

        ### Replace:
        
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

#        matrixrows = [ # Level, field, command.
#            (u"Visit", u"Visit year", u"self.asText('MYEAR')"),
#            (u"Visit", u"Visit date", u"self.asText('SDATE')"),
##                        (u"Visit", u"Station name", u"getStation(asText('STATN'))"),
#            (u"Visit", u"Reported station name", u"self.asText('STATN')"),
#            
#            (u"Sample", u"Sample min depth", u"self.asText('MNDEP')"),
#            (u"Sample", u"Sample max depth", u"self.asText('MXDEP')"),
#            (u"Sample", u"Sampling laboratory code", u"self.asText('SLABO')"),
#
#            
#            (u"Sample", u"Test dict", u"{'a': 1, 'b':2}")
#            ]
#        
#        matrixcommands = []
#        
#        for matrixlevel, matrixfield, matrixcommand in matrixrows:
#            if matrixlevel == u'Visit':
#                matrixcommands.append(compile(u"currentvisit.addData('" + matrixfield + u"', " + matrixcommand + u")", '', 'exec'))
#            if matrixlevel == u'Sample':
#                matrixcommands.append(compile(u"currentsample.addData('" + matrixfield + u"', " + matrixcommand + u")", '', 'exec'))
#            if matrixlevel == u'Variable':
#                matrixcommands.append(compile(u"currentvariable.addData('" + matrixfield + u"', " + matrixcommand + u")", '', 'exec'))

        try:
            print(u'DEBUG: Start.')
            debug_start = datetime.datetime.now()
            rowcount = 0
            #

            
            
            
            
#            infile = zipfile.openZipEntry(u'data.skv')
            infile = open(filename)

            
            
            
            
            
            
            # Iterate over rows in file.            
            fieldseparator = None
            for rowindex, row in enumerate(infile):
                # Convert to unicode.
                row = unicode(row, self.field_encoding, 'strict')
                # Check if header row.
                if rowindex == 0:
                    fieldseparator = self.getSeparator(row)
                    row = [item.strip() for item in row.split(fieldseparator)]
                    self.setHeader(row)
                else:
                    row = [item.strip() for item in row.split(fieldseparator)]
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
                        
                    
#                    matrixrows = [ # Level, field, command.
#                        (u"Visit", u"Visit year", u"self.asText('MYEAR')"),
#                        (u"Visit", u"Visit date", u"self.asText('MYEAR')"),
##                        (u"Visit", u"Station name", u"getStation(asText('STATN'))"),
#                        (u"Visit", u"Reported station name", u"self.asText('STATN')"),
#                        
#                        (u"Sample", u"Sample min depth", u"self.asText('MNDEP')"),
#                        (u"Sample", u"Sample max depth", u"self.asText('MXDEP')"),
#                        (u"Sample", u"Sampling laboratory code", u"self.asText('SLABO')")
#                        ]
#                    
#                    for matrixlevel, matrixfield, matrixcommand in matrixrows:
#                        
#                        
#                        if matrixlevel == u'Visit':
#                            exec(u"currentvisit.addData('" + matrixfield + u"', \"" + matrixcommand + u"\")")
#                        if matrixlevel == u'Sample':
#                            exec(u"currentsample.addData('" + matrixfield + u"', \"" + matrixcommand + u"\")")
#                        if matrixlevel == u'Variable':
#                            exec(u"currentvariable.addData('" + matrixfield + u"', \"" + matrixcommand + u"\")")
                            
                        
                        
                    
                    
                    
#Dataset    Monitoringyears                    asText('MYEAR')    
#Dataset    Import matrix column                    getColumnName()    
#                            
#Visit    Visit id                        
#Visit    Visit year                    asText('MYEAR')    
#Visit    Visit date                    asText('SDATE')    
#Visit    Station name                    getStation(asText('STATN'))    
#Visit    Reported station name                    asText('STATN')    
#Visit    Visit position                Lagras som dictionary med parametrarna Lat och Long.    dict('Lat': asText('LATIT'), 'Long': asText('LONGI')    
#Visit    Visit comment                    asText('COMNT_VISIT')    
#Visit    Water depth                    asFloat('WADEP')    
#Visit    Visit reported latitude                    asText('LATIT')    
#Visit    Visit reported longitude                    asText('LONGI')    
#Visit    Positioning system code                    asText('POSYS')    
#                            
#Sample    Sample id                    asText('SMPNO')    
#Sample    Sample series                        
#Sample    Sample min depth                    asText('MNDEP')    
#Sample    Sample max depth                    asText('MXDEP')    
#Sample    Project code                    asText('PROJ')    
#Sample    Project name                    asText('PROJ_NAME')    
#Sample    Orderer                    asText('ORDERER')    
#Sample    Sampling laboratory code                    asText('SLABO')    
#Sample    Method documentation                    asText('METDC')    
#Sample    Sample comment                    asText('COMNT_SAMP')    
#Sample    Sampler type code                    asText('SMTYP')    
#Sample    Sampled volume                    asText('SMVOL')    
#                            
#Variable    Method of analysis code                    asText('METFP')    ???
#Variable    Analytical laboratory code                    asText('ALABO')    
#Variable    Analysed by                        
#Variable    Analysis date                        
#Variable    Variable comment                    asText('COMNT_VAR')    
#Variable                            
#Variable    Size class                    asText('SIZCL')    
#Variable    Size class ref list code                    asText('SIZRF')    
#Variable    Species flag code                    asText('SFLAG')    
#Variable    Trophy                    asText('TRPHY    
#Variable    Coefficient                    asText('COEFF    
#Variable    Magnification                    asText('MAGNI    
#Variable    Reported taxon name                    asText('LATNM    
#Variable    Taxonomist                    asText('TAXNM    
#Variable                            
#Variable    Sedimentation time                    asText('SDTIM    
#Variable    Sedimentation volume                    asText('SDVOL    
#                            
#Variable    Parameter                        
#Variable    Value                        
#Variable    Unit                        
#                            
#FUNCTION    modifyVariable(p='COUNTNR', v=par1, u='ind', q=par2)                    asText('COUNTNR,asText('QFLAG')    CONC_IND_L-1
#FUNCTION    copyVariable(p='BIOVOL', v=par1, u='µm3/cell', q=par2)                    asText('BIOVOL µm3/cell,asText('QFLAG')    
#FUNCTION    copyVariable(p='CARBON', v=par1, u='pg/cell', q=par2)                    asText('CARBON pg/cell,asText('QFLAG')    BIOVOL µm3/cell
#                            CARBON pg/cell
#Variable    Parameter object                    asParameter(p='COUNTNR', v=par1, u='ind', q=par2)    
                    
#                    exec(u"currentvisit.addData(u'SDATE', self.asText(u'SDATE'))")
#                    exec(u"currentvisit.addData(u'STATN', self.asText(u'STATN'))")
#                    
##                    currentvisit.addData(u'SDATE', self.asText(u'SDATE'))
##                    currentvisit.addData(u'STATN', self.asText(u'STATN'))
#
#                    currentsample.addData(u'SMPNO', self.asText(u'SMPNO'))

                    currentvariable.addData(u'PARAMETER', u'COUNTNR')
                    currentvariable.addData(u'VALUE', self.asText(u'COUNTNR'))
                    currentvariable.addData(u'UNIT', u'ind')
                    
                    rowcount += 1
                    
            infile.close()
            
            print(unicode(len(dataset.getChildren())))            
            
            print(u'DEBUG: Done. ' + unicode(rowcount))
            debug_end = datetime.datetime.now()
            print(debug_end - debug_start)            
        #
        finally:
            print(u'') # Dummy. 
#        except Exception as e:
#            print("ERROR: Failed to import data: %s" % (e.args[0]))
            
