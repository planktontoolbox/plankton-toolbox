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
            print(u"Failed when loading code lists. Exception: " + unicode(e))
        #
        # Used for DEBUG:
        import locale
        import codecs
        import json
        fileencoding = locale.getpreferredencoding()
        out = codecs.open(u'DEBUG_codelist.txt', mode = 'w', encoding = fileencoding)
        out.write(json.dumps(self._codelist, encoding = 'utf8', sort_keys=True, indent=4))
        out.close()
        # end DEBUG.
        
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

