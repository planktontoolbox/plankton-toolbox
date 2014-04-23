#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2010-2014 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
#

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
# import plankton_toolbox.tools.tool_manager as tool_manager
import plankton_toolbox.toolbox.utils_qt as utils_qt
# import plankton_toolbox.toolbox.help_texts as help_texts
import envmonlib

class AnalyseDatasetsTab8(QtGui.QWidget):
    """ """
    def __init__(self):
        """ """
        self._main_activity = None
        self._analysisdata = None
        super(AnalyseDatasetsTab8, self).__init__()

    def setMainActivity(self, main_activity):
        """ """
        self._main_activity = main_activity
        self._analysisdata = main_activity.getAnalysisData()
                
    def clear(self):
        """ """
        self._parameter_list.clear()
        
    def update(self):
        """ """
        self.clear()
        analysisdata = self._analysisdata.getData()
        if analysisdata:        
            # Search for all parameters in analysis data.
            parameterset = set()
            for visitnode in analysisdata.getChildren():
                for samplenode in visitnode.getChildren():
                    for variablenode in samplenode.getChildren():
                        parameterset.add(variablenode.getData(u'parameter') + u' (' + variablenode.getData(u'unit') + u')')
            parameterlist = sorted(parameterset)
            self._parameter_list.setList(parameterlist)

    # ===== TAB: Reports ===== 
    def contentReports(self):
        """ """
        # Active widgets and connections.
#         introlabel = utils_qt.RichTextQLabel()
#         introlabel.setText(help_texts.HelpTexts().getText(u'AnalyseDatasetsTab8_intro'))
        # Parameters.
        self._parameter_list = utils_qt.SelectableQListView()       
        clearall_label = utils_qt.ClickableQLabel("Clear all")
        markall_label = utils_qt.ClickableQLabel("Mark all")
        self.connect(clearall_label, QtCore.SIGNAL("clicked()"), self._parameter_list.uncheckAll)                
        self.connect(markall_label, QtCore.SIGNAL("clicked()"), self._parameter_list.checkAll)                
        # Predefined reports.
        self._report_1_button = QtGui.QPushButton("PRIMER")
        self.connect(self._report_1_button, QtCore.SIGNAL("clicked()"), self._createReport_1)                
        self._report_2_button = QtGui.QPushButton("Zooplankton: Abundance m2 and m3, length median and mean")
        self.connect(self._report_2_button, QtCore.SIGNAL("clicked()"), self._createReport_2)                

        # Layout widgets.
        form1 = QtGui.QGridLayout()
        gridrow = 0
        label1 = QtGui.QLabel("Parameters (for PRIMER):")
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
        vbox1 = QtGui.QVBoxLayout()
        vbox1.addWidget(self._report_1_button)
        vbox1.addWidget(self._report_2_button)
        vbox1.addStretch(5)
        #
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addLayout(form1)
        hbox1.addLayout(vbox1)
        hbox1.addStretch(5)
        #
        layout = QtGui.QVBoxLayout()
#         layout.addWidget(introlabel)
#         layout.addLayout(form1)
        layout.addLayout(hbox1)
        layout.addStretch(5)
        self.setLayout(layout)                
        #
        return self
                
    def _createReport_1(self):
        """ """
        # Clear the report and view the report area.
        reportdata = self._main_activity.getReportData()
        reportdata.clearData()
        self._main_activity.viewReportData()
        # Filtered data should be used.
        self._main_activity.updateFilter() # Must be done before createFilteredDataset().
        analysisdata = self._analysisdata.createFilteredDataset()
        if not analysisdata:
            return # Can't create a report from an empty dataset.
        # Create the report.
        parameters = self._parameter_list.getSelectedDataList()        
        self.createPrimerReport(parameters, # Note:Support for multiple parameters.
                                [analysisdata], # Note:Support for multiple datasets. Not used here.
                                reportdata)
        # View the result in the report area.
        self._main_activity.viewReportData()
        
    def _createReport_2(self):
        """ """
        # Clear the report and view the report area.
        reportdata = self._main_activity.getReportData()
        reportdata.clearData()
        self._main_activity.viewReportData()
        # Filtered data should be used.
        self._main_activity.updateFilter() # Must be done before createFilteredDataset().
        analysisdata = self._analysisdata.createFilteredDataset()
        if not analysisdata:
            return # Can't create a report from an empty dataset.
        # Create the report.
        self._createReportZooplanktonAbundanceLengthMedianAndMean(analysisdata, reportdata)
        # View the result in the report area.
        self._main_activity.viewReportData()



    def createPrimerReport(self, 
                           parameters, 
                           datasets, 
                           reportdata):
        """  """
        # Create a dataset (table, not tree).
        tabledata = envmonlib.DatasetTable()
        reportdata.setData(tabledata)
        # Check indata.
        if parameters == None:
            raise UserWarning('Parameters are missing.')
        if datasets == None:
            raise UserWarning('Datasets are missing.')
        #
        # Calculate number of samples and columns.
        numberofsamples = 0
        for dataset in datasets:
            for visit in dataset.getChildren():
                numberofsamples += len(visit.getChildren())
        numberofparameters = len(parameters)
        numberofcolumns = 6 + (numberofsamples * numberofparameters)
        # Set header. Note: Normal header is not used.
        tabledata.setHeader([u''] * numberofcolumns)
        #
        # Part 1: Create header rows with columns for sample related data.
        #
        header_row_1 = [unicode()] * numberofcolumns 
        header_row_2 = [unicode()] * numberofcolumns 
        header_row_3 = [unicode()] * numberofcolumns 
        header_row_4 = [unicode()] * numberofcolumns 
        header_row_1[5] = u'Station name:'
        header_row_2[5] = u'Date:'
        header_row_3[5] = u'Sample min depth:'
        header_row_4[5] = u'Sample max depth:'
        #
        # Iterate over file to create column headers.
        sampleindex = 0
        for dataset in datasets:
            for visit in dataset.getChildren():
                for sample in visit.getChildren():
                    header_row_1[6 + (sampleindex * numberofparameters)] = visit.getData('station_name')
                    header_row_2[6 + (sampleindex * numberofparameters)] = visit.getData('date')
                    header_row_3[6 + (sampleindex * numberofparameters)] = sample.getData('sample_min_depth')
                    header_row_4[6 + (sampleindex * numberofparameters)] = sample.getData('sample_max_depth')
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
            for visit in dataset.getChildren():
                for sample in visit.getChildren():
                    for variable in sample.getChildren():
                        scientific_name = variable.getData('scientific_name')
                        size_class = variable.getData(u'size_class')
                        trophic_level = variable.getData(u'trophic_level')
                        stage = variable.getData(u'stage')
                        sex = variable.getData(u'sex')
                        #
                        taxon_key = unicode(scientific_name) + ':' + unicode(size_class) + ':' + unicode(trophic_level) + ':' + unicode(stage) + ':' + unicode(sex)
                        if taxon_key not in taxon_values_dict:
                            taxon_values_dict[taxon_key] = [unicode()] * (numberofsamples * numberofparameters) # Add new value list.
                        #
                        for paramindex, param in enumerate(parameters):
                            parameter = variable.getData('parameter')
                            unit = variable.getData('unit')
                            value = variable.getData('value')
                            #
                            if param == (parameter + u' (' + unit + u')'):
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
            trophic_level = taxon_key_parts[2]
            stage = taxon_key_parts[3]
            sex = taxon_key_parts[4]
            #
            row = [u''] * (numberofcolumns * numberofparameters)
            row[0] = scientific_name
            row[1] = size_class
            row[2] = trophic_level
            row[3] = stage
            row[4] = sex
            for index, value in enumerate(taxon_values_dict[taxon_key]):
                row[6 + index] = value
#                 row[6 + (index * numberofparameters) + 1] = values[1]
#                 row[6 + (index * numberofparameters) + 1] = values[2]
            # Add the row the report.
            taxon_rows.append(row)
             
        # Sort the outdata list before writing to file. 
        taxon_rows.sort(primer_report_count_table_sort) # Note: Sort function defined below.        
        #
        # Part 4: Put all parts together and add to result table.
        # 
        tabledata.appendRow(header_row_1)
        tabledata.appendRow(header_row_2)
        tabledata.appendRow(header_row_3)
        tabledata.appendRow(header_row_4)

        tabledata.appendRow([u'Scientific name', u'Size class', u'Trophic level', u'Stage', u'Sex', u''] + \
                            parameters * numberofsamples) # Multiple columns per sample.
        #
        for row in taxon_rows:
            tabledata.appendRow(row)

   
    def _createReportZooplanktonAbundanceLengthMedianAndMean(self, dataset, reportdata):
        """ """
        # Create a dataset (table, not tree).
        tabledata = envmonlib.DatasetTable()
        reportdata.setData(tabledata)
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
        tabledata.setHeader(header_row)
        # Extract values for the plot.
        date = u'-'
        station_name = u'-'
        sample_min_depth = u'-'
        sample_max_depth = u'-'
        for visitnode in dataset.getChildren():
            station_name = visitnode.getData(u"station_name")
            date = visitnode.getData(u"date")
            for samplenode in visitnode.getChildren():
                sample_min_depth = samplenode.getData(u"sample_min_depth")
                sample_max_depth = samplenode.getData(u"sample_max_depth")
                
                # Iterate over sample content. 
                # Note: Create a level between sample and variabel.
                grouped_lifestages = {}
                for variablenode in samplenode.getChildren():
                    group_key = variablenode.getData(u'scientific_name')
                    group_key += u':' + variablenode.getData(u'stage') # Specific for zooplankton.
                    group_key += u':' + variablenode.getData(u'sex') # Specific for zooplankton.
                    if group_key not in grouped_lifestages:
                        grouped_lifestages[group_key] = [] # Starts a new group.
                    grouped_lifestages[group_key].append(variablenode)
                
                # Get variables from the new set of groups.
                for group_key in grouped_lifestages.keys():
                    # This should be available in each group.
                    scientific_name = u'-'
                    stage = u'-'
                    sex = u'-'
                    abundance_ind_m2 = u'-'
                    abundance_ind_m3 = u'-'
                    length_median = u'-'
                    length_mean = u'-'
                    #
                    for variablenode in grouped_lifestages[group_key]:
                        # This should be same for all variables in the group.                       
                        scientific_name = variablenode.getData(u'scientific_name')
                        stage = variablenode.getData(u'stage')
                        sex = variablenode.getData(u'sex')
                        # Parameters.
                        parameter = variablenode.getData(u'parameter')
                        unit = variablenode.getData(u'unit')
                        if (parameter == u'Abundance') and (unit == u'ind/m2'):
                            abundance_ind_m2 = variablenode.getData(u'value')
                        if (parameter == u'Abundance') and (unit == u'ind/m3'):
                            abundance_ind_m3 = variablenode.getData(u'value')
                        if parameter == u'Length (median)':
                            length_median = variablenode.getData(u'value')
                        if parameter == u'Length (mean)':
                            length_mean = variablenode.getData(u'value')
                    
                    # Organism group is finished. Add row to report.
                    report_row = []
                    report_row.append(station_name)
                    report_row.append(date)
                    report_row.append(sample_min_depth)
                    report_row.append(sample_max_depth)
                    report_row.append(scientific_name)
                    report_row.append(stage)
                    report_row.append(sex)
                    report_row.append(abundance_ind_m2)
                    report_row.append(abundance_ind_m3)
                    report_row.append(length_median)
                    report_row.append(length_mean)
                    #
                    tabledata.appendRow(report_row)



# Sort function for the result table.
def primer_report_count_table_sort(s1, s2):
    """ """
    # Sort order: 
    # - 0: scientific_name
    # - 1: size_class
    # - 2: trophic_level
    # - 3: stage
    # - 4: sex
    columnsortorder = [0, 1, 2, 3, 4]
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
#         report_table.setHeader([u''] * numberofcolumns) # Note: Header is not used.
#         #
#         # Part 1: Create header rows with columns for sample related data.
#         #
#         header_row_1 = [unicode()] * numberofcolumns 
#         header_row_2 = [unicode()] * numberofcolumns 
#         header_row_3 = [unicode()] * numberofcolumns 
#         header_row_4 = [unicode()] * numberofcolumns 
#         header_row_5 = [unicode()] * numberofcolumns 
#         header_row_6 = [unicode()] * numberofcolumns 
#         header_row_1[5] = u'Station:'
#         header_row_2[5] = u'Provtagningsdatum:'
#         header_row_3[5] = u'Min. djup:'
#         header_row_4[5] = u'Max. djup:'
#         header_row_5[5] = u'Datum för analys:'
#         header_row_6[5] = u'Analys utförd av:'
#         #
#         # Iterate over file to create columns.
#         for datasetindex, datasetnode in enumerate(datasets):
#             visitnode = datasetnode.getChildren()[0] # Only one child.
#             samplenode = visitnode.getChildren()[0] # Only one child.
#             #
#             header_row_1[6 + (datasetindex * 2)] = visitnode.getData('Stat name')
#             header_row_2[6 + (datasetindex * 2)] = visitnode.getData('Date')
#             header_row_3[6 + (datasetindex * 2)] = samplenode.getData('Min. depth')
#             header_row_4[6 + (datasetindex * 2)] = samplenode.getData('Max. depth')
#             header_row_5[6 + (datasetindex * 2)] = samplenode.getData('Counted on')
#             header_row_6[6 + (datasetindex * 2)] = samplenode.getData('Counted by')
#         #
#         # Part 2: Iterate over all rows in all samples. Create a dictionary with 
#         #         species as keys and lists of abundances for each sample.
#         #         Size class included with ':' as delimiter.
#         #         Example: "Incertae sedis:1": [1234.5, 1234.5, 1234.5, 1234.5]
#         species_sample_dict = {}
#         # Iterate through datasets.
#         for datasetindex, datasetnode in enumerate(datasets):
#             visitnode = datasetnode.getChildren()[0] # Only one child.
#             samplenode = visitnode.getChildren()[0] # Only one child.
#             for variablenode in samplenode.getChildren():
#                 # "Species","Abundance (scale 1 to 5)" 
#                 phytowinnameandsize = variablenode.getData('Species') + ':' + variablenode.getData(u'Size')
#                 #
#                 countedunits = variablenode.getData('Units')
#                 coeff = variablenode.getData('Coeff')
#                 try:
#                     abundance = int(countedunits) * int(coeff)                    
#                 except:
#                     abundance = u'ERROR' + u' [' + countedunits + u' * ' + coeff + u']'
#                     mmfw.Logging().error(u"Calculation error. Units * coeff: " + countedunits + u' * ' + coeff)
#                 #
#                 if species_sample_dict.has_key(phytowinnameandsize):
#                     species_sample_dict[phytowinnameandsize][datasetindex] = abundance
#                 else:
#                     species_sample_dict[phytowinnameandsize] = [unicode()] * numberofsamples # Add new value list.
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
#             #parts = phytowinname.split(u' ')
#             #speciesname = u''
#             #for part in parts:
#             #    if part not in [u'cf.', u'HET', u'32', u'(cell:', u'(width:', u'(no']:
#             #        speciesname += part + u' '
#             #    else:
#             #        if part not in [u'cf.']:
#             #            break # Break loop.
#             #speciesname = speciesname.strip()
#             #
#             # Counted samples:
#             namesize = phytowinnameandsize.split(':')
#             phytowinname = namesize[0]
#             # Remove 'cf.'
#             if u'cf.' in phytowinname:  
#                 parts = phytowinname.split(u' ')
#                 speciesname = u''
#                 for part in parts:
#                     if part not in [u'cf.']:
#                         speciesname += part + u' '
#                 phytowinname = speciesname.strip()
#             #
#             sizeclass = namesize[1]
#             #
#             pegname, pegsize, sflag = taxa_phytowin.TaxaPhytowin().convertFromPhytowinToPeg(phytowinname, phytowin_size_class = sizeclass)
#             # Check if 'cf.' was included in name. Add to Sflag.
#             if u'cf.' in variablenode.getData('Species'):
#                 if sflag:
#                     sflag = 'cf., ' + sflag
#                 else:
#                     sflag = 'cf.'
#             
#             taxonname = taxa.Taxa().getTaxonValue(u'Scientific name', pegname)
#             taxonclass = taxa.Taxa().getTaxonValue(u'Class', pegname)
# #            author = taxa.Taxa().getTaxonValue(u'Author', pegname)
#             harmful = taxa.Taxa().getTaxonValue(u'Harmful', pegname)
#             trophic_level = taxa.Taxa().getSizeclassValue(u'Trophic level', pegname, pegsize)
#             # If trophic_level not available for this sizeclass, get it from taxon.
#             trophic_level = taxa.Taxa().getTaxonValue(u'Trophic level', pegname)
#             volume = taxa.Taxa().getSizeclassValue(u'Calculated volume, µm3', pegname, pegsize)
#             #
#             if show_debug_info:
#                 taxonname = taxonname + u' [' + phytowinnameandsize + u']'
#             # Put the row together.
#             row = [unicode()] * (numberofcolumns * 2)
#             row[0] = taxonclass
#             row[1] = u'X' if harmful else u''
#             row[2] = taxonname
#             row[3] = pegsize if pegsize else ''
#             row[4] = sflag.lower() if sflag else '' # Lowercase.
#             row[5] = trophic_level if trophic_level else ''
#             for index, abund in enumerate(species_sample_dict[phytowinnameandsize]):
#                 row[6 + (index * 2)] = abund
#                 #
#                 volumestring = u''
#                 if (volume != None) and (abund):
#                     try:
#                         # calculatedvolume = int(countedunits) * int(coeff) * float(volume)
#                         calculatedvolume = float(volume) * float(abund) / 1000000000. # Should be mm3/l (2012-12-12) 
#                         volumestring = format(calculatedvolume, '.8f').replace(u'.', u',')
#                     except:
#                         volumestring = u'ERROR' + u' [' + unicode(abund) + u' * ' + unicode(volume) + u' / 1000000000]'
#                 row[6 + (index * 2) + 1] = volumestring
#             # Add the row the report.
#             species_rows.append(row)
#             
#         # Sort the outdata list before writing to file. 
#         species_rows.sort(report_count_table_sort) # Sort function defined below.
#         
#         #
#         # Aggregate values. Same species and trophic_level but different size classes will be aggregated.
#         if aggregate_rows:
#             oldrow = None
#             for row in species_rows:
#                 row[3] = u'' # Size classes should be removed. 
#                 if oldrow:
#                     if row[2]: # Don't aggregate if species is missing.
#                         # Iterate over samples.
#                         if oldrow[2] == row[2]: # Column 2: Species.
#                             if oldrow[5] == row[5]: # Column 5: trophic_level may differ for Unicells etc.
#                                 sampleindex = 0
#                                 while sampleindex < numberofsamples:
#                                     abundcol = 6 + (sampleindex * 2)
#                                     volumecol = abundcol + 1
#                                     if row[abundcol] and oldrow[abundcol]:
#                                         row[abundcol] = unicode(int(row[abundcol]) + int(oldrow[abundcol]))
#                                         oldrow[0] = u'REMOVE AGGREGATED' #
#                                     if row[volumecol] and oldrow[volumecol]:
#                                         row[volumecol] = unicode(float(row[volumecol].replace(u',', u'.')) + float(oldrow[volumecol].replace(u',', u'.'))).replace(u'.', u',')
#                                         oldrow[0] = u'REMOVE AGGREGATED' #
#                                     #
#                                     sampleindex += 1     
#                 #
#                 oldrow = row
# 
#         #
#         # Part 4: Put all parts together and add to result table.
#         # 
#         report_table.appendRow(header_row_1)
#         report_table.appendRow(header_row_2)
#         report_table.appendRow(header_row_3)
#         report_table.appendRow(header_row_4)
#         report_table.appendRow(header_row_5)
#         report_table.appendRow(header_row_6)
#         # NET samples:
#         #report_table.appendRow([u'Klass', u'Pot. giftig', u'Art', u'Sflag'] + [u'Förekomst'] * numberofsamples) 
#         # Counted samples:
#         if aggregate_rows:
#             report_table.appendRow([u'Klass', u'Pot. giftig', u'Art', u'', u'Sflag', u'Trofigrad'] + [u'Celler/l', u'Biovolym (mm3/l)'] * numberofsamples) # Two columns per sample.
#         else:
#             report_table.appendRow([u'Klass', u'Pot. giftig', u'Art', u'Storleksklass (PEG)', u'Sflag', u'Trofigrad'] + [u'Celler/l', u'Biovolym (mm3/l)'] * numberofsamples) # Two columns per sample.
#         #
#         for row in species_rows:
#             if row[0] != u'REMOVE AGGREGATED':
#                 report_table.appendRow(row)
# 
# 
# # Sort function for the result table.
# def report_count_table_sort(s1, s2):
#     """ """
#     # Sort order: Class and scientific name.
#     columnsortorder = [0, 2, 5] # Class, Species and trophic level.
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




