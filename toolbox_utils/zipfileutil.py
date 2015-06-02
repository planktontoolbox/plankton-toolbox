#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import zipfile
import locale

class ZipFileUtil():
    """ """
    def __init__(self, 
                 zip_file_name): 
        """ """
        self._filepathname = zip_file_name
        self._zip = None
        if not zipfile.is_zipfile(self._filepathname):
            raise UserWarning('Selected file is not a valid zip file: ' + self._filepathname)

    def open(self):
        """ """
        self._zip = zipfile.ZipFile(self._filepathname, 'r')

    def close(self):
        """ """
        self._zip.close()
        self._zip = None

    def listContent(self):
        """ """
        if self._zip is None:
            self.open()    
        if self._zip:
            return self._zip.namelist()
        else:
            return {}

    def getZipEntry(self,
                    zip_entry_name):
        """ """
        if self._zip is None:
            self.open()    
        if zip_entry_name not in self._zip.namelist():
            raise UserWarning('The entry ' + zip_entry_name + ' is missing in ' + self._filepathname)
        #    
        return self._zip.open(zip_entry_name).read()

    def getZipEntryAsTable(self,
                           zip_entry_name, 
                           encoding = None):
        
#                         field_separator = '\t',
#                           row_separator = '\r\n'):

        
        
        """ """
        if self._zip is None:
            self.open()    
        if zip_entry_name not in self._zip.namelist():
            raise UserWarning('The entry ' + zip_entry_name + ' is missing in ' + self._filepathname)
        # Get encoding.
        if encoding is None:
            encoding = locale.getpreferredencoding()
        #
        target_header = [] 
        target_rows = []
        #
        try:
            zipfiledata = self._zip.open(zip_entry_name).read()
            #
            fieldseparator = None
            # Iterate over rows in file.            
#             for rowindex, row in enumerate(zipfiledata.split('\r\n')):
            for rowindex, row in enumerate(zipfiledata.split('\n')):
#             for rowindex, row in enumerate(zipfiledata.split('\r\n')):
                # Convert to unicode.
#                 row = unicode(row, encoding, 'strict')
                if rowindex == 0:
                    # Header.
                    fieldseparator = self.getSeparator(row)
                    row = [item.strip() for item in row.split(fieldseparator)]
                    target_header = row
                else:
                    # Row.
                    if len(row.strip()) == 0: 
                        continue # Don't add empty rows.
                    row = [item.strip() for item in row.split(fieldseparator)]
                    target_rows.append(row)             
        #
        except Exception as e:
            msg = 'Can\'t read zip file. Entry name: ' + zip_entry_name + '. Exception: ' + unicode(e)
            print(msg)
            raise UserWarning(msg)
        #
        return (target_header, target_rows)

    def getSeparator(self, row):
        """ """
        if '\t' in row: # First alternative.
            return '\t'
        elif ';' in row: # Second alternative. 
            return ';'
        else:
            return '\t' # Default alternative.
