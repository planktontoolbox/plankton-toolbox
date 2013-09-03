#!/usr/bin/env python


###### -*- coding:utf-8 -*-


#
# Project: Plankton Toolbox. http://plankton-toolbox.org
# Author: Arnold Andreasson, info@mellifica.se
# Copyright (c) 2010-2013 SMHI, Swedish Meteorological and Hydrological Institute 
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

class FormatSingleFile(envmonlib.ParsedFormat):
    """ Import format for single file. """
    def __init__(self):
        """ Import format for single file. """
        super(FormatSingleFile, self).__init__()

    def parseTableDataset(self, dataset, imported_table):
        """ """
        self._dataset = dataset        
        #        
        datasetparserrows = dataset.getDatasetParserRows()
        #
        visitkeycommand = None
        samplekeycommand = None
#        variablekeycommand = None
        #
        try:
            for parserrow in datasetparserrows:
                parsernode = parserrow.get(u'node', u'') 
                parserkey = parserrow.get(u'key', u'') 
                parsercommand = parserrow.get(u'command', u'')
                if parsercommand:         
                    #
#                    parserkey = self.replaceMethodKeywords(parserkey, parsernode)    
#                    parsercommand = self.replaceMethodKeywords(parsercommand, parsernode)    
                    #
                    parserkey = unicode(self.replaceMethodKeywords(parserkey, parsernode))    
                    parsercommand = unicode(self.replaceMethodKeywords(parsercommand, parsernode))    
                    #
                    if parsernode == u'dataset':
                        commandstring = u"dataset.addData('" + parserkey + u"', " + parsercommand + u")"
                        self.appendParserCommand(commandstring)
                    if parsernode == u'visit':
                        commandstring = u"currentvisit.addData('" + parserkey + u"', " + parsercommand + u")"
                        self.appendParserCommand(commandstring)
                    elif parsernode == u'sample':
                        commandstring = u"currentsample.addData('" + parserkey + u"', " + parsercommand + u")"
                        self.appendParserCommand(commandstring)
                    elif parsernode == u'variable':
                        commandstring = u"currentvariable.addData('" + parserkey + u"', " + parsercommand + u")"
                        self.appendParserCommand(commandstring)
                    #
                    elif (parsernode == u'info') and (parserkey == u'visit_key'):
                        commandstring = u"keystring = " + parsercommand
                        visitkeycommand = compile(commandstring, '', 'exec')
                    elif (parsernode == u'info') and (parserkey == u'sample_key'):
                        commandstring = u"keystring = " + parsercommand
                        samplekeycommand = compile(commandstring, '', 'exec')
#                    elif (parsernode == u'INFO') and (parserkey == u'Variable key'):
#                        commandstring = u"keystring = " + parsercommand
#                        variablekeycommand = compile(commandstring, '', 'exec')
                    #
                    elif parsernode == u'function_dataset':
#                        parserkey = parserkey.replace(u'()', u'') # Remove () from function name and add later.
#                        commandstring = u"self._" + parserkey + u"(dataset, "  + parsercommand + u")"
                        commandstring = parserkey + parsercommand
                        self.appendParserCommand(commandstring)
                    elif parsernode == u'function_visit':
#                        parserkey = parserkey.replace(u'()', u'') # Remove () from function name and add later.
#                        commandstring = u"self._" + parserkey + u"(currentvisit, "  + parsercommand + u")"
                        commandstring = parserkey + parsercommand
                        self.appendParserCommand(commandstring)
                    elif parsernode == u'function_sample':
#                        parserkey = parserkey.replace(u'()', u'') # Remove () from function name and add later.
#                        commandstring = u"self._" + parserkey + u"(currentsample, "  + parsercommand + u")"
                        commandstring = parserkey + parsercommand
                        self.appendParserCommand(commandstring)
                    elif parsernode == u'function_variable':
                        parserkey = parserkey.replace(u'()', u'') # Remove () from function name and add later.
#                        commandstring = u"self._" + parserkey + u"(currentvariable, "  + parsercommand + u")"
#                        commandstring = parserkey + u"(currentvariable, "  + parsercommand + u")"
                        commandstring = parserkey + parsercommand
                        self.appendParserCommand(commandstring)
       
        except Exception as e:
            envmonlib.Logging().warning(u"Failed to parse dataset: %s" % (e.args[0]) + 
                                        "- Command string: %s" % (commandstring))
            raise
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
#                     exec(visitkeycommand.encode('windows-1252')) # Command assigns keystring.
                    
                    
                    currentvisit = dataset.getVisitLookup(keystring)
                    if not currentvisit:
                        currentvisit = envmonlib.VisitNode()
                        dataset.addChild(currentvisit)    
                        currentvisit.setIdString(keystring)
                    # Check if sample exists. Create or reuse.
                    keystring = None


                    exec(samplekeycommand) # Command assigns keystring.
#                     exec(samplekeycommand.encode('windows-1252')) # Command assigns keystring.
                    
                    
                    currentsample = dataset.getSampleLookup(keystring)
                    if not currentsample:
                        currentsample = envmonlib.SampleNode()
                        currentvisit.addChild(currentsample)    
                        currentsample.setIdString(keystring)    
                    # Add all variables in row.
                    currentvariable = envmonlib.VariableNode()
                    currentsample.addChild(currentvariable)    
                    # === Parse row and add fields on nodes. ===
                    
                    for cmd in self._parsercommands:
                        try:


                            exec(cmd[u'command'])
#                             exec(cmd[u'command'].encode('windows-1252'))

                        
                        except Exception as e:
                            envmonlib.Logging().warning(u"Failed to parse command: %s" % (e.args[0]) + 
                                                        "- Command string: %s" % (cmd[u'Command string']))
        #
        except Exception as e:
            envmonlib.Logging().warning(u"Failed to parse dataset: %s" % (e.args[0]))
