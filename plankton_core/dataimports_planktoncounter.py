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
            ['visit', 'visit_year', 'text', 'visit_year', ''], 
            ['visit', 'sample_date', 'text', 'sample_date', ''], 
            ['sample', 'sample_time', 'text', 'sample_time', ''], 
            ['visit', 'country_code', 'text', 'country_code', ''], 
            ['visit', 'platform_code', 'text', 'platform_code', ''], 
            ['visit', 'sampling_series', 'text', 'sampling_series', ''], 
            
            ['visit', 'project_code', 'text', 'project_code', ''], 
            ['visit', 'station_name', 'text', 'station_name', ''], 
            ['visit', 'sample_latitude_dd', 'text', 'sample_latitude_dd', ''], 
            ['visit', 'sample_longitude_dd', 'text', 'sample_longitude_dd', ''], 
            ['visit', 'sample_latitude_dm', 'text', 'sample_latitude_dm', ''], 
            ['visit', 'sample_longitude_dm', 'text', 'sample_longitude_dm', ''], 
            #
            ['sample', 'sample_name', 'text', 'sample_name', ''], 
            ['sample', 'sample_id', 'text', 'sample_id', ''], 
            ['sample', 'sampler_type_code', 'text', 'sampler_type_code', ''], 
            ['sample', 'sample_min_depth_m', 'float', 'sample_min_depth_m', ''], 
            ['sample', 'sample_max_depth_m', 'float', 'sample_max_depth_m', ''], 
            ['visit', 'water_depth_m', 'float', 'water_depth_m', ''], 
            ['sample', 'sampled_volume_l', 'text', 'sampled_volume_l', ''], 
            
            ['sample', 'net_type_code', 'text', 'net_type_code', ''], 
            ['sample', 'sampler_area_m2', 'text', 'sampler_area_m2', ''], 
            ['sample', 'net_mesh_size_um', 'text', 'net_mesh_size_um', ''], 
            ['sample', 'wire_angle_deg', 'text', 'wire_angle_deg', ''], 
            ['sample', 'net_tow_length_m', 'text', 'net_tow_length_m', ''], 
            #
            ['variable', 'scientific_full_name', 'text', 'scientific_full_name', None], # Internal use only. 
            ['variable', 'scientific_name', 'text', 'scientific_name', ''], 
            ['variable', 'species_flag_code', 'text', 'species_flag_code', ''], # TODO: Add cf.
            ['variable', 'size_class', 'text', 'size_class', ''], 
            ['variable', 'unit_type', 'text', 'unit_type', ''], 
#             ['variable', 'reported_trophic_type', 'text', 'trophic_type', None], # Internal use only. 
            ['variable', 'trophic_type', 'text', 'trophic_type', ''], # Will be calculated later.
            # Param/value/unit.
            ['variable', 'parameter', 'text', 'parameter', ''], 
            ['variable', 'value', 'float', 'value', ''], 
            ['variable', 'unit', 'text', 'unit', ''], 
            #
            ['variable', 'taxon_class', 'text', 'taxon_class', ''], # Will be calculated later.
            ['sample', 'sample_comment', 'text', 'sample_comment', ''], 
            ['variable', 'variable_comment', 'text', 'variable_comment', ''], 
            # From counting_method.txt in sample.
            ['variable', 'counting_method_step', 'text', 'counting_method_step', ''], 
#             ['variable', 'method_step_description', 'text', 'method_step_description', ''], 
            ['variable', 'sampled_volume_ml', 'text', 'sampled_volume_ml', ''], 
            ['variable', 'preservative', 'text', 'preservative', ''], 
            ['variable', 'preservative_volume_ml', 'text', 'preservative_volume_ml', ''], 
            ['variable', 'counted_volume_ml', 'text', 'counted_volume_ml', ''], 
            ['variable', 'chamber_filter_diameter_mm', 'text', 'chamber_filter_diameter_mm', ''], 
            ['variable', 'magnification', 'text', 'magnification', ''], 
            ['variable', 'microscope', 'text', 'microscope', ''], 
            ['variable', 'count_area_type', 'text', 'count_area_type', ''], 
            ['variable', 'diameter_of_view_mm', 'text', 'diameter_of_view_mm', ''], 
            ['variable', 'transect_rectangle_length_mm', 'text', 'transect_rectangle_length_mm', ''], 
            ['variable', 'transect_rectangle_width_mm', 'text', 'transect_rectangle_width_mm', ''], 
            ['variable', 'coefficient_one_unit', 'text', 'coefficient_one_unit', ''], 
            #
            ['variable', 'coefficient', 'text', 'coefficient', ''], 
            ['sample', 'analysis_laboratory', 'text', 'analysis_laboratory', ''], 
            ['variable', 'analysis_date', 'text', 'analysis_date', ''], 
            ['variable', 'taxonomist', 'text', 'taxonomist', ''], 
            # Copy parameters.
            ['copy_parameter', '# counted:ind', 'text', 'counted_units'], 
            ['copy_parameter', 'Abundance:ind/l', 'text', 'abundance_units_l'], 
            ['copy_parameter', 'Wet weight:mg/m3', 'text', 'volume_mg_m3'], 
            ['copy_parameter', 'Carbon content:µgC/m3', 'text', 'carbon_ugc_m3'], 
        ]
        #
        self.clear() # 

    def clear(self):
        """ """
        self._dataset_metadata = {}
        self._sample_info = {}
        self._sample_header = []
        self._sample_rows = []
        self._sample_method_header = []
        self._sample_method_rows = []


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
        self._sample_method_dict = {}
        
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

        # Sample method on table format.
        tablefilereader = toolbox_utils.TableFileReader(
                    file_path = sample_path,
                    text_file_name = 'counting_method.txt',                 
                    )
        self._sample_method_header = tablefilereader.header()
        self._sample_method_rows = tablefilereader.rows()
        # Create dictionary with method step as key.
        self._sample_method_dict = {}
        for row in self._sample_method_rows:
            method_dict = dict(zip(self._sample_method_header, row))
            if 'counting_method_step' in method_dict:
                self._sample_method_dict[method_dict['counting_method_step']] = method_dict

    def create_tree_dataset(self, dataset_top_node):    
        """ """
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
        # Add visit_year and visit_month.
        sample_date = visitnode.get_data('sample_date', '')
        try:
            visitnode.add_data('visit_year', sample_date[0:4])
        except: pass      
        try:
            visitnode.add_data('visit_month', sample_date[5:7])        
        except: pass 
             
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
                 
            # Merge data header and row.     
            row_dict = dict(zip(self._sample_header, row))

            # Get info from sample_method and add to row_dict.
            if 'method_step' in row_dict:
                method_dict = self._sample_method_dict[row_dict['method_step']]
                row_dict.update(method_dict) 

            # Get info from row.
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

