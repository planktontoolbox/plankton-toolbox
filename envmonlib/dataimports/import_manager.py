#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import envmonlib
import toolbox_utils
import toolbox_core

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
            if rowdict['node'] == 'info':
                if rowdict['key'] == 'header_row':
                    headerrow = int(float(rowdict.get('command', '1')))
                    if headerrow: headerrow -= 1
                if rowdict['key'] == 'first_data_row':
                    datarowsfrom = int(float(rowdict.get('command', '2')))
                    if datarowsfrom: datarowsfrom -= 1

        tablefilereader = toolbox_utils.TableFileReader(text_file_name = filename, 
                                                 encoding = textfile_encoding,
                                                 header_row = headerrow,
                                                 data_rows_from = datarowsfrom)
        tabledataset = toolbox_core.DatasetTable()
        tabledataset.setHeader(tablefilereader.header())
        for row in tablefilereader.rows():
            tabledataset.appendRow(row)
        #
        toolbox_utils.Logging().info('Loading file. Header content: ' +  
                                 unicode(tabledataset.getHeader()))
        
        # Phase 2: Parse the table and create a corresponding tree structure.
        targetdataset = toolbox_core.DatasetNode()
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
            if rowdict['node'] == 'info':
                if rowdict['key'] == 'excel_sheet_name':
                    sheetname = rowdict.get('Command', None)
                if rowdict['key'] == 'header_row':
                    headerrow = int(float(rowdict.get('Command', '1')))
                    if headerrow: headerrow -= 1
                if rowdict['key'] == 'first_data_row':
                    datarowsfrom = int(float(rowdict.get('Command', '2')))
                    if datarowsfrom: datarowsfrom -= 1
#        for rowdict in self._importrows:
#            if rowdict['Node'] == 'INFO':
#                if rowdict['Key'] == 'Excel sheet name':
#                    sheetname = rowdict.get('Command', None)
#                if rowdict['Key'] == 'Header row':
#                    headerrow = toolbox_utils.ViewFormats().format(rowdict.get('Command', '1'), 'Integer')
#                    if headerrow: headerrow -= 1
#                if rowdict['Key'] == 'First data row':
#                    datarowsfrom = toolbox_utils.ViewFormats().format(rowdict.get('Command', '2'), 'Integer')
#                    if datarowsfrom: datarowsfrom -= 1
        
        tablefilereader = toolbox_utils.TableFileReader(excel_file_name = filename,
                                                  sheet_name = sheetname,
                                                  header_row = headerrow,
                                                  data_rows_from = datarowsfrom)
        tabledataset = toolbox_core.DatasetTable()
        tabledataset.setHeader(tablefilereader.header())
        for row in tablefilereader.rows():
            tabledataset.appendRow(row)
        #
        toolbox_utils.Logging().info('Loading file. Header content: ' +  
                                 unicode(tabledataset.getHeader()))

        # Phase 2: Parse the table and create a corresponding tree structure.
        targetdataset = toolbox_core.DatasetNode()
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
#    #        zipfile = toolbox_utils.ZipPackageReader(zipfilename)
#            zipfile = toolbox_utils.ZipFileReader(self._zipfilepath) # TODO:
#            print(zipfile.listContent())
#            
#            
#            formatparser = toolbox_utils.FormatSingleFile()
#                   
#    #        parsercolumn = self.metadata.getField('Dataset format')
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
        tablefilereader = toolbox_utils.TableFileReader(excel_file_name = self._parser_file_path)
        tabledata = toolbox_core.DatasetTable()
        tabledata.setHeader(tablefilereader.header())
        for row in tablefilereader.rows():
            tabledata.appendRow(row)
        # Create import info.
        if self._import_column:
#            self.addMetadata('Import column', self._import_column)
            self._importrows = []
            for rowindex in xrange(0, tabledata.getRowCount()):
                importcolumndata = tabledata.getDataItemByColumnName(rowindex, self._import_column)
                if importcolumndata:
                    nodelevel = tabledata.getDataItem(rowindex, 0)
                    key = tabledata.getDataItem(rowindex, 1)
                    viewformat = tabledata.getDataItem(rowindex, 2)
                    self._importrows.append({'node': nodelevel, 'key': key, 'view_format': viewformat, 'command': importcolumndata}) 
#            self.setDatasetParserRows(self._importrows)
        # Create export info.
        if self._export_column:
#            self.addMetadata('Export column', self._export_column)
            self._columnsinfo = []
            for rowindex in xrange(0, tabledata.getRowCount()):
                exportcolumndata = tabledata.getDataItemByColumnName(rowindex, self._export_column)
                if exportcolumndata:
                    nodelevel = tabledata.getDataItem(rowindex, 0)
                    if nodelevel != 'info':
                        key = tabledata.getDataItem(rowindex, 1)
                        viewformat = tabledata.getDataItem(rowindex, 2)
                        self._columnsinfo.append({'header': exportcolumndata, 'node': nodelevel, 'key': key, 'view_format': viewformat}) 
#            self.setExportTableColumns(self._columnsinfo)
