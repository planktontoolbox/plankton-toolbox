#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os
import toolbox_utils

class TableFileReader():
    """ """
    def __init__(self,
                 file_path = None, # Used for text and excel files. 
                 text_file_name = None, # Used for text files.
                 excel_file_name = None, # Used for excel files.
                 zip_file_path = None, # Used for zip files.
                 zip_file_name = None, # Used for zip files.
                 zip_file_entry = None, # Used for text files in zip files.
                 select_columns_by_name = None,
                 select_columns_by_index = None,
                 encoding = None,
                 field_delimiter = None,
                 row_delimiter = None,
                 ):
        """ """
        self._file_path = file_path
        self._text_file_name = text_file_name
        self._excel_file_name = excel_file_name
        self._zip_file_path = zip_file_path
        self._zip_file_name = zip_file_name
        self._zip_file_entry = zip_file_entry
        self._select_columns_by_name = select_columns_by_name
        self._elect_columns_by_index = select_columns_by_index
        self._encoding = encoding
        self._field_delimiter = field_delimiter
        self._row_delimiter = row_delimiter
        #
        self._header = []
        self._rows = []
        # Read data from file.
        self.reload_file()
    
    def header(self):
        """ Header as list. """
        return self._header
    
    def rows(self):
        """ Rows as a list of lists. """
        return self._rows
    
    def clear(self):
        """ """
        self._header = []
        self._rows = []
        
    def create_dictionary(self,
                          # By name.
                          key_column_by_name = None,
                          value_column_by_name = None,
                          # By index.
                          key_column_by_index = None,
                          value_column_by_index = None,
#                           # List by name.
#                           key_columns_by_name = None,
#                           value_columns_by_name = None,
#                           # List by index.
#                           key_columns_by_index = None,
#                           value_columns_by_index = None,
#                           # Column and value delimiters for lists.
#                           # String 
#                           column_delimiter_for_keys = None, # Example: None, '+', etc.
#                           value_delimiter_for_keys = None, # Example: None, '+', etc. 
                          ):
        """ Generates a dictionary based on one or multiple columns. """
        dictionary = {}
        #
        keyindex = None
        valueindex = None
        #
        if key_column_by_name is not None:
            for index, field in enumerate(self._header):
                if field == key_column_by_name:
                    keyindex = index
                    break
        elif key_column_by_index is not None:
            if key_column_by_index < len(self._header):
                keyindex = key_column_by_index
        #
        if value_column_by_name is not None:
            for index, field in enumerate(self._header):
                if field == value_column_by_name:
                    valueindex = index
                    break
        elif value_column_by_index is not None:
            if value_column_by_index < len(self._header):
                valueindex = value_column_by_index
        #
        if (keyindex is not None) and (valueindex is not None):
            for row in self._rows:
                dictionary[row[keyindex]] = row[valueindex]
        else:
            raise UserWarning('Failed to generate dictionary.')            
        #
        return dictionary
        
    def reload_file(self):
        """ """
        
        # Text file.                
        if self._text_file_name is not None:
            filepathname = os.path.join(self._file_path, self._text_file_name)
            textfiles = toolbox_utils.TextFiles()            
            (self._header, self._rows) = textfiles.readToTableDataset(
                                                    filepathname, 
                                                    encoding = self._encoding,
                                                    )
        # Excel.    
        elif self._excel_file_name is not None:
            filepathname = os.path.join(self._file_path, self._excel_file_name)
            excelfiles = toolbox_utils.ExcelFiles()           
            (self._header, self._rows) = excelfiles.readToTableDataset(
                                                    filepathname, 
                                                    )
#         # Text file in zip.    
#         elif self._zip_file_name:
#              self._zip_file_path
#             self._zip_file_name
#             self._zip_file_entry
#             
#             self._encoding
#             self._field_delimiter
#             self._row_delimiter
        else:
            raise UserWarning('File name is missing.')


if __name__ == "__main__":
    """ Used for testing of this utility. """    
    
#     print('\n=== TEST: Text files. ===')
#     tablefilereader = TableFileReader(
#                  file_path = 'test_data',
#                  text_file_name = 'test.txt',
#                  )
#     #
#     print('Header: ' + unicode(tablefilereader.header()))
#     print('Rows:   ' + unicode(tablefilereader.rows()))
#     #
#     testdict = tablefilereader.create_dictionary(key_column_by_name = 'bbb', value_column_by_name = 'ccc')
#     print('Dict by name: ' + unicode(testdict))
#     #
#     testdict = tablefilereader.create_dictionary(key_column_by_index = 0, value_column_by_index = 2)
#     print('Dict by index: ' + unicode(testdict))
    
    print('\n=== TEST: Excel files. ===')
    tablefilereader = TableFileReader(
                 file_path = 'test_data',
                 excel_file_name = 'test.xlsx',
                 )
    #
    print('Header: ' + unicode(tablefilereader.header()))
    print('Rows:   ' + unicode(tablefilereader.rows()))
    #
    testdict = tablefilereader.create_dictionary(key_column_by_name = 'bbb', value_column_by_name = 'ccc')
    print('Dict by name: ' + unicode(testdict))
    #
    testdict = tablefilereader.create_dictionary(key_column_by_index = 0, value_column_by_index = 2)
    print('Dict by index: ' + unicode(testdict))
    
#     print('\n=== TEST: Zip files. ===')
#     tablefilereader = TableFileReader(
#                  file_path = 'test_data',
#                  zip_file_name = 'test.zip', 
#                  zip_file_entry = 'test.txt',
#                  )
#     #
#     print('Header: ' + unicode(tablefilereader.header()))
#     print('Rows:   ' + unicode(tablefilereader.rows()))
#     #
#     testdict = tablefilereader.create_dictionary(key_column_by_name = 'bbb', value_column_by_name = 'ccc')
#     print('Dict by name: ' + unicode(testdict))
#     #
#     testdict = tablefilereader.create_dictionary(key_column_by_index = 0, value_column_by_index = 2)
#     print('Dict by index: ' + unicode(testdict))
    
