#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os
import codecs
import toolbox_utils
import plankton_core

class ImportPlanktonCounter(plankton_core.DataImportPreparedBase):
    """ Class for parsing Plankton Counter files. """
    def __init__(self):
        """ """
        # Initialize parent.
        super(ImportPlanktonCounter, self).__init__()

        # Information needed for parsing. List of lists with: 
        #   Column 0: node level. 
        #   Column 1: internal key. 
        #   Column 2: view format. 
        #   Column 3: source file column name. Multiple alternatives should be separated by '<or>'. 
        #   Column 4: export column name. None = not used, empty string ('') = same as column 1 (internal key).
        self._parsing_info = [
#             ['dataset', 'sample_id', 'text', 'Sample Id', ''], 
#             ['dataset', 'project', 'text', 'Project', ''], 
#             ['visit', 'platform_code', 'text', 'Ship', ''], 
#             ['visit', 'station_number', 'text', 'StatNo', ''], 
            ['visit', 'station_name', 'text', 'station_name', ''], 
            ['visit', 'reported_latitude', 'text', 'latitude', ''], 
            ['visit', 'reported_longitude', 'text', 'longitude', ''], 
            ['visit', 'date', 'text', 'sample_date', ''], 
            ['visit', 'time', 'text', 'sample_time', ''], 
            ['visit', 'water_depth_m', 'float', 'water_depth_m', ''], 
            ['sample', 'sample_min_depth_m', 'float', 'sample_min_depth_m', ''], 
            ['sample', 'sample_max_depth_m', 'float', 'sample_max_depth_m', ''], 

            ['variable', 'reported_scientific_name', 'text', 'scientific_full_name', None], # Internal use only. 
            ['variable', 'scientific_name', 'text', 'scientific_name', ''], 
#             ['variable', 'species_flag', 'text', '', ''], 
            ['variable', 'size_class', 'text', 'size_class', ''], 
            ['variable', 'unit_type', 'text', 'unit_type', ''], 
#             ['variable', 'reported_trophic_type', 'text', 'trophic_type', None], # Internal use only. 
            ['variable', 'trophic_type', 'text', 'trophic_type', ''], # Will be calculated later.
            # Param/value/unit.
            ['variable', 'parameter', 'text', 'parameter', ''], 
            ['variable', 'value', 'float', 'value', ''], 
            ['variable', 'unit', 'text', 'unit', ''], 
            #
            ['variable', 'class', 'text', '', ''], # Will be calculated later.
#             ['variable', 'magnification', 'text', 'Magnification', 'magnification'], 
            ['variable', 'coefficient', 'text', 'coefficient', ''], 
#             ['variable', 'counted_units', 'text', 'Units', ''], 
#             ['sample', 'number_of_depths', 'text', 'No. Depths', ''], 
            ['sample', 'sampler_type', 'text', 'sampler_type_code', ''], 
#             ['sample', 'sample_size', 'text', 'Sample size', ''], 
#             ['sample', 'sampled_by', 'text', 'Sample by', ''], 
            ['sample', 'sample_comment', 'text', 'sample_comment', ''], 
#             ['variable', 'mixed_volume', 'text', 'Mixed volume', ''], 
#             ['variable', 'preservative', 'text', 'Preservative', ''], 
#             ['variable', 'sedimentation_volume', 'text', 'Sedim. volume', ''], 
#             ['variable', 'preservative', 'text', 'Preservative', ''], 
#             ['variable', 'preservative_amount', 'text', 'Amt. preservative', ''], 
#             ['variable', 'sedimentation_time_h', 'text', 'Sedim. time (hr)', ''], 
#             ['variable', 'chamber_diameter', 'text', 'Chamber diam.', ''], 
            ['variable', 'counted_on', 'text', 'analysis_date', ''], 
            ['variable', 'counted_by', 'text', 'analysed_by', ''], 
#             ['variable', 'description', 'text', 'Descr', ''], 
            # Copy parameters.
            ['copy_parameter', '# counted:ind', 'text', 'counted_units'], 
            ['copy_parameter', 'Abundance:ind/l', 'text', 'abundance_units/l'], 
            ['copy_parameter', 'Wet weight:mg/m3', 'text', 'volume_mg/m3'], 
            ['copy_parameter', 'Carbon content:µgC/m3', 'text', 'carbon_ugc/m3'], 
        ]
        #
        self.clear() # 

    def clear(self):
        """ """
        self._dataset_metadata = {}
        self._sample_info = {}
        self._sample_header = []
        self._sample_rows = []

    def read_file(self, dataset_name = None, sample_name = None):
        """ """
        if dataset_name == None:
            raise UserWarning('Dataset name is missing.')
        if sample_name == None:
            raise UserWarning('Sample name is missing.')
        #
        dir_path = plankton_core.PlanktonCounterManager().get_dataset_dir_path()
        dataset_path = os.path.join(dir_path, dataset_name)
        sample_path = os.path.join(dataset_path, sample_name)
        #
        if (not dataset_path) or (not os.path.exists(dataset_path)):
            raise UserWarning('Dataset files are missing.')
        if (not sample_path) or (not os.path.exists(sample_path)):
            raise UserWarning('Sample files are missing.')
        #
        self._dataset_metadata = {}
        self._sample_info = {}
        self._sample_header = []
        self._sample_rows = []
        
        # Dataset metadata as <key>:<value>.
        try:
            tablefilereader = toolbox_utils.TableFileReader(
                        file_path = dataset_path,
                        text_file_name = 'dataset_metadata.txt',                
                        )
            # Merge header and rows. Create dict.
            dataset_metadata = [tablefilereader.header()] + tablefilereader.rows()
            for row in dataset_metadata:
                if len(row) >= 2:
                    self._dataset_metadata[row[0].strip()] = row[1].strip()
        except:
            pass
               
        # Sample info as <key>:<value>. 
        tablefilereader = toolbox_utils.TableFileReader(
                    file_path = sample_path,
                    text_file_name = 'sample_info.txt',                 
                    )
        # Merge header and rows. Create dict from ':'-separated rows. 
        sample_info = [tablefilereader.header()] + tablefilereader.rows()
        for row in sample_info:
            if len(row) >= 2:
                self._sample_info[row[0].strip()] = row[1].strip()
                
        # Sample data on table format.
        tablefilereader = toolbox_utils.TableFileReader(
                    file_path = sample_path,
                    text_file_name = 'sample_data.txt',                 
                    )
        self._sample_header = tablefilereader.header()
        self._sample_rows = tablefilereader.rows()

    def create_tree_dataset(self, dataset_top_node):    
        """ """
        
        # TODO: Concatenate dataset metadata and sample info.
        
        
        # Add data to dataset node.
        for parsinginforow in self._parsing_info:
            if parsinginforow[0] == 'dataset':
                if parsinginforow[3] in self._sample_info:
                    dataset_top_node.add_data(parsinginforow[1], self._sample_info[parsinginforow[3]])        
        
        # Create visit node and add data. Note: Only one visit in each file. 
        visitnode = plankton_core.VisitNode()
        dataset_top_node.add_child(visitnode)
        #
        for parsinginforow in self._parsing_info:
            if parsinginforow[0] == 'visit':
                if parsinginforow[3] in self._sample_info:
                    visitnode.add_data(parsinginforow[1], self._sample_info[parsinginforow[3]])        
        
        # Create sample node and add data. Note: Only one sample in each file. 
        samplenode = plankton_core.SampleNode()
        visitnode.add_child(samplenode)
        #
        for parsinginforow in self._parsing_info:
            if parsinginforow[0] == 'sample':
                if parsinginforow[3] in self._sample_info:
                    samplenode.add_data(parsinginforow[1], self._sample_info[parsinginforow[3]])        
        
        # Create variable nodes.
        for row in self._sample_rows:
            variablenode = plankton_core.VariableNode()
            samplenode.add_child(variablenode)
            
            # Get info from sample_info.
            for parsinginforow in self._parsing_info:
                if parsinginforow[0] == 'variable':
                    value = self._sample_info.get(parsinginforow[3], '')
                    variablenode.add_data(parsinginforow[1], value)
                 
            # Get info from row.
            row_dict = dict(zip(self._sample_header, row))
            for parsinginforow in self._parsing_info:
                if parsinginforow[0] == 'variable':
                    value = row_dict.get(parsinginforow[3], '')
                    if len(value) > 0: # Don't overwrite from previous step.
                        variablenode.add_data(parsinginforow[1], value)
                                       
            # Copy to new variable nodes for parameters.
            for parsinginforow in self._parsing_info:
                if parsinginforow[0] == 'copy_parameter':
                    paramunit = parsinginforow[1].split(':')
                    parameter = paramunit[0]
                    unit = paramunit[1]
                    value = row_dict.get(parsinginforow[3], '')
                    if len(value.strip()) > 0:
                        self.copy_variable(variablenode, p = parameter, v = value, u = unit)

