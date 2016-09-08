#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import copy
import toolbox_utils
import plankton_core

@toolbox_utils.singleton
class Datasets(object):
    """ Singleton object used to hold a list of datasets. """
    
    def __init__(self):
        """ """
        self._datasets = []

    def clear(self):
        """ """
        self._datasets = []
        
    def get_datasets(self):
        """ """
        return self._datasets 
        
    def get_dataset_by_index(self, index):
        """ """
        if len(self._datasets) > index:
            return self._datasets[index]
        return None 
        
    def add_dataset(self, dataset_node):
        """ """
        self._datasets.append(dataset_node)
        
    def remove_dataset_by_index(self, index):
        """ """
        if (index >= 0) or (len(self._datasets) > index):
            del self._datasets[index]


class DatasetBase(object):
    def __init__(self):
        """ Base class for datasets, mainly used for metadata. """
        super(DatasetBase, self).__init__()
        self._metadata = {}
        
    def clear(self):
        """ """
        self._metadata = {}

    def get_metadata(self, key):
        """ """
        return self._metadata.get(key, '')

    def add_metadata(self, key, value):
        """ """
        self._metadata[key] = value

#     def save_as_text_file(self, file_name):
#         """ """
#         toolbox_utils.TextFiles().writeTableDataset(self, file_name)
# 
#     def save_as_excel_file(self, file_name):
#         """ """
#         toolbox_utils.ExcelFiles().writeTableDataset(self, file_name)


class DatasetTable(DatasetBase):
    def __init__(self):
        """ 
        This class should be used for datasets organized as a table with header and rows. 
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

    def clear_rows(self):
        """ """
        self._rows = []

    def set_header(self, header):
        """ """
        self._header = header

    def append_row(self, row):
        """ """
        self._rows.append(row)

    def get_header(self):
        """ """
        return self._header

    def get_rows(self):
        """ """
        return self._rows

    def get_header_item(self, column):
        """ Used for calls from QAbstractTableModel. """
        try:
            return self._header[column]
        except Exception:
            return ''

    def get_data_item(self, row, column):
        """ Used for calls from QAbstractTableModel. """
        try:
            return self._rows[row][column]
        except Exception:
            return ''

    def set_data_item(self, row, column, value):
        """ Used for calls from editable table model. """
        self._rows[row][column] = value

    def get_data_item_by_column_name(self, row, column_name):
        """  """
        try:
            column = self._header.index(column_name)
            return self._rows[row][column]
        except Exception:
            return ''

    def get_column_count(self):
        """ Used for calls from QAbstractTableModel. """
        try:
            return len(self._header)
        except Exception:
            return 0

    def get_row_count(self):
        """ Used for calls from QAbstractTableModel. """
        try:
            return len(self._rows)
        except Exception:
            return 0

    def save_as_file(self, text_file_name = None, excel_file_name = None):
        """ Save to text or Excel, depending on which parameter is used. """
        tablefilewriter = toolbox_utils.TableFileWriter(
                                file_path = '', # Is included in the file names below.
                                text_file_name = text_file_name,                 
                                excel_file_name = excel_file_name,                 
                                )
        #
        tablefilewriter.write_file(self._header, 
                                   self._rows)
        

"""
Functions and classes below should be used for datasets organized as trees.
Valid node order in the tree is dataset - visit - sample - variable.
"""

class DataNode(object):
    """
    Abstract base class for tree nodes. 
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
        self._idstring = None
        
    def set_parent(self, parent):
        """ """
        self._parent = parent
        
    def get_parent(self):
        """ """
        return self._parent
        
    def add_child(self, child):
        """ """
        self._children.append(child)
        # Set this node as parent for child.
        child.set_parent(self)

    def get_children(self):
        """ """
        return self._children

    def remove_all_children(self):
        """ """
        self._children = []
        
    def remove_child(self, child_object):
        """ """
        if child_object in self._children: 
            self._children.remove(child_object)
        else:
            print('DEBUG: Can\'t remove child.')
        
    def add_data(self, key, value):
        """ """
#        if value:
#            self._datadict[key] = value
        # TODO: Will use more memory, but otherwise float with value 0 will be missed in dict. Check other types... 
        if key:
            self._datadict[key] = value
        
    def get_data(self, key, default_value = ''):
        """ """
        return self._datadict.get(key, default_value)

    def get_data_dict(self):
        """ """
        return self._datadict
        
    def set_data_dict(self, data_dict):
        """ """
        self._datadict = data_dict
        
#    def set_id_string(self, _idstring):
#        """ """
#        self._idstring = _idstring
#        
    def get_id_string(self):
        """ """
        return self._idstring
        
        
class DatasetNode(DatasetBase, DataNode):
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
        self._datasetparserrows = []
        self._exporttablecolumns = []

    def clear(self):
        """ """
#        self._lookuplist = None
        super(DatasetNode, self).clear()

    def get_counters(self):
        """ """
        return (self._visit_count, self._sample_count, self._variable_count)

    def add_child(self, child):
        """ """
        if not isinstance(child, VisitNode):
            raise UserWarning('AddChild failed. Dataset children must be of visit type')
        #
        self._visit_count += 1
        super(DatasetNode, self).add_child(child)

    def remove_all_children(self):
        """ """
        self._visit_count -= len(self._children)
        self._children = []
        
    def get_visit_lookup(self, idString):
        """ """
        return self._visit_lookup.get(idString, None)
        
    def get_sample_lookup(self, idString):
        """ """
        return self._sample_lookup.get(idString, None)
        
    def get_variable_lookup(self, idString):
        """ """
        return self._variable_lookup.get(idString, None)

#    def load_parser_info(self, parser_file, import_column = None, export_column = None):
#        """ """
#        # Add metadata
#        self.add_metadata('Parser', parser_file)
#        # Read dataset parser.
#        tabledata = plankton_core.DatasetTable()
#        toolbox_utils.ExcelFiles().readToTableDataset(tabledata, file_name = parser_file)
#        # Create import info.
#        if import_column:
#            self.add_metadata('Import column', import_column)
#            importrows = []
#            for rowindex in xrange(0, tabledata.get_row_count()):
#                importcolumndata = tabledata.get_data_item_by_column_name(rowindex, import_column)
#                if importcolumndata:
#                    nodelevel = tabledata.get_data_item(rowindex, 0)
#                    key = tabledata.get_data_item(rowindex, 1)
#                    importrows.append({'Node': nodelevel, 'Key': key, 'Command': importcolumndata}) 
#            self.set_dataset_parser_rows(importrows)
#        # Create export info.
#        if export_column:
#            self.add_metadata('Export column', export_column)
#            columnsinfo = []
#            for rowindex in xrange(0, tabledata.get_row_count()):
#                exportcolumndata = tabledata.get_data_item_by_column_name(rowindex, export_column)
#                if exportcolumndata:
#                    nodelevel = tabledata.get_data_item(rowindex, 0)
#                    if nodelevel != 'INFO':
#                        key = tabledata.get_data_item(rowindex, 1)
#                        columnsinfo.append({'Header': exportcolumndata, 'Node': nodelevel, 'Key': key}) 
#            self.set_export_table_columns(columnsinfo)

    def set_dataset_parser_rows(self, dataset_parser_rows):
        """ """
        self._datasetparserrows = dataset_parser_rows

    def get_dataset_parser_rows(self):
        """ """
        return self._datasetparserrows

    def set_export_table_columns(self, columns_info_list):
        """ """
        self._exporttablecolumns = columns_info_list

    def get_export_table_columns(self):
        """ """
        return self._exporttablecolumns

#     def save_as_text_file(self, file_name):
#         """ """
#         targetdataset = DatasetTable()
#         self.convert_to_table_dataset(targetdataset)
#         toolbox_utils.TextFiles().writeTableDataset(targetdataset, file_name)
# 
#     def save_as_excel_file(self, file_name):
#         """ """
#         targetdataset = plankton_core.DatasetTable()
#         self.convert_to_table_dataset(targetdataset)
#         toolbox_utils.ExcelFiles().writeTableDataset(targetdataset, file_name)       
        
    def convert_to_table_dataset(self, target_dataset):
        """ Converts the tree dataset to a corresponding table based dataset.
        The parameter self._exporttablecolumns should be on the form [{"Header": "", "Node": "", "Key": ""}, ...]
        Example: [{"Header": "SDATE", "Node": "Visit", "Key": "Date"},
                  {"Header": "MNDEP", "Node": "Sample", "Key": "Min depth"}]
        """
        #
        if not target_dataset:
            raise UserWarning('Target dataset is missing.')
        if not isinstance(target_dataset, DatasetTable):
            raise UserWarning('Target dataset is not of valid type.')
        if not self._exporttablecolumns:
            raise UserWarning('Info for converting from tree to table dataset is missing.')
        # Header.
        header = []
        for item in self._exporttablecolumns:
            header.append(item.get('header', '---'))
        target_dataset.set_header(header)
        # Rows.
        for visitnode in self.get_children():
            for samplenode in visitnode.get_children():
                for variablenode in samplenode.get_children():
                    #  Create row based on column_info from self._exporttablecolumns.
                    row = []
                    for column_info in self._exporttablecolumns:
                        if column_info.get('node', '') == 'dataset':
                            row.append(self.get_data(column_info.get('key', '---')))
                        elif column_info.get('node', '') == 'visit':
                            row.append(visitnode.get_data(column_info.get('key', '---')))
                        elif column_info.get('node', '') == 'sample':
                            row.append(samplenode.get_data(column_info.get('key', '---')))
                        elif column_info.get('node', '') == 'variable':
                            row.append(variablenode.get_data(column_info.get('key', '---')))
                        else:
                            row.append('')
                    # To target.
                    target_dataset.append_row(row)


class VisitNode(DataNode):
    """ """
    def __init__(self):
        """ """
        super(VisitNode, self).__init__()

    def clear(self):
        """ """
        super(VisitNode, self).clear()

    def add_child(self, child):
        """ """
        if not isinstance(child, SampleNode):
            raise UserWarning('AddChild failed. Visit children must be of sample type')
        #
        self.get_parent()._sample_count += 1
        super(VisitNode, self).add_child(child)

    def remove_all_children(self):
        """ """
        self.get_parent()._sample_count -= len(self._children)
        self._children = []
        
    def set_id_string(self, idstring):
        """ """
        self._idstring = idstring
        # Register in dataset for fast lookup.
        try:
            self.get_parent()._visit_lookup[idstring] = self
        except:
            raise UserWarning('SetIdString failed. Check if parent is assigned.')
        
        
class SampleNode(DataNode):
    """ """
    def __init__(self):
        """ """
        super(SampleNode, self).__init__()

    def clear(self):
        """ """
        super(SampleNode, self).clear()
        
    def add_child(self, child):
        """ """
        if not isinstance(child, VariableNode):
            raise UserWarning('AddChild failed. Sample children must be of variable type')
        #
        self.get_parent().get_parent()._variable_count += 1
        super(SampleNode, self).add_child(child)

    def remove_all_children(self):
        """ """
        self.get_parent().get_parent()._variable_count -= len(self._children)
        self._children = []
        
    def set_id_string(self, idstring):
        """ """
        self._idstring = idstring
        # Register in dataset for fast lookup.
        try:
            self.get_parent().get_parent()._sample_lookup[idstring] = self
        except:
            raise UserWarning('SetIdString failed. Check if parent is assigned.')
        

class VariableNode(DataNode):
    """ """
    def __init__(self):
        """ """
        super(VariableNode, self).__init__()

    def clear(self):
        """ """
        super(VariableNode, self).clear()
        
    def clone(self):
        """ """
        newvariable = VariableNode()
        self.get_parent().add_child(newvariable) # Connect to the same parent.
        newvariable._children = [] # Not used for variables.
        newvariable._datadict = copy.deepcopy(self._datadict)
        newvariable._idstring = None # Not used for variables.
        return newvariable
        
    def add_child(self, child):
        """ """
        raise UserWarning('VariableNode.add_child() failed. Variables can\'t contain children.')

    def remove_all_children(self):
        """ """
        raise UserWarning('VariableNode.remove_all_children() failed. Variables can\'t contain children.')
        
    def set_id_string(self, idstring):
        """ """
        self._idstring = idstring
        # Register in dataset for fast lookup.
        try:
            self.get_parent().get_parent().get_parent()._variable_lookup[idstring] = self
        except:
            raise UserWarning('SetIdString failed. Check if parent is assigned.')

