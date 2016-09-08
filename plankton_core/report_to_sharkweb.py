#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import plankton_core

class CreateReportToSharkweb(object):
    """ """
    def __init__(self, report_type = 'counted'): # 'counted' or 'net'.):
        """ """
        super(CreateReportToSharkweb, self).__init__()
        self._reporttype = report_type
        self._taxaphytowin = None
        # Header for "qualitative" counting.
        self._header_counted_items = [
            'MYEAR',
            'PROJ',
            'ORDERER',
            'SDATE',
            'LATIT',
            'LONGI',
            'POSYS',
            'STATN',
            'SHIPC',
            'WADEP',
            'COMNT_VISIT',
            'WINDIR',
            'WINSP',
            'AIRTEMP',
            'AIRPRES',
            'WEATH',
            'CLOUD',
            'WAVES',',',
            'ICEOB',
            'SECCHI',
            'Q_SECCHI',
            'SMPNO',
            'MNDEP',
            'MXDEP',
            'SLABO',
            'ACKR_SMP',
            'SMTYP',
            'SMVOL',
            'METFP',
            'COMNT_SAMP',
            'LATNM',
            'SFLAG',
            'TRPHY',
            'COUNTNR',
            'COEFF',
            'CONC_IND_L-1',
            'SIZCL',
            'SIZRF',
            'BIOVOL',
            'QFLAG',
            'TAXNM',
            'SDVOL',
            'SDTIM',
            'MAGNI',
            'ALABO',
            'ACKR_ANA',
            'ANADATE',
            'METDC',
            'REFSK',
            'COMNT_VAR',
        ]                  
        # Header for "quantitative" counting.
        self._header_net_items = [
            'MYEAR',
            'PROJ',
            'ORDERER',
            'SDATE',
            'LATIT',
            'LONGI',
            'POSYS',
            'STATN',
            'SHIPC',
            'WADEP',
            'COMNT_VISIT',
            'WINDIR',
            'WINSP',
            'AIRTEMP',
            'AIRPRES',
            'WEATH',
            'CLOUD',
            'WAVES',
            'ICEOB',
            'SECCHI',
            'Q_SECCHI',
            'SMPNO',
            'MNDEP',
            'MXDEP',
            'SLABO',
            'ACKR_SMP',
            'SMTYP',
            'METFP',
            'COMNT_SAMP',
            'LATNM',
            'SFLAG',
            'TRPHY',
            'COUNT_CLASS',
            'QFLAG',
            'TAXNM',
            'ALABO',
            'ACKR_ANA',
            'METDC',
            'REFSK',
            'COMNT_VAR',
        ]                  
     
    def create_report(self, datasets, result_table,
                     show_debug_info = False, 
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
            result_table.set_header(self._header_counted_items)
        elif self._reporttype == 'net':
            result_table.set_header(self._header_net_items)
        # Iterate through datasets.
        rowdict = {}
        #
        for datasetnode in datasets:
            #
            for visitnode in datasetnode.get_children():
                #
                for samplenode in visitnode.get_children():
                    # 
                    for variablenode in samplenode.get_children():
                        rowdict = {}
                        datadict = {}
                        datadict.update(datasetnode.get_data_dict())
                        datadict.update(visitnode.get_data_dict())
                        datadict.update(samplenode.get_data_dict())
                        datadict.update(variablenode.get_data_dict())
                                    
                        # Dataset:
                        rowdict['PROJ'] = datadict.get('project_code', '?')
                        rowdict['SMPNO'] = datadict.get('sample_id', '?')
                        
                        # Visit:
                        year = datadict.get('sample_date', '0000')[:4] # Get substring.
                        if not year: year = datadict.get('visit_year', '0000')
                        rowdict['MYEAR'] = year
                        rowdict['SDATE'] = datadict.get('sample_date', '?')
                        rowdict['LATIT'] = datadict.get('reported_latitude', '?')
                        rowdict['LONGI'] = datadict.get('reported_longitude', '?')
                        rowdict['STATN'] = datadict.get('station_name', '?')
                        rowdict['WADEP'] = datadict.get('water_depth_m', '?')
                        rowdict['SHIPC'] = datadict.get('platform_code', '?')
                        rowdict['SERNO'] = datadict.get('station_number', '?') # 'Stat no', used for serial-number.
                        # Unique visit id with "serial-number".
                        rowdict['VISIT_ID'] = year + '-' + \
                                               datadict.get('platform_code', '') + '-' + \
                                               datadict.get('station_number', '') # Used for serial-number.            
            
                        # Sample:
                        rowdict['SMTYP'] = datadict.get('sampler_type_code', '?')
                        rowdict['MNDEP'] = datadict.get('sample_min_depth_m', '?')
                        rowdict['MXDEP'] = datadict.get('sample_max_depth_m', '?')
                        rowdict['TAXNM'] = datadict.get('taxonomist', '?')
                        rowdict['ANADATE'] = datadict.get('analysis_date', '?')
                        rowdict['SDVOL'] = datadict.get('sedimentation_volume', '?')
                        rowdict['SDTIM'] = datadict.get('sedimentation_time_h', '?')
                        rowdict['METFP'] = datadict.get('preservative', '?')
                        
                        if self._reporttype == 'net':
                            # Net samples with conc-class 1-5:
                            # Species
                            phytowinname = variablenode.get_data('scientific_name', '?')
                            parts = phytowinname.split(' ')
                            speciesname = ''
                            for part in parts:
                                if part not in ['cf.', 'HET', '32', '(cell:', '(width:', '(no']:
                                    speciesname += part + ' '
                                else:
                                    if part not in ['cf.']:
                                        break # Break loop.
                            speciesname = speciesname.strip()
                            #
                            if self._taxaphytowin is not None:
                                pegname, pegsize, sflag = self._taxaphytowin.convert_from_phytowin_to_peg(speciesname, phytowin_size_class = '32')
                            else:
                                pegname = speciesname
                                pegsize = ''
                                sflag = ''
                            # Check if 'cf.' was included in name. Add to Sflag.
                            if 'cf.' in variablenode.get_data('Species', '?'):
                                if sflag:
                                    sflag = 'cf., ' + sflag
                                else:
                                    sflag = 'cf.'
                            #
                            taxonname = plankton_core.Species().get_taxon_value(pegname, 'scientific_name')
                            trophy = plankton_core.Species().get_bvol_value(pegname, pegsize, 'bvol_trophic_type')
                            # If trophy not available for this sizeclass, get it from taxon.
                            if not trophy: 
                                trophy = plankton_core.Species().get_taxon_value(pegname, 'bvol_trophic_type')
                            #
                            if show_debug_info:
                                if not pegname: pegname = '' 
                                pegname = pegname + ' [' + phytowinname + ']'
                            #
                            rowdict['LATNM'] = pegname
                            rowdict['LATNM_DYNTAXA'] = taxonname
                            rowdict['SFLAG'] = sflag.lower() if sflag else '' # Lowercase.
                            rowdict['TROPHY'] = trophy
                            rowdict['COUNTNR'] = '' # Not used for 'net' samples.
                            if variablenode.get_data('parameter', '') == 'Abundance class':
                                    rowdict['ABUND_CLASS'] = variablenode.get_data('value', '?')
                            rowdict['COEFF'] = variablenode.get_data('coefficient', '?')
                            rowdict['MAGNI'] = variablenode.get_data('magnification').replace(u"Part counted with ", u"")
                            rowdict['SIZCL'] = pegsize
                            rowdict['COMNT_VAR'] = samplenode.get_data('sample_comment', '?')
                        else:
                            # Normal samples with countnr and coeff:
                            # Species
                            phytowinname = variablenode.get_data('scientific_name', '?')
                            # Remove 'cf.'
                            if 'cf.' in phytowinname:  
                                parts = phytowinname.split(' ')
                                speciesname = ''
                                for part in parts:
                                    if part not in ['cf.']:
                                        speciesname += part + ' '
                                phytowinname = speciesname.strip()
                            #
                            phytowinsize = variablenode.get_data('size_class', '?')
                            # Phytowin names and sizeclasses may differ from PEG. SFLAG is also handled.
        #                     if self._taxaphytowin is not None:
        #                         pegname, pegsize, sflag = self._taxaphytowin.convert_from_phytowin_to_peg(phytowinname, phytowinsize)
        #                     else:
        #                         pegname = phytowinname
        #                         pegsize = phytowinsize
        #                         sflag = ''
                            pegname = phytowinname
                            pegsize = phytowinsize
                            sflag = ''
                            # Check if 'cf.' was included in name. Add to Sflag.
                            if 'cf.' in variablenode.get_data('Species', '?'):
                                if sflag:
                                    sflag = 'cf., ' + sflag
                                else:
                                    sflag = 'cf.'
                            # 
                            taxonname = plankton_core.Species().get_taxon_value(pegname, 'scientific_name')
                            trophy = plankton_core.Species().get_bvol_value(pegname, pegsize, 'bvol_trophic_type')
                            # If trophy not available for this sizeclass, get it from taxon.
                            if not trophy: 
                                trophy = plankton_core.Species().get_taxon_value(pegname, 'bvol_trophic_type')
                            # Debug:
                            if show_debug_info:
                                if not pegname: pegname = '' 
                                if not phytowinname: phytowinname = '' 
                                if not phytowinsize: phytowinsize = '' 
                                pegname = pegname + ' [' + phytowinname + ' : ' + unicode(phytowinsize) + ']'
                            #
                            rowdict['LATNM'] = pegname
                            rowdict['LATNM_DYNTAXA'] = taxonname
                            rowdict['SFLAG'] = sflag.lower() if sflag else '' # Lowercase.
                            rowdict['TRPHY'] = trophy
                            rowdict['COUNTNR'] = variablenode.get_data('Units', '?')
                            rowdict['ABUND_CLASS'] = '' # Only for 'net' samples.
                            rowdict['COEFF'] = variablenode.get_data('coefficient', '?')
                            rowdict['MAGNI'] = variablenode.get_data('magnification', '?').replace(u"Part counted with ", u"")
                            rowdict['SIZCL'] = pegsize
                            rowdict['COMNT_VAR'] = samplenode.get_data('sample_comment', '?')
                        #
#      station_name    
#      sample_date    
# time    
#      reported_latitude    
#      reported_longitude    
#      sample_min_depth_m    
#      sample_max_depth_m    
#      water_depth_m    
# scientific_name    
# species_flag_code    
# trophic_type_code    
# size_class    
# description    
# coefficient    
# parameter    
# value    
# unit    
#      sample_id    
# project_code    
#      platform_code    
#      station_number    
# taxon_class    
# magnification    
# counted_units    
# number_of_depths    
#      sampler_type_code    
# sample_size    
# sampled_by    
# sample_comment    
# mixed_volume    
#      preservative    
#      sedimentation_volume    
#      preservative    
# preservative_amount    
#      sedimentation_time_h    
# chamber_diameter    
#      analysis_date    
#      taxonomist                           # Create row by using order in header row.
                        report_row = []
                        
                        if self._reporttype == 'counted':
                            for item in self._header_counted_items:
                                report_row.append(rowdict.get(item, '')) 
                        elif self._reporttype == 'net':
                            for item in self._header_net_items:
                                report_row.append(rowdict.get(item, '')) 
                        #
                        result_table.append_row(report_row)
