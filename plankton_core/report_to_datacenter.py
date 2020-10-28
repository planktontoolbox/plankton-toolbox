#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import plankton_core

class CreateReportToDataCenter(object):
    """ """
    def __init__(self):
        """ """
        super().__init__()
        
        # Header.
        self._header_counted_items = [
            'project_code', 
            'project_name', 
            'orderer', 
            'sample_date', 
            'sample_time', 
            'sample_id', 
            'platform_code', 
            'station_name', 
            'station_code', 
            'sample_latitude_dd', 
            'sample_longitude_dd', 
            'sample_min_depth_m', 
            'sample_max_depth_m', 
            'taxon_class', 
            'scientific_full_name', 
            'scientific_name', 
            'rank', 
            'species_flag_code', 
            'cf',
            'size_class', 
            'bvol_size_range', 
            'param_abundance', 
            'param_biovolume', 
            'param_carbonconc', 
            'param_abundance_class', 
            'param_counted', 
            'coefficient', 
            'counted_volume_ml', 
            'magnification', 
            'trophic_type', 
            'potential_harmful', 
            'method_documentation', # 'METDC',
            'method_reference_code', # 'REFSK',
            'analysed_by', 
            'analysis_date', 
            'sampling_laboratory', 
            'analytical_laboratory', 
        ]
        
        self._translate_header = {
            'project_code': 'Project_code', 
            'project_name': 'Project_name', 
            'orderer': 'Orderer', 
            'sample_date': 'Sample_date', 
            'sample_time': 'Sample_time', 
            'sample_id': 'Sample_id', 
            'platform_code': 'Platform', 
            'station_name': 'Station_name', 
            'station_code': 'Station_code', 
            'sample_latitude_dd': 'Latitude',
            'sample_longitude_dd': 'Longitude',
            'sample_min_depth_m': 'Min_depth', 
            'sample_max_depth_m': 'Max_depth', 
            'taxon_class': 'Taxon_class', 
            'scientific_full_name': 'Taxon_name_extended', 
            'scientific_name': 'Taxon_name', 
            'rank': 'Rank', 
            'species_flag_code': 'Species_flag', 
            'cf': 'Cf', 
            'size_class': 'Size_class', 
            'bvol_size_range': 'Size_range', 
            'param_abundance': 'Abundance_ind_l', 
            'param_biovolume': 'Biovolume_mm3_l', 
            'param_carbonconc': 'Calculated_carbon_ugC_l', 
            'param_abundance_class': 'Presence', 
            'param_counted': 'Counted_nr', 
            'coefficient': 'Coefficient', 
            'counted_volume_ml': 'Counted_volume', 
            'magnification': 'Magnification', 
            'trophic_type': 'Trophic_type', 
            'potential_harmful': 'Potential_harmful', 
            'method_documentation': 'Method_documentation', # 'METDC',
            'method_reference_code': 'Method_reference_code', # 'REFSK',
            'analysed_by': 'Analysed_by', 
            'analysis_date': 'Analysis_date', 
            'sampling_laboratory': 'Sampling_laboratory', 
            'analytical_laboratory': 'Analytical_laboratory', 
        }
        # Used as row key and for sort order.
        self._row_key_items = [
            'station_name', 
            'sample_date', 
            'sample_time', 
            'sample_id', 
            'sample_min_depth_m', 
            'sample_max_depth_m', 
            'scientific_name', 
            'species_flag_code', 
            'cf', 
            'size_class', 
           ]
            
    def create_report(self, datasets, result_table,
                     aggregate_rows = False): # Aggregated rows not used.
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
        header_items = self._header_counted_items
        # Transleate headers.
        translated_header = []
        for item in header_items:
            translated_header.append(self._translate_header.get(item, item))
        #   
        result_table.set_header(translated_header)

        # Iterate through datasets.
        report_rows_dict = {}
        for datasetnode in datasets:
            #
            for visitnode in datasetnode.get_children():
                #
                for samplenode in visitnode.get_children():
                    # 
                    for variablenode in samplenode.get_children():
                        row_dict = {}
                        row_dict.update(datasetnode.get_data_dict())
                        row_dict.update(visitnode.get_data_dict())
                        row_dict.update(samplenode.get_data_dict())
                        row_dict.update(variablenode.get_data_dict())
                        #
                        parameter = row_dict.get('parameter', '')
                        if parameter in ['# counted', 'Abundance', 'Biovolume concentration', 'Carbon concentration', 'Abundance class']:
                            # Create key:
                            row_key = ''
                            for item in self._row_key_items:
                                if row_key: row_key += '<+>'
                                row_key += str(row_dict.get(item, ''))
                            # Add to dict if first time.
                            if row_key not in report_rows_dict:
                                report_rows_dict[row_key] = row_dict
                            # Parameters as columns.
                            if parameter == '# counted':
                                report_rows_dict[row_key]['param_counted'] = row_dict.get('value', '')
                            if parameter == 'Abundance':
                                report_rows_dict[row_key]['param_abundance'] = row_dict.get('value', '')
                            if parameter == 'Biovolume concentration':
                                report_rows_dict[row_key]['param_biovolume'] = row_dict.get('value', '')
                            if parameter == 'Carbon concentration':
                                report_rows_dict[row_key]['param_carbonconc'] = row_dict.get('value', '')
                            if parameter == 'Abundance class':
                                report_rows_dict[row_key]['param_abundance_class'] = row_dict.get('value', '')
                            # Complement columns.
#                             self._add_more_content(row_dict)
        #
        sorted_key_list = sorted(report_rows_dict.keys())
        for key in sorted_key_list:
            # Copy items.
            report_row = []
            row_dict = report_rows_dict[key]
            #
            self.cleanup_fields(row_dict)
            #
            self.add_new_fields(row_dict)
            #
            for item in self._header_counted_items:
                report_row.append(row_dict.get(item, ''))
            # Add all rows to result.
            result_table.append_row(report_row)
    
    def add_new_fields(self, row_dict):
        """ """
        scientificname = row_dict.get('scientific_name', '')
        sizeclass = row_dict.get('size_class', '')
        if scientificname:
            taxon_class = plankton_core.Species().get_taxon_value(scientificname, u'taxon_class')
            taxon_rank = plankton_core.Species().get_taxon_value(scientificname, u'rank')
            counted_unit = plankton_core.Species().get_bvol_value(scientificname, sizeclass, u'bvol_unit')
            bvol_size_range = plankton_core.Species().get_bvol_value(scientificname, sizeclass, u'bvol_size_range')
            harmful = plankton_core.Species().get_taxon_value(scientificname, u'harmful')
            if len(str(harmful).strip()) > 0:
                harmful = 'Y'
            else:
                harmful = ''
            row_dict['taxon_class'] = taxon_class
            row_dict['rank'] = taxon_rank
            row_dict['potential_harmful'] = harmful
            row_dict['counted_unit'] = counted_unit
            row_dict['bvol_size_range'] = bvol_size_range
    
    def cleanup_fields(self, row_dict):
        """ """
        cf = str(row_dict.get('cf', '')).strip()
        # if 'CF' in cf.upper():
        #     row_dict['cf'] = 'Cf.'
        
#         # Concatenate CF into SFLAG.
#         sflag = str(row_dict.get('species_flag_code', '')).strip()
#         cf = str(row_dict.get('cf', '')).strip()
#         if 'CF' in cf.upper():
#             if len(sflag) > 0:
#                 row_dict['species_flag_code'] = sflag + ' CF'
#             else:
#                 row_dict['species_flag_code'] = 'CF'

        # Biovol and carbon: '' if 0.00.
        biovol = str(row_dict.get('param_biovolume', '')).strip()
        try:
            biovol = float(biovol)
            if biovol == 0.0:
                row_dict['param_biovolume'] = ''
        except:
            pass

        # Remove descriptions for codes.
        smtyp = str(row_dict.get('sampler_type_code', ''))
        if '(' in smtyp:
            row_dict['sampler_type_code'] = smtyp.split('(')[0].strip()
        
        metfp = str(row_dict.get('preservative', ''))
        if '(' in metfp:
            row_dict['preservative'] = metfp.split('(')[0].strip()
