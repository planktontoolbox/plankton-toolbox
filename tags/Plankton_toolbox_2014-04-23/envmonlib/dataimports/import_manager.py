#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import envmonlib

class ImportManager(object):
    """ 
    
    Parser file columns and values:
    
    - First column: Node level. Content: INFO, VISIT, SAMPLE, VARIABLE, FUNCTION Visit, FUNCTION Sample, FUNCTION Variable. 
    - Second column: Key. INFO: Fixed set of key values. Other: Field name in the internal memory model.
    - Fourth column: View format. Content:  text, 
                                            integer, 
                                            float: number of shown decimals,
                                            date: view format,
                                            datetime: view format. 
    
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
                
        sheetname = None
        headerrow = 1
        datarowsfrom = 2
        #
        for rowdict in self._importrows:
            if rowdict[u'node'] == u'info':
                if rowdict[u'key'] == u'header_row':
                    headerrow = int(float(rowdict.get(u'command', u'1')))
                    if headerrow: headerrow -= 1
                if rowdict[u'key'] == u'first_data_row':
                    datarowsfrom = int(float(rowdict.get(u'command', u'2')))
                    if datarowsfrom: datarowsfrom -= 1

        tabledataset = envmonlib.DatasetTable()
        envmonlib.TextFiles().readToTableDataset(tabledataset, filename, 
                                                 encoding = textfile_encoding,
                                                 header_row = headerrow,
                                                 data_rows_from = datarowsfrom)
        #
        envmonlib.Logging().info(u"Loading file. Header content: " +  
                                 unicode(tabledataset.getHeader()))
        
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
        #
        for rowdict in self._importrows:
            if rowdict[u'node'] == u'info':
                if rowdict[u'key'] == u'excel_sheet_name':
                    sheetname = rowdict.get(u'Command', None)
                if rowdict[u'key'] == u'header_row':
                    headerrow = int(float(rowdict.get(u'Command', u'1')))
                    if headerrow: headerrow -= 1
                if rowdict[u'key'] == u'first_data_row':
                    datarowsfrom = int(float(rowdict.get(u'Command', u'2')))
                    if datarowsfrom: datarowsfrom -= 1
#        for rowdict in self._importrows:
#            if rowdict[u'Node'] == u'INFO':
#                if rowdict[u'Key'] == u'Excel sheet name':
#                    sheetname = rowdict.get(u'Command', None)
#                if rowdict[u'Key'] == u'Header row':
#                    headerrow = envmonlib.ViewFormats().format(rowdict.get(u'Command', u'1'), u'Integer')
#                    if headerrow: headerrow -= 1
#                if rowdict[u'Key'] == u'First data row':
#                    datarowsfrom = envmonlib.ViewFormats().format(rowdict.get(u'Command', u'2'), u'Integer')
#                    if datarowsfrom: datarowsfrom -= 1
        
        tabledataset = envmonlib.DatasetTable()
        envmonlib.ExcelFiles().readToTableDataset(tabledataset, filename,
                                                  sheet_name = sheetname,
                                                  header_row = headerrow,
                                                  data_rows_from = datarowsfrom)
        #
        envmonlib.Logging().info(u"Loading file. Header content: " +  
                                 unicode(tabledataset.getHeader()))

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
                    viewformat = tabledata.getDataItem(rowindex, 2)
                    self._importrows.append({u'node': nodelevel, u'key': key, u'view_format': viewformat, u'command': importcolumndata}) 
#            self.setDatasetParserRows(self._importrows)
        # Create export info.
        if self._export_column:
#            self.addMetadata(u'Export column', self._export_column)
            self._columnsinfo = []
            for rowindex in xrange(0, tabledata.getRowCount()):
                exportcolumndata = tabledata.getDataItemByColumnName(rowindex, self._export_column)
                if exportcolumndata:
                    nodelevel = tabledata.getDataItem(rowindex, 0)
                    if nodelevel != u'info':
                        key = tabledata.getDataItem(rowindex, 1)
                        viewformat = tabledata.getDataItem(rowindex, 2)
                        self._columnsinfo.append({u'header': exportcolumndata, u'node': nodelevel, u'key': key, u'view_format': viewformat}) 
#            self.setExportTableColumns(self._columnsinfo)
