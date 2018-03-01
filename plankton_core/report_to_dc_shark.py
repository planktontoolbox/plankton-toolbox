#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import plankton_core

class CreateReportToDataCenterShark(object):
    """ """
    def __init__(self):
        """ """
        super(CreateReportToDataCenterShark, self).__init__()

        # Header for combined "quantitative" and "qualitative" counting.
        self._header_counted_items = [
            'visit_year', # 'MYEAR',
            'project_code', # 'PROJ',
            'orderer', # 'ORDERER',
            'sample_date', # 'SDATE',
            'sample_latitude_dd', # 'LATIT',
            'sample_longitude_dd', # 'LONGI',
            'positioning_system_code', # 'POSYS',
            'station_name', # 'STATN',
            'platform_code', # 'SHIPC',
            'sampling_series', # SERIES
            'water_depth_m', # 'WADEP',
            'visit_comment', # 'COMNT_VISIT',
            'wind_direction_code', # 'WINDIR',
            'wind_speed_ms', # 'WINSP',
            'air_temperature_wet_degc', # 'AIRTEMP',
            'air_pressure_hpa', # 'AIRPRES',
            'weather_observation_code', # 'WEATH',
            'cloud_observation_code', # 'CLOUD',
            'wave_observation_code', # 'WAVES','
            'ice_observation_code', # 'ICEOB',
            'secchi_depth_m', # 'SECCHI',
            'secchi_depth_quality_flag', # 'Q_SECCHI',
            'sample_id', # 'SMPNO',
            'sample_min_depth_m', # 'MNDEP',
            'sample_max_depth_m', # 'MXDEP',
            'sampling_laboratory', # 'SLABO',
            'sampling_laboratory_accreditated', # 'ACKR_SMP',
            'sampler_type_code', # 'SMTYP',
            'sampled_volume_l', # 'SMVOL',
            'preservative', # 'METFP',
            'sample_comment', # 'COMNT_SAMP',
            'scientific_name', # 'LATNM',
            'species_flag_code', # 'SFLAG',
            'cf', # 'CF',
            'trophic_type', # 'TRPHY',
            'param_counted', # 'COUNTNR', # Parameter.
            'param_abundance_class', # 'COUNT_CLASS', # Parameter.
            'coefficient', # 'COEFF',
            'param_abundance', # 'CONC_IND_L-1', # Parameter.
            'size_class', # 'SIZCL',
            'size_class_ref_list', # 'SIZRF',
            'param_biovolume', # 'BIOVOL', # Parameter.
            'quality_flag', # 'QFLAG',
            'analysed_by', # 'TAXNM',
            'counted_volume_ml', # 'SDVOL', # sedimentation_volume_ml
            'sedimentation_time_h', # 'SDTIM',
            'magnification', # 'MAGNI',
            'analytical_laboratory', # 'ALABO',
            'analytical_laboratory_accreditated', # 'ACKR_ANA',
            'analysis_date', # 'ANADATE',
            'method_documentation', # 'METDC',
            'method_reference_code', # 'REFSK',
            'variable_comment', # 'COMNT_VAR',
        ]                  
     
        self._translate_header = {
            'visit_year': 'MYEAR',
            'project_code': 'PROJ',
            'orderer': 'ORDERER',
            'sample_date': 'SDATE',
            'sample_latitude_dd': 'LATIT',
            'sample_longitude_dd': 'LONGI',
            'positioning_system_code': 'POSYS',
            'station_name': 'STATN',
            'platform_code': 'SHIPC',
            'sampling_series':  'SERIES',
            'water_depth_m': 'WADEP',
            'visit_comment': 'COMNT_VISIT',
            'wind_direction_code': 'WINDIR',
            'wind_speed_ms': 'WINSP',
            'air_temperature_wet_degc': 'AIRTEMP',
            'air_pressure_hpa': 'AIRPRES',
            'weather_observation_code': 'WEATH',
            'cloud_observation_code': 'CLOUD',
            'wave_observation_code': 'WAVES',
            'ice_observation_code': 'ICEOB',
            'secchi_depth_m': 'SECCHI',
            'secchi_depth_quality_flag': 'Q_SECCHI',
            'sample_id': 'SMPNO',
            'sample_min_depth_m': 'MNDEP',
            'sample_max_depth_m': 'MXDEP',
            'sampling_laboratory': 'SLABO',
            'sampling_laboratory_accreditated': 'ACKR_SMP',
            'sampler_type_code': 'SMTYP',
            'sampled_volume_l': 'SMVOL',
            'preservative': 'METFP',
            'sample_comment': 'COMNT_SAMP',
            'scientific_name': 'LATNM',
            'species_flag_code': 'SFLAG',
            'cf': 'CF',
            'trophic_type': 'TRPHY',
            'param_counted': 'COUNTNR', # Parameter.
            'coefficient': 'COEFF',
            'param_abundance': 'CONC_IND_L-1', # Parameter.
            'param_abundance_class': 'COUNT_CLASS', # Parameter for NET samples.
            'size_class': 'SIZCL',
            'size_class_ref_list': 'SIZRF',
            'param_biovolume': 'BIOVOL', # Parameter.
            'quality_flag': 'QFLAG',
            'analysed_by': 'TAXNM',
            'counted_volume_ml': 'SDVOL', # sedimentation_volume_ml
            'sedimentation_time_h': 'SDTIM',
            'magnification': 'MAGNI',
            'analytical_laboratory': 'ALABO',
            'analytical_laboratory_accreditated': 'ACKR_ANA',
            'analysis_date': 'ANADATE',
            'method_documentation': 'METDC',
            'method_reference_code': 'REFSK',
            'variable_comment': 'COMNT_VAR',
            }
        
        # Used as row key and for sort order.
        self._row_key_items = [
            'station_name', 
            'sample_date', 
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
            for item in self._header_counted_items:
                report_row.append(row_dict.get(item, ''))
            # Add all rows to result.
            result_table.append_row(report_row)

