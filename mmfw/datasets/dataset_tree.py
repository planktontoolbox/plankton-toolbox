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

"""
Functions and classes in this module should be used for datasets organized as trees.
Valid node order in the tree is dataset - visit - sample - variable.
"""

import mmfw
#from mmfw import DatasetBase

class DataNode(object):
    """
    Abstract base class for nodes. 
    """
    def __init__(self):
        self._parent = None # Parent node.
        self._children = [] # List of child nodes.
        self._datadict = {} # Dictionary for node data.
        self._idstring = None # Used during import when searching for existing nodes.
        
    def clear(self):
        """ """
        self._parent = None
        self._children = []
        self._datadict = {}
        
    def setParent(self, parent):
        """ """
        self._parent = parent
        
    def getParent(self):
        """ """
        return self._parent
        
    def addChild(self, child):
        """ """
        self._children.append(child)
        # Set this node as parent for child.
        child.setParent(self)

    def getChildren(self):
        """ """
        return self._children
        
    def addData(self, key, value):
        """ """
        self._datadict[key] = value
        
    def getData(self, key):
        """ """
        return self._datadict.get(key, '')
        
    def getDataDict(self):
        """ """
        return self._datadict
        
#    def setIdString(self, _idstring):
#        """ """
#        self._idstring = _idstring
#        
    def getIdString(self):
        """ """
        return self._idstring
        
        
class DatasetNode(mmfw.DatasetBase, DataNode):
    """ This it the top node for tree datasets. 
    Note: Multiple inheritance. DataNode for data and tree structure. DatasetBase for metadata. 
    """
    def __init__(self):
        """ """
#        self._lookuplist = None        
        super(DatasetNode, self).__init__()
        #
        self._visit_count = 0
        self._sample_count = 0
        self._variable_count = 0
        self._visit_lookup = {}
        self._sample_lookup = {}
        self._variable_lookup = {}
        #
        self._importmatrixrows = []
        self._exporttablecolumns = []

    def clear(self):
        """ """
#        self._lookuplist = None
        super(DatasetNode, self).clear()

    def getCounters(self):
        """ """
        return (self._visit_count, self._sample_count, self._variable_count)

    def addChild(self, child):
        """ """
        if not isinstance(child, mmfw.VisitNode):
            raise UserWarning("AddChild failed. Dataset children must be of visit type")
        #
        self._visit_count += 1
        super(DatasetNode, self).addChild(child)

    def getVisitLookup(self, idString):
        """ """
        return self._visit_lookup.get(idString, None)
        
    def getSampleLookup(self, idString):
        """ """
        return self._sample_lookup.get(idString, None)
        
    def getVariableLookup(self, idString):
        """ """
        return self._variable_lookup.get(idString, None)

    def setImportsMatrixRows(self):
        """ """

    def loadImportMatrix(self, matrix_file, import_column, export_column):
        """ """
        # Add metadata
        self.addMetadata(u'Matrix', matrix_file)
        self.addMetadata(u'Import column', import_column)
        self.addMetadata(u'Export column', export_column)
        # Read matrix.
        excelreader = mmfw.ExcelFileReader()
        excelreader.readFile(file_name = matrix_file)
        # Create import info.
        importrows = []
        for rowindex in xrange(0, excelreader.getRowCount()):
            importcolumndata = excelreader.getDataCellByName(rowindex, import_column)
            if importcolumndata:
                nodelevel = excelreader.getDataCell(rowindex, 0)
                key = excelreader.getDataCell(rowindex, 1)
                importrows.append({u'Node': nodelevel, u'Key': key, u'Command': importcolumndata}) 
        self.setImportMatrixRows(importrows)
        # Create export info.
        columnsinfo = []
        for rowindex in xrange(0, excelreader.getRowCount()):
            exportcolumndata = excelreader.getDataCellByName(rowindex, export_column)
            if exportcolumndata:
                nodelevel = excelreader.getDataCell(rowindex, 0)
                key = excelreader.getDataCell(rowindex, 1)
                columnsinfo.append({u'Header': exportcolumndata, u'Node': nodelevel, u'Key': key}) 
        self.setExportTableColumns(columnsinfo)

    def setImportMatrixRows(self, import_matrix_rows):
        """ """
        self._importmatrixrows = import_matrix_rows

    def getImportMatrixRows(self):
        """ """
        return self._importmatrixrows

    def setExportTableColumns(self, columns_info_dict):
        """ """
        self._exporttablecolumns = columns_info_dict

    def getExportTableColumns(self):
        """ """
        return self._exporttablecolumns

    def convertToTableDataset(self, target_dataset):
        """ Converts the tree dataset to a corresponding table based dataset.
        The parameter self._exporttablecolumns should be on the form [{"Header": "", "Node": "", "Key": ""}, ...]
        Example: [{"Header": "SDATE", "Node": "Visit", "Key": "Date"},
                  {"Header": "MNDEP", "Node": "Sample", "Key": "Min. depth"}]
        """
        # TODO: For test.
#        self._exporttablecolumns = \
#            [{"Header": "YEAR", "Node": "Visit", "Key": "Visit year"},
#             {"Header": "SDATE", "Node": "Visit", "Key": "Visit date"},
#             {"Header": "MXDEP", "Node": "Sample", "Key": "Sample max depth"}]
        #
        if not target_dataset:
            raise UserWarning('Target dataset is missing.')
        if not isinstance(target_dataset, mmfw.DatasetTable):
            raise UserWarning('Target dataset is not of a valid type.')
        if not self._exporttablecolumns:
            raise UserWarning('Info for converting from tree to table dataset is missing.')
        # Header.
        header = []
        for item in self._exporttablecolumns:
            header.append(item.get('Header', u'---'))
        # To target.
        target_dataset.setHeader(header)
        # Rows.
        for visitnode in self.getChildren():
            for samplenode in visitnode.getChildren():
                for variablenode in samplenode.getChildren():
                    #  Create row based on column_info from self._exporttablecolumns.
                    row = []
                    for column_info in self._exporttablecolumns:
                        if column_info.get('Node', u'') == 'Dataset':
                            row.append(self.getData(column_info.get('Key', u'---')))
                        elif column_info.get('Node', u'') == 'Visit':
                            row.append(visitnode.getData(column_info.get('Key', u'---')))
                        elif column_info.get('Node', u'') == 'Sample':
                            row.append(samplenode.getData(column_info.get('Key', u'---')))
                        elif column_info.get('Node', u'') == 'Variable':
                            row.append(variablenode.getData(column_info.get('Key', u'---')))
                        else:
                            row.append(u'')
                    # To target.
                    target_dataset.appendRow(row)


class VisitNode(DataNode):
    """ """
    def __init__(self):
        """ """
        super(VisitNode, self).__init__()

    def clear(self):
        """ """
        super(VisitNode, self).clear()

    def addChild(self, child):
        """ """
        if not isinstance(child, mmfw.SampleNode):
            raise UserWarning("AddChild failed. Visit children must be of sample type")
        #
        self.getParent()._sample_count += 1
        super(VisitNode, self).addChild(child)

    def setIdString(self, idstring):
        """ """
        self._idstring = idstring
        # Register in dataset for fast lookup.
        try:
            self.getParent()._visit_lookup[idstring] = self
        except:
            raise UserWarning("SetIdString failed. Check if parent is assigned.")
        
        
class SampleNode(DataNode):
    """ """
    def __init__(self):
        """ """
        super(SampleNode, self).__init__()

    def clear(self):
        """ """
        super(SampleNode, self).clear()
        
    def addChild(self, child):
        """ """
        if not isinstance(child, mmfw.VariableNode):
            raise UserWarning("AddChild failed. Sample children must be of variable type")
        #
        self.getParent().getParent()._variable_count += 1
        super(SampleNode, self).addChild(child)

    def setIdString(self, idstring):
        """ """
        self._idstring = idstring
        # Register in dataset for fast lookup.
        try:
            self.getParent().getParent()._sample_lookup[idstring] = self
        except:
            raise UserWarning("SetIdString failed. Check if parent is assigned.")
        

class VariableNode(DataNode):
    """ """
    def __init__(self):
        """ """
        super(VariableNode, self).__init__()

    def clear(self):
        """ """
        super(VariableNode, self).clear()
        
    def addChild(self, child):
        """ """
        raise UserWarning("AddChild failed. Variables can't add children.")

    def setIdString(self, idstring):
        """ """
        self._idstring = idstring
        # Register in dataset for fast lookup.
        try:
            self.getParent().getParent().getParent()._variable_lookup[idstring] = self
        except:
            raise UserWarning("SetIdString failed. Check if parent is assigned.")

