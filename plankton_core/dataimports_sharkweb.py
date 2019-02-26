#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import codecs
import toolbox_utils
import plankton_core

class ImportSharkWeb(plankton_core.DataImportPreparedBase):
    """ Class for parsing sharkweb text files. """
    def __init__(self):
        """ """
        # Initialize parent.
        super(ImportSharkWeb, self).__init__()

        # Information needed for parsing. List of lists with: 
        #   Column 0: node level. 
        #   Column 1: internal key. 
        #   Column 2: view format. 
        #   Column 3: source file column name. Multiple alternatives should be separated by '<or>'. TODO: '<or>' not implemented.
        #   Column 4: export column name. None = not used, empty string ('') = same as column 1 (internal key).
        self._parsing_info = [
            ['visit', 'visit_year', 'integer', 'visit_year', ''], 
            ['visit', 'sample_date', 'date', 'sample_date', ''], 
            ['visit', 'visit_month', 'integer', '', ''], # Calculate. Code below.
            ['visit', 'station_name', 'text', 'station_name', ''], 
            ['visit', 'sample_latitude_dd', 'float', 'sample_latitude_dd', ''], 
            ['visit', 'sample_longitude_dd', 'float', 'sample_longitude_dd', ''], 
            ['visit', 'water_depth_m', 'float', 'water_depth_m', ''],
            # 
            ['sample', 'sample_id', 'text', 'sample_id', ''], 
            ['sample', 'sample_min_depth_m', 'float', 'sample_min_depth_m', ''], 
            ['sample', 'sample_max_depth_m', 'float', 'sample_max_depth_m', ''], 
            #
            ['variable', 'scientific_name', 'text', 'scientific_name', ''], 
            ['variable', 'species_flag_code', 'text', 'species_flag_code', ''], 
            ['variable', 'size_class', 'text', 'size_class', ''], 
            ['variable', 'trophic_type', 'text', 'trophic_type_code', ''], 
            #
            ['variable', 'parameter', 'text', 'parameter', ''], 
            ['variable', 'value', 'float', 'value', ''], 
            ['variable', 'unit', 'text', 'unit', ''], 
            #
            ['variable', 'plankton_group', 'text', '', ''], # Calculate. Code below.
            ['variable', 'taxon_kingdom', 'text', 'taxon_kingdom', ''], 
            ['variable', 'taxon_phylum', 'text', 'taxon_phylum', ''], 
            ['variable', 'taxon_class', 'text', 'taxon_class', ''], 
            ['variable', 'taxon_order', 'text', 'taxon_order', ''], 
            ['variable', 'taxon_family', 'text', 'taxon_family', ''], 
            ['variable', 'taxon_genus', 'text', 'taxon_genus', ''], 
            ['variable', 'taxon_hierarchy', 'text', 'taxon_hierarchy', ''], 
            #
            ['variable', 'sampling_laboratory', 'text', 'sampling_laboratory_name_sv', ''], 
            ['variable', 'analytical_laboratory', 'text', 'analytical_laboratory_name_sv', ''], 
            ['variable', 'analysis_date', 'text', 'analysis_date', ''], 
            ['variable', 'analysed_by', 'text', 'analysed_by', ''], 
        ]
        # Keys:
        self._visit_key_fields = ['sample_date', 'station_name']
        self._sample_key_fields = ['sample_date', 'station_name', 'sample_id', 'sample_min_depth_m', 'sample_max_depth_m', 'sample_id']
        #
        self.clear() # 

    def clear(self):
        """ """
        self._header = []
        self._rows = []

    def read_file(self, file_name = None):
        """ """
        if file_name == None:
            raise UserWarning('File name is missing.')
        input_file = None
        try:
###            txtencode = toolbox_settings.ToolboxSettings().getValue('General:Character encoding, txt-files', 'cp1252')
            txtencode = 'cp1252'
            input_file = codecs.open(file_name, mode = 'r', encoding = txtencode)
            
            # Read data header. Same header used for data and aggregated data.
            separator = '\t' # Use ',' as default item separator.
            first_row = input_file.readline()
            if ';' in first_row:
                separator = ';' # Use ';' as item separator.
            # 
            self._header = []
            for headeritem in first_row.split(separator):
                item = headeritem.strip()
                self._header.append(item)   
            # Read data rows. Continue until empty line occurs.
            self._rows = []
            for row in input_file.readlines():
                rowitems = []
                for item in row.split(separator):
                    rowitems.append(item.strip())
                self._rows.append(rowitems) 
        #                       
        except (IOError, OSError):
            raise
        finally:
            if input_file: input_file.close()

    def create_tree_dataset(self, dataset, update_trophic_type):
        """ """
        try:
            # Base class must know header for _asText(), etc.
#             self._set_header(self._header)
            # Iterate over rows in imported_table.            
            for row in self._rows:
                row_dict = dict(zip(self._header, row))
                # Get or create nodes. 
                currentvisit = None
                currentsample = None
                currentvariable = None
                # Check if visit exists. Create or reuse.
                keystring = ''
                delimiter = ''
                for key_field in self._visit_key_fields:
                    keystring += delimiter + row_dict.get(key_field, '') 
                    delimiter = '<+>'
                #
                currentvisit = dataset.get_visit_lookup(keystring)
                if not currentvisit:
                    currentvisit = plankton_core.VisitNode()
                    dataset.add_child(currentvisit)    
                    currentvisit.set_id_string(keystring)
                # Check if sample exists. Create or reuse.
                keystring = ''
                delimiter = ''
                for key_field in self._sample_key_fields:
                    keystring += delimiter + row_dict.get(key_field, '') 
                    delimiter = '<+>'
                #
                currentsample = dataset.get_sample_lookup(keystring)
                if not currentsample:
                    currentsample = plankton_core.SampleNode()
                    currentvisit.add_child(currentsample)    
                    currentsample.set_id_string(keystring)    
                # Add all variables in row.
                currentvariable = plankton_core.VariableNode()
                currentsample.add_child(currentvariable)    
                # === Parse row and add fields on nodes. ===                    
                for parsinginforow in self._parsing_info:
                    #
                    value = row_dict.get(parsinginforow[3], '')
                    # Fix float.
                    if parsinginforow[2] == 'float': 
                        value = value.replace(',', '.')
                    # Calculate some values.
                    if parsinginforow[1] == 'visit_month':
                        try:
                            value = row_dict.get('sample_date', '')
                            value = value[5:7]
                        except: 
                            pass        
                    if parsinginforow[1] == 'plankton_group':
                        try:
                            value = row_dict.get('scientific_name', '')
                            value = plankton_core.Species().get_plankton_group_from_taxon_name(value)
                        except: 
                            pass 
                    if parsinginforow[1] == 'analysed_by':
                        try:
                            if not value:
                                value = row_dict.get('taxonomist', '')
                        except: 
                            pass 
                    if parsinginforow[1] == 'trophic_type':
                    
                    
                        # Update trophic_type.
                        if parsinginforow[1] == 'trophic_type':
                            if update_trophic_type:
                                scientific_name = row_dict.get('scientific_name', '')
                                size_class = row_dict.get('size_class', '')
                                trophic_type = plankton_core.Species().get_bvol_value(scientific_name, size_class, 'trophic_type')
                                if trophic_type:
                                    value = trophic_type # Use existing if not in local list.
                            # Replace empty with NS=Not specified.
                            if not value:
                                value = 'NS'
                    
                    # Add at right level.
                    if parsinginforow[0] == 'visit':
                        currentvisit.add_data(parsinginforow[1], value)        
                    #
                    if parsinginforow[0] == 'sample':
                        currentsample.add_data(parsinginforow[1], value)        
                    #
                    if parsinginforow[0] == 'variable':
                        currentvariable.add_data(parsinginforow[1], value) 

        #
        except Exception as e:
            toolbox_utils.Logging().warning('Failed to parse dataset: %s' % (e.args[0]))

