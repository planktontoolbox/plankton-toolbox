#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Project: Moray
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

import locale
import codecs
import envmonlib

class TextFiles():
    """
    This class ...  
    """
    def __init__(self):
        """ """
        
    def readToTableDataset(self, 
                           target_dataset, 
                           file_name,
                           encoding = None):
        """ """
        if file_name == None:
            raise UserWarning("File name is missing.")
        if not isinstance(target_dataset, envmonlib.DatasetTable):
            raise UserWarning("Target dataset is not of valid type.")
        # Get encoding.
        if not encoding:
            encoding = locale.getpreferredencoding()
        # Read file.
        infile = open(file_name, u'r')
        try:
            fieldseparator = None
            # Iterate over rows in file.            
            for rowindex, row in enumerate(infile):
                # Convert to unicode.
                row = unicode(row, encoding, 'strict')
                if rowindex == 0:
                    # Header.
                    fieldseparator = self.getSeparator(row)
                    row = [item.strip() for item in row.split(fieldseparator)]
                    target_dataset.setHeader(row)
                else:
                    # Row.
                    row = [item.strip() for item in row.split(fieldseparator)]
                    target_dataset.appendRow(row)             
        #
        finally:
            if infile: infile.close()


    def writeTableDataset(self, 
                          table_dataset, 
                          file_name,
                          encoding = None,
                          field_separator = u'\t',
                          row_separator = u'\r\n'):
        """ """
        if file_name == None:
            raise UserWarning("File name is missing.")
        if not isinstance(table_dataset, envmonlib.DatasetTable):
            raise UserWarning("Dataset is not of a valid type.")
        #
        if not encoding:
            encoding = locale.getpreferredencoding()
        #
        try:
            out = codecs.open(file_name, mode = 'w', encoding = encoding)
            # Header.
            out.write(field_separator.join(map(unicode, table_dataset.getHeader())) + '\r\n')
            # Rows.
            for row in table_dataset.getRows():
                out.write(field_separator.join(map(unicode, row)) + '\r\n')
        except (IOError, OSError):
            envmonlib.Logging().log("Failed to write to text file: " + file_name)
            raise UserWarning("Failed to write to text file: " + file_name)
        finally:
            if out: out.close()

    def getSeparator(self, row):
        """ """
        if u'\t' in row: # First alternative.
            return u'\t'
        elif u';' in row: # Second alternative. 
            return u';'
        else:
            return u'\t' # Default alternative.
             

