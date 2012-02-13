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

class ImportManager(object):
    """ """
    def __init__(self):
        """ """
        # Initialize parent.
        super(ImportManager, self).__init__()
        # TESTDATA:
        self._importmatrixfilepath = u'mmfw/data/templates/pp_import_matrix.txt'
#        self._zipfilepath = u'mmfw/data/testdata/data.txt'
        self._zipfilepath = u'mmfw/data/testdata/2009_SMHI_PP_version-2010-11-16.zip'
        self._importmatrixcolumn = u'Plankton-excel-format'
        
    def setImportMatrix(self, importmatrixfilepath):
        """ """
#        self._importmatrixfilepath = importmatrixfilepath
        
    def importFileToDataset(self, dataset, filename):
        """ """
        #
#        try:            
        formatparser = mmfw.FormatSingleFile()
               
#        matrixcolumn = self.metadata.getField(u'Dataset format')
        
        # Phase 1: Parse file and import to memory model.
        formatparser.importDataset(dataset, filename)

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
    #        zipfile = mmfw.ZipPackageReader(zipfilename)
            zipfile = mmfw.ZipPackageReader(self._zipfilepath) # TODO:
            print(zipfile.listContent())
            
            
            formatparser = mmfw.FormatSingleFile()
                   
    #        matrixcolumn = self.metadata.getField(u'Dataset format')
            
            # Phase 1: Parse file and import to memory model.
            formatparser.importDataset(dataset, zipfile)
    
    
            # Phase 2: Reorganize between nodes in memory model.
    
            # Phase 3: Reformat fields in memory model.
    
            # Phase 4: Basic screening.
            
        finally:
            zipfile.close() # Close zip file.
            del zipfile

