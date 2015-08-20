#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2015 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import plankton_core

class CreateReportToSharkweb(object):
    """ """
    def __init__(self, report_type = 'counted'): # 'counted' or 'net'.):
        """ """
        # Initialize parent.
        super(CreateReportToSharkweb, self).__init__()
        #
        self._reporttype = report_type
        #
        self._taxaphytowin = None
        #
        self._header_counted_items = [
            'MYEAR',
            'SDATE',
            'STATN',
            'EXPID',
            'SHIPC',
            'VISIT_ID', # Added.    
            'WADEP',
            'WINSP',
            'WAVHT',
            'WINDR',
            'CLOUD',
            'ICEOB',
            'WEATH',
            'LATIT',
            'LONGI',
            'POSYS',
            'SMPNO',
            'SERNO',
            'STIME',
            'MNDEP',
            'MXDEP',
            'PROJ',
            'ORDERER',
            'MPROG',
            'SLABO',
            'REFSK',
            'METDC',
            'SMTYP',
            'SMVOL',
            'PDMET',
            'QFLAG',
            'METOA',
            'ALABO',
            'ANADATE',
            'COMNT_VAR',
            'SIZCL',
            'SIZRF',
            'SFLAG',
            'TROPHY',
            'COEFF',
            'MAGNI',
            'CEVOL',
            'LATNM',
            'LATNM_DYNTAXA',
            'TAXNM',
            'METFP',
            'SDTIM',
            'SDVOL',
            'COUNTNR',
            'ABUND'
        ]                  

        self._header_net_items = [
            'MYEAR',
            'SDATE',
            'STATN',
            'SHIPC',
            'VISIT_ID', # Added.    
            'WADEP',
            'LATIT',
            'LONGI',
            'POSYS',
            'SMPNO',
            'MNDEP',
            'MXDEP',
            'PROJ',
            'ORDERER',
            'SLABO',
            'METDC',
            'SMTYP',
            'QFLAG',
            'ALABO',
            'COMNT_VAR',
            'SFLAG',
            'TROPHY',
            'LATNM',
            'LATNM_DYNTAXA',
            'TAXNM',
            'METFP',
            'ABUND_CLASS'    
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
        
        # Add default values.
        rowdict['EXPID'] = ''
        rowdict['WINSP'] = ''
        rowdict['WAVHT'] = ''
        rowdict['WINDR'] = ''
        rowdict['CLOUD'] = ''
        rowdict['ICEOB'] = ''
        rowdict['WEATH'] = ''
        rowdict['POSYS'] = '?'
        rowdict['SERNO'] = ''
        rowdict['STIME'] = ''
        rowdict['ORDERER'] = '?'
        rowdict['MPROG'] = ''
        rowdict['SLABO'] = '?'
        rowdict['REFSK'] = '?'
        rowdict['METDC'] = ''
        rowdict['SMVOL'] = ''
        rowdict['PDMET'] = '?'
        rowdict['QFLAG'] = ''
        rowdict['METOA'] = '?'
        rowdict['ALABO'] = '?'
        rowdict['SIZRF'] = ''
        rowdict['MAGNI'] = ''
        rowdict['CEVOL'] = ''
        rowdict['ABUND'] = ''
        
        for datasetnode in datasets:

            # Dataset:
            rowdict['PROJ'] = datasetnode.get_data('project')
            rowdict['SMPNO'] = datasetnode.get_data('sample_id')

            # Visit:
            visitnode = datasetnode.get_children()[0] # Only one child.
            year = visitnode.get_data('date')[:4] # Get substring.
            rowdict['MYEAR'] = year if year else ''
            rowdict['SDATE'] = visitnode.get_data('date')
            rowdict['LATIT'] = visitnode.get_data('reported_latitude')
            rowdict['LONGI'] = visitnode.get_data('reported_longitude')
            rowdict['STATN'] = visitnode.get_data('station_name')
            rowdict['WADEP'] = visitnode.get_data('water_depth_m')
            rowdict['SHIPC'] = visitnode.get_data('platform_code')
            rowdict['SERNO'] = visitnode.get_data('station_number') # 'Stat no', used for serial-number.
            # Unique visit id with "serial-number".
            rowdict['VISIT_ID'] = year + '-' + \
                                   visitnode.get_data('Ship') + '-' + \
                                   visitnode.get_data('Stat no') # Used for serial-number.            

            # Sample:
            samplenode = visitnode.get_children()[0] # Only one child.
            rowdict['SMTYP'] = samplenode.get_data('sampler_type')
            rowdict['MNDEP'] = samplenode.get_data('sample_min_depth_m')
            rowdict['MXDEP'] = samplenode.get_data('sample_max_depth_m')
            rowdict['TAXNM'] = samplenode.get_data('counted_by')
            rowdict['ANADATE'] = samplenode.get_data('counted_on')
            rowdict['SDVOL'] = samplenode.get_data('Sedim. volume')
            rowdict['SDTIM'] = samplenode.get_data('sedimentation_time_h')
            rowdict['METFP'] = samplenode.get_data('preservative')
            #
            for variablenode in samplenode.get_children():
                if variablenode.get_data('Abundance (scale 1 to 5)'):
                    # Net samples with conc-class 1-5:
                    # Species
                    phytowinname = variablenode.get_data('Species')
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
                    if 'cf.' in variablenode.get_data('Species'):
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
                    rowdict['ABUND_CLASS'] = variablenode.get_data('Abundance (scale 1 to 5)')
                    rowdict['COEFF'] = variablenode.get_data('Coeff')
                    rowdict['MAGNI'] = variablenode.get_data('Magnification').replace(u"Part counted with ", u"")
                    rowdict['SIZCL'] = pegsize
                    rowdict['COMNT_VAR'] = samplenode.get_data('Comment')
                else:
                    # Normal samples with countnr and coeff:
                    # Species
                    phytowinname = variablenode.get_data('scientific_name')
                    # Remove 'cf.'
                    if 'cf.' in phytowinname:  
                        parts = phytowinname.split(' ')
                        speciesname = ''
                        for part in parts:
                            if part not in ['cf.']:
                                speciesname += part + ' '
                        phytowinname = speciesname.strip()
                    #
                    phytowinsize = variablenode.get_data('size_class')
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
                    if 'cf.' in variablenode.get_data('Species'):
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
                    rowdict['TROPHY'] = trophy
                    rowdict['COUNTNR'] = variablenode.get_data('Units')
                    rowdict['ABUND_CLASS'] = '' # Only for 'net' samples.
                    rowdict['COEFF'] = variablenode.get_data('coefficient')
                    rowdict['MAGNI'] = variablenode.get_data('magnification').replace(u"Part counted with ", u"")
                    rowdict['SIZCL'] = pegsize
                    rowdict['COMNT_VAR'] = samplenode.get_data('sample_comment')
                #
                # Create row by using order in header row.
                report_row = []
                
                if self._reporttype == 'counted':
                    for item in self._header_counted_items:
                        report_row.append(rowdict.get(item, '')) 
                elif self._reporttype == 'net':
                    for item in self._header_net_items:
                        report_row.append(rowdict.get(item, '')) 
                #
                result_table.append_row(report_row)
        
