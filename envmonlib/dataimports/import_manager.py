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

import envmonlib

class ImportManager(object):
    """ """
    def __init__(self):
        """ """
        # Initialize parent.
        super(ImportManager, self).__init__()
        
    def importTextFileToDataset(self, dataset, filename, textfile_encoding):
        """ """
        #
#        try:            
        formatparser = envmonlib.FormatSingleFile()
               
#        matrixcolumn = self.metadata.getField(u'Dataset format')
        
        # Phase 1: Parse file and import to memory model.
        tabledataset = envmonlib.DatasetTable()
        envmonlib.TextFiles().readToTableDataset(tabledataset, filename, encoding = textfile_encoding)
        formatparser.parseTableDataset(dataset, tabledataset)

        # Phase 2: Reorganize between nodes in memory model.

        # Phase 3: Reformat fields in memory model.

        # Phase 4: Basic screening.
            
#        finally:
#            zipfile.close() # Close zip file.
#            del zipfile

    def importExcelFileToDataset(self, dataset, filename):
        """ """
        #
#        try:            
        formatparser = envmonlib.FormatSingleFile()
               
#        matrixcolumn = self.metadata.getField(u'Dataset format')

#Header row
#First data row
#First column
#Excel sheet name


        
        # Phase 1: Parse file and import to memory model.
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, filename,
                                             sheet_name = u'Kolumner',
                                             header_row = 3-1,
                                             data_rows_from = 4-1,
                                             data_columns_from = 2-1)
        formatparser.parseTableDataset(dataset, tabledataset)

        # Phase 2: Reorganize between nodes in memory model.

        # Phase 3: Reformat fields in memory model.

        # Phase 4: Basic screening.
            
#        finally:
#            zipfile.close() # Close zip file.
#            del zipfile

    def importZipToDataset(self, dataset, zipfilename):
        """ """
        #
        try:
    #        zipfile = envmonlib.ZipPackageReader(zipfilename)
            zipfile = envmonlib.ZipFileReader(self._zipfilepath) # TODO:
            print(zipfile.listContent())
            
            
            formatparser = envmonlib.FormatSingleFile()
                   
    #        matrixcolumn = self.metadata.getField(u'Dataset format')
            
            # Phase 1: Parse file and import to memory model.
            formatparser.importDataset(dataset, zipfile)
    
    
            # Phase 2: Reorganize between nodes in memory model.
    
            # Phase 3: Reformat fields in memory model.
    
            # Phase 4: Basic screening.
            
        finally:
            zipfile.close() # Close zip file.
            del zipfile

