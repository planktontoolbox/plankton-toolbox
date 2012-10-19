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

class ImportManager(object):
    """ 
    
    Parser file columns and values:
    
    - First column: Node level. Content: INFO, VISIT, SAMPLE, VARIABLE, FUNCTION Sample, FUNCTION Variable 
    - Second column: Key. INFO: Fixed set of key values. Other: Field name in the internal memory model.
    - Fourth column: Format. Content: Text, Date:format, Time:format, Datetime:format, Integer, Float:n (where n = shown decimals).
    
    ...
    
    
    """
    def __init__(self, parser_file_path, import_column, export_column):
        """ """
        #
        self._parser_file_path = parser_file_path
        self._import_column = import_column
        self._export_column = export_column
        # Initialize parent.
        super(ImportManager, self).__init__()
        # 
        self._importrows = None
        self._columnsinfo = None
        self._loadParserInfo()

    def importTextFile(self, filename, textfile_encoding):
        """ """
        # Select import format.
        formatparser = envmonlib.FormatSingleFile()
        # Phase 1: Read file into a temporary table.
        tabledataset = envmonlib.DatasetTable()
        envmonlib.TextFiles().readToTableDataset(tabledataset, filename, encoding = textfile_encoding)
        # Phase 2: Parse the table and create a corresponding tree structure.
        targetdataset = envmonlib.DatasetNode()
        #
        targetdataset.setDatasetParserRows(self._importrows)
        targetdataset.setExportTableColumns(self._columnsinfo)
        #
        formatparser.parseTableDataset(targetdataset, tabledataset)
        # Phase 3: Reorganize between nodes in tree structure.
        formatparser.reorganizeDataset()
        # Phase 4: Reformat fields in tree structure.
        formatparser.reformatDataset()
        # Phase 5: Perform basic screening.
        formatparser.basicScreening()
        #
        return targetdataset

    def importExcelFile(self, filename):
        """ """
        # Select import format.
        formatparser = envmonlib.FormatSingleFile()
        # Phase 1: Read file into a temporary table.
                
        sheetname = None
        headerrow = 1
        datarowsfrom = 2
        columnsfrom = 1
        #
        for rowdict in self._importrows:
            if rowdict[u'Node'] == u'INFO':
                if rowdict[u'Key'] == u'Excel sheet name':
                    sheetname = rowdict.get(u'Command', None)
                if rowdict[u'Key'] == u'Header row':
                    headerrow = int(float(rowdict.get(u'Command', u'1')))
                    if headerrow: headerrow -= 1
                if rowdict[u'Key'] == u'First data row':
                    datarowsfrom = int(float(rowdict.get(u'Command', u'2')))
                    if datarowsfrom: datarowsfrom -= 1
                if rowdict[u'Key'] == u'First column':
                    columnsfrom = int(float(rowdict.get(u'Command', u'1')))
                    if columnsfrom: columnsfrom -= 1
#        for rowdict in self._importrows:
#            if rowdict[u'Node'] == u'INFO':
#                if rowdict[u'Key'] == u'Excel sheet name':
#                    sheetname = rowdict.get(u'Command', None)
#                if rowdict[u'Key'] == u'Header row':
#                    headerrow = envmonlib.FieldFormats().format(rowdict.get(u'Command', u'1'), u'Integer')
#                    if headerrow: headerrow -= 1
#                if rowdict[u'Key'] == u'First data row':
#                    datarowsfrom = envmonlib.FieldFormats().format(rowdict.get(u'Command', u'2'), u'Integer')
#                    if datarowsfrom: datarowsfrom -= 1
#                if rowdict[u'Key'] == u'First column':
#                    columnsfrom = envmonlib.FieldFormats().format(rowdict.get(u'Command', u'1'), u'Integer')
#                    if columnsfrom: columnsfrom -= 1
        
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, filename,
                                                  sheet_name = sheetname,
                                                  header_row = headerrow,
                                                  data_rows_from = datarowsfrom,
                                                  columns_from = columnsfrom)
        # Phase 2: Parse the table and create a corresponding tree structure.
        targetdataset = envmonlib.DatasetNode()
        #
        targetdataset.setDatasetParserRows(self._importrows)
        targetdataset.setExportTableColumns(self._columnsinfo)
        #
        formatparser.parseTableDataset(targetdataset, tabledataset)
        # Phase 3: Reorganize between nodes in tree structure.
        formatparser.reorganizeDataset()
        # Phase 4: Reformat fields in tree structure.
        formatparser.reformatDataset()
        # Phase 5: Perform basic screening.
        formatparser.basicScreening()
        #
        return targetdataset

#    def importZipToDataset(self, dataset, zipfilename):
#        """ """
#        #
#        try:
#    #        zipfile = envmonlib.ZipPackageReader(zipfilename)
#            zipfile = envmonlib.ZipFileReader(self._zipfilepath) # TODO:
#            print(zipfile.listContent())
#            
#            
#            formatparser = envmonlib.FormatSingleFile()
#                   
#    #        parsercolumn = self.metadata.getField(u'Dataset format')
#            
#            # Phase 1: Parse file and import to memory model.
#            formatparser.importDataset(dataset, zipfile)
#    
#    
#            # Phase 2: Reorganize between nodes in memory model.
#    
#            # Phase 3: Reformat fields in memory model.
#    
#            # Phase 4: Basic screening.
#            
#        finally:
#            zipfile.close() # Close zip file.
#            del zipfile

    def _loadParserInfo(self):
        """ """
        # Read dataset parser.
        tabledata = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledata, file_name = self._parser_file_path)
        # Create import info.
        if self._import_column:
#            self.addMetadata(u'Import column', self._import_column)
            self._importrows = []
            for rowindex in xrange(0, tabledata.getRowCount()):
                importcolumndata = tabledata.getDataItemByColumnName(rowindex, self._import_column)
                if importcolumndata:
                    nodelevel = tabledata.getDataItem(rowindex, 0)
                    key = tabledata.getDataItem(rowindex, 1)
                    fieldformat = tabledata.getDataItem(rowindex, 2)
                    self._importrows.append({u'Node': nodelevel, u'Key': key, u'Format': fieldformat, u'Command': importcolumndata}) 
#            self.setDatasetParserRows(self._importrows)
        # Create export info.
        if self._export_column:
#            self.addMetadata(u'Export column', self._export_column)
            self._columnsinfo = []
            for rowindex in xrange(0, tabledata.getRowCount()):
                exportcolumndata = tabledata.getDataItemByColumnName(rowindex, self._export_column)
                if exportcolumndata:
                    nodelevel = tabledata.getDataItem(rowindex, 0)
                    if nodelevel != u'INFO':
                        key = tabledata.getDataItem(rowindex, 1)
                        fieldformat = tabledata.getDataItem(rowindex, 2)
                        self._columnsinfo.append({u'Header': exportcolumndata, u'Node': nodelevel, u'Key': key, u'Format': fieldformat}) 
#            self.setExportTableColumns(self._columnsinfo)
