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

@envmonlib.singleton
class ScreeningManager(object):
    """ """
    def __init__(self,
                 codelist_filenames = [u'toolbox_data/code_lists/smhi_code_list.xlsx']):
        # Parameters.
        self._codelist_filenames = codelist_filenames 
        # Local storage.
        self._codelist = {} # Main dictionary.
        # Run (only done once because the class is declared as singleton).
        self._loadAllData()

    def getCodeTypes(self):
        """ """
        return self._codelist.keys() 
    
    def getCodes(self, code_type):
        """ """
        if code_type in self._codelist.keys():
            return self._codelist[code_type]
        return []
    
    def _clear(self):
        """ """
        self._codelist = {} # Main dictionary.

    def _loadAllData(self):
        """ """
        try:
            self._clear()
            # Create codelist from files.
            for excelfilename in self._codelist_filenames:
                self._loadCodeLists(excelfilename)                
        #
        except Exception, e:
            envmonlib.Logging().error(u"Failed when loading code lists. Exception: " + unicode(e))
#        # Used for DEBUG:
#        import locale
#        import codecs
#        import json
#        fileencoding = locale.getpreferredencoding()
#        out = codecs.open(u'DEBUG_codelist.txt', mode = 'w', encoding = fileencoding)
#        out.write(json.dumps(self._codelist, encoding = 'utf8', sort_keys=True, indent=4))
#        out.close()
#        # end DEBUG.
        
    def _loadCodeLists(self, excel_file_name):
        """ """
        # Get data from Excel file.
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, excel_file_name)
        #
        for row in tabledataset.getRows():
            codetype = row[0]
            code = row[1]
            #
            if codetype:
                if codetype not in self._codelist:
                    self._codelist[codetype] = []
                self._codelist[codetype].append(code)

    def codeListScreening(self, datasets):
        """ """
        # Checked code types shoud be returned to caller.
        checked_codetypes_set = set()
        #
        for dataset in datasets:
            #
            for visitnode in dataset.getChildren():
                #
                data_dict = visitnode.getDataDict()
                for key in data_dict:
                    if key in self.getCodeTypes():
                        checked_codetypes_set.add(key)
                        if data_dict[key] not in self.getCodes(key):
                            envmonlib.Logging().warning(u"Visit level. Code is not valid.  Code type: " + unicode(key) + u"  Code: " + unicode(data_dict[key]))
                #
                for samplenode in visitnode.getChildren():
                    #
                    data_dict = samplenode.getDataDict()
                    for key in data_dict:
                        if key in self.getCodeTypes():
                            checked_codetypes_set.add(key)
                            if data_dict[key] not in self.getCodes(key):
                                envmonlib.Logging().warning(u"Sample level. Code is not valid.  Code type: " + unicode(key) + u"  Code: " + unicode(data_dict[key]))
                    #                        
                    for variablenode in samplenode.getChildren():
                        #
                        data_dict = variablenode.getDataDict()
                        for key in data_dict:
                            if key in self.getCodeTypes():
                                checked_codetypes_set.add(key)
                                if data_dict[key] not in self.getCodes(key):
                                    envmonlib.Logging().warning(u"Variable level. Code is not valid.  Code type: " + unicode(key) + u"  Code: " + unicode(data_dict[key]))
        # Returns set of checked code types.
        return checked_codetypes_set

    def speciesScreening(self, datasets):
        """ """
        species = envmonlib.Species()
        #
        for dataset in datasets:
            #
            for visitnode in dataset.getChildren():
                #
                for samplenode in visitnode.getChildren():
                    #
                    for variablenode in samplenode.getChildren():
                        #
                        data_dict = variablenode.getDataDict()
                        if u'Taxon name' in data_dict:
                            if data_dict[u'Taxon name'] not in species.getTaxaLookupDict():
                                envmonlib.Logging().warning(u"Taxon name not in species list.  Taxon name: " + unicode(data_dict[u'Taxon name']))
     
    def bvolSpeciesScreening(self, datasets):
        """ """
        species = envmonlib.Species()
        #
        for dataset in datasets:
            #
            for visitnode in dataset.getChildren():
                #
                for samplenode in visitnode.getChildren():
                    #
                    for variablenode in samplenode.getChildren():
                        #
                        data_dict = variablenode.getDataDict()
                        if (u'Taxon name' in data_dict) and (u'Size class' in data_dict):
                            taxonname = data_dict[u'Taxon name']
                            sizeclass = data_dict[u'Size class'] 
                            
                            if species.getBvolValue(taxonname, sizeclass, u'Size class') == None:
                                envmonlib.Logging().warning(u"Taxon name/size clas not in BVOL list.  Taxon name: " + unicode(taxonname) + u"  Size class: " + unicode(sizeclass))
     

