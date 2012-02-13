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
Valid nodes in the trees are dataset - visit - sample - variable.
"""

import mmfw

#def get_visit_by_idstring(dataset_node, idstring):
#    """ Used during import when searching for existing nodes. """
#    if not dataset_node:
#        return None
#    if not isinstance(dataset_node, DatasetNode):
#        return None # Must be of the right type.
#    #
#    object = dataset_node.getVisitLookup(idstring)
#    if object:
#        return object
#    else:    
#        for visitnode in dataset_node.getChildren():
#            if visitnode.getIdString() == idstring:
#                dataset_node.setVisitLookup(idstring, visitnode)
#                return visitnode
#    return None
#
#def get_sample_by_idstring(dataset_node, idstring):
#    """ Used during import when searching for existing nodes. """
#    if not dataset_node:
#        return None
#    if not isinstance(dataset_node, SampleNode):
#        return None # Must be of the right type.
#    #
#    object = dataset_node.getSampleLookup(idstring)
#    #
#    object = dataset_node.getSampleLookup(idstring)
#    if object:
#        return object
#    else:            
#        for visitnode in dataset_node.getChildren():
#            for samplenode in visitnode.getChildren():
#                if samplenode.GetIdString() == idstring:
#                    dataset_node.setSampleLookup(idstring, visitnode)
#                    return samplenode
#    return None
#
#def get_variable_by_idstring(dataset_node, idstring):
#    """ Used during import when searching for existing nodes. """
#    if not dataset_node:
#        return None
#    if not isinstance(dataset_node, VariableNode):
#        return None # Must be of the right type.
#    #
#    object = dataset_node.getVariableLookup(idstring)
#    # 
#    object = dataset_node.getVariableLookup(idstring)
#    if object:
#        return object
#    else:    
#        for visitnode in dataset_node.getChildren():
#            for samplenode in visitnode.getChildren():
#                for variablenode in samplenode.getChildren():
#                    if variablenode.GetIdString() == idstring:
#                        dataset_node.setVariableLookup(idstring, visitnode)
#                        return variablenode
#    return None


class DataNode(object):
    """
    Abstract base class for nodes. 
    """
    def __init__(self, parent = None):
        self._parent = parent # Parent node.
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
        
        
class DatasetNode(DataNode):
    """ """
    def __init__(self):
        """ """
#        self._lookuplist = None        
        self._metadata = {}
        self._visit_count = 0
        self._sample_count = 0
        self._variable_count = 0
        self._visit_lookup = {}
        self._sample_lookup = {}
        self._variable_lookup = {}
        super(DatasetNode, self).__init__()

    def clear(self):
        """ """
#        self._lookuplist = None
        super(DatasetNode, self).clear()

    def getMetadata(self):
        """ """
        return self._metadata

    def addMetadata(self, key, value):
        """ """
        self._metadata[key] = value

    def getCounters(self):
        """ """
        return (self._visit_count, self._sample_count, self._variable_count)

    def addChild(self, child):
        """ """
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
        
    def convertToTableDataset(self, target_dataset):
        """ Converts the dataset to a corresponding table based dataset.
        The parameter columns_info should be on the form [{"Header": "", "Node": "", "Key": ""}, ...]
        Example: [{"Header": "SDATE", "Node": "Visit", "Key": "Date"},
                  {"Header": "MNDEP", "Node": "Sample", "Key": "Min. depth"}]
        """



        columns_info = \
            [{"Header": "YEAR", "Node": "Visit", "Key": "Visit year"},
             {"Header": "SDATE", "Node": "Visit", "Key": "Visit date"},
             {"Header": "MXDEP", "Node": "Sample", "Key": "Sample max depth"}]



        if not target_dataset:
            raise UserWarning('Target dataset is missing.')
        if not isinstance(target_dataset, mmfw.DatasetTable):
            raise UserWarning('Target dataset is not of a valid type.')
        if not columns_info:
            raise UserWarning('Columns info is missing.')
        # Header.
        header = []
        for item in columns_info:
            header.append(item['Header'])
        # To target.
        target_dataset.setHeader(header)
        # Rows.
        for visitnode in self.getChildren():
            for samplenode in visitnode.getChildren():
                for variablenode in samplenode.getChildren():
                    #  Create row based on column_info.
                    row = []
                    for column_info in columns_info:
                        if column_info['Node'] == 'Dataset':
                            row.append(self.getData(column_info['Key']))
                        elif column_info['Node'] == 'Visit':
                            row.append(visitnode.getData(column_info['Key']))
                        elif column_info['Node'] == 'Sample':
                            row.append(samplenode.getData(column_info['Key']))
                        elif column_info['Node'] == 'Variable':
                            row.append(variablenode.getData(column_info['Key']))
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
        self.getParent()._sample_count += 1
        super(VisitNode, self).addChild(child)

    def setIdString(self, idstring):
        """ """
        self._idstring = idstring
        # Register in dataset for fast lookup.
        self.getParent()._visit_lookup[idstring] = self
        
        
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
        self.getParent().getParent()._variable_count += 1
        super(SampleNode, self).addChild(child)

    def setIdString(self, idstring):
        """ """
        self._idstring = idstring
        # Register in dataset for fast lookup.
        self.getParent().getParent()._sample_lookup[idstring] = self
        

class VariableNode(DataNode):
    """ """
    def __init__(self):
        """ """
        super(VariableNode, self).__init__()

    def clear(self):
        """ """
        super(VariableNode, self).clear()
        
    def setIdString(self, idstring):
        """ """
        self._idstring = idstring
        # Register in dataset for fast lookup.
        self.getParent().getParent().getParent()._variable_lookup[idstring] = self

