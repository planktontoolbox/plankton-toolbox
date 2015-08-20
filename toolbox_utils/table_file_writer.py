#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os
import locale
import codecs
import zipfile
import tempfile
import shutil
 
# This utility should work even if openpyxl is not installed, but with no Excel support.
openpyxl_installed = True
try: import lib.openpyxl as openpyxl
except ImportError: 
    openpyxl_installed = False
    print('Excel files not suported since openpyxl is not installed.')
 
class TableFileWriter():
    """ 
    This class can write table oriented data to text files, Excel files or to text entries in zip files.      
    For usage examples see the test part at the end of the source code file.
    """
    def __init__(self,
                file_path = None, # Used for all files. 
                text_file_name = None, # Used for text files.
                excel_file_name = None, # Used for excel files.
                excel_sheet_name = None, # Used to select sheet in excel files. None = first sheet.
                zip_file_name = None, # Used for zip files.
                zip_file_entry = None, # Used for text file entries in zip files.
                field_delimiter = '\t', 
                row_delimiter = '\r\n', 
                encoding = 'cp1252', # 'cp1252': Mostly used by windows users and accepts latin-1. 
                encoding_error_handling = 'ignore', # Alternatives: 'strict', 'replace', 'ignore', 
                                                    # 'xmlcharrefreplace', 'backslashreplace'. 
                ):
        """ """
        self._file_path = file_path
        self._text_file_name = text_file_name
        self._excel_file_name = excel_file_name
        self._excel_sheet_name = excel_sheet_name
        self._zip_file_name = zip_file_name
        self._zip_file_entry = zip_file_entry
        self._field_delimiter = field_delimiter
        self._row_delimiter = row_delimiter
        self._encoding = encoding
        self._encoding_error_handling = encoding_error_handling

    def set_filename(self,
                    file_path = None,
                    text_file_name = None,
                    excel_file_name = None,
                    excel_sheet_name = None,
                    zip_file_name = None,
                    zip_file_entry = None,
                    ):
        """ Update filenames if changed from object creation. """
        self._file_path = file_path
        self._text_file_name = text_file_name
        self._excel_file_name = excel_file_name
        self._excel_sheet_name = excel_sheet_name
        self._zip_file_name = zip_file_name
        self._zip_file_entry = zip_file_entry

    def write_file(self, table_header, table_rows):
        """ Write files in different formats depending on parameter values
            defined in constructor. Multiple file formats are possible to create simultaneous. """
        # Text file.                
        if self._text_file_name is not None:
            self._write_text_file(table_header, table_rows)
        # Excel.    
        if self._excel_file_name is not None:
            self._write_excel_file(table_header, table_rows)
        # Text file in zip.    
        if self._zip_file_name:
            self._write_zip_entry(table_header, table_rows)

    def _write_text_file(self, table_header, table_rows):
        """ Private method. Use write_file() above. """
        # File path and name.
        filepathname = self._text_file_name
        if self._file_path and self._text_file_name:
            filepathname = os.path.join(self._file_path, self._text_file_name)
        if filepathname is None:
            raise UserWarning('File name is missing.')
        #Create path if not exists.
        if (self._file_path) and (not os.path.exists(self._file_path)):
            try:
                os.makedirs(self._file_path)
                print('Directories created for this path: ' + self._file_path)
            except Exception as e:
                raise UserWarning('Can\'t create directories in path. Path: ' + self._file_path + '. Exception: ' + e)
        # Get encoding.
        if self._encoding is None:
            self._encoding = locale.getpreferredencoding()
        #
        out = None
        try:
            out = codecs.open(filepathname, mode = 'w', encoding = self._encoding, errors = self._encoding_error_handling)
            # Header.
            out.write(self._field_delimiter.join(table_header) + self._row_delimiter)
            # Rows.
            for row in table_rows:
                out.write(self._field_delimiter.join(row) + self._row_delimiter)
        except Exception as e:
            print('Failed to write to text file: ' + filepathname )
            raise
        finally:
            if out: out.close()
        
    def _write_excel_file(self, table_header, table_rows):
        """ Private method. Use write_file() above. """
        #
        if openpyxl_installed == False:
            raise UserWarning('Can\'t write to .xlsx files ("openpyxl" is not installed).')
        # File path and name.
        filepathname = self._excel_file_name
        if self._file_path and self._excel_file_name:
            filepathname = os.path.join(self._file_path, self._excel_file_name)
        if filepathname is None:
            raise UserWarning('File name is missing.')
        #Create path if not exists.
        if (self._file_path) and (not os.path.exists(self._file_path)):
            try:
                os.makedirs(self._file_path)
                print('Directories created for this path: ' + self._file_path)
            except Exception as e:
                raise UserWarning('Can\'t create directories in path. Path: ' + self._file_path + '. Exception: ' + e)
        # Get encoding.
        if self._encoding is None:
            self._encoding = locale.getpreferredencoding()
        #
        try:
            workbook = openpyxl.Workbook(optimized_write = True)  # Supports big files.
            worksheet = workbook.create_sheet()
            # Header.
            worksheet.append(table_header)
            # Rows.
            for row in table_rows:
                worksheet.append(row)
            # Save to file.   
            workbook.save(filepathname)
        #
        except Exception as e:
            msg = 'Failed to write to file: ' + filepathname + '. Exception: ' + unicode(e)
            print(msg)
            raise

    def _write_zip_entry(self, table_header, table_rows):
        """ Private method. Use write_file() above. """
        # File path and name.
        filepathname = self._zip_file_name
        if self._file_path and self._zip_file_name:
            filepathname = os.path.join(self._file_path, self._zip_file_name)
        if filepathname is None:
            raise UserWarning('File name is missing.')
        #Create path if not exists.
        if (self._file_path) and (not os.path.exists(self._file_path)):
            try:
                os.makedirs(self._file_path)
                print('Directories created for this path: ' + self._file_path)
            except Exception as e:
                raise UserWarning('Can\'t create directories in path. Path: ' + self._file_path + '. Exception: ' + e)
        # Get encoding.
        if self._encoding is None:
            self._encoding = locale.getpreferredencoding()
        #
        zip_entries = []
        zip_entries.append(self._zip_file_entry)
        #
        if len(zip_entries) > 0:
            self._remove_entries_from_zip(self._file_path, 
                                          self._zip_file_name, 
                                          zip_entries)
            #
            zip_write = zipfile.ZipFile(filepathname, 'a', zipfile.ZIP_DEFLATED) # Append to zip.
            try:
                data = self._field_delimiter.join(table_header)
                for row in table_rows:
                    data += self._row_delimiter + self._field_delimiter.join(row)
                #
                zip_write.writestr(self._zip_file_entry, 
                                   data.encode(self._encoding, self._encoding_error_handling))
            finally:
                zip_write.close()
        
    def _remove_entries_from_zip(self, zip_file_path, zip_file_name, entries):
        """ There is no method in Python for this. 
            Copy everything else to a temporary zip file and rename when finished. """
        #
        zip_file = os.path.join(zip_file_path, zip_file_name)
        if (zip_file) and (not os.path.exists(zip_file)):
            return # Nothing to remove. 
        #
        zip_read = zipfile.ZipFile(zip_file, 'r')
        try:
            # Check if zip file contains selected entries.
            containsentry = False
            for entry in zip_read.infolist():
                if entry.filename in entries:
                    containsentry = True
                    break
            if containsentry:
                tmpdir = tempfile.mkdtemp()
                try:
                    new_tmp_file = os.path.join(tmpdir, 'tmp.zip')
                    zip_write = zipfile.ZipFile(new_tmp_file, 'w', zipfile.ZIP_DEFLATED)
                    for item in zip_read.infolist():
                        if item.filename not in entries:
                            data = zip_read.read(item.filename)
                            zip_write.writestr(item, data)
                    #
                    zip_write.close()
                    shutil.move(new_tmp_file, zip_file)
                finally:
                    shutil.rmtree(tmpdir) # Delete the temporary directory.
        finally:
            zip_read.close()


 
# ===== TEST =====
 
if __name__ == "__main__":
    """ Used for testing. """
     
    header = ['aaa', 'bbb', 'ccc']
    rows = [['111', '222', '333'], 
            ['444', '555', '666'],
            ['777', '888', '999'],
            ]
    
    print('\n=== TEST: Write text file. ===')
    tablefilewriter = TableFileWriter(
                file_path = '../test_data',
                text_file_name = 'test_text_writer.txt',                 
                )
    tablefilewriter.write_file(header, rows)
               
    print('\n=== TEST: Write excel file. ===')
    tablefilewriter.set_filename(
                file_path = '../test_data',
                excel_file_name = 'test_text_writer.xlsx',
                )
    tablefilewriter.write_file(header, rows)
     
    print('\n=== TEST: Write to zip file. ===')
    tablefilewriter.set_filename(
                file_path = '../test_data',
                zip_file_name = 'test_text_writer.zip', 
                zip_file_entry = 'test_text_writer.txt',
                )
    tablefilewriter.write_file(header, rows)

