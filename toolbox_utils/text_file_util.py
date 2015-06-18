#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os
import locale
import codecs

class TextFileUtil():
    """ """
    def __init__(self):
        """ """
        
    def read_table_data(self, 
                        file_path,
                        file_name, # May contain both path and name if 'file_path' is empty.
                        header_row = 0, # First row.
                        data_rows_from = 1, # Second row. 
                        data_rows_to = None, # None = Read all rows.
                        select_columns_by_name = [], # To reduce the number of columns.
                        select_columns_by_index = [], # To reduce the number of columns.
                        encoding = 'cp1252', # Alternatives: None(=preferred), 'cp1252', 'utf8', etc. 
                        encoding_error_handling = 'strict', # Alternatives: 'strict', 'replace', 'ignore', 
                                                            # 'xmlcharrefreplace', 'backslashreplace'. 
                        field_delimiter = None, # Alternatives: '\t', ';', ','.
                        row_delimiter = None, # Alternatives: '\r\n', '\n'.
                        ):
        """ """
        table_header = [] 
        table_rows = []
        # File path and name.
        filename = file_name
        if file_path and file_name:
            filename = os.path.join(file_path, file_name)
        if filename is None:
            raise UserWarning('File name is missing.')
        if not os.path.exists(filename):
            raise UserWarning('File is not found.  File: ' + filename)
        # Get encoding.
        if encoding is None:
            encoding = locale.getpreferredencoding()
        # 
        columnsbyindex = None
        if select_columns_by_index:
            columnsbyindex = select_columns_by_index
        # Read file.
        infile = open(filename, 'r')
        try:
            fielddelimiter = None
            # Iterate over rows in file.            
            for rowindex, row in enumerate(infile):
                if data_rows_to and (rowindex > data_rows_to):
                    break # Break loop if data_row_to is defined and exceeded.
                # Convert to unicode.
                row = unicode(row, encoding, 'strict')
                if rowindex == header_row:
                    # Header.
                    if field_delimiter:
                        fielddelimiter = field_delimiter
                    else:
                        fielddelimiter = self.get_field_delimiter(row)
                    #
                    row = [item.strip() for item in row.split(fielddelimiter)]
                    #
                    if select_columns_by_name:
                        columnsbyindex = [] # Overrides selected_columns_by_index.
                        for headerindex, headername in enumerate(row):
                            if headername in select_columns_by_name:
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

    def write_table_data(self, 
                        file_path,
                        file_name,
                        table_header, 
                        table_rows, 
                        encoding = 'cp1252', # Alternatives: None(=preferred), 'cp1252', 'utf8', etc. 
                        field_delimiter = '\t', # Alternatives: '\t', ';', ','.
                        row_delimiter = '\r\n'):  # Alternatives: '\r\n', '\n'.
        """ """
        # File path and name.
        filename = file_name
        if file_path and file_name:
            filename = os.path.join(file_path, file_name)
        if filename is None:
            raise UserWarning('File name is missing.')
        if (file_path) and (not os.path.exists(file_path)):
            try:
                os.makedirs(file_path)
                print('Directories created for this path: ' + file_path)
            except Exception as e:
                raise UserWarning('Can\'t create directories in path. Path: ' + file_path + '. Exception: ' + e)
        # Get encoding.
        if encoding is None:
            encoding = locale.getpreferredencoding()
        #
        try:
            out = codecs.open(file_name, mode = 'w', encoding = encoding)
            # Header.
            out.write(field_delimiter.join(map(unicode, table_header())) + row_delimiter)
            # Rows.
            for row in table_rows():
                out.write(field_delimiter.join(map(unicode, row)) + row_delimiter)
        except Exception as e:
            print('Failed to write to text file: ' + file_name )
            raise
        finally:
            if out: out.close()

    def get_field_delimiter(self, row):
        """ """
        if '\t' in row: return '\t'
        elif ';' in row: return ';'
        else:
            return '\t' # Default.
