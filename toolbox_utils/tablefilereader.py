#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os
import locale
import zipfile

# This util should work even if openpyxl is not installed, but with no Excel support.
openpyxl_installed = True
try: import openpyxl
except ImportError: openpyxl_installed = False

class TableFileReader():
    """ """
    def __init__(self,
                 file_path = None, # Used for all files. 
                 text_file_name = None, # Used for text files.
                 excel_file_name = None, # Used for excel files.
                 excel_sheet_name = None, # Used to select sheet in excel files. None = first sheet.
                 zip_file_name = None, # Used for zip files.
                 zip_file_entry = None, # Used for text file entries in zip files.
                 select_columns_by_name = None, # Save memory, don't load all columns. Alternative 1.
                 select_columns_by_index = None, # Save memory, don't load all columns. Alternative 2.
                 field_delimiter = None, # None = autodetect. '\t' is recommended. 
                 encoding = 'cp1252', # Mostly used by windows users and accepts latin-1. 
                 encoding_error_handling = 'strict', # Alternatives: 'strict', 'replace', 'ignore', 
                                                     # 'xmlcharrefreplace', 'backslashreplace'. 
                 ):
        """ """
        self._file_path = file_path
        self._text_file_name = text_file_name
        self._excel_file_name = excel_file_name
        self._excel_sheet_name = excel_sheet_name
        self._zip_file_name = zip_file_name
        self._zip_file_entry = zip_file_entry
        self._select_columns_by_name = select_columns_by_name
        self._select_columns_by_index = select_columns_by_index
        self._field_delimiter = field_delimiter
        self._encoding = encoding
        self._encoding_error_handling = encoding_error_handling
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
        """ Call this to free memory. """
        self._header = []
        self._rows = []
        
    def reload_file(self):
        """ Read files in different formats depending on parameter values
            defined in constructor. """
        # Text file.                
        if self._text_file_name is not None:
            (self._header, self._rows) = self._read_text_file()
        # Excel.    
        elif self._excel_file_name is not None:
            (self._header, self._rows) = self._read_excel_file()
        # Text file in zip.    
        elif self._zip_file_name:
            (self._header, self._rows) = self._read_zip_entry()
        else:
            raise UserWarning('File name is missing.')

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
        
    def _read_text_file(self, 
                        header_row = 0, # First row.
                        data_rows_from = 1, # Second row. 
                        data_rows_to = None, # None = Read all rows.
                        ):
        """ """
        table_header = [] 
        table_rows = []
        # File path and name.
        filename = self._text_file_name
        if self._file_path and self._text_file_name:
            filename = os.path.join(self._file_path, self._text_file_name)
        if filename is None:
            raise UserWarning('File name is missing.')
        if not os.path.exists(filename):
            raise UserWarning('File is not found.  File: ' + filename)
        # Get encoding.
        if self._encoding is None:
            self._encoding = locale.getpreferredencoding()
        # 
        columnsbyindex = None
        if self._select_columns_by_index:
            columnsbyindex = self._select_columns_by_index
        # Read file.
        infile = open(filename, 'r')
        try:
            fielddelimiter = None
            # Iterate over rows in file.            
            for rowindex, row in enumerate(infile):
                if data_rows_to and (rowindex > data_rows_to):
                    break # Break loop if data_row_to is defined and exceeded.
                # Convert to unicode.
                row = unicode(row, self._encoding, 'strict')
                if rowindex == header_row:
                    # Header.
                    if self._field_delimiter:
                        fielddelimiter = self._field_delimiter
                    else:
                        fielddelimiter = self._get_field_delimiter(row)
                    #
                    row = [item.strip() for item in row.split(fielddelimiter)]
                    #
                    if self._select_columns_by_name:
                        columnsbyindex = [] # Overrides selected_columns_by_index.
                        for headerindex, headername in enumerate(row):
                            if headername in self._select_columns_by_name:
                                columnsbyindex.append(headerindex)
                    #
                    if columnsbyindex:
                        new_header = []
                        for headerindex, headername in enumerate(row):
                            if headerindex in columnsbyindex:
                                new_header.append(headername)
                        table_header = new_header    
                    else:    
                        table_header = row
                #                                       
                elif rowindex >= data_rows_from:
                    # Row.
                    if len(row.strip()) == 0: 
                        continue # Don't add empty rows.
                    row = [item.strip() for item in row.split(fielddelimiter)]
                    #
                    if columnsbyindex:
                        new_row = []
                        for itemindex, rowitem in enumerate(row):
                            if itemindex in columnsbyindex:
                                new_row.append(rowitem)
                        table_rows.append(new_row)    
                    else:
                        table_rows.append(row)             
        #
        finally:
            if infile: infile.close()
        #
        return (table_header, table_rows)

    def _read_excel_file(self, 
                        header_row = 0, # If header not the first row. 
                        data_rows_from = 1, # If data not starts at second row. 
                        data_rows_to = None, # None = read all.
                        ):
        """ """
        table_header = [] 
        table_rows = []
        #
        if openpyxl_installed == False:
            raise UserWarning('Can\'t read .xlsx files ("openpyxl" is not installed).')
        # File path and name.
        filename = self._excel_file_name
        if self._file_path and self._excel_file_name:
            filename = os.path.join(self._file_path, self._excel_file_name)
        if filename is None:
            raise UserWarning('File name is missing.')
        if not os.path.exists(filename):
            raise UserWarning('File is not found.  File: ' + filename)
        # 
        self._columnsbyindex = None
        if self._select_columns_by_index:
            columnsbyindex = self._select_columns_by_index
        #
        try:
            workbook = openpyxl.load_workbook(filename, use_iterators = True) # Supports big files.
            if workbook == None:
                raise UserWarning('Can\'t read Excel (.xlsx) file.')
            worksheet = None
            if self._excel_sheet_name:
                # 
                if self._excel_sheet_name in workbook.get_sheet_names():
                    worksheet = workbook.get_sheet_by_name(name = self._excel_sheet_name)
                else:
                    raise UserWarning('Excel sheet ' + self._excel_sheet_name + ' not available.')      
            else:
                # Use the first sheet if not specified.
                worksheet = workbook.get_sheet_by_name(name = workbook.get_sheet_names()[0])
            #
            header = []
            for rowindex, row in enumerate(worksheet.iter_rows()):
                if (data_rows_to is not None) and (rowindex > data_rows_to):
                    break # Break loop if data_row_to is defined and exceeded.
                elif rowindex == header_row:
                    for cell in row:
                        value = cell.value
                        if value == None:
                            header.append('')
                        else:
                            header.append(unicode(value).strip())
                    #
                    table_header = header
                elif rowindex >= data_rows_from:
                    newrow = []
                    for cell in row:
                        value = cell.value
                        if value == None:
                            newrow.append('')
                        else:
                            newrow.append(unicode(value).strip())
                    #
                    table_rows.append(newrow)
            #
            return (table_header, table_rows)
        #  
        except Exception as e:
            msg = 'Failed to read from file. File name: ' + filename + '. Exception: ' + unicode(e)
            print(msg)
            raise

    def _read_zip_entry(self):
        """ """
        filename = self._zip_file_name
        if self._file_path and self._zip_file_name:
            filename = os.path.join(self._file_path, self._zip_file_name)
        #
        zip = None
        if not zipfile.is_zipfile(filename):
            raise UserWarning('Selected file is not a valid zip file: ' + filename)

        zip = zipfile.ZipFile(filename, 'r')

        if self._zip_file_entry not in zip.namelist():
            raise UserWarning('The entry ' + self._zip_file_entry + ' is missing in ' + filename)
        #    
        # Get encoding.
        if self._encoding is None:
            self._encoding = locale.getpreferredencoding()
        #
        target_header = [] 
        target_rows = []
        #
        try:
            zipfiledata = zip.open(self._zip_file_entry).read()
            #
            fieldseparator = None
            # Iterate over rows in file.            
#             for rowindex, row in enumerate(zipfiledata.split('\r\n')):
            for rowindex, row in enumerate(zipfiledata.split('\n')):
#             for rowindex, row in enumerate(zipfiledata.split('\r\n')):
#             for rowindex, row in enumerate(unicode(zipfiledata).splitline()):
                # Convert to unicode.
#                 row = unicode(row, encoding, 'strict')
                if rowindex == 0:
                    # Header.
                    fielddelimiter = self._get_field_delimiter(row)
                    row = [item.strip() for item in row.split(fielddelimiter)]
                    target_header = row
                else:
                    # Row.
                    if len(row.strip()) == 0: 
                        continue # Don't add empty rows.
                    row = [item.strip() for item in row.split(fieldseparator)]
                    target_rows.append(row)             
        #
        except Exception as e:
            msg = 'Can\'t read zip file. Entry name: ' + self._zip_file_entry + '. Exception: ' + unicode(e)
            print(msg)
            raise UserWarning(msg)
        #

        zip.close()

        return (target_header, target_rows)

    def _get_field_delimiter(self, row):
        """ """
        if '\t' in row: return '\t'
        elif ';' in row: return ';'
        else:
            return '\t' # Default.


# ===== TEST =====

if __name__ == "__main__":
    """ Used for testing of this utility. """    
    
    print('\n=== TEST: Text files. ===')
    tablefilereader = TableFileReader(
                 file_path = 'test_data',
                 text_file_name = 'test.txt',                 
                select_columns_by_index = [0, 1],
#                  select_columns_by_name = ['ccc', 'aaa'],
                 )
    print('Header: ' + unicode(tablefilereader.header()))
    print('Rows:   ' + unicode(tablefilereader.rows()))
    testdict = tablefilereader.create_dictionary(key_column_by_name = 'bbb', value_column_by_name = 'aaa')
    print('Dict by name: ' + unicode(testdict))
    testdict = tablefilereader.create_dictionary(key_column_by_index = 0, value_column_by_index = 1)
    print('Dict by index: ' + unicode(testdict))
     
    print('\n=== TEST: Excel files. ===')
    tablefilereader = TableFileReader(
                 file_path = 'test_data',
                 excel_file_name = 'test.xlsx',
                 )
    print('Header: ' + unicode(tablefilereader.header()))
    print('Rows:   ' + unicode(tablefilereader.rows()))
    testdict = tablefilereader.create_dictionary(key_column_by_name = 'bbb', value_column_by_name = 'ccc')
    print('Dict by name: ' + unicode(testdict))    #
    testdict = tablefilereader.create_dictionary(key_column_by_index = 1, value_column_by_index = 2)
    print('Dict by index: ' + unicode(testdict))
    
    print('\n=== TEST: Zip files. ===')
    tablefilereader = TableFileReader(
                 file_path = 'test_data',
                 zip_file_name = 'test.zip', 
                 zip_file_entry = 'test.txt',
                 )
    print('Header: ' + unicode(tablefilereader.header()))
    print('Rows:   ' + unicode(tablefilereader.rows()))
    testdict = tablefilereader.create_dictionary(key_column_by_name = 'ccc', value_column_by_name = 'aaa')
    print('Dict by name: ' + unicode(testdict))
    testdict = tablefilereader.create_dictionary(key_column_by_index = 2, value_column_by_index = 0)
    print('Dict by index: ' + unicode(testdict))

