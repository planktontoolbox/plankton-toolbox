#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import os
import math
import toolbox_utils
import plankton_core

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
        # Use all prealoaded species.
        if counting_species_file_name == '<all species>':
            species_list_of_list = []
            for key in sorted(plankton_core.Species().get_taxa_lookup_dict().keys()):
                species_list_of_list.append([key])
            return ['scientific_name'], species_list_of_list
                
        # Read stored species file.
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
#                'method_step_description',
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
            # Update all rows with filds connected to the whole method.
            for key in ['sampled_volume_ml', 
                        'preservative',
                        'preservative_volume_ml',
                        'counted_volume_ml',
                        'chamber_filter_diameter_mm',
                        ]:
                if key in self._method_step_header:
                    method_dict[key] = field_dict[key]
            # Recalculate all coefficients.
            self.calculate_coefficient_one_unit(method_dict)
                    
    def calculate_coefficient_one_unit(self, fields_dict):
        """ """
        # Clear result.
        fields_dict['coefficient_one_unit'] = '0'
        #
        try:
            # From analysis method.
            sampledvolume_ml = fields_dict.get('sampled_volume_ml', 0.0).replace(',', '.')
            preservative_volume_ml = fields_dict.get('preservative_volume_ml', 0.0).replace(',', '.')
            counted_volume_ml = fields_dict.get('counted_volume_ml', 0.0).replace(',', '.')
            chamber_filter_diameter_mm = fields_dict.get('chamber_filter_diameter_mm', 0.0).replace(',', '.')
            # From analysis method step.
            countareatype = fields_dict.get('count_area_type', 0.0).replace(',', '.')
            diameterofview_mm = fields_dict.get('diameter_of_view_mm', 0.0).replace(',', '.')
            transectrectanglelength_mm = fields_dict.get('transect_rectangle_length_mm', 0.0).replace(',', '.')
            transectrectanglewidth_mm = fields_dict.get('transect_rectangle_width_mm', 0.0).replace(',', '.')
            #
            if not chamber_filter_diameter_mm:
                return
            if not sampledvolume_ml:
                return
            if not counted_volume_ml:
                return
            #
            chamber_filter_area = ((float(chamber_filter_diameter_mm) / 2) ** 2) * math.pi # r2*pi.
            sampledvolume = float(sampledvolume_ml)
            counted_volume = float(counted_volume_ml)
            #
            try: preservative_volume = float(preservative_volume_ml)
            except: preservative_volume = 0.0
            singlearea = 1.0
            #
            if countareatype == 'Chamber/filter':
                singlearea = chamber_filter_area
            if countareatype == '1/2 Chamber/filter':
                singlearea = chamber_filter_area * 0.5
            if countareatype == 'Field of views':
                singlearea = ((float(diameterofview_mm) / 2) ** 2) * math.pi # r2*pi.
            if countareatype == 'Transects':
                singlearea = float(transectrectanglelength_mm) * float(transectrectanglewidth_mm) # l * w.
            if countareatype == 'Rectangles':
                singlearea = float(transectrectanglelength_mm) * float(transectrectanglewidth_mm) # l * w.
            
            # Calculate coeff.
            onelitre_ml = 1000.0
            coeffoneunit = chamber_filter_area * sampledvolume * onelitre_ml / (singlearea * counted_volume * (sampledvolume + preservative_volume))
            coeffoneunit = int(coeffoneunit + 0.5) # Round.
            fields_dict['coefficient_one_unit'] = unicode(coeffoneunit)
        except:
            pass


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
