#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

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
                view_format = parserrow.get(u'view_format', u'')
                parsercommand = parserrow.get(u'command', u'')
                if parsercommand:         
                    #
                    parsercommand = unicode(self.replaceMethodKeywords(parsercommand, parsernode, view_format))    
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
                    #
                    elif parsernode == u'function_dataset':
                        commandstring = parserkey + parsercommand
                        self.appendParserCommand(commandstring)
                    elif parsernode == u'function_visit':
                        commandstring = parserkey + parsercommand
                        self.appendParserCommand(commandstring)
                    elif parsernode == u'function_sample':
                        commandstring = parserkey + parsercommand
                        self.appendParserCommand(commandstring)
                    elif parsernode == u'function_variable':
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
                    currentvisit = dataset.getVisitLookup(keystring)
                    if not currentvisit:
                        currentvisit = envmonlib.VisitNode()
                        dataset.addChild(currentvisit)    
                        currentvisit.setIdString(keystring)
                    # Check if sample exists. Create or reuse.
                    keystring = None
                    exec(samplekeycommand) # Command assigns keystring.
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
                        
                        except Exception as e:
                            envmonlib.Logging().warning(u"Failed to parse command: %s" % (e.args[0]) + 
                                                        "- Command string: %s" % (cmd[u'command_string']))
        #
        except Exception as e:
            envmonlib.Logging().warning(u"Failed to parse dataset: %s" % (e.args[0]))

