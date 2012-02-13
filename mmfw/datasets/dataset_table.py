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

class DatasetTable(object):
    def __init__(self):
        """ This class should be used for datasets organazed as a table with header and rows. 
        It is prepared to be displayed via QAbstractTableModel in Qt.
        """
        self._metadata = {}
        self._header = []
        self._rows = []
        
    def clear(self):
        """ """
        self._metadata = {}
        self._header = []
        self._rows = []

    def getMetadata(self):
        """ """
        return self._metadata

    def addMetadata(self, key, value):
        """ """
        self._metadata[key] = value

    def setHeader(self, header):
        """ """
        self._header = header

    def appendRow(self, row):
        """ """
        self._rows.append(row)

    def getHeader(self):
        """ """
        return self._header

    def getRows(self):
        """ """
        return self._rows

    def getHeaderItem(self, column):
        """ Used for calls from QAbstractTableModel. """
        try:
            return self._header[column]
        except Exception:
            return ''

    def getDataItem(self, row, column):
        """ Used for calls from QAbstractTableModel. """
        try:
            return self._rows[row][column]
        except Exception:
            return ''

    def getColumnCount(self):
        """ Used for calls from QAbstractTableModel. """
        try:
            return len(self._header)
        except Exception:
            return 0

    def getRowCount(self):
        """ Used for calls from QAbstractTableModel. """
        try:
            return len(self._rows)
        except Exception:
            return 0

#    def SaveAsTextFile(self, fileName):
#        """ """
#        if fileName == None:
#            raise UserWarning('File name is missing.')
#        try:
##            txtencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, txt-files', 'cp1252')
##            txtencode = 'UTF8'
#            txtencode = u'cp1252'
#            out = codecs.open(fileName, mode = 'w', encoding = txtencode)
#            separator = '\t' # Use tab as item separator.
#            # Header.
#            out.write(separator.join(map(unicode, self._header)) + '\r\n')
#            # Rows.
#            for row in self._rows:
#                # Use tab as column separator and CR/LF as row delimiter.
#                out.write(separator.join(map(unicode, row)) + '\r\n')
#        except (IOError, OSError):
#            mmfw.Logging().log("Failed to write to file: " + fileName)
#            raise
#        finally:
#            if out: out.close()

#    def SaveExcelXlsxFile(self, fileName):
#        """ """
#        if fileName == None:
#            raise UserWarning('File name is missing.')
#        try:
#            workbook = excelworkbook.Workbook() # Create workbook.
#            worksheet = workbook.get_active_sheet() # Workbooks contains at least one worksheet.
#            # Header.
#            for columnindex, item in enumerate(self._header):
#                cell = worksheet.cell(row=0, column=columnindex)
#                cell.value = unicode(item)
#            # Rows.
#            for rowindex, row in enumerate(self._rows):
#                for columnindex, item in enumerate(row):
#                    cell = worksheet.cell(row=rowindex + 1, column=columnindex)
#                    cell.value = unicode(item)
#            #    
#            excelwriter.save_workbook(workbook, fileName)
#        except (IOError, OSError):
#            mmfw.Logging().log("Failed to write to file: " + fileName)
#            raise
