#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import plankton_core

class CreateReportToDataCenterShark(object):
    """ """
    def __init__(self, report_type = 'counted'): # 'counted' or 'net'.):
        """ """
        super(CreateReportToDataCenterShark, self).__init__()
        self._reporttype = report_type
#         self._taxaphytowin = None
        # Header for "qualitative" counting.
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
            'trophic_type', # 'TRPHY',
            'param_counted', # 'COUNTNR', # Parameter.
            'coefficient', # 'COEFF',
            'param_abundance', # 'CONC_IND_L-1', # Parameter.
            'size_class', # 'SIZCL',
            'size_class_ref_list', # 'SIZRF',
            'param_biovolume', # 'BIOVOL', # Parameter.
            'quality_flag', # 'QFLAG',
            'analysed_by', # 'TAXNM',
            'sedimentation_volume_ml', # 'SDVOL',
            'sedimentation_time_h', # 'SDTIM',
            'magnification', # 'MAGNI',
            'analytical_laboratory', # 'ALABO',
            'analytical_laboratory_accreditated', # 'ACKR_ANA',
            'analysis_date', # 'ANADATE',
            'method_documentation', # 'METDC',
            'method_reference_code', # 'REFSK',
            'variable_comment', # 'COMNT_VAR',
        ]                  
        # Header for "quantitative" counting.
        self._header_net_items = [
            'visit_year', # 'MYEAR',
            'project_code', # 'PROJ',
            'orderer', # 'ORDERER',
            'sample_date', # 'SDATE',
            'sample_latitude_dd', # 'LATIT',
            'sample_longitude_dd', # 'LONGI',
            'positioning_system_code', # 'POSYS',
            'station_name', # 'STATN',
            'platform_code', # 'SHIPC',
            'water_depth_m', # 'WADEP',
            'visit_comment', # 'COMNT_VISIT',
            'wind_direction_code', # 'WINDIR',
            'wind_speed_ms', # 'WINSP',
            'air_temperature_wet_degc', # 'AIRTEMP',
            'air_pressure_hpa', # 'AIRPRES',
            'weather_observation_code', # 'WEATH',
            'cloud_observation_code', # 'CLOUD',
            'wave_observation_code', # 'WAVES',
            'ice_observation_code', # 'ICEOB',
            'secchi_depth_m', # 'SECCHI',
            'secchi_depth_quality_flag', # 'Q_SECCHI',
            'sample_id', # 'SMPNO',
            'sample_min_depth_m', # 'MNDEP',
            'sample_max_depth_m', # 'MXDEP',
            'sampling_laboratory', # 'SLABO',
            'sampling_laboratory_accreditated', # 'ACKR_SMP',
            'sampler_type_code', # 'SMTYP',
            'preservative', # 'METFP',
            'sample_comment', # 'COMNT_SAMP',
            'scientific_name', # 'LATNM',
            'species_flag_code', # 'SFLAG',
            'trophic_type', # 'TRPHY',
            'param_abundance_class', # 'COUNT_CLASS', # Parameter.
            'quality_flag', # 'QFLAG',
            'analysed_by', # 'TAXNM',
            'analytical_laboratory', # 'ALABO',
            'analytical_laboratory_accreditated', # 'ACKR_ANA',
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
            'sedimentation_volume_ml': 'SDVOL',
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
        if self._reporttype == 'counted':
            header_items = self._header_counted_items
        elif self._reporttype == 'net':
            header_items = self._header_net_items
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
                                row_key += unicode(row_dict.get(item, ''))
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
                            # For NET samples.
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
#             for item in self._header_items:
#                 report_row.append(row_dict.get(item, ''))
            # Create row by using order in header row.
            if self._reporttype == 'counted':
                
                
#                 print(unicode(self._header_counted_items))
#                 print(unicode(row_dict.keys()))
                
                
                for item in self._header_counted_items:
                    report_row.append(row_dict.get(item, '')) 
            elif self._reporttype == 'net':
                for item in self._header_net_items:
                    report_row.append(row_dict.get(item, '')) 
            # Add all rows to result.
            result_table.append_row(report_row)

        
#                         if self._reporttype == 'net':
#                             # Net samples with conc-class 1-5:
#                             # Species
#                             phytowinname = variablenode.get_data('scientific_name', '?')
#                             parts = phytowinname.split(' ')
#                             speciesname = ''
#                             for part in parts:
#                                 if part not in ['cf.', 'HET', '32', '(cell:', '(width:', '(no']:
#                                     speciesname += part + ' '
#                                 else:
#                                     if part not in ['cf.']:
#                                         break # Break loop.
#                             speciesname = speciesname.strip()
#                             #
#                             if self._taxaphytowin is not None:
#                                 pegname, pegsize, sflag = self._taxaphytowin.convert_from_phytowin_to_peg(speciesname, phytowin_size_class = '32')
#                             else:
#                                 pegname = speciesname
#                                 pegsize = ''
#                                 sflag = ''
#                             # Check if 'cf.' was included in name. Add to Sflag.
#                             if 'cf.' in variablenode.get_data('Species', '?'):
#                                 if sflag:
#                                     sflag = 'cf., ' + sflag
#                                 else:
#                                     sflag = 'cf.'
#                             #
#                             taxonname = plankton_core.Species().get_taxon_value(pegname, 'scientific_name')
#                             trophy = plankton_core.Species().get_bvol_value(pegname, pegsize, 'bvol_trophic_type')
#                             # If trophy not available for this sizeclass, get it from taxon.
#                             if not trophy: 
#                                 trophy = plankton_core.Species().get_taxon_value(pegname, 'bvol_trophic_type')
#                             #
#                             row_dict['LATNM'] = pegname
#                             row_dict['LATNM_DYNTAXA'] = taxonname
#                             row_dict['SFLAG'] = sflag.lower() if sflag else '' # Lowercase.
#                             row_dict['TROPHY'] = trophy
#                             row_dict['COUNTNR'] = '' # Not used for 'net' samples.
#                             if variablenode.get_data('parameter', '') == 'Abundance class':
#                                     row_dict['ABUND_CLASS'] = variablenode.get_data('value', '?')
#                             row_dict['COEFF'] = variablenode.get_data('coefficient', '?')
#                             row_dict['MAGNI'] = variablenode.get_data('magnification').replace(u"Part counted with ", u"")
#                             row_dict['SIZCL'] = pegsize
#                             row_dict['COMNT_VAR'] = samplenode.get_data('sample_comment', '?')

#                         # Create row by using order in header row.
#                         report_row = []
#                         
#                         if self._reporttype == 'counted':
#                             for item in self._header_counted_items:
#                                 report_row.append(row_dict.get(item, '')) 
#                         elif self._reporttype == 'net':
#                             for item in self._header_net_items:
#                                 report_row.append(row_dict.get(item, '')) 
#                         #
#                         result_table.append_row(report_row)
