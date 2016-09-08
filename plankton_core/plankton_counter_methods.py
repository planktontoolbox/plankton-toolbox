#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os
import toolbox_utils

@toolbox_utils.singleton
class PlanktonCounterMethods():
    """ """
    def __init__(self,
                 config_dir_path = 'toolbox_data/plankton_counter/config',
                 methods_methods_dir_path = 'toolbox_data/plankton_counter/config/counting_methods',
                 methods_species_lists_dir_path = 'toolbox_data/plankton_counter/config/counting_species_lists',
                 ):
        """ """
        self._config_dir_path = config_dir_path
        self._methods_dir_path = methods_methods_dir_path
        self._methods_species_lists_dir_path = methods_species_lists_dir_path
        #
        self._check_dir_path(self._methods_dir_path) 
        self._check_dir_path(self._methods_species_lists_dir_path) 
        self._check_dir_path(self._methods_dir_path) 

    def _check_dir_path(self, dir_path):
        """ Check if exists. Create if not. """
        if (dir_path) and (not os.path.exists(dir_path)):
            try:
                os.makedirs(dir_path)
#                 print('Directories created for this path: ' + dir_path)
            except Exception as e:
                print('Can\'t create directories in path. Path: ' + dir_path + '. Exception: ' + e)
    
    def get_methods_dir_path(self):
        """ """
        return self._methods_dir_path

    # === Counting methods ===

    def get_analysis_method_list(self):
        """ Returns a list with counting methods. """
        methods = []
        for methodfile in os.listdir(self._methods_dir_path):
            if os.path.isfile(os.path.join(self._methods_dir_path, methodfile)):
                if methodfile.endswith('.txt'):
                    methods.append(methodfile.replace('.txt', ''))
        return sorted(methods)

    def get_counting_method_table(self, path, filename):
        """ """
        tablefilereader = toolbox_utils.TableFileReader(
                    file_path = path,
                    text_file_name = filename,                 
                    )
        return tablefilereader.header(), tablefilereader.rows()
    
    # === Counting species lists ===
    
    def get_counting_species_lists(self):
        """ Returns a list with counting lists of species. """
        specieslists = []
        speciesdirpath = os.path.join(self._config_dir_path, 'counting_species_lists')
        if (speciesdirpath) and (os.path.exists(speciesdirpath)):
            for listfile in os.listdir(speciesdirpath):
                if os.path.isfile(os.path.join(speciesdirpath, listfile)):
                    if listfile.endswith('.txt'):
                        specieslists.append(listfile.replace('.txt', ''))
            return sorted(specieslists)
        else:
            raise UserWarning('The directory ' + speciesdirpath + ' does not exists.')

    def get_counting_species_table(self, counting_species_file_name):
        """ """
        filepath = os.path.join(self._methods_species_lists_dir_path, counting_species_file_name + '.txt')
        if os.path.isfile(filepath):
            tablefilereader = toolbox_utils.TableFileReader(
                        file_path = self._methods_species_lists_dir_path,
                        text_file_name = counting_species_file_name + '.txt',                 
                        )
            return tablefilereader.header(), tablefilereader.rows()
        else:
            return [], []

    def create_counting_species_list(self, specieslistname, species_list_rows):
        """ """
        tablefilewriter_method = toolbox_utils.TableFileWriter(
            file_path = self._methods_species_lists_dir_path,
            text_file_name = specieslistname + '.txt',                 
            )
        #
        header = ['scientific_name']
        tablefilewriter_method.write_file(header, species_list_rows)
    
    def delete_counting_species_list(self, counting_species_list):
        """ """
        filepath = os.path.join(self._methods_species_lists_dir_path, counting_species_list + '.txt')
        if os.path.isfile(filepath):
            os.remove(filepath)
        
    def delete_counting_method(self, counting_method_name):
        """ """
        filepath = os.path.join(self._methods_dir_path, counting_method_name + '.txt')
        if os.path.isfile(filepath):
            os.remove(filepath)
        
#     def get_preferred_sizeclasses_columns(self, counting_species_file_name):
#         """ """
#         preferedcolumns = []
#         try:
#             header, rows = self.get_counting_species_table(counting_species_file_name)
#             for headeritem in header:
#                 if headeritem.startswith('Sizeclasses'):
#                     preferedcolumns.append(headeritem)
#         except:
#             pass
#         #
#         return preferedcolumns
# 
#     def get_preferred_sizeclasses_dict(self, counting_species_file_name, column_name):
#         """ """
#         preferredsizes_dict = {} # Key: Scientific name, value =  String with sizeclasses.
#         #
#         try:
#             header, rows = self.get_counting_species_table(counting_species_file_name)
#             column_index = header.index(column_name)
#             for row in rows:
#                 if len(row) > column_index:
#                     sizes = row[column_index].strip()
#                     if len(sizes) > 0:
#                         preferredsizes_dict[row[0]] = sizes
#         except:
#             pass # Ok to return empty dict if it fails.
#         #
#         return preferredsizes_dict


class PlanktonCounterMethod():
    """ """
    def __init__(self, table_header, table_rows):
        """ """
        self._table_header = table_header
        self._table_rows = table_rows
        #
        self._method_step_header = [
               'counting_method_step',
               'method_step_description',
               'sampled_volume_ml',
               'preservative',
               'preservative_volume_ml',
               'counted_volume_ml',
               'chamber_filter_diameter_mm',
               'magnification',
               'microscope',
               'count_area_type',
               'diameter_of_view_mm',
               'transect_rectangle_length_mm',
               'transect_rectangle_width_mm',
               'coefficient_one_unit',
               'counting_species_list',
               'view_sizeclass_info',
               ]
        #
        self._method_dicts = []
        #
        for row in table_rows:   
            row_dict = dict(zip(table_header, row))
            self._method_dicts.append(row_dict)
        
    def add_method_step(self, new_method_step_dict):
        """ """
        if new_method_step_dict.get('counting_method_step', ''):
            # Remove old with the sam name.
            for index, method_dict in enumerate(self._method_dicts):
                if method_dict['counting_method_step'] == new_method_step_dict['counting_method_step']:
                    del self._method_dicts[index]
            #
            self._method_dicts.append(new_method_step_dict)

    def delete_method_step(self, method_step_name):
        """ """
        for index, method_dict in enumerate(self._method_dicts):
            if method_dict['counting_method_step'] == method_step_name:
                del self._method_dicts[index]
                return

    def get_counting_method_steps_list(self):
        """ """
        countingmethodsteps_set = set() 
        try:
            for method_dict in self._method_dicts:
                if 'counting_method_step' in method_dict:
                    if method_dict['counting_method_step']:
                        countingmethodsteps_set.add(method_dict['counting_method_step'])
        except:
            pass
        #
        return sorted(list(countingmethodsteps_set))
    
    def get_counting_method_step_fields(self, method_step_name): 
        """ """
        field_dict = {} 
        try:
            for method_dict in self._method_dicts:
                if method_dict['counting_method_step'] == method_step_name:
                    return method_dict
        except:
            pass
        #
        return field_dict

    def update_counting_method_step_fields(self, method_step_name, field_dict): 
        """ """
        for method_dict in self._method_dicts:
            if method_dict['counting_method_step'] == method_step_name:
                for key in field_dict.keys():
                    if key in self._method_step_header:
                        method_dict[key] = field_dict[key]
          
    def save_method_to_file(self, path, filename):
        """ """
        tablefilewriter_method = toolbox_utils.TableFileWriter(
            file_path = path,
            text_file_name = filename,                 
            )
        #
        header = self._method_step_header
        rows = []
        #
        for method_dict in self._method_dicts:
            row = []
            for headeritem in header:
                row.append(method_dict.get(headeritem, ''))
            #
#             rows.append('\t'.join(row))
            rows.append(row)
        #
        tablefilewriter_method.write_file(header, rows)
