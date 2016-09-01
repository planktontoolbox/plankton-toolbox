#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import toolbox_utils
import plankton_core

@toolbox_utils.singleton
class DataImportManager(object):
    """ """
    def __init__(self):
        """ """
#         super(DataImportManager, self).__init__()

    def import_dataset_file(self, filename, 
                            file_format = 'txt', 
                            import_format = None):
        """ """
        datasetnode = None
        #
        if import_format == 'PhytoWin':
            datasetnode = self._import_phytowin_file(filename)
        #
        return datasetnode
        
        
        
        #                     phytowin.clear()
#                     phytowin.read_file(filename)
# #                     # Used for report 'combined datasets'.
# #                     phytowin.add_to_table_dataset(self._tabledataset)
#                     # Add as tree dataset for calculated reports.
#                     datasetnode = plankton_core.DatasetNode()
#                     phytowin.add_to_dataset_node(datasetnode)
#                     # Add to dataset list. (Note:ToolboxDatasets is a wrapper containing the 'datasetListChanged'-signal).
#                     toolbox_datasets.ToolboxDatasets().add_dataset(datasetnode)

    def _import_phytowin_file(self, filename):
        """ """
        
        phytowin = plankton_core.ImportPhytowin()
        self._tabledataset = plankton_core.DatasetTable()

        phytowin.clear()
        phytowin.read_file(filename)
#                     # Used for report 'combined datasets'.
#                     phytowin.add_to_table_dataset(self._tabledataset)
        # Add as tree dataset for calculated reports.
        datasetnode = plankton_core.DatasetNode()
        phytowin.add_to_dataset_node(datasetnode)
        
        plankton_core.Datasets().add_dataset(datasetnode)
        
        return datasetnode
        
        
#         # Add to dataset list. (Note:ToolboxDatasets is a wrapper containing the 'datasetListChanged'-signal).
#         toolbox_datasets.ToolboxDatasets().add_dataset(datasetnode)
