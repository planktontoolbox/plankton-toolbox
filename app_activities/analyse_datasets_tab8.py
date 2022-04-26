#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://plankton-toolbox.org
# Copyright (c) 2010-2018 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import sys
import operator
from PyQt6 import QtWidgets
from PyQt6 import QtCore

import toolbox_utils
import plankton_core
import app_framework

class AnalyseDatasetsTab8(QtWidgets.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab8, self).__init__()

    def set_main_activity(self, main_activity):
        """ """
        try:
            self._main_activity = main_activity
            self._analysisdata = main_activity.get_analysis_data()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
                
    def clear(self):
        """ """
        try:
            self._parameter_list.clear()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def update(self):
        """ """
        try:
            self.clear()
            analysisdata = self._analysisdata.get_data()
            if analysisdata:        
                # Search for all parameters in analysis data.
                parameterset = set()
                for visitnode in analysisdata.get_children():
                    for samplenode in visitnode.get_children():
                        for variablenode in samplenode.get_children():
                            parameterset.add(variablenode.get_data('parameter') + ' (' + variablenode.get_data('unit') + ')')
                parameterlist = sorted(parameterset)
                self._parameter_list.setList(parameterlist)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    # ===== TAB: Reports ===== 
    def content_reports(self):
        """ """
        # Active widgets and connections.
#         introlabel = app_framework.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText('AnalyseDatasetsTab8_intro'))
        # Parameters.
        self._parameter_list = app_framework.SelectableQListView()       
        clearall_label = app_framework.ClickableQLabel('Clear all')
        markall_label = app_framework.ClickableQLabel('Mark all')
        clearall_label.label_clicked.connect(self._parameter_list.uncheckAll)                
        markall_label.label_clicked.connect(self._parameter_list.checkAll)                
        # Predefined reports.
        self._report_1_button = QtWidgets.QPushButton('PRIMER')
        self._report_1_button.clicked.connect(self._create_report_1)                
        self._report_2_button = QtWidgets.QPushButton('Zooplankton: Abundance m2 and m3, length median and mean')
        self._report_2_button.clicked.connect(self._create_report_2)                

        # Layout widgets.
        form1 = QtWidgets.QGridLayout()
        gridrow = 0
        label1 = QtWidgets.QLabel('Parameters (for PRIMER):')
        form1.addWidget(label1, gridrow, 0, 1, 2)
        gridrow += 1
        form1.addWidget(self._parameter_list, gridrow, 0, 1, 2)
#         form1.addWidget(self._report_1_button, gridrow, 5, 1, 1)
        gridrow += 1
#         form1.addWidget(self._report_2_button, gridrow, 5, 1, 1)
        gridrow += 1
        form1.addWidget(clearall_label, gridrow, 0, 1, 1)
        form1.addWidget(markall_label, gridrow, 1, 1, 1)
        #
        vbox1 = QtWidgets.QVBoxLayout()
        vbox1.addWidget(self._report_1_button)
        vbox1.addWidget(self._report_2_button)
        vbox1.addStretch(5)
        #
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addLayout(form1)
        hbox1.addLayout(vbox1)
        hbox1.addStretch(5)
        #
        layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(introlabel)
#         layout.addLayout(form1)
        layout.addLayout(hbox1)
        layout.addStretch(5)
        self.setLayout(layout)                
        #
        return self
                
    def _create_report_1(self):
        """ """
        try:
            # Clear the report and view the report area.
            reportdata = self._main_activity.get_report_data()
            reportdata.clear_data()
            self._main_activity.view_report_data()
            # Filtered data should be used.
            self._main_activity.update_filter() # Must be done before create_filtered_dataset().
            analysisdata = self._analysisdata.create_filtered_dataset()
            if not analysisdata:
                return # Can't create a report from an empty dataset.
            # Create the report.
            parameters = self._parameter_list.getSelectedDataList()        
            self.create_primer_report(parameters, # Note:Support for multiple parameters.
                                    [analysisdata], # Note:Support for multiple datasets. Not used here.
                                    reportdata)
            # View the result in the report area.
            self._main_activity.view_report_data()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
        
    def _create_report_2(self):
        """ """
        try:
            # Clear the report and view the report area.
            reportdata = self._main_activity.get_report_data()
            reportdata.clear_data()
            self._main_activity.view_report_data()
            # Filtered data should be used.
            self._main_activity.update_filter() # Must be done before create_filtered_dataset().
            analysisdata = self._analysisdata.create_filtered_dataset()
            if not analysisdata:
                return # Can't create a report from an empty dataset.
            # Create the report.
            self._create_report_zooplankton_abundance_length_median_and_mean(analysisdata, reportdata)
            # View the result in the report area.
            self._main_activity.view_report_data()
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

    def create_primer_report(self, 
                           parameters, 
                           datasets, 
                           reportdata):
        """  """
        try:
            # Create a dataset (table, not tree).
            tabledata = plankton_core.DatasetTable()
            reportdata.set_data(tabledata)
            # Check indata.
            if parameters == None:
                raise UserWarning('Parameters are missing.')
            if datasets == None:
                raise UserWarning('Datasets are missing.')
            #
            # Calculate number of samples and columns.
            numberofsamples = 0
            for dataset in datasets:
                for visit in dataset.get_children():
                    numberofsamples += len(visit.get_children())
            numberofparameters = len(parameters)
            numberofcolumns = 6 + (numberofsamples * numberofparameters)
            # Set header. Note: Normal header is not used.
            tabledata.set_header([''] * numberofcolumns)
            #
            # Part 1: Create header rows with columns for sample related data.
            #
            header_row_1 = [str()] * numberofcolumns 
            header_row_2 = [str()] * numberofcolumns 
            header_row_3 = [str()] * numberofcolumns 
            header_row_4 = [str()] * numberofcolumns 
            header_row_1[5] = 'Station name:'
            header_row_2[5] = 'Date:'
            header_row_3[5] = 'Sample min depth:'
            header_row_4[5] = 'Sample max depth:'
            #
            # Iterate over file to create column headers.
            sampleindex = 0
            for dataset in datasets:
                for visit in dataset.get_children():
                    for sample in visit.get_children():
                        header_row_1[6 + (sampleindex * numberofparameters)] = visit.get_data('station_name')
                        header_row_2[6 + (sampleindex * numberofparameters)] = visit.get_data('sample_date')
                        header_row_3[6 + (sampleindex * numberofparameters)] = sample.get_data('sample_min_depth_m')
                        header_row_4[6 + (sampleindex * numberofparameters)] = sample.get_data('sample_max_depth_m')
                        sampleindex += 1
            #
            # Part 2: Iterate over all rows in all samples. Create a dictionary with 
            #         species as keys and lists of abundances for each sample.
            #         Size class included with ':' as delimiter.
            #         Example: "Incertae sedis:1": [1234.5, 1234.5, 1234.5, 1234.5]
            taxon_values_dict = {}
            # Iterate through datasets.
            sampleindex = 0
            for dataset in datasets:
                for visit in dataset.get_children():
                    for sample in visit.get_children():
                        for variable in sample.get_children():
                            scientific_name = variable.get_data('scientific_name')
                            size_class = variable.get_data('size_class')
                            trophic_type = variable.get_data('trophic_type')
                            stage = variable.get_data('stage')
                            sex = variable.get_data('sex')
                            #
                            taxon_key = str(scientific_name) + ':' + str(size_class) + ':' + str(trophic_type) + ':' + str(stage) + ':' + str(sex)
                            if taxon_key not in taxon_values_dict:
                                taxon_values_dict[taxon_key] = [str()] * (numberofsamples * numberofparameters) # Add new value list.
                            #
                            for paramindex, param in enumerate(parameters):
                                parameter = variable.get_data('parameter')
                                unit = variable.get_data('unit')
                                value = variable.get_data('value')
                                #
                                if param == (parameter + ' (' + unit + ')'):
                                    taxon_values_dict[taxon_key][sampleindex * numberofparameters + paramindex] = value
                        #
                        sampleindex += 1
            #
            # Part 3: Create the species rows in the report.        
            #
            taxon_rows = []
            # Iterate over species in the dictionary.
            for taxon_key in taxon_values_dict.keys():
                #
                taxon_key_parts = taxon_key.split(':')
                scientific_name = taxon_key_parts[0]
                size_class = taxon_key_parts[1]
                trophic_type = taxon_key_parts[2]
                stage = taxon_key_parts[3]
                sex = taxon_key_parts[4]
                #
                row = [''] * (numberofcolumns * numberofparameters)
                row[0] = scientific_name
                row[1] = size_class
                row[2] = trophic_type
                row[3] = stage
                row[4] = sex
                for index, value in enumerate(taxon_values_dict[taxon_key]):
                    row[6 + index] = value
    #                 row[6 + (index * numberofparameters) + 1] = values[1]
    #                 row[6 + (index * numberofparameters) + 1] = values[2]
                # Add the row the report.
                taxon_rows.append(row)
                 
            # Sort the outdata list before writing to file. 
            # Sort order: 
            # - 0: scientific_name
            # - 1: size_class
            # - 2: trophic_type
            # - 3: stage
            # - 4: sex
            taxon_rows.sort(key=operator.itemgetter(0, 1, 2, 3, 4))  
            #
            # Part 4: Put all parts together and add to result table.
            # 
            tabledata.append_row(header_row_1)
            tabledata.append_row(header_row_2)
            tabledata.append_row(header_row_3)
            tabledata.append_row(header_row_4)
    
            tabledata.append_row(['Scientific name', 'Size class', 'Trophic type', 'Stage', 'Sex', ''] + \
                                parameters * numberofsamples) # Multiple columns per sample.
            #
            for row in taxon_rows:
                tabledata.append_row(row)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))
   
    def _create_report_zooplankton_abundance_length_median_and_mean(self, dataset, reportdata):
        """ """
        try:
            # Create a dataset (table, not tree).
            tabledata = plankton_core.DatasetTable()
            reportdata.set_data(tabledata)
            # Header.
            header_row = []
            header_row.append('Station name')
            header_row.append('Date')
            header_row.append('Sample min depth')
            header_row.append('Sample max depth')
            header_row.append('Scientific name')
            header_row.append('Stage')
            header_row.append('Sex')
            header_row.append('Abundance (ind/m2)')
            header_row.append('Abundance (ind/m3)')
            header_row.append('Length (median)')
            header_row.append('Length (mean)')
            tabledata.set_header(header_row)
            # Extract values for the plot.
            date = '-'
            station_name = '-'
            sample_min_depth_m = '-'
            sample_max_depth_m = '-'
            for visitnode in dataset.get_children():
                station_name = visitnode.get_data('station_name')
                date = visitnode.get_data('sample_date')
                for samplenode in visitnode.get_children():
                    sample_min_depth_m = samplenode.get_data('sample_min_depth_m')
                    sample_max_depth_m = samplenode.get_data('sample_max_depth_m')
                    
                    # Iterate over sample content. 
                    # Note: Create a level between sample and variabel.
                    grouped_lifestages = {}
                    for variablenode in samplenode.get_children():
                        group_key = variablenode.get_data('scientific_name')
                        group_key += ':' + variablenode.get_data('stage') # Specific for zooplankton.
                        group_key += ':' + variablenode.get_data('sex') # Specific for zooplankton.
                        if group_key not in grouped_lifestages:
                            grouped_lifestages[group_key] = [] # Starts a new group.
                        grouped_lifestages[group_key].append(variablenode)
                    
                    # Get variables from the new set of groups.
                    for group_key in grouped_lifestages.keys():
                        # This should be available in each group.
                        scientific_name = '-'
                        stage = '-'
                        sex = '-'
                        abundance_ind_m2 = '-'
                        abundance_ind_m3 = '-'
                        length_median = '-'
                        length_mean = '-'
                        #
                        for variablenode in grouped_lifestages[group_key]:
                            # This should be same for all variables in the group.                       
                            scientific_name = variablenode.get_data('scientific_name')
                            stage = variablenode.get_data('stage')
                            sex = variablenode.get_data('sex')
                            # Parameters.
                            parameter = variablenode.get_data('parameter')
                            unit = variablenode.get_data('unit')
                            if (parameter == 'Abundance') and (unit == 'ind/m2'):
                                abundance_ind_m2 = variablenode.get_data('value')
                            if (parameter == 'Abundance') and (unit == 'ind/m3'):
                                abundance_ind_m3 = variablenode.get_data('value')
                            if parameter == 'Length (median)':
                                length_median = variablenode.get_data('value')
                            if parameter == 'Length (mean)':
                                length_mean = variablenode.get_data('value')
                        
                        # Organism group is finished. Add row to report.
                        report_row = []
                        report_row.append(station_name)
                        report_row.append(date)
                        report_row.append(sample_min_depth_m)
                        report_row.append(sample_max_depth_m)
                        report_row.append(scientific_name)
                        report_row.append(stage)
                        report_row.append(sex)
                        report_row.append(abundance_ind_m2)
                        report_row.append(abundance_ind_m3)
                        report_row.append(length_median)
                        report_row.append(length_mean)
                        #
                        tabledata.append_row(report_row)
        #
        except Exception as e:
            debug_info = self.__class__.__name__ + ', row  ' + str(sys._getframe().f_lineno)
            toolbox_utils.Logging().error('Exception: (' + debug_info + '): ' + str(e))

# # Sort function for the result table.
# def primer_report_count_table_sort(s1, s2):
#     """ """
#     # Sort order: 
#     # - 0: scientific_name
#     # - 1: size_class
#     # - 2: trophic_type
#     # - 3: stage
#     # - 4: sex
#     columnsortorder = [0, 1, 2, 3, 4]
#     #
#     for index in columnsortorder:
#         s1item = s1[index]
#         s2item = s2[index]
#         # Empty strings should be at the end.
#         if (s1item != '') and (s2item == ''): return -1
#         if (s1item == '') and (s2item != ''): return 1
#         if s1item < s2item: return -1
#         if s1item > s2item: return 1
#     #
#     return 0 # All are equal.


##########################################################################
# import plankton_reports.core.resources.taxa as taxa
# import plankton_reports.core.resources.taxa_phytowin as taxa_phytowin
# import mmfw
# 
# class CreateReport(object):
#     """ 
#     """
#     def __init__(self):
#         """ """
#         # Initialize parent.
#         super(CreateReport, self).__init__()
#         #
#         
#     def createReport(self, datasets, report_table,
#                      show_debug_info = False, 
#                      aggregate_rows = False):
#         """
#         Note:
#         - Datasets must be of the format used in the modules dataset_tree and datasets_tree. 
#         - The report_table object must contain self._header = [] and self._rows = [].
#         """
#         # Check indata.
#         if datasets == None:
#             raise UserWarning('Datasets are missing.')
#         if report_table == None:
#             raise UserWarning('Result table is missing.')
#         # Load Phytowin species translate list.
#         try:
#             taxa_phytowin.TaxaPhytowin()
#         except:
#             raise UserWarning('Failed when loading Phytowin translation list.')
#         #
#         # Set header.
#         numberofsamples = len(datasets)
#         numberofcolumns = 6 + (numberofsamples * 2) # Two columns per sample.
#         report_table.set_header([''] * numberofcolumns) # Note: Header is not used.
#         #
#         # Part 1: Create header rows with columns for sample related data.
#         #
#         header_row_1 = [str()] * numberofcolumns 
#         header_row_2 = [str()] * numberofcolumns 
#         header_row_3 = [str()] * numberofcolumns 
#         header_row_4 = [str()] * numberofcolumns 
#         header_row_5 = [str()] * numberofcolumns 
#         header_row_6 = [str()] * numberofcolumns 
#         header_row_1[5] = 'Station:'
#         header_row_2[5] = 'Provtagningsdatum:'
#         header_row_3[5] = 'Min. djup:'
#         header_row_4[5] = 'Max. djup:'
#         header_row_5[5] = 'Datum för analys:'
#         header_row_6[5] = 'Analys utförd av:'
#         #
#         # Iterate over file to create columns.
#         for datasetindex, datasetnode in enumerate(datasets):
#             visitnode = datasetnode.get_children()[0] # Only one child.
#             samplenode = visitnode.get_children()[0] # Only one child.
#             #
#             header_row_1[6 + (datasetindex * 2)] = visitnode.get_data('Stat name')
#             header_row_2[6 + (datasetindex * 2)] = visitnode.get_data('sample_date')
#             header_row_3[6 + (datasetindex * 2)] = samplenode.get_data('Min. depth')
#             header_row_4[6 + (datasetindex * 2)] = samplenode.get_data('Max. depth')
#             header_row_5[6 + (datasetindex * 2)] = samplenode.get_data('Counted on')
#             header_row_6[6 + (datasetindex * 2)] = samplenode.get_data('Counted by')
#         #
#         # Part 2: Iterate over all rows in all samples. Create a dictionary with 
#         #         species as keys and lists of abundances for each sample.
#         #         Size class included with ':' as delimiter.
#         #         Example: "Incertae sedis:1": [1234.5, 1234.5, 1234.5, 1234.5]
#         species_sample_dict = {}
#         # Iterate through datasets.
#         for datasetindex, datasetnode in enumerate(datasets):
#             visitnode = datasetnode.get_children()[0] # Only one child.
#             samplenode = visitnode.get_children()[0] # Only one child.
#             for variablenode in samplenode.get_children():
#                 # "Species","Abundance (scale 1 to 5)" 
#                 phytowinnameandsize = variablenode.get_data('Species') + ':' + variablenode.get_data('Size')
#                 #
#                 countedunits = variablenode.get_data('Units')
#                 coeff = variablenode.get_data('Coeff')
#                 try:
#                     abundance = int(countedunits) * int(coeff)                    
#                 except:
#                     abundance = 'ERROR' + ' [' + countedunits + ' * ' + coeff + ']'
#                     mmfw.Logging().error('Calculation error. Units * coeff: ' + countedunits + ' * ' + coeff)
#                 #
#                 if species_sample_dict.has_key(phytowinnameandsize):
#                     species_sample_dict[phytowinnameandsize][datasetindex] = abundance
#                 else:
#                     species_sample_dict[phytowinnameandsize] = [str()] * numberofsamples # Add new value list.
#                     species_sample_dict[phytowinnameandsize][datasetindex] = abundance
#         #
#         # Part 3: Create the species rows in the report.        
#         #
#         species_rows = []
#         # Iterate over species in the dictionary.
#         for phytowinnameandsize in species_sample_dict.keys():
#             # NET samples:            
#             ## Extract useful part from Species-column.
#             ## Example: "Protoperidinium steinii HET 32 (cell: 32-37µm)"
#             #parts = phytowinname.split(' ')
#             #speciesname = ''
#             #for part in parts:
#             #    if part not in ['cf.', 'HET', '32', '(cell:', '(width:', '(no']:
#             #        speciesname += part + ' '
#             #    else:
#             #        if part not in ['cf.']:
#             #            break # Break loop.
#             #speciesname = speciesname.strip()
#             #
#             # Counted samples:
#             namesize = phytowinnameandsize.split(':')
#             phytowinname = namesize[0]
#             # Remove 'cf.'
#             if 'cf.' in phytowinname:  
#                 parts = phytowinname.split(' ')
#                 speciesname = ''
#                 for part in parts:
#                     if part not in ['cf.']:
#                         speciesname += part + ' '
#                 phytowinname = speciesname.strip()
#             #
#             sizeclass = namesize[1]
#             #
#             pegname, pegsize, sflag = taxa_phytowin.TaxaPhytowin().convertFromPhytowinToPeg(phytowinname, phytowin_size_class = sizeclass)
#             # Check if 'cf.' was included in name. Add to Sflag.
#             if 'cf.' in variablenode.get_data('Species'):
#                 if sflag:
#                     sflag = 'cf., ' + sflag
#                 else:
#                     sflag = 'cf.'
#             
#             taxonname = taxa.Taxa().getTaxonValue('Scientific name', pegname)
#             taxonclass = taxa.Taxa().getTaxonValue('Class', pegname)
# #            author = taxa.Taxa().getTaxonValue('Author', pegname)
#             harmful = taxa.Taxa().getTaxonValue('Harmful', pegname)
#             trophic_type = taxa.Taxa().getSizeclassValue('Trophic type', pegname, pegsize)
#             # If trophic_type not available for this sizeclass, get it from taxon.
#             trophic_type = taxa.Taxa().getTaxonValue('Trophic type', pegname)
#             volume = taxa.Taxa().getSizeclassValue('Calculated volume, µm3', pegname, pegsize)
#             #
#             if show_debug_info:
#                 taxonname = taxonname + ' [' + phytowinnameandsize + ']'
#             # Put the row together.
#             row = [str()] * (numberofcolumns * 2)
#             row[0] = taxonclass
#             row[1] = 'X' if harmful else ''
#             row[2] = taxonname
#             row[3] = pegsize if pegsize else ''
#             row[4] = sflag.lower() if sflag else '' # Lowercase.
#             row[5] = trophic_type if trophic_type else ''
#             for index, abund in enumerate(species_sample_dict[phytowinnameandsize]):
#                 row[6 + (index * 2)] = abund
#                 #
#                 volumestring = ''
#                 if (volume != None) and (abund):
#                     try:
#                         # calculatedvolume = int(countedunits) * int(coeff) * float(volume)
#                         calculatedvolume = float(volume) * float(abund) / 1000000000. # Should be mm3/l (2012-12-12) 
#                         volumestring = format(calculatedvolume, '.8f').replace('.', ',')
#                     except:
#                         volumestring = 'ERROR' + ' [' + str(abund) + ' * ' + str(volume) + ' / 1000000000]'
#                 row[6 + (index * 2) + 1] = volumestring
#             # Add the row the report.
#             species_rows.append(row)
#             
#         # Sort the outdata list before writing to file. 
#         species_rows.sort(report_count_table_sort) # Sort function defined below.
#         
#         #
#         # Aggregate values. Same species and trophic_type but different size classes will be aggregated.
#         if aggregate_rows:
#             oldrow = None
#             for row in species_rows:
#                 row[3] = '' # Size classes should be removed. 
#                 if oldrow:
#                     if row[2]: # Don't aggregate if species is missing.
#                         # Iterate over samples.
#                         if oldrow[2] == row[2]: # Column 2: Species.
#                             if oldrow[5] == row[5]: # Column 5: trophic_type may differ for Unicells etc.
#                                 sampleindex = 0
#                                 while sampleindex < numberofsamples:
#                                     abundcol = 6 + (sampleindex * 2)
#                                     volumecol = abundcol + 1
#                                     if row[abundcol] and oldrow[abundcol]:
#                                         row[abundcol] = str(int(row[abundcol]) + int(oldrow[abundcol]))
#                                         oldrow[0] = 'REMOVE AGGREGATED' #
#                                     if row[volumecol] and oldrow[volumecol]:
#                                         row[volumecol] = str(float(row[volumecol].replace(',', '.')) + float(oldrow[volumecol].replace(',', '.'))).replace('.', ',')
#                                         oldrow[0] = 'REMOVE AGGREGATED' #
#                                     #
#                                     sampleindex += 1     
#                 #
#                 oldrow = row
# 
#         #
#         # Part 4: Put all parts together and add to result table.
#         # 
#         report_table.append_row(header_row_1)
#         report_table.append_row(header_row_2)
#         report_table.append_row(header_row_3)
#         report_table.append_row(header_row_4)
#         report_table.append_row(header_row_5)
#         report_table.append_row(header_row_6)
#         # NET samples:
#         #report_table.append_row(['Klass', 'Pot. giftig', 'Art', 'Sflag'] + ['Förekomst'] * numberofsamples) 
#         # Counted samples:
#         if aggregate_rows:
#             report_table.append_row(['Klass', 'Pot. giftig', 'Art', '', 'Sflag', 'Trofigrad'] + ['Celler/l', 'Biovolume (mm3/L)'] * numberofsamples) # Two columns per sample.
#         else:
#             report_table.append_row(['Klass', 'Pot. giftig', 'Art', 'Storleksklass (PEG)', 'Sflag', 'Trofigrad'] + ['Celler/L', 'Biovolume (mm3/L)'] * numberofsamples) # Two columns per sample.
#         #
#         for row in species_rows:
#             if row[0] != 'REMOVE AGGREGATED':
#                 report_table.append_row(row)
# 
# 
# # Sort function for the result table.
# def report_count_table_sort(s1, s2):
#     """ """
#     # Sort order: Class and scientific name.
#     columnsortorder = [0, 2, 5] # Class, Species and Trophic type.
#     #
#     for index in columnsortorder:
#         s1item = s1[index]
#         s2item = s2[index]
#         # Empty strings should be at the end.
#         if (s1item != '') and (s2item == ''): return -1
#         if (s1item == '') and (s2item != ''): return 1
#         if s1item < s2item: return -1
#         if s1item > s2item: return 1
#     #
#     return 0 # All are equal.




