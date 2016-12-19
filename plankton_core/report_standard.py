#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

class CreateReportStandard(object):
    """ """
    def __init__(self):
        """ """
        # Initialize parent.
        super(CreateReportStandard, self).__init__()
        #
        self._header_items = [
            'visit_year', 
            'sample_date', 
            'visit_month', 
            'station_name', 
            'sample_latitude_dd', 
            'sample_longitude_dd', 
            'water_depth_m', 
            'sample_id', 
            'sample_min_depth_m', 
            'sample_max_depth_m', 
            'scientific_name', 
            'species_flag_code', 
            'size_class', #'text', 
            'trophic_type', 
            'parameter', 
            'value', 
            'unit', 
            'plankton_group', 
            'taxon_kingdom', 
            'taxon_phylum', 
            'taxon_class', 
            'taxon_order', 
            'taxon_family', 
            'taxon_genus', 
            'taxon_hierarchy', 
            'sampling_laboratory', 
            'analytical_laboratory', 
            'analysed_by', 
            ]
    
    def create_report(self, datasets, result_table,
                     aggregate_rows = False):
        """
        Note:
        - Datasets must be of the format used in the modules dataset_tree and datasets_tree. 
        - The result_table object must contain self._header = [] and self._rows = [].
        """
        # Check indata.
        if datasets == None:
            raise UserWarning('Datasets are missing.')
        if result_table == None:
            raise UserWarning('Result table is missing.')
        # Set header.
        result_table.set_header(self._header_items)
        
        # Iterate through datasets.
        for datasetnode in datasets:
            #
            for visitnode in datasetnode.get_children():
                #
                for samplenode in visitnode.get_children():
                    # 
                    for variablenode in samplenode.get_children():
                        datadict = {}
                        datadict.update(datasetnode.get_data_dict())
                        datadict.update(visitnode.get_data_dict())
                        datadict.update(samplenode.get_data_dict())
                        datadict.update(variablenode.get_data_dict())
                        #
                        report_row = []
                        #
                        for item in self._header_items:
                            report_row.append(datadict.get(item, '')) 
                        #
                        result_table.append_row(report_row)
        #
        result_table.get_rows().sort(report_table_sort)


# Sort function for the result table.
def report_table_sort(s1, s2):
    """ """
    # Sort order: Station, date min depth, max depth and scientific name.
    columnsortorder = [0, 1, 3,] 
    #
    for index in columnsortorder:
        s1item = s1[index]
        s2item = s2[index]
        # Empty strings should be at the end.
        if (s1item != '') and (s2item == ''): return -1
        if (s1item == '') and (s2item != ''): return 1
        if s1item < s2item: return -1
        if s1item > s2item: return 1
    #
    return 0 # All are equal.

