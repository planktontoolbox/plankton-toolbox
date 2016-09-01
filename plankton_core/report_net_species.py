#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2016 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#
from __future__ import unicode_literals

import plankton_core

class CreateReportNetSpecies(object):
    """ """
    def __init__(self):
        """ """
        # Initialize parent.
        super(CreateReportNetSpecies, self).__init__()
        #
#         self._taxaphytowin = None
        #
        
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
        numberofsamples = len(datasets)
        numberofcolumns = 4 + numberofsamples
        result_table.set_header([''] * numberofcolumns) # Note: Header is not used.
        #
        # Part 1: Create header rows with columns for sample related data.
        #
        header_row_1 = [unicode()] * numberofcolumns 
        header_row_2 = [unicode()] * numberofcolumns 
        header_row_3 = [unicode()] * numberofcolumns 
        header_row_4 = [unicode()] * numberofcolumns 
        header_row_5 = [unicode()] * numberofcolumns 
        header_row_6 = [unicode()] * numberofcolumns 
        header_row_1[3] = 'Station:'
        header_row_2[3] = 'Provtagningsdatum:'
        header_row_3[3] = 'Min. djup:'
        header_row_4[3] = 'Max. djup:'
        header_row_5[3] = 'Datum för analys:'
        header_row_6[3] = 'Analys utförd av:'
        # Iterate over file to create columns.
        for datasetindex, datasetnode in enumerate(datasets):
            visitnode = datasetnode.get_children()[0] # Only one child.
            samplenode = visitnode.get_children()[0] # Only one child.
            #
            header_row_1[4 + datasetindex] = visitnode.get_data('station_name')
            header_row_2[4 + datasetindex] = visitnode.get_data('date')
            header_row_3[4 + datasetindex] = samplenode.get_data('sample_min_depth_m')
            header_row_4[4 + datasetindex] = samplenode.get_data('sample_max_depth_m')
            header_row_5[4 + datasetindex] = samplenode.get_data('counted_on')
            header_row_6[4 + datasetindex] = samplenode.get_data('counted_by')
        #
        # Part 2: Iterate over all rows in all samples. Create a dictionary with 
        #         species as keys and lists of abundances for each sample.
        #         Example: "Incertae sedis": [1234.5, 1234.5, 1234.5, 1234.5]
        species_sample_dict = {}
        # Iterate through datasets.
        for datasetindex, datasetnode in enumerate(datasets):
            visitnode = datasetnode.get_children()[0] # Only one child.
            samplenode = visitnode.get_children()[0] # Only one child.
            for variablenode in samplenode.get_children():
                # "Species","Abundance (scale 1 to 5)"
                phytowinname = variablenode.get_data('scientific_name')
                abundance = variablenode.get_data('Abundance (scale 1 to 5)')
                #
                if species_sample_dict.has_key(phytowinname):
                    species_sample_dict[phytowinname][datasetindex] = abundance
                else:
                    species_sample_dict[phytowinname] = [unicode()] * numberofsamples
                    species_sample_dict[phytowinname][datasetindex] = abundance
        #
        # Part 3: Create the species rows in the report.        
        #
        species_rows = []
        # Iterate over species in the dictionary.
        for phytowinname in species_sample_dict.keys():
            # Extract useful part from Species-column.
            # Example: "Protoperidinium steinii HET 32 (cell: 32-37µm)"
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
#             if self._taxaphytowin is not None:
#                 pegname, pegsize, sflag = self._taxaphytowin.TaxaPhytowin().convert_from_phytowin_to_peg(speciesname, phytowin_size_class = '32')
#             else:
#                 pegname = speciesname
#                 pegsize = ''
#                 sflag = ''
            pegname = speciesname
            pegsize = ''
            sflag = ''
                
            # Check if 'cf.' was included in name. Add to Sflag.
            if 'cf.' in variablenode.get_data('scientific_name'):
                if sflag:
                    sflag = 'cf. ' + sflag
                else:
                    sflag = 'cf.'
            
            taxonname = plankton_core.Species().get_taxon_value(pegname, 'scientific_name')
            taxonclass = plankton_core.Species().get_taxon_value(pegname, 'class')
#            author = taxa.Taxa().get_taxon_value(pegname, 'Author')
            harmful = plankton_core.Species().get_taxon_value(pegname, 'harmful')
#            trophy = taxa.Taxa().getBvolValue(pegname, pegsize, 'Trophy')
#            # If trophy not available for this sizeclass, get it from taxon.
#            trophy = taxa.Taxa().get_taxon_value(pegname, 'Trophy')
            #
            if show_debug_info:
                taxonname = taxonname + ' [' + phytowinname + ']'
            # Put the row together.
            row = [unicode()] * numberofcolumns
            row[0] = taxonclass
            row[1] = 'X' if harmful else ''
            row[2] = taxonname
            row[3] = sflag.lower() if sflag else '' # Lowercase.
            for index, abund in enumerate(species_sample_dict[phytowinname]):
                row[4 + index] = abund
            # Add the row the report.
            species_rows.append(row)
        # Sort the outdata list before writing to file. 
        species_rows.sort(report_net_table_sort) # Sort function defined below.
        #
        # Part 4: Put all parts together and add to result table.
        #
        result_table.append_row(header_row_1)
        result_table.append_row(header_row_2)
        result_table.append_row(header_row_3)
        result_table.append_row(header_row_4)
        result_table.append_row(header_row_5)
        result_table.append_row(header_row_6)
        result_table.append_row(['Class', 'Pot. toxic', 'Scientific name', 'Sflag'] + ['Occurrence'] * numberofsamples) 
        #
        species_rows.sort(report_net_table_sort)
        #
        for row in species_rows:
            result_table.append_row(row)


# Sort function for the result table.
def report_net_table_sort(s1, s2):
    """ """
    # Sort order: Class and scientific name.
    columnsortorder = [0, 2] 
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

