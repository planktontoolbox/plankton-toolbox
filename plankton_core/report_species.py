#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import plankton_core

class CreateReportSpecies(object):
    """ """
    def __init__(self, report_type = 'counted'):
        """ """
        super(CreateReportSpecies, self).__init__()
        self._reporttype = report_type # 'counted' or 'net'
        
    def create_report(self, datasets, result_table,
                      aggregate_rows = False,
                      abundance_class_samples = False):
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
        # Check number of samples.
        self._numberofsamples = 0
        for dataset in datasets:
            for visit in dataset.get_children():
                self._numberofsamples += len(visit.get_children())
        
        # Number of columns per sample.
        self._numberofcolumnspersample = None
        if self._reporttype == 'counted':
            self._numberofcolumnspersample = 2
        elif self._reporttype == 'net':
            self._numberofcolumnspersample = 1
        else:
            raise UserWarning('Unknown report type.')
        
        # Set header.
        self._numberofcolumns = 8 + (self._numberofsamples * self._numberofcolumnspersample)
        result_table.set_header([u''] * (8 + self._numberofsamples * self._numberofcolumnspersample)) # Note: Header is not used.
        #
        # Part 1: Create header rows with columns for sample related data.
        #
        header_row_1 = [''] * self._numberofcolumns 
        header_row_2 = [''] * self._numberofcolumns 
        header_row_3 = [''] * self._numberofcolumns 
        header_row_4 = [''] * self._numberofcolumns 
        header_row_5 = [''] * self._numberofcolumns 
        header_row_6 = [''] * self._numberofcolumns 
        header_row_1[7] = u'Station:'
        header_row_2[7] = u'Sampling date:'
        header_row_3[7] = u'Min. depth:'
        header_row_4[7] = u'Max. depth:'
        header_row_5[7] = u'Analysis date:'
        header_row_6[7] = u'Analysed by:'
        #
        # Iterate over file to create columns.
        sampleindex = 0
        for dataset in datasets:
            for visitnode in dataset.get_children():
                for samplenode in visitnode.get_children():
                    #
                    header_row_1[8 + (sampleindex * self._numberofcolumnspersample)] = visitnode.get_data('station_name')
                    header_row_2[8 + (sampleindex * self._numberofcolumnspersample)] = visitnode.get_data('sample_date')
                    header_row_3[8 + (sampleindex * self._numberofcolumnspersample)] = samplenode.get_data('sample_min_depth_m')
                    header_row_4[8 + (sampleindex * self._numberofcolumnspersample)] = samplenode.get_data('sample_max_depth_m')
                    header_row_5[8 + (sampleindex * self._numberofcolumnspersample)] = samplenode.get_data('analysis_date')
                    header_row_6[8 + (sampleindex * self._numberofcolumnspersample)] = samplenode.get_data('analysed_by')
                    #
                    sampleindex += 1
        #
        # Part 2: Iterate over all rows in all samples. Create a dictionaries  
        #         containing taxon/size as key and lists of abundances for each sample.
        #         Size class included with ':' as delimiter.
        #         Example: "Incertae sedis:1": [1234.5, 1234.5, 1234.5, 1234.5]
        parameter_values_dict = {}
        # Iterate through datasets.
        sampleindex = 0
        for dataset in datasets:
            for visitnode in dataset.get_children():
                
                for samplenode in visitnode.get_children():
                
                    for variablenode in samplenode.get_children():
                        #  
                        taxonandsize = variablenode.get_data('scientific_name') + ':' + \
                                       variablenode.get_data(u'size_class') + ':' + \
                                       variablenode.get_data(u'species_flag_code') + ':' + \
                                       variablenode.get_data(u'cf') + ':' + \
                                       variablenode.get_data(u'trophic_type') 
                        #
                        parameter = variablenode.get_data('parameter')
                        value = variablenode.get_data('value')
                        #
                        if taxonandsize not in parameter_values_dict:
                            parameter_values_dict[taxonandsize] = [''] * self._numberofsamples * self._numberofcolumnspersample # Add new value list. 
                        #
                        if self._reporttype == 'counted':
                            # Counted, column 1.
                            if parameter == 'Abundance':
                                parameter_values_dict[taxonandsize][sampleindex * self._numberofcolumnspersample] = value
                            # Counted, column 2.
                            if parameter == 'Biovolume concentration':
                                parameter_values_dict[taxonandsize][sampleindex * self._numberofcolumnspersample + 1] = value
                        elif self._reporttype == 'net':
                            if parameter == 'Abundance class':
                                parameter_values_dict[taxonandsize][sampleindex * self._numberofcolumnspersample] = value
                    #
                    sampleindex += 1
        #
        # Part 3: Create the species rows in the report.        
        #
        species_rows = []
        # Iterate over species in the dictionary.
        for phytowinnameandsize in parameter_values_dict.keys():
            # Counted samples:
            taxonandsize = phytowinnameandsize.split(':')
            scientificname = taxonandsize[0]
            sizeclass = taxonandsize[1]
            sflag = taxonandsize[2]
            cf = taxonandsize[3]
            trophic_type = taxonandsize[4]
            # Get extra info.
            taxonclass = plankton_core.Species().get_taxon_value(scientificname, u'taxon_class')
            harmful = plankton_core.Species().get_taxon_value(scientificname, u'harmful')
            unit_type = plankton_core.Species().get_bvol_value(scientificname, sizeclass, u'bvol_unit')
            # trophic_type = plankton_core.Species().get_bvol_value(scientificname, sizeclass, u'trophic_type')
            # if not trophic_type:
            #     trophic_type = plankton_core.Species().get_taxon_value(scientificname, u'trophic_type')
            #
            # Put the row together.
            row = [''] * (8 + (self._numberofcolumns * self._numberofcolumnspersample))
            row[0] = taxonclass
            row[1] = u'X' if harmful else u''
            row[2] = scientificname
            row[3] = sizeclass
            row[4] = sflag.lower() if sflag else '' # Lowercase.
            row[5] = cf.lower() if cf else '' # Lowercase.
            row[6] = trophic_type
            row[7] = unit_type 
            #
            for index, value in enumerate(parameter_values_dict[phytowinnameandsize]):
                row[8 + (index)] = value
            # Add the row the report.
            species_rows.append(row)
            
        # Sort the outdata list before writing to file. 
        species_rows.sort(report_count_table_sort) # Sort function defined below.
        
        #
        # Aggregate values. Same species and trophy but different size classes will be aggregated.
        if aggregate_rows and (self._reporttype == 'counted'):
            oldrow = None
            for row in species_rows:
                row[3] = u'' # Size classes should be removed. 
                if oldrow:
                    if row[2]: # Don't aggregate if species is missing.
                        # Iterate over samples.
                        if oldrow[2] == row[2]: # Column 2: Species.
                            if oldrow[5] == row[5]: # Column 5: Trophy may differ for Unicells etc.
                                sampleindex = 0
                                while sampleindex < self._numberofsamples:
                                    abundcol = 8 + (sampleindex * self._numberofcolumnspersample)
                                    volumecol = abundcol + 1
                                    if row[abundcol] and oldrow[abundcol]:
                                        row[abundcol] = str(int(row[abundcol]) + int(oldrow[abundcol]))
                                        oldrow[0] = u'REMOVE AGGREGATED' #
                                    if row[volumecol] and oldrow[volumecol]:
                                        row[volumecol] = str(float(row[volumecol].replace(u',', u'.')) + 
                                                                 float(oldrow[volumecol].replace(u',', u'.'))).replace(u'.', u',')
                                        oldrow[0] = u'REMOVE AGGREGATED' #
                                    #
                                    sampleindex += 1     
                #
                oldrow = row

        #
        # Part 4: Put all parts together and add to result table.
        # 
        result_table.append_row(header_row_1)
        result_table.append_row(header_row_2)
        result_table.append_row(header_row_3)
        result_table.append_row(header_row_4)
        result_table.append_row(header_row_5)
        result_table.append_row(header_row_6)
        # NET samples:
        #report_table.append_row([u'Klass', u'Pot. giftig', u'Art', u'Sflag'] + [u'Förekomst'] * numberofsamples) 
        # Counted samples:
        if self._reporttype == 'counted':
            if aggregate_rows:
                result_table.append_row([u'Class', u'Pot. toxic', 
                                         u'Scientific name', u'', u'Sflag', u'Cf', u'Trophic type', u'Unit type'] + 
                                        [u'Units/L', u'Biovolume (mm3/L)'] * self._numberofsamples) # Two columns per sample.
            else:
                result_table.append_row([u'Class', u'Pot. toxic', 
                                         u'Scientific name', u'Size class', u'Sflag', u'Cf', u'Trophic type', u'Unit type'] + 
                                        [u'Units/L', u'Biovolume (mm3/L)'] * self._numberofsamples) # Two columns per sample.
        elif self._reporttype == 'net':
            result_table.append_row([u'Class', u'Pot. toxic', 
                                     u'Scientific name', u'', u'Sflag', u'Cf', u'Trophic type', u'Unit type'] + 
                                    [u'Occurrence'] * self._numberofsamples) # Two columns per sample.
        #
        for row in species_rows:
            if row[0] != u'REMOVE AGGREGATED':
                result_table.append_row(row)

# Sort function for the result table.
def report_count_table_sort(s1, s2):
    """ """
    # Sort order: Class and scientific name.
    columnsortorder = [0, 2, 3, 6] # Class, species, size class and trophy.
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

