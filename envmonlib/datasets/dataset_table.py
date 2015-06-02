#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import envmonlib
#from envmonlib import DatasetBase

class DatasetTable(envmonlib.DatasetBase):
    def __init__(self):
        """ This class should be used for datasets organized as a table with header and rows. 
        It is prepared to be displayed via QAbstractTableModel in Qt, but Qt is not required here.
        """
        super(DatasetTable, self).__init__()
        #
        self._header = []
        self._rows = []
        
    def clear(self):
        """ """
        self._header = []
        self._rows = []

    def clearRows(self):
        """ """
        self._rows = []

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

    def setDataItem(self, row, column, value):
        """ Used for calls from editable table model. """
        self._rows[row][column] = value

    def getDataItemByColumnName(self, row, column_name):
        """  """
        try:
            column = self._header.index(column_name)
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

