#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import string
import plankton_core

class DataImportPreparedBase(object):
    """ """
    def __init__(self):
        """ """
        # Initialize parent.
        super(DataImportPreparedBase, self).__init__()

        # Information needed for parsing. List of lists with: 
        #   Column 0: node level. 
        #   Column 1: internal key. 
        #   Column 2: view format. 
        #   Column 3: source file column name. Multiple alternatives should be separated by '<or>'. 
        #   Column 4: export column name. None = not used, empty string ('') = same as column 1 (internal key).
        self._parsing_info = None # Should be defined in subclasses.
    
    def create_export_table_info(self):
        """ Used in tree datasets. """
        export_table_info = []
        for parsinginforow in self._parsing_info:
            nodelevel = parsinginforow[0]
            key = parsinginforow[1]
            viewformat = parsinginforow[2]
            exportheader = parsinginforow[4] if len(parsinginforow) > 4 else None
            if exportheader == '':
                exportheader = key # Empty string means copy internal key.
            if nodelevel in ['dataset', 'visit', 'sample', 'variable']:
                if exportheader:
                    export_table_info.append({'header': exportheader, 'node': nodelevel, 'key': key, 'view_format': viewformat}) 
        #
        return export_table_info
    
    def copy_variable(self, current_node, **kwargs):
        """ """
        if isinstance(current_node, plankton_core.VariableNode):
            if len(current_node.get_data('parameter')) > 0:
                # Clone if already contains parameter.
                variable = current_node.clone()
            else:
                variable = current_node
            #
            variable.add_data('parameter', kwargs['p'])    
            variable.add_data('value', kwargs['v'])    
            #variable.add_data('value_float', kwargs['v'])    
            variable.add_data('unit', kwargs['u'])    

