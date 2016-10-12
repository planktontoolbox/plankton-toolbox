#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import plankton_core

class CreateReportCounted(object):
    """ """
    def __init__(self):
        """ """
        # Initialize parent.
        super(CreateReportCounted, self).__init__()
        #
#         self._header_items = [
#             'Station', # 0
#             'Provtagningsdatum', # 1
#             'Analysdatum', # 2
#             'Min djup', # 3
#             'Max djup', # 4
#             #
#             'Klass', # 5
#             'Art/Taxonomisk enhet', # 6
#             'Sflag', # 7
#             'Author', # 8
#             'Trofigrad', # 9
#             'Potentiellt giftig', # 10
#             'Celler/l', # 11
#             'Biovolym (mm3/L)', # 12
#             #
#             'Analys laboratorium', # 13
# #            'Mikroskopist' # 14
#             'Mikroskopist', # 14
#             'Storleksklass (PEG)' # 15
#             ]
        self._header_items = [
            'Station', # 0
            'Provtagningsdatum', # 1
            'Analysdatum', # 2
            'Min djup', # 3
            'Max djup', # 4
            #
            'Klass', # 5
            'Art/Taxonomisk enhet', # 6
            'Sflag', # 7
            'Author', # 8
            'Trofigrad', # 9
            'Potentiellt giftig', # 10
            'Celler/l', # 11
            'Biovolym (mm3/L)', # 12
            #
            'Analys laboratorium', # 13
#            'Mikroskopist' # 14
            'Mikroskopist', # 14
            'Storleksklass (PEG)' # 15
            ]
        
    def create_report(self, datasets, result_table,
                     show_debug_info = False, 
                     aggregate_rows = False):
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
        # Iterate through datasets.
        report_rows = [] # Local copy before sorting.
        report_row = [unicode()]*16 # 16 columns.
        for datasetnode in datasets:
            #
            visitnode = datasetnode.get_children()[0] # Only one child.
            report_row[0] = visitnode.get_data('station_name') 
            report_row[1] = visitnode.get_data('sample_date')
            #
            samplenode = visitnode.get_children()[0] # Only one child.
            report_row[2] = samplenode.get_data('analysis_date') 
            report_row[3] = samplenode.get_data('sample_min_depth_m') 
            report_row[4] = samplenode.get_data('sample_max_depth_m') 
            report_row[14] = samplenode.get_data('taxonomist') 
            #
            for variablenode in samplenode.get_children():
                # Clear columns:
                report_row[5] = ''                
                report_row[6] = ''                
                report_row[7] = ''                
                report_row[8] = ''                
                report_row[9] = ''                
                report_row[10] = ''                
                report_row[11] = ''                
                report_row[12] = ''                
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
                
                phytowinsize = variablenode.get_data('Size')
                # Phytowin names and sizeclasses may differ from PEG. SFLAG is also handled.
#                 if self._taxaphytowin:
#                     pegname, pegsize, sflag = self._taxa_phytowin.TaxaPhytowin().convert_from_phytowin_to_peg(phytowinname, phytowinsize)
#                 else:
#                     pegname = phytowinname
#                     pegsize = phytowinsize
#                     sflag = ''
                pegname = phytowinname
                pegsize = phytowinsize
                sflag = ''
                # Check if 'cf.' was included in name. Add to Sflag.
                if 'cf.' in variablenode.get_data('scientific_name'):
                    if sflag:
                        sflag = 'CF. ' + sflag
                    else:
                        sflag = 'CF.'
                # 
                taxonname = plankton_core.Species().get_taxon_value(pegname, 'scientific_name')
                taxonclass = plankton_core.Species().get_taxon_value(pegname, 'taxon_class')
                author = plankton_core.Species().get_taxon_value(pegname, 'author')
                harmful = plankton_core.Species().get_taxon_value(pegname, 'harmful')
                trophy = plankton_core.Species().get_bvol_value(pegname, pegsize, 'bvol_trophic_type')
                # If trophy not available for this sizeclass, get it from taxon.
                if not trophy: 
                    trophy = plankton_core.Species().get_taxon_value(pegname, 'bvol_trophic_type')
                #
                countedunits = variablenode.get_data('units')
                coeff = variablenode.get_data('coefficient')
                volume = plankton_core.Species().get_bvol_value(pegname, pegsize, 'calculated_volume, µm3')
                carbon = plankton_core.Species().get_bvol_value(pegname, pegsize, 'calculated_per_unit_pg')
                #
                report_row[5] = taxonclass
                report_row[6] = taxonname
                report_row[7] = sflag.lower() if sflag else '' # Lowercase.
                report_row[8] = author
                report_row[9] = trophy
                report_row[10] = 'X' if harmful else ''
                report_row[15] = pegsize
                
                # Number.
                try:
                    report_row[11] = int(countedunits) * int(coeff)                    
                except:
                    report_row[11] = 'ERROR' + ' [' + countedunits + ' * ' + coeff + ']'
                # Volume.
                if volume != None:
                    try:
                        # calculatedvolume = int(countedunits) * int(coeff) * float(volume)
                        calculatedvolume = float(volume) * int(countedunits) * int(coeff) / 1000000000. # Should be mm3/l (2012-12-12) 
                        report_row[12] = format(calculatedvolume, '.8f').replace('.', ',')
                    except:
                        report_row[12] = 'ERROR' + ' [' + countedunits + ' * ' + coeff + ' * ' + volume + ' / 1000000000]'
                else:
                    report_row[12] = ''
                # Number and volume with debug info.
                if show_debug_info:
                    report_row[6] = taxonname + ' [' + phytowinname + ' : ' + phytowinsize + ']'
                    try:
                        report_row[11] = unicode(int(countedunits) * int(coeff)) + \
                                         ' [' + countedunits + ' * ' + coeff + ']'
                    except:
                        report_row[11] = 'ERROR' + ' [' + countedunits + ' * ' + coeff + ']'
                    #
                    if volume != None:
                        try:
                            calculatedvolume = int(countedunits) * int(coeff) * float(volume)
                            report_row[12] = format(calculatedvolume, '.2f').replace('.', ',') + \
                                             ' [' + countedunits + ' * ' + coeff + ' * ' + volume + ']'
                        except:
                            report_row[12] = 'ERROR' + ' [' + countedunits + ' * ' + coeff + ' * ' + volume + ']'
                    else:
                        report_row[12] = ''
                #
                report_rows.append(report_row[:]) # Clone
        # Sort the rows in the report.
        report_rows.sort(report_conc_table_sort)
        # Aggregate values. Same species but different size classes will be aggregated.
        if aggregate_rows:
            self._header_items[15] = '' # Size classes should be removed. 
            oldrow = None
            for row in report_rows:
                row[15] = '' # Size classes should be removed. 
                if oldrow:
                    if row[6]: # Don't aggregate if species is missing.
                        if oldrow[1:8] == row[1:8]:
                            if row[11] and oldrow[11]:
                                row[11] = unicode(int(row[11]) + int(oldrow[11]))
                                oldrow[0] = 'REMOVE AGGREGATED' #
                            if row[12] and oldrow[12]:
                                row[12] = unicode(float(row[12].replace(',', '.')) + float(oldrow[12].replace(',', '.'))).replace('.', ',')
                                oldrow[0] = 'REMOVE AGGREGATED' #
                oldrow = row

        # Set header in preview table.
        result_table.set_header(self._header_items)
        # Write rows to preview table.
        for row in report_rows:
            # Remove None items, they may otherwise appear in reports.
            row = [item if item else '' for item in row]
            if row[0] != 'REMOVE AGGREGATED':
                # Move all to the report table.
                result_table.append_row(row)


# Sort function for the result table.
def report_conc_table_sort(s1, s2):
    """ """
    # Sort order: Station, date min depth, max depth and scientific name.
    columnsortorder = [0, 1, 3, 4, 5, 6] 
    #
    for index in columnsortorder:
        s1item = s1[index]
        s2item = s2[index]
        # Empty strings should be at the end.
        if (s1item != '') and (s2item == ''): return -1
        if (s1item == '') and (s2item != ''): return 1
        if s1item < s2item: return -1
        if s1item > s2item: return 1
    #
    return 0 # All are equal.

